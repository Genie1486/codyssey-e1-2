from constants.menu_format import MenuFormat


class OutputView:
    TITLE = "🎯 나만의 퀴즈 게임 🎯"

    @classmethod
    def display_menu(cls, menus: list[str]) -> None:
        print(MenuFormat.DIVIDER.value)
        print(f"{MenuFormat.PADDING.value}{cls.TITLE}")
        print(MenuFormat.DIVIDER.value)
        for i, menu in enumerate(menus, start=1):
            print(f"{i}. {menu}")
        print(MenuFormat.DIVIDER.value)

    @classmethod
    def display_exit(cls):
        print("프로그램을 종료합니다.")
