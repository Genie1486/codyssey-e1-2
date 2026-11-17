from model import Quiz, BestScore, GameState, ScoreHistory

import json
from pathlib import Path
from copy import deepcopy
import shutil


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

    DEFAULT_BEST_SCORE = BestScore(0, 0, 0)

    def __init__(self, file_path: Path = None) -> None:  # 주입!
        if file_path is None:
            # Path(__file__) = 현재 파일 경로
            # .parent = repository/
            # .parent = 프로젝트 루트
            file_path = Path(__file__).parent.parent / "state.json"

        self.file_path = file_path
        self.backup_path = file_path.with_suffix(".json.bak")
        self.game_state = None

    def load_data(self) -> dict | None:
        """저장된 파일 있으면 True 반환, 없으면 None 반환"""
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    def set_game_state(self, game_state: GameState) -> None:
        next_id = self._get_next_quiz_id(game_state.quizzes)

        for quiz in game_state.quizzes:
            if quiz.id is None:
                quiz.id = next_id
                next_id += 1

        self.game_state = game_state

    def get_default_game_state(self) -> GameState:
        """기본값으로 game_state 생성"""

        return GameState(
            quizzes=deepcopy(self.DEFAULT_QUIZZES),
            best_score=deepcopy(self.DEFAULT_BEST_SCORE),
            histories=list(),
        )

    def save_data(self) -> None:
        """기존 state.json을 백업한 뒤 self.game_state를 저장"""
        if self.file_path.exists():
            shutil.copy2(self.file_path, self.backup_path)  # 덮어쓰기 전 백업 생성

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.game_state.to_dict(), f, ensure_ascii=False, indent=4)

    def load_backup_data(self) -> dict:
        """백업 파일(state.json.bak)에서 데이터 로드"""
        with open(self.backup_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # ===== Quiz 관련  =====
    def get_all_quizzes(self) -> list[Quiz]:
        """모든 퀴즈 조회"""
        return self.game_state.quizzes

    def get_quiz_by_id(self, quiz_id):
        """특정 퀴즈 조회"""

    def save_quiz(self, quiz: Quiz) -> None:
        """퀴즈 추가"""
        quiz.id = self._get_next_quiz_id(self.game_state.quizzes)
        self.game_state.quizzes.append(quiz)

    def save_quizzes(self, quizzes: list[Quiz]) -> None:
        """여러 퀴즈 일괄 저장"""
        next_id = self._get_next_quiz_id(self.game_state.quizzes)

        for quiz in quizzes:
            quiz.id = next_id
            next_id += 1

        self.game_state.quizzes.extend(quizzes)

    def delete_quiz(self, quiz_id: int) -> bool:
        """퀴즈 삭제"""
        quiz_to_delete = None
        for quiz in self.game_state.quizzes:
            if quiz.id == quiz_id:
                quiz_to_delete = quiz
                break

        if quiz_to_delete is None:
            return False

        self.game_state.quizzes.remove(quiz_to_delete)

        return True

    def _get_next_quiz_id(self, quizzes: list[Quiz]) -> int:
        """
        기존 퀴즈들의 최대 id를 찾아
        다음 id 반환
        """
        existing_ids = [
            quiz.id for quiz in quizzes if hasattr(quiz, "id") and quiz.id is not None
        ]
        return max(existing_ids) + 1 if existing_ids else 1

    # ===== BestScore 관련  =====
    def get_best_score(self) -> BestScore:
        """최고점수 조회"""
        return self.game_state.best_score

    def save_best_score(self, best_score: BestScore) -> None:
        """최고점수 갱신"""
        self.game_state.best_score = best_score

    def get_all_histories(self) -> list[ScoreHistory]:
        """전체 점수 기록 조회"""
        return deepcopy(self.game_state.histories)

    def save_history(self, history: ScoreHistory) -> bool:
        """점수 기록 저장"""
        self.game_state.histories.append(history)
        return True
