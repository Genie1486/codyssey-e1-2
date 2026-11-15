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
        # BestScore가 받을 수 있는 필드 목록 추출
        valid_keys = cls.__init__.__code__.co_varnames

        # data에서 유효한 키만 걸러내기
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}

        return cls(**filtered_data)
