from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from pydantic import BaseModel, Field
import os

# --- Environment Setup ---
# It's recommended to set the API key in your environment variables.
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    # This is a fallback for local testing if the env var isn't set,
    # but it's not recommended for production.
    print("WARNING: OPENAI_API_KEY environment variable not set.")
    # You could add a hardcoded key here for testing, e.g., api_key = "sk-..."
    # but be careful not to commit it to version control.

# Initialize Flask App
app = Flask(__name__)

# --- LangChain Components with JSON Output ---

# 1. Define the desired data structure with Pydantic
class YouTubeVideo(BaseModel):
    title: str = Field(description="a catchy and SEO-friendly YouTube video title")
    script_outline: list[str] = Field(description="a list of strings, where each string is a point in the script outline, including a hook, main points, and a call-to-action")
    hashtags: list[str] = Field(description="a list of 5-7 relevant YouTube hashtags")

# 2. LLM Model
# Use a specific model version for more consistent outputs
model = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", api_key=api_key)

# 3. Create the Parsers
# The PydanticOutputParser defines the desired format
parser = PydanticOutputParser(pydantic_object=YouTubeVideo)

# The OutputFixingParser is a wrapper that can repair malformed JSON
# It uses the same LLM to perform the correction.
fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=model)

# 4. Create the Prompt Template
# The template now includes format instructions from the original parser.
prompt_template = PromptTemplate(
    template=(
        "Generate content for a YouTube video about the topic: {topic}.\n"
        "Ensure your response is only a JSON object and contains no other text.\n" # Added explicit instruction
        "{format_instructions}\n"
    ),
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# 5. LangChain Expression Language (LCEL) Chain
# We now pipe the model's output through our more robust fixing_parser
chain = prompt_template | model | fixing_parser

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
        # Invoke the chain with the topic
        result = chain.invoke({"topic": topic})
        # The parser returns a Pydantic object, so we convert it to a dict
        return jsonify(result.dict())

    except Exception as e:
        # Provide a more generic error to the user for security
        print(f"An error occurred: {e}") # Log the detailed error for debugging
        return jsonify({"error": "An internal error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=True)
    # removed Cannot get / message
    