# think.py

This script leverages the LLaMA 2 model to engage in an automated, iterative conversation aiming to generate comprehensive responses to user input. The application functions by posing a single question to the user, after which it initiates a self-sustaining dialogue where LLaMA 2 competes against itself. This process is designed to extract as detailed an answer as possible, effectively allowing the AI to "think out loud."

## Features

- **Interactive Question Prompting:** Collects a topic or question from the user to initiate the discussion.
- **Continuous Self-Dialogue:** Engages LLaMA 2 in a self-reflective conversation, iterating over the user's query to refine the response.
- **Dynamic Response Generation:** Utilizes both chat and generation APIs to expand on ideas and synthesize a summary.
- **Adaptive Conversation Flow:** Adjusts the dialogue direction based on the AI's responses, ensuring relevance and depth.
- **Quality Assessment:** Employs a unique rating system allowing the AI to evaluate its responses, aiming for clarity and conciseness.

## Usage

To start the script, ensure that you have the required dependencies installed, particularly `requests` for HTTP requests. Run the script in your terminal or command prompt:

```sh
python think.py
```

Upon execution, the script prompts for a topic or question. Enter your query, and watch as LLaMA 2 delves into an explorative discussion with itself, iterating towards a comprehensive answer.

## Technical Details

- **Language & Libraries:** Written in Python, the script primarily uses the `requests` library to interact with a locally hosted LLaMA 2 API.
- **API Interaction:** Makes `POST` requests to two endpoints: `/api/chat` for engaging in dialogue and `/api/generate` for synthesizing responses.
- **Streaming Responses:** Utilizes streaming responses from the API to process data in real-time, enhancing efficiency and responsiveness.
- **User Interaction:** Facilitates an interactive session where users can input a query and receive an AI-generated deep dive into the topic.
- **Conversation Management:** Manages conversation flow by dynamically adjusting message roles (user/assistant) to maintain an engaging and productive AI dialogue.

## Requirements

- Python 3.x
- `requests` library

Ensure you have a local instance of the LLaMA 2 API running and accessible at `http://localhost:11434/api`.

## Installation

1. Clone this repository or download the script.
2. Install the `requests` library using pip:

```sh
pip install requests
```

3. Ensure your LLaMA 2 API server is running.
4. Execute `think.py` and follow the on-screen prompts.
