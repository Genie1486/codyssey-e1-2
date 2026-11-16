# model/game_state.py
from model import BestScore, Quiz, ScoreHistory


class GameState:
    """게임의 전체 상태"""

    def __init__(
        self, quizzes: list[Quiz], best_score: BestScore, histories: list[ScoreHistory]
    ):
        self.quizzes = quizzes
        self.best_score = best_score
        self.histories = histories

    def to_dict(self):
        """JSON 저장용으로 변환"""
        return {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score.to_dict(),
            "histories": [h.to_dict() for h in self.histories],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        if data is None:
            return cls(
                quizzes=[],
                best_score=BestScore(score=0, correct=0, total=0, histories=[]),
            )

        # quizzes dict 리스트 → Quiz 객체 리스트로 변환
        quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]

        best_score_dict = data.get("best_score", {"score": 0, "correct": 0, "total": 0})

        histories = [ScoreHistory.from_dict(h) for h in data.get("histories", [])]

        return cls(
            quizzes=quizzes,
            best_score=BestScore(**best_score_dict),
            histories=histories,
        )
