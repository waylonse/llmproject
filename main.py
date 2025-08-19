import os
import sys
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.run_python_file import run_python_file

def extract_function_call(response_text):
    """Extract the last non-comment line from a ```tool_code block in the response."""
    match = re.search(r'```tool_code\n(.*?)```', response_text, re.DOTALL)
    if not match:
        return None

    code_block = match.group(1).strip()
    lines = code_block.splitlines()
    for line in reversed(lines):
        line = line.strip()
        if line and not line.startswith("#"):
            return run_python_file(line)
    return None

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python main.py '<your prompt>' [--verbose]")
        sys.exit(1)

    user_prompt = sys.argv[1]

    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )


    if len(sys.argv) > 2 and sys.argv[2] == '--verbose':
        print(f"User prompt: {user_prompt}")
        if hasattr(response, "usage_metadata"):
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Output text content
    if hasattr(response, "text"):
        print(response.text)
        func_call = extract_function_call(response.text)
        if func_call:
            print(f"Extracted function call: {func_call}")
            
        else:
            print("No function call found in response.")
    else:
        print("No text in response.")

if __name__ == "__main__":
    main()
