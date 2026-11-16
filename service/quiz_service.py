from model.game_state import GameState
from model.score_history import ScoreHistory
from repository.quiz_repository import QuizRepository
from model import Quiz, BestScore
from common.enums.error_type import ResultType

import random
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo


class QuizService:
    HINT_PENALTY = 10  # 힌트당 10점 차감
    MAX_IO_RETRIES = 3

    def __init__(self, repository: QuizRepository) -> None:
        self.repository = repository

    def load_game_state(self) -> tuple[bool, ResultType]:
        """Repository의 load_game_state 호출"""
        try:
            data = self.repository.load_data()
            game_state = GameState.from_dict(data)

            if len(game_state.quizzes) == 0:
                game_state.quizzes = self.repository.get_default_game_state().quizzes
                self.repository.set_game_state(game_state)
                return False, ResultType.NO_QUIZZES

            self.repository.set_game_state(game_state)

            return True, ResultType.DATA_LOAD_COMPLETE

        except FileNotFoundError as e:
            self._initialize_with_default_game_state()
            return False, ResultType.FILE_NOT_FOUND
        except json.JSONDecodeError as e:
            self._initialize_with_default_game_state()
            return False, ResultType.FILE_CORRUPTED
        except IOError as e:
            # IOError 발생 시 최대 3번 재시도
            return self._retry_on_io_error(
                self.repository.load_data, ResultType.DATA_LOAD_COMPLETE
            )

    def save_game_state(self) -> tuple[bool, ResultType]:
        try:
            self.repository.save_data()
            return True, ResultType.DATA_SAVE_COMPLETE
        # 파일 쓰기 작업이라 FileNotFoundError, json.JSONDecodeError 발생 안함
        except IOError:
            return self._retry_on_io_error(
                self.repository.save_data, ResultType.DATA_SAVE_COMPLETE
            )

    def _retry_on_io_error(
        self, operation, success_result: ResultType
    ) -> tuple[bool, ResultType]:
        for attempt in range(1, self.MAX_IO_RETRIES + 1):
            try:
                print(f"재시도 {attempt}/{self.MAX_IO_RETRIES}...")
                operation()
                return True, success_result  # ✅ 호출부에서 결정
            except IOError:
                if attempt == self.MAX_IO_RETRIES:
                    return False, ResultType.FILE_IO_ERROR
                time.sleep(0.5)

        return False, ResultType.FILE_IO_ERROR

    def _initialize_with_default_game_state(self):
        """Repository의 get_default_game_state 호출"""
        game_state = self.repository.get_default_game_state()
        self.repository.set_game_state(game_state)

    def get_quiz_count_and_best_score(self) -> tuple[int, float]:
        quizzes = self.repository.get_all_quizzes()
        best_score = self.repository.get_best_score()

        return len(quizzes), best_score.score

    def get_all_quizzes(self) -> list[Quiz]:
        """모든 퀴즈 조회"""
        return self.repository.get_all_quizzes()

    def get_best_score(self) -> BestScore:
        """최고 점수 조회"""
        return self.repository.get_best_score()

    def add_quiz(self, quiz_data: dict) -> bool:
        """사용자가 입력한 퀴즈 1개 추가"""
        quiz = Quiz.from_dict(quiz_data)
        self.repository.save_quiz(quiz)
        return True

    def is_correct(self, quiz: Quiz, user_answer: int) -> bool:
        """사용자 답이 정답인지 확인"""
        return quiz.answer == user_answer

    def calculate_score(
        self, user_correct: int, total: int, hint_view_cnt: int
    ) -> dict:
        """정답률 계산 (소수 둘째자리)"""
        if total == 0:
            score = 0.0
        else:
            score = (
                round((user_correct / total) * 100, 2)
                - hint_view_cnt * self.HINT_PENALTY
            )

        return {
            "score": score,
            "correct": user_correct,
            "total": total,
            "hint_view_cnt": hint_view_cnt,
        }

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

    def get_shuffled_quizzes(self, quizzes: list[Quiz]) -> list[Quiz]:
        """퀴즈 랜덤 출제"""
        shuffled = quizzes.copy()
        random.shuffle(shuffled)
        return shuffled

    def get_quizzes_by_count(self, quizzes: list[Quiz], count: int) -> list[Quiz]:
        """개수 만큼 퀴즈 출제"""
        shuffled_quizzes = self.get_shuffled_quizzes(quizzes)
        return shuffled_quizzes[:count]

    def remove_quiz(self, quiz: Quiz) -> bool:
        return self.repository.delete_quiz(quiz.id)  # ← 검사 생략 가능

    def add_score_history(self, total: int, correct: int, score: float, **_) -> bool:
        kst_now = datetime.now(ZoneInfo("Asia/Seoul"))
        played_at = kst_now.strftime("%Y-%m-%d %H:%M:%S")

        history = ScoreHistory(played_at, total, correct, score)

        return self.repository.save_history(history)

    def get_all_histories(self, ascending: bool = False) -> list[ScoreHistory]:
        histories = self.repository.get_all_histories()

        # 날짜기준 내림차순(최신이 앞에?!)
        sorted_by_time = sorted(
            histories, key=lambda h: h.played_at, reverse=not ascending
        )

        return sorted_by_time
