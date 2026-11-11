from view import InputView, OutputView
from constants.menu import Menu
from service.quiz_service import QuizService
import os
from model.quiz import Quiz


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
            print("퀴즈 추가 메뉴를 선택하였습니다.")
        elif choice == Menu.LIST.number:
            self._show_quiz_list()
        elif choice == Menu.SCORE.number:
            print("퀴즈 점수확인 메뉴를 선택하였습니다.")

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
