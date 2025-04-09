import subprocess
import os
from gpt4all import GPT4All

JAVA_FILE = "UserCode.java"


def read_java_code():
    if not os.path.exists(JAVA_FILE):
        return None
    with open(JAVA_FILE, "r") as f:
        return f.read()


def check_java_with_javac(file_path):
    result = subprocess.run(["javac", file_path], capture_output=True, text=True)
    return result.stderr if result.stderr else "Syntax is correct!"


def explain_error_with_llm(model, error_message):
    prompt = f"""
You are a Java expert helping students understand compiler errors.

Here is a Java compiler error message:

{error_message}

Please explain clearly what the error means and how to fix it. Keep it concise and easy to understand.
"""
    response = model.generate(prompt, max_tokens=300)
    return response.strip()


def chatbot():
    print("Java Syntax Checker + LLM Explanation")
    print(f"Write Java code into '{JAVA_FILE}' and press Enter to check.")
    print("Type 'quit' to exit.\n")

    model = GPT4All("gpt4all-falcon-newbpe-q4_0.gguf", model_path="./")

    while True:
        command = input("Press Enter to check code, or type 'quit': ")
        if command.lower() == "quit":
            print("Exiting...")
            break

        java_code = read_java_code()
        if not java_code:
            print(f"Could not find '{JAVA_FILE}'. Make sure it exists and has content.")
            continue

        print("\nReading code from file...\n")
        print(java_code)

        print("\nCompiling with javac...\n")
        javac_result = check_java_with_javac(JAVA_FILE)
        print(f"javac result:\n{javac_result}")

        if "error" in javac_result.lower():
            print("\n🔍 Asking LLM to explain the error...\n")
            explanation = explain_error_with_llm(model, javac_result)
            print(f"💡 LLM Explanation:\n{explanation}")
        else:
            print("\n✅ No syntax errors. Code is valid.")

        print("\n---\n")


if __name__ == "__main__":
    chatbot()
