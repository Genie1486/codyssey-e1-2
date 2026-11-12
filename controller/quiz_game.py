from view import InputView, OutputView
from model.quiz import Quiz
from constants.menu import Menu
from service.quiz_service import QuizService
import os
from constants.error_message import QuizMessage


class QuizGame:
    def __init__(self):
        # 현재 파일(quiz_controller.py)의 디렉토리
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # controller/ → project/ (부모 디렉토리)
        project_dir = os.path.dirname(base_dir)
        # project/state.json
        file_path = os.path.join(project_dir, "state.json")

        self.service = QuizService(file_path)

    def run(self):
        while True:
            self.show_menu()  # 이미 만들어둔 메서드 활용!
            choice = self._get_choice()

            if choice == Menu.EXIT.number:
                OutputView.display_exit()
                break

            self._handle_menu(choice)

    def _handle_menu(self, choice: int):
        if choice == Menu.PLAY.number:
            self.play_quiz()
        elif choice == Menu.ADD.number:
            self.add_quiz()
        elif choice == Menu.LIST.number:
            self.show_quiz_list()
        elif choice == Menu.SCORE.number:
            self.show_best_score()

    def show_menu(self) -> None:
        display_names = [menu.display_name for menu in Menu]
        OutputView.display_menu(display_names)

    def _get_choice(self) -> int:
        min_val, max_val = Menu.number_range()
        return InputView.get_menu_choice(min_val, max_val)

    def show_quiz_list(self) -> None:
        quizzes, message = self.service.get_all_quizzes()
        if message:
            OutputView.display_message(message)
        OutputView.display_quiz_list(quizzes)

    def show_best_score(self) -> None:
        best_score, message = self.service.get_best_score()
        if message:
            OutputView.display_message(message)
        OutputView.display_best_score(best_score)

    def add_quiz(self) -> None:
        # 1. 시작 메시지
        OutputView.display_add_quiz_start()

        # 2. 입력받기
        quiz_data = InputView.get_quiz_input()

        # 3. 서비스 처리
        is_success = self.service.add_quiz(quiz_data)

        if is_success:
            OutputView.display_add_quiz_success_result()
        else:
            OutputView.display_message(QuizMessage.ADD_FAILED.value)

    def play_quiz(self) -> None:
        quizzes, _ = self.service.get_all_quizzes()

        OutputView.display_quiz_start(len(quizzes))

        if len(quizzes) == 0:
            OutputView.display_no_quiz()
            return

        shuffled_quizzes = self.service.get_shuffled_quizzes(quizzes)

        user_correct = self._play_all_quizzes(shuffled_quizzes)

        self._display_and_save_result(user_correct, len(quizzes))

    # ===== 헬퍼메서드 =====

    def _play_all_quizzes(self, quizzes):
        """모든 퀴즈 풀기"""
        user_correct = 0

        for i, quiz in enumerate(quizzes, start=1):
            if self._play_single_quiz(quiz, i):
                user_correct += 1

        return user_correct

    def _play_single_quiz(self, quiz: Quiz, question_number: int) -> bool:
        """1개 퀴즈 풀기"""
        OutputView.display_quiz(quiz, question_number)
        user_answer = InputView.get_quiz_answer(1, 4)

        if self.service.is_correct(quiz, user_answer):
            OutputView.display_correct()
            return True
        else:
            OutputView.display_incorrect(quiz.answer)
            return False

    def _display_and_save_result(self, user_correct: int, total_quiz_count: int):
        """결과 표시 및 저장"""
        user_score = self.service.calculate_score(user_correct, total_quiz_count)
        is_update_best_score = self.service.update_best_score_if_needed(user_score)
        OutputView.display_quiz_result(user_score, is_update_best_score)
