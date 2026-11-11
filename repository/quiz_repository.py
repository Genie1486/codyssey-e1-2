import json
from model import Quiz, BestScore
from exceptions.repository_exceptions import (
    QuizFileNotFoundError,
    QuizFileCorruptedError,
    QuizFileIOError,
)


class QuizRepository:
    # 파일 손상 시 복구용 기본값
    # total == 0은 "아직 풀지 않은 상태"를 의미
    DEFAULT_BEST_SCORE = {"score": 0, "correct": 0, "total": 0}

    def __init__(self, file_path: str) -> None:  # 주입!
        self.file_path = file_path

    # ===== 헬퍼 메서드 (중복 제거) =====

    def _initialize_file(self) -> dict:
        """파일 없을 때 초기 state.json 생성"""
        initial_data = {"quizzes": [], "best_score": self.DEFAULT_BEST_SCORE.copy()}
        self._save_data(initial_data)
        return initial_data

    def _load_data(self) -> dict:
        """파일에서 JSON 데이터 로드"""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as e:
            self._initialize_file()
            raise QuizFileNotFoundError(
                f"파일을 찾을 수 없습니다: {self.file_path}"
            ) from e
        except json.JSONDecodeError as e:
            self._initialize_file()
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

    def save_quiz(self, quiz: Quiz) -> None:
        """퀴즈 추가"""
        data = self._load_data()
        quizzes = data.get("quizzes", [])
        quizzes.append(quiz.to_dict())

        data["quizzes"] = quizzes

        self._save_data(data)

    def save_quizzes(self, quizzes: list[Quiz]) -> None:
        """여러 퀴즈 일괄 저장"""
        data = self._load_data()
        quiz_dicts = [quiz.to_dict() for quiz in quizzes]
        data["quizzes"] = quiz_dicts  # 기존 데이터 덮어쓰기
        self._save_data(data)

    def delete_quiz(self, quiz_id):
        """퀴즈 삭제"""

    # ===== BestScore 관련  =====
    def _is_valid_best_score(self, best_score: dict) -> bool:
        """best_score 유효성 검증"""
        required_keys = {"score", "correct", "total"}
        return required_keys.issubset(best_score.keys())

    def get_best_score(self) -> BestScore:
        """최고점수 조회 (없거나 손상되면 초기화)"""
        data = self._load_data()
        best_score = data.get("best_score")

        # best_score가 없거나 유효하지 않으면 초기화
        if not best_score or not self._is_valid_best_score(best_score):
            data["best_score"] = self.DEFAULT_BEST_SCORE.copy()
            self._save_data(data)
            best_score = data["best_score"]

        return BestScore.from_dict(best_score)

    def save_best_score(self, best_score: BestScore) -> None:
        """최고점수 갱신"""
        data = self._load_data()
        data["best_score"] = best_score.to_dict()
        self._save_data(data)
