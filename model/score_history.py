from datetime import datetime


class ScoreHistory:
    def __init__(
        self, played_at: datetime, total: int = 0, correct: int = 0, score: float = 0.0
    ):
        self.played_at = played_at
        self.total = total
        self.correct = correct
        self.score = score

    def to_dict(self) -> dict:
        return {
            "played_at": self.played_at,
            "total": self.total,
            "correct": self.correct,
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, data) -> "ScoreHistory":
        # ScoreHistory가 받을 수 있는 필드 목록 추출
        valid_keys = cls.__init__.__code__.co_varnames

        # data에서 유효한 키만 걸러내기
        filtered_data = {k: v for k, v in data.items() if k in valid_keys}

        return cls(**filtered_data)
