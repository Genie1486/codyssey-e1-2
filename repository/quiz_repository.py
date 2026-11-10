import json
from model.quiz import Quiz
from exceptions.repository_exceptions import (
    QuizFileNotFoundError,
    QuizFileCorruptedError,
    QuizFileIOError,
)


class QuizRepository:
    def __init__(self, file_path: str) -> None:  # 주입!
        self.file_path = file_path

    # ===== 헬퍼 메서드 (중복 제거) =====

    def _load_data(self) -> dict:
        """파일에서 JSON 데이터 로드"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as e:
            raise QuizFileNotFoundError(
                f"파일을 찾을 수 없습니다: {self.file_path}"
            ) from e
        except json.JSONDecodeError as e:
            raise QuizFileCorruptedError(
                f"JSON 파일이 손상되었습니다: {self.file_path}"
            ) from e
        except IOError as e:
            raise QuizFileIOError(f"파일 읽기 중 오류 발생: {str(e)}") from e

    def _save_data(self, data: dict) -> None:
        """파일에 JSON 데이터 저장"""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise QuizFileIOError(f"파일 쓰기 중 오류 발생: {str(e)}") from e

    # ===== Quiz 관련  =====
    def get_all_quizzes(self) -> list[Quiz]:
        """모든 퀴즈 조회"""
        data = self._load_data()
        quizzes = data.get("quizzes", [])

        return [Quiz.from_dict(quiz) for quiz in quizzes]

    def get_quiz_by_id(self, quiz_id):
        """특정 퀴즈 조회"""

    def create_quiz(self, quiz: Quiz) -> None:
        """퀴즈 추가"""
        data = self._load_data()
        quizzes = data.get("quizzes", [])
        quizzes.append(quiz.to_dict())

        data["quizzes"] = quizzes

        self._save_data(data)

    def remove_quiz(self, quiz_id):
        """퀴즈 삭제"""

    # ===== BestScore 관련  =====
    def get_best_score(self) -> int:
        data = self._load_data()
        return data.get("best_score", 0)

    def update_best_score(self, score: int) -> None:
        """최고점수 갱신"""
        data = self._load_data()
        data["best_score"] = score
        self._save_data(data)
