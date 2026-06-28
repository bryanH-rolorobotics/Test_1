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


def load_scores(path="scores.json"):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"high_score": 0, "history": []}


def save_scores(scores, path="scores.json"):
    with open(path, "w") as f:
        json.dump(scores, f, indent=2)


def run_quiz():
    scores = load_scores()
    print(f"Current high score: {scores['high_score']}")

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

    scores["history"].append({"score": score, "total": len(questions)})
    if score > scores["high_score"]:
        scores["high_score"] = score
        save_scores(scores)
        print("New high score! Congratulations!")
    else:
        save_scores(scores)


if __name__ == "__main__":
    run_quiz()
