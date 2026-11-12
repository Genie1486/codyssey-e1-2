from view import InputView, OutputView
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
            self._show_menu()  # 이미 만들어둔 메서드 활용!
            choice = self._get_choice()

            if choice == Menu.EXIT.number:
                OutputView.display_exit()
                break

            self._handle_menu(choice)

    def _handle_menu(self, choice: int):
        if choice == Menu.PLAY.number:
            print("퀴즈 풀기 메뉴를 선택하였습니다.")
        elif choice == Menu.ADD.number:
            self.add_quiz()
        elif choice == Menu.LIST.number:
            self._show_quiz_list()
        elif choice == Menu.SCORE.number:
            self.show_best_score()

    def _show_menu(self) -> None:
        display_names = [menu.display_name for menu in Menu]
        OutputView.display_menu(display_names)

    def _get_choice(self) -> int:
        min_val, max_val = Menu.number_range()
        return InputView.get_menu_choice(min_val, max_val)

    def _show_quiz_list(self) -> None:
        quizzes, message = self.service.get_all_quizzes()
        if message:
            OutputView.display_message(message)
        OutputView.display_quiz_list(quizzes)

    def show_best_score(self):
        best_score, message = self.service.get_best_score()
        if message:
            OutputView.display_message(message)
        OutputView.display_best_score(best_score)

    def add_quiz(self):
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
