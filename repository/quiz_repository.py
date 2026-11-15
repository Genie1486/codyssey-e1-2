import json
from common.constants.output_message import OutputMessage
from model import Quiz, BestScore, GameState
from common.exceptions.repository_exceptions import (
    QuizFileNotFoundError,
    QuizFileCorruptedError,
    QuizFileIOError,
)
from pathlib import Path
from copy import deepcopy


class QuizRepository:
    DEFAULT_QUIZZES = [
        Quiz(
            question="The manager requested that all employees _______ the mandatory training session next Monday.",
            choices=["attend", "attends", "attended", "will attend"],
            answer=1,
            hint="request, suggest, insist, recommend 등의 동사 뒤에 오는 that절에서는 동사원형을 써요! (가정법 현재 / 당위성의 should 생략)",
        ),
        Quiz(
            question="The new policy will be implemented _______ all departments have reviewed and approved the proposal.",
            choices=["despite", "once", "although", "so that"],
            answer=2,
            hint="빈칸 앞뒤 문맥을 살펴보세요. '~하고 나면 / ~하자마자' 라는 시간의 접속사가 필요해요!",
        ),
        Quiz(
            question="The report _______ by the research team was presented to the board of directors yesterday.",
            choices=["compile", "compiling", "compiled", "to compile"],
            answer=3,
            hint="명사(report)를 뒤에서 꾸며주는 분사를 골라야 해요. report와 compile의 관계가 능동인지 수동인지 생각해보세요!",
        ),
        Quiz(
            question="She finished the project _______ than anyone had expected.",
            choices=["more quickly", "most quickly", "much quickly", "as quickly"],
            answer=1,
            hint="than이 있으면 비교급이 필요해요! quickly는 부사라서 more를 붙여 비교급을 만들어요 😊",
        ),
        Quiz(
            question="Please submit your application form _______ the deadline on Friday.",
            choices=["until", "during", "by", "for"],
            answer=3,
            hint="마감 기한을 나타낼 때 쓰는 전치사를 고르세요! '~까지 (완료)'의 의미예요.",
        ),
    ]

    DEFAULT_BEST_SCORE = {"score": 0, "correct": 0, "total": 0}

    def __init__(self, file_path: Path = None) -> None:  # 주입!
        if file_path is None:
            # Path(__file__) = 현재 파일 경로
            # .parent = repository/
            # .parent = 프로젝트 루트
            file_path = Path(__file__).parent.parent / "state.json"

        self.file_path = file_path

    def load_game_state(self) -> bool:

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.game_state = GameState(
            quizzes=[Quiz.from_dict(q) for q in data.get("quizzes", list())],
            best_score=BestScore.from_dict(
                data.get("best_score", {"score": 0, "correct": 0, "total": 0})
            ),
        )

        return True

    def get_default_game_state(self):
        """기본값으로 game_state 생성"""
        self.game_state = GameState(
            quizzes=deepcopy(self.DEFAULT_QUIZZES),
            best_score=BestScore(0, 0, 0),
        )

        return (
            True,
            f"기본 데이터로 초기화했습니다. 퀴즈 {len(self.game_state.quizzes)}개",
        )

    def save_game_state(self):
        """현재 game_state를 state.json에 저장"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.game_state.to_dict(), f, ensure_ascii=False, indent=4)
        return (True, "게임 데이터가 저장되었습니다.")

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

    def _get_defaults(self):
        return self.DEFAULT_QUIZZES.copy(), self.DEFAULT_BEST_SCORE.copy()

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
