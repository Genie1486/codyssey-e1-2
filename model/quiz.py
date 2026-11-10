class Quiz:
    def __init__(self, **kwargs):
        self.question = kwargs.get("question", "")
        self.choices = kwargs.get("choices", [])
        self.answer = kwargs.get("answer", 0)
        self.hint = kwargs.get("hint", "힌트가 등록되지 않았습니다.")

    def info(self):
        print(self.question)
        print(self.choices)
        print(self.answer)
        print(self.hint)

    def check_answer(self, user_answer: int) -> bool:
        """
        사용자의 답변이 정답과 일치하는지 확인합니다.

        Args:
            user_answer: 사용자가 입력한 답변 (선택지 인덱스)

        Returns:
            bool: 정답이면 True, 아니면 False
        """
        return self.answer == user_answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data) -> "Quiz":
        return cls(**data)
