import sys
import json
import requests


def chat(messages, temperature=0.8, model="llama2"):
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    chars = ""

    with requests.post("http://localhost:11434/api/chat", stream=True, json=data, headers=headers) as response:
        for line in response.iter_lines():
            if line:
                parsed_data = json.loads(line.decode('utf-8'))
                if parsed_data["message"]["content"]:
                    print(parsed_data["message"]
                          ["content"], end="", flush=True)
                    chars += parsed_data["message"]["content"]
            else:
                continue

    return chars


def generate(system, prompt="", temperature=0.8, model="llama2"):
    data = {
        "model": model,
        "system": system,
        "temperature": temperature,
    }

    if prompt:
        data["prompt"] = prompt

    chars = ""

    with requests.post("http://localhost:11434/api/generate", stream=True, json=data, headers=headers) as response:
        for line in response.iter_lines():
            if line:
                parsed_data = json.loads(line.decode('utf-8'))
                if parsed_data["response"]:
                    print(parsed_data["response"], end="", flush=True)
                    chars += parsed_data["response"]
            else:
                continue

    return chars


# Try to read 'question' from command line arguments
if len(sys.argv) > 1:
    question = " ".join(sys.argv[1:])
else:
    question = input("What's the topic? ")

messages = [{"role": "user",
             "content": question}]

while True:
    data = {
        "model": "llama2",
        "messages": [{"role": "system", "content": (

        )}] + messages,
        "temperature": 0.8,
    }
    headers = {'Content-Type': 'application/json'}

    # clear the screen and print the conversation
    print("\033c", end="", flush=True)
    for message in messages:
        color = 33 if message["role"] == "user" else 32
        icon = "👤" if message["role"] == "user" else "🤖"
        print(
            f"{icon} {message['role'].capitalize()}: \033[{color}m{message['content']}\033[0m")

    print("🤖 Assistant...", end="", flush=True)

    thought = chat(messages, temperature=0.8)
    messages.append({"role": "assistant", "content": thought})

    if len(messages) > 10:
        # Summarize the conversation
        summary = "\n".join([message["content"] for message in messages])
        data = {
            "model": "llama2",
            "system": f"Answer the question \"{question}\" by summarizing the following text. WRITE THE ANSWER USING ONLY THE MEANING FROM THE TEXT, WITHOUT REPETITIONS, AND KEEP IT SHORT.",
            "prompt": f"{summary}\n\n{question}",
            "temperature": 0.1,
        }
        print("🤖 Summarizing... ")
        generated_summary = generate(
            "Answer the question", f"{summary}\n\n{question}", temperature=0.1)

        print()

        rating_response = ""
        tries = 0
        while not rating_response.isnumeric() and tries < 10:
            tries += 1
            feedback_messages = []
            if rating_response != "":
                feedback_messages = [{"role": "assistant", "content": rating_response},
                                     {"role": "user", "content": "You may ONLY reply with a number from 1 to 10. NO text. The response is interpreted by a computer so it must be a number. Try again."}]

            messages = [
                {"role": "system", "content": (
                    "You numerically rate text on how well it answers a question. "
                    "You answer only with a number from 1 to 10. "
                    "1 means it doesn't answer the question at all, 10 means it answers the question perfectly.\n\n"
                    "Examples:\n"
                    "## Example 1, exactly right:\n"
                    "  Question: \"What is the capital of France?\"\n"
                    "  Text: \"The capital of France is Paris.\"\n"
                    "  Rating: 10\n"
                    "## Example 2, not right at all:\n"
                    "  Question: \"What is the capital of France?\"\n"
                    "  Text: \"The capital of France is Stockholm.\"\n"
                    "  Rating: 1\n"
                    "## Example 3, not quite right, but nearing the answer:\n"
                    "  Question: \"What is the capital of France?\"\n"
                    "  Text: \"The capital of France begins with Par.\"\n"
                    "  Rating: 5\n\n "
                    "YOU ONLY REPLY IN NUMBERS, NO APOLOGIES, NO TEXT. "
                )},
                {"role": "user", "content": (
                    f"Question: \"{question}\"\n"
                    f"Text:\n```{generated_summary}```.\n"
                    "Rate how well the text answers the question from 1 to 10."
                )}
            ]+feedback_messages

            print(f"🤖 Rating summary 1-10 ({tries} of 10)...")

            rating_response = chat(messages, temperature=0.1).strip()

            # If the format is "Rating: {number}", and nothing else, extract the number
            if rating_response.startswith("Rating: ") and rating_response[8:].isnumeric():
                rating_response = rating_response[8:]

        if not rating_response.isnumeric():
            print("Unable to obtain rating of summary. Quitting.")
            break
        else:
            print(
                f"🤖 Summary rated {rating_response} after {tries} tries.", end="", flush=True)
            rating = int(rating_response)

            if rating > 7:
                print("🤖 Summary rated 8 or higher. Quitting.")
                print("Final Result: \n\n" + generated_summary)
                break
            else:
                messages = [{"role": "user", "content": f"We're trying to answer the question \"{question}\". We've had along conversation that can be sumamrized like this: " +
                            generated_summary + ". We didn't deem that enough to fully answer the question, so let's continue."}]

    # Flip assistant messages to user, and user to assistant,
    # so the AI keeps thinking it's talking to a human as per its training
    for message in messages:
        if message["role"] == "assistant":
            message["role"] = "user"
        elif message["role"] == "user":
            message["role"] = "assistant"
