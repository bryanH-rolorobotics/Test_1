class Question:
    def __init__(self, prompt, answer, choices=None):
        self.prompt = prompt
        self.choices = choices if choices is not None else []
        self.answer = answer

    def check(self, answer):
        return answer.casefold() == self.answer.casefold()
