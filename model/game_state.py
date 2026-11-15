# model/game_state.py
from model.best_score import BestScore
from model.quiz import Quiz


class GameState:
    """게임의 전체 상태"""

    def __init__(self, quizzes: list[Quiz], best_score: BestScore):
        self.quizzes = quizzes
        self.best_score = best_score

    def to_dict(self):
        """JSON 저장용으로 변환"""
        return {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        if data is None:
            return cls(quizzes=[], best_score=BestScore(score=0, correct=0, total=0))

        # quizzes dict 리스트 → Quiz 객체 리스트로 변환
        quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]

        best_score_dict = data.get("best_score", {"score": 0, "correct": 0, "total": 0})

        return cls(
            quizzes=quizzes,
            best_score=BestScore(**best_score_dict),
        )
