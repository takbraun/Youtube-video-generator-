from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import os

# --- Environment Setup ---
# It's recommended to set the API key in your environment variables.
# For local run: os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
# Ensure the API key is set before running the app.
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    # In a real app, you might raise an error or handle this differently
    print("WARNING: OPENAI_API_KEY environment variable not set.")
    # For development, you can fallback to a hardcoded key, but this is not recommended for production.
    # api_key = "YOUR_FALLBACK_API_KEY"

# Initialize Flask App
app = Flask(__name__)

# --- LangChain Components with JSON Output ---

# 1. Define the desired data structure with Pydantic
# This model tells the JsonOutputParser how to structure the LLM's response.
class YouTubeVideo(BaseModel):
    title: str = Field(description="a catchy and SEO-friendly YouTube video title")
    script_outline: list[str] = Field(description="a list of strings, where each string is a point in the script outline, including a hook, main points, and a call-to-action")
    hashtags: list[str] = Field(description="a list of 5-7 relevant YouTube hashtags")

# 2. LLM Model
model = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", api_key=api_key)

# 3. Create a PydanticOutputParser
# This parser will format the LLM's output into our defined Pydantic model.
parser = PydanticOutputParser(pydantic_object=YouTubeVideo)

# 4. Create the Prompt Template
# The template now includes format instructions from the parser.
prompt_template = PromptTemplate(
    template=(
        "Generate content for a YouTube video about the topic: {topic}.\n"
        "{format_instructions}\n"
    ),
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# 5. LangChain Expression Language (LCEL) Chain
# This single chain will now generate a complete JSON object.
chain = prompt_template | model | parser

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main page."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Handles the AI content generation."""
    try:
        data = request.get_json()
        if not data or 'topic' not in data:
            return jsonify({"error": "Topic is required"}), 400

        topic = data['topic']

        # Invoke the chain with the user's topic
        # The result will be a Pydantic object (YouTubeVideo)
        result = chain.invoke({"topic": topic})

        # The Pydantic object can be easily converted to a dictionary
        # which can then be sent as a JSON response.
        return jsonify(result.dict())

    except Exception as e:
        # Basic error handling
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

