
import re
import json,os
import google.generativeai as genai
from dotenv import load_dotenv
from FileSystem import makeFileSysytem

load_dotenv()

def get_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    return model

def get_file_params(query: str) -> str:
    try:
        model = get_model()
        prompt =  f"""
                    Extract the following information from the user's file search query:
                    - created_at in DD/MM/YYYY format or empty if none.
                    - file extensions as list based on keywords like 'excel'-> ['xlsx'], 'java file'-> ['java'], 'text file'-> ['txt'], etc.
                    - other keywords as a list (e.g., financial, User)
                    Return ONLY a JSON object with keys 'created_at', 'file extensions', and 'other_keywords'.
                    Example:
                    Input: give me my financial excel file which i created in 15/07/2023
                    Output: {{"created_at": "15/07/2023", "file extensions": ["xlsx"], "other_keywords": ["financial"]}}
                    Now process this input:
                    {query}
                   """

        response = model.generate_content(prompt)
        file_params = response.text.strip()
        return file_params

    except Exception as e:
        print(f"Gemini extraction failed: {e}, using regex fallback")
    


if __name__ == "__main__":

    root = makeFileSysytem()

    while True:
        user_query = input("Enter your file search queries (type 'exit' or 'quit' to stop) : ").strip()
        if user_query.lower() in ('exit', 'quit'):
            print("Exiting...")
            break

        source_dir = input("Enter source directory to start from (or type 'skip' to start from root) : ").strip()

        start_dir = root

        if source_dir and source_dir.lower() != "skip":
            start_dir = root.find_dir(source_dir)
            if not start_dir:
                print(f"Directory '{source_dir}' not found. Starting from root instead.")
                start_dir = root

        json_result = get_file_params(user_query)
        if not json_result:
            print("Warning: Empty response from Gemini API, skipping JSON parsing.")
        else:
            json_result = re.sub(r"```json\s*", "", json_result)
            json_result = re.sub(r"```\s*", "", json_result)
            json_match = re.search(r"\{.*\}", json_result, re.DOTALL)
    
            if json_match:
                json_substring = json_match.group(0)
                try:
                    parsed_json = json.loads(json_substring)
                    file_paths = start_dir.ls(parsed_json['file extensions'],parsed_json['created_at'],parsed_json['other_keywords'])
                    if len(file_paths) > 0:
                        print("\nAll file paths related to your query:")
                        for i in range(len(file_paths)):
                            print(f"{i+1}.) {file_paths[i]}")
                    else:
                        print("No such files exist in filesystem")
                except Exception as e2:
                    print("Failed again:", e2)
                    print("Raw response was:\n", json_result)
            else:
                print("No JSON found in response.")
        print("-" * 40)
        print("\n")