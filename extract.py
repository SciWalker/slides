import sys
import os
import csv
import re
import time
import json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain_anthropic import ChatAnthropic
import yaml
import google.generativeai as genai

# Load project parameters
with open("src/params.yaml", "r") as file:
    params = yaml.safe_load(file)

# Load API keys
with open("config.yml") as file:
    config = yaml.safe_load(file)
    google_ai_studio_api_key = config.get("google_ai_studio_api_key")
    anthropic_api_key = config.get("anthropic_api_key")

# Mapping between friendly model keys and actual model ids
MODEL_OPTIONS = params.get("models", {})

# Project‑specific JSON paths
json_file = f'data/youtube_projects/{params["videowiz"]["channel_name"]}/{params["videowiz"]["project_name"]}/structures.json'
output_file = f'data/youtube_projects/{params["videowiz"]["channel_name"]}/{params["videowiz"]["project_name"]}/processed/output.json'


# Prompt for keyword extraction
PROMPT_TEMPLATE = """
Read the following text and extract keywords and image prompts.
Text: {text}

Return the results as a valid JSON dictionary (no markdown code fences):
{{"Keywords for Image Search": [...], "main_keywords": [...], "Image Generation Prompts": [...]}}
Keep ≤5 search keywords and ≤2 main keywords.
"""

# === Utility LLM callers ===

def call_ollama(text: str) -> str:
    llm = Ollama(model=MODEL_OPTIONS.get("ollama", "phi4"))
    prompt = PROMPT_TEMPLATE.format(text=text)
    return llm(prompt)


def call_claude(text: str, model_key: str) -> str:
    """Calls the Anthropic Claude API."""
    model_name = MODEL_OPTIONS.get(model_key, "claude-3-sonnet-20240229")
    llm = ChatAnthropic(model=model_name, api_key=anthropic_api_key)
    prompt = PROMPT_TEMPLATE.format(text=text)
    response = llm.invoke(prompt)
    return response.content


def call_gemini(text: str, model_key: str) -> str:
    genai.configure(api_key=google_ai_studio_api_key)
    model_name = MODEL_OPTIONS[model_key]
    prompt = PROMPT_TEMPLATE.format(text=text)
    time.sleep(30)  # avoid rate limits
    response = genai.GenerativeModel(model_name).generate_content(prompt)
    return response.text

## read a folder to get the raw image files
def read_image_folder(folder_path: str) -> list:
    """Reads image files from the specified folder and returns a list of file paths."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff'}
    image_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(root, file))
    return image_files


## pass the image files to claude or gemini to extract data
def extract_data_from_images(image_files: list, model_key: str) -> list:
    """Extracts data from a list of image files using the specified model."""
    extracted_data = []
    for image_file in image_files:
        with open(image_file, "rb") as f:
            image_data = f.read()
        if model_key.startswith("claude"):
            response = call_claude(image_data, model_key)
        else:
            response = call_gemini(image_data, model_key)
        extracted_data.append(response)
    return extracted_data

def analyze_text(text: str, model_key: str) -> str:
    """Route the call to the correct model based on *model_key*."""
    if model_key.startswith("gemini"):
        print("calling gemini")
        return call_gemini(text, model_key)
    if model_key.startswith("claude"):
        print("calling claude")
        return call_claude(text, model_key)
    return call_ollama(text)

# === Main processing ===

def process_json(model_key: str = "gemini-flash") -> None:
    if model_key not in MODEL_OPTIONS:
        print(f"Invalid model '{model_key}', falling back to 'gemini-flash'.")
        model_key = "gemini-flash"

    with open(json_file, "r") as f:
        data = json.load(f)
    for chapter in data["Chapters"]:
        print(chapter["Script"])
        raw_response = analyze_text(chapter["Script"], model_key)
        try:
            cleaned = re.sub(r"```(json)?", "", raw_response).strip("` ")
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"JSON decode error for chapter {chapter['Chapter']}: {e}")
            parsed = {}
        print("working on chapter", chapter['Chapter'])
        chapter["Keywords for Image Search"] = parsed.get("Keywords for Image Search", [])
        chapter["main_keywords"] = parsed.get("main_keywords", [])
        chapter["Image Generation Prompts"] = parsed.get("Image Generation Prompts", [])

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)
    print("Keywords and prompts extracted successfully.")

# === Entry point ===
if __name__ == "__main__":
    chosen_model = sys.argv[1] if len(sys.argv) > 1 else "gemini-flash"
    print(f"Using model: {chosen_model}")
    process_json(chosen_model)