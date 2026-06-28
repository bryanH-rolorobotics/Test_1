import json
import os


class Question:
    def __init__(self, prompt, answer, choices=None):
        self.prompt = prompt
        self.choices = choices or []
        self.answer = answer

    def check(self, user_answer):
        return user_answer.strip().lower() == self.answer.lower()


def run_quiz(questions_path=None):
    if questions_path is None:
        questions_path = os.path.join(os.path.dirname(__file__), "questions.json")

    with open(questions_path) as f:
        data = json.load(f)

    questions = [
        Question(
            prompt=item["question"],
            answer=item["answer"],
            choices=item.get("choices"),
        )
        for item in data
    ]

    score = 0
    total = len(questions)

    print(f"Starting quiz: {total} questions\n")

    for i, q in enumerate(questions, 1):
        user_answer = input(f"Q{i}: {q.prompt}\nYour answer: ").strip()
        if q.check(user_answer):
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. The answer was: {q.answer}\n")

    print(f"Quiz complete! You scored {score}/{total}.")
