from typing import TypeVar
from repository.quiz_repository import QuizRepository
from model import Quiz, BestScore
from data.default_quizzes import load_default_quizzes
from exceptions.repository_exceptions import (
    QuizFileNotFoundError,
    QuizFileCorruptedError,
    QuizFileIOError,
)
from constants.error_message import QuizMessage

T = TypeVar("T")


class QuizService:
    def __init__(self, file_path: str) -> None:
        self.repository = QuizRepository(file_path)

        # 속성으로 기본 데이터 저장
        self.default_quizzes = load_default_quizzes()
        self.default_best_score = BestScore(0, 0, 0)

        self._initialize_data()

    def _initialize_data(self) -> None:
        """앱 시작 시 한 번만 실행"""
        try:
            quizzes = self.repository.get_all_quizzes()
            if not quizzes:
                self._save_default_data()
        except (QuizFileNotFoundError, QuizFileCorruptedError):
            self._save_default_data()

    def _save_default_data(self) -> None:
        """기본 데이터를 DB에 저장 (저장만 담당)"""
        self.repository.save_quizzes(self.default_quizzes)
        self.repository.save_best_score(self.default_best_score)

    def _handle_file_error(self, error: Exception, default_value: T) -> tuple[T, str]:
        """파일 에러 처리 + 기본값 복구"""
        self._save_default_data()

        error_messages = {
            QuizFileNotFoundError: QuizMessage.FILE_NOT_FOUND.value,
            QuizFileCorruptedError: QuizMessage.FILE_CORRUPTED.value,
            QuizFileIOError: QuizMessage.FILE_IO_ERROR.value,
        }

        return default_value, error_messages.get(type(error), "Unknown error")

    def get_all_quizzes(self) -> tuple[list[Quiz], str | None]:
        """모든 퀴즈 조회"""
        try:
            quizzes = self.repository.get_all_quizzes()
            if not quizzes:
                self._save_default_data()
                return self.default_quizzes, None
            return quizzes, None
        except (QuizFileNotFoundError, QuizFileCorruptedError, QuizFileIOError) as e:
            return self._handle_file_error(e, self.default_quizzes)

    def get_best_score(self) -> tuple[BestScore | None, str | None]:
        """최고 점수 조회"""
        try:
            best_score = self.repository.get_best_score()
            if best_score.total == 0:
                return None, None
            return best_score, None
        except (QuizFileNotFoundError, QuizFileCorruptedError, QuizFileIOError) as e:
            return self._handle_file_error(e, self.default_best_score)

    def add_quiz(self, quiz_data: dict) -> bool:
        """
        반환값: True (성공), False (실패)
        에러메시지는 OutputView에서 처리
        """
        try:
            quiz = Quiz.from_dict(quiz_data)
            self.repository.save_quiz(quiz)
            return True
        except (QuizFileNotFoundError, QuizFileCorruptedError, QuizFileIOError) as e:
            return False

    def is_correct(self, quiz: Quiz, user_answer: int) -> bool:
        """사용자 답이 정답인지 확인"""
        return quiz.answer == user_answer

    def calculate_score(self, user_correct: int, total: int) -> dict:
        """정답률 계산 (소수 둘째자리)"""
        if total == 0:
            score = 0.0
        else:
            score = round((user_correct / total) * 100, 2)

        return {"score": score, "correct": user_correct, "total": total}

    def _is_new_best_score(self, current_score: dict) -> bool:
        """현재 점수가 최고 점수보다 높은지 확인"""
        best_score = self.repository.get_best_score()
        return current_score["score"] > best_score.score

    def update_best_score_if_needed(self, current_score: dict) -> bool:
        """필요하면 최고 점수 업데이트"""
        if self._is_new_best_score(current_score):
            self.repository.save_best_score(BestScore.from_dict(current_score))
            return True
        return False
