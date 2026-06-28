import json
import os


def run_quiz(questions_path=None):
    if questions_path is None:
        questions_path = os.path.join(os.path.dirname(__file__), "questions.json")

    with open(questions_path) as f:
        questions = json.load(f)

    score = 0
    total = len(questions)

    print(f"Starting quiz: {total} questions\n")

    for i, item in enumerate(questions, 1):
        user_answer = input(f"Q{i}: {item['question']}\nYour answer: ").strip()
        if user_answer.lower() == item["answer"].lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. The answer was: {item['answer']}\n")

    print(f"Quiz complete! You scored {score}/{total}.")
