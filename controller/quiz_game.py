from view import InputView, OutputView
from constants.menu import Menu


class QuizGame:

    def run(self):
        while True:
            self._display_menu()  # 이미 만들어둔 메서드 활용!
            choice = self._get_choice()

            if choice == Menu.EXIT.number:
                OutputView.print_exit()
                break

            self._handle_menu(choice)

    def _handle_menu(self, choice: int):
        if choice == Menu.PLAY.number:
            print("퀴즈 풀기 메뉴를 선택하였습니다.")
        elif choice == Menu.ADD.number:
            print("퀴즈 추가 메뉴를 선택하였습니다.")
        elif choice == Menu.LIST.number:
            print("퀴즈 목록보기 메뉴를 선택하였습니다.")
        elif choice == Menu.SCORE.number:
            print("퀴즈 점수확인 메뉴를 선택하였습니다.")

    def _display_menu(self) -> None:
        display_names = [menu.display_name for menu in Menu]
        OutputView.print_menu(display_names)

    def _get_choice(self) -> int:
        min_val, max_val = Menu.number_range()
        return InputView.get_menu_choice(min_val, max_val)
