class BestScore:
    def __init__(self, score, correct, total):
        self.score = score
        self.correct = correct
        self.total = total

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "correct": self.correct,
            "total": self.total,
        }

    @classmethod
    def from_dict(cls, data) -> "BestScore":
        return cls(**data)
