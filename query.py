
import google.generativeai as genai
from dotenv import load_dotenv
import json,os
import re

load_dotenv()

def get_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    return model

def parse_query_with_gemini(query: str) -> str:
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
        price = response.text.strip()
       
        return price if price else "0"

    except Exception as e:
        print(f"Gemini extraction failed: {e}, using regex fallback")
    


if __name__ == "__main__":
    
    # print("Enter your file search queries (type 'exit' or 'quit' to stop):")
    while True:
        user_query = input()
        if user_query.lower() in ('exit', 'quit'):
            print("Exiting...")
            break

        json_result = parse_query_with_gemini(user_query)
        if not json_result:
            print("Warning: Empty response from Gemini API, skipping JSON parsing.")
        else:
            json_result = re.sub(r"```json\s*", "", json_result)
            json_result = re.sub(r"```\s*", "", json_result)
            parsed_json = json.loads(json_result)
            print("Extracted JSON1:\n", type(parsed_json))
            match = re.search(r"\{.*\}", json_result, re.DOTALL)
    
            if match:
                json_substring = match.group(0)
                print("Trying to parse extracted JSON substring:")
                try:
                    parsed_json = json.loads(json_substring)
                    print("Extracted JSON:\n", parsed_json)
                except Exception as e2:
                    print("Failed again:", e2)
                    print("Raw response was:\n", json_result)
            else:
                print("No JSON found in response.")
        print("-" * 40)