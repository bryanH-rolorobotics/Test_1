import json


class Question:
    def __init__(self, prompt, answer, choices=None):
        self.prompt = prompt
        self.choices = choices if choices is not None else []
        self.answer = answer

    def check(self, answer):
        return answer.casefold() == self.answer.casefold()


def load_questions(path="questions.json"):
    with open(path) as f:
        data = json.load(f)
    return [Question(q["question"], q["answer"], q.get("choices", [])) for q in data]


def run_quiz():
    questions = load_questions()
    score = 0
    for question in questions:
        print(question.prompt)
        if question.choices:
            for i, choice in enumerate(question.choices, 1):
                print(f"  {i}. {choice}")
        user_answer = input("Your answer: ")
        if question.check(user_answer):
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {question.answer}")
    print(f"You scored {score}/{len(questions)}")


if __name__ == "__main__":
    run_quiz()
