from constants.menu_format import MenuFormat
from model import Quiz, BestScore


class OutputView:
    TITLE = "🎯 나만의 퀴즈 게임 🎯"
    QUIZ_LIST = "📋 등록된 퀴즈 목록 (총 {}개)"

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

    @classmethod
    def display_quiz_list(cls, quizzes: list[Quiz]):  # 목록 출력
        print(MenuFormat.NEWLINE.value)
        title = cls.QUIZ_LIST.format(len(quizzes))
        print(f"{MenuFormat.PADDING.value}{title}")
        print(MenuFormat.DIVIDER.value)
        for i, quiz in enumerate(quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print(MenuFormat.DIVIDER.value)
        print(MenuFormat.NEWLINE.value)

    @classmethod
    def display_message(cls, message: str):
        print(message)

    @classmethod
    def display_best_score(cls, best_score: BestScore):
        # 🏆 최고 점수: 80점 (5문제 중 4문제 정답)
        print(MenuFormat.NEWLINE.value)
        if best_score is None:
            print("아직 최고 점수가 없습니다.")
        else:
            print(
                f"🏆 최고 점수: {best_score.score}점 ({best_score.total}문제 중 {best_score.correct}문제 정답)"
            )
        print(MenuFormat.NEWLINE.value)
