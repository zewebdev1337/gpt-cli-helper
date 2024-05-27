import sys
from openai import OpenAI
from dotenv import load_dotenv
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

env_path = resource_path('.env')
load_dotenv(env_path)

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def ask_question(question):
    try:
        response = client.chat.completions.create(model="gpt-4o",
        temperature=0,
        max_tokens=500,
        messages=[
            {"role": "system", "content": "Respond as short as possible. You're cmdline shell assistant. No markdown but use all quote types available."},
            {"role": "user", "content": question},
        ])
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: gpt <question>")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    answer = ask_question(question)
    if answer:
        print(answer)

if __name__ == "__main__":
    main()
