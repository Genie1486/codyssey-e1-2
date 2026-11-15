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
