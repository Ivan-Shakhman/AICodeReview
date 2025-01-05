import os
from openai import OpenAI
from utils import is_valid_file


def analyze_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8-sig", errors="ignore") as f:
            return f.read()
    except Exception as e:
        print(f"Can't read the file {file_path}: {e}")
        return ""


def analyze_repo(
    description: str,
    level: str,
    api_key: str,
    repo_dir: str = "downloaded_repo",

):
    all_files_content = ""

    for root, dirs, files in os.walk(repo_dir):
        dirs[:] = [d for d in dirs if d != ".git"]

        for file in files:
            if is_valid_file(file):
                file_path = os.path.join(root, file)
                print(f"Analise of file: {file_path}")
                all_files_content += f"\n\n--- File: {file_path} ---\n"
                all_files_content += analyze_file(file_path)

    client = OpenAI(api_key=api_key)

    prompt = (
        f" Analyze the following project, here is a short description{description} "
        f"(keep in mind that I am a level developer {level} level)"
        "and return the result in the following format:\n"
        "1. Found files\n"
        "2. Cons/Comments\n"
        f"3. Rating on a 5-point scale for the level{level}\n"
        "4. Conclusion\n\n"
        "Here is the content of the project in each branch:\n"
        f"{all_files_content}\n"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a Python expert and you perform code reviews.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
