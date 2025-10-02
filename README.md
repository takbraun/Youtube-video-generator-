# Youtube-video-generator-
Flask Youtube video Idea Generator 
AI-Powered YouTube Content Generator
This is a simple web application that uses LangChain and the OpenAI API to generate ideas for YouTube videos. Based on a user-provided topic, it generates a catchy title, a script outline, and relevant hashtags, returning the result in a structured JSON format.

This project is built with a Flask backend and a simple HTML/JavaScript frontend.

Features
AI-Powered Content: Leverages a Large Language Model (LLM) to brainstorm creative video ideas.

Structured JSON Output: The AI is prompted to return clean, reliable JSON, which is parsed and validated using LangChain and Pydantic.

Error Handling: Implements an OutputFixingParser to automatically correct common LLM formatting errors, making the application more robust.

Interactive Frontend: A clean, user-friendly interface to input topics and view the generated results.

Flask Backend: A lightweight and simple server to handle API requests securely.

Project Structure
For the application to work correctly, your files must be organized in the following structure:

.
├── app.py              # The main Flask application
├── requirements.txt    # Project dependencies
└── templates/
    └── index.html      # The HTML frontend

Setup and Installation
Follow these steps to get the application running on your local machine.

1. Clone the Repository
First, clone this repository to your local machine or create the files as described in the structure above.

2. Install Dependencies
It's recommended to use a virtual environment to manage your project's dependencies.

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

Once your virtual environment is active, install the required Python libraries from the requirements.txt file.

pip install -r requirements.txt

3. Set Your OpenAI API Key
This application requires an API key from OpenAI. The key should be set as an environment variable so that it remains secure and is not hard-coded into the application.

On macOS/Linux:

export OPENAI_API_KEY="your-api-key-goes-here"

On Windows (Command Prompt):

set OPENAI_API_KEY="your-api-key-goes-here"

On Windows (PowerShell):

$env:OPENAI_API_KEY="your-api-key-goes-here"

Note: The environment variable must be set in the same terminal session where you intend to run the application.

How to Run the Application
With the setup complete, you can now run the Flask server.

Make sure you are in the root directory of the project (the same directory as app.py).

Run the following command in your terminal:

python app.py

The server will start, and you should see output similar to this:

 * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)

Open your web browser and navigate to http://127.0.0.1:5000 to use the application.

Enter a topic, click "Generate Ideas," and watch the AI do its work!