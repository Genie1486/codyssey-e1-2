from repository.quiz_repository import QuizRepository
from model.quiz import Quiz
from data.default_quizzes import load_default_quizzes
from exceptions.repository_exceptions import (
    QuizFileNotFoundError,
    QuizFileCorruptedError,
    QuizFileIOError,
)
from constants.error_message import QuizMessage


class QuizService:
    def __init__(self, file_path: str) -> None:
        self.repository = QuizRepository(file_path)  # ← 파라미터 사용!

    def _load_and_save_default_quizzes(self) -> list[Quiz]:
        """기본 데이터 로드 후 DB 저장 (헬퍼 메서드)"""
        quizzes = load_default_quizzes()  # 데이터만 가져오고
        self.repository.save_quizzes(quizzes)  # 퀴즈 저장
        self.repository.save_best_score(0)  # best_score 초기화
        return quizzes

    def get_all_quizzes(self) -> list[Quiz]:

        try:
            quizzes = self.repository.get_all_quizzes()

            # 퀴즈 개수 없으면 기본 데이터 로드
            if not quizzes:
                return (
                    self._load_and_save_default_quizzes(),
                    QuizMessage.NO_QUIZZES.value,
                )

            return quizzes, None

        except QuizFileNotFoundError:
            return (
                self._load_and_save_default_quizzes(),
                QuizMessage.FILE_NOT_FOUND.value,
            )

        except QuizFileCorruptedError:
            return (
                self._load_and_save_default_quizzes(),
                QuizMessage.FILE_CORRUPTED.value,
            )

        except QuizFileIOError:
            return (
                self._load_and_save_default_quizzes(),
                QuizMessage.FILE_IO_ERROR.value,
            )
