from constants.menu_format import MenuFormat
from model import Quiz, BestScore


class OutputView:
    TITLE = "🎯 나만의 퀴즈 게임 🎯"
    QUIZ_LIST = "📋 등록된 퀴즈 목록 (총 {}개)"
    ADD_QUIZ = "📌 새로운 퀴즈를 추가합니다."
    ADD_QUIZ_COMPLETE_MESSAGE = "✅ 퀴즈가 추가되었습니다!"
    QUIZ_START = "📝 퀴즈를 시작합니다! (총 {total}문제)"
    QUESTION_NUMBER = "[문제 {number}]"
    CORRECT = "✅ 정답입니다!"
    INCORRECT = "❌ 오답입니다!"
    CORRECT_ANSWER = "정답: {answer}번"
    RESULT_SCORE = "🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)"
    NEW_RECORD = "🎉 새로운 최고 점수입니다!"
    NO_QUIZ = "퀴즈가 없습니다."
    NO_BEST_SCORE = "아직 최고 점수가 없습니다."
    BEST_SCORE = "🏆 최고 점수: {score}점 ({total}문제 중 {correct}문제 정답)"
    EXIT_MESSAGE = "프로그램을 종료합니다."

    @classmethod
    def display_menu(cls, menus: list[str]) -> None:
        print(MenuFormat.DIVIDER_EQUAL.value)
        print(f"{MenuFormat.PADDING.value}{cls.TITLE}")
        print(MenuFormat.DIVIDER_EQUAL.value)
        for i, menu in enumerate(menus, start=1):
            print(f"{i}. {menu}")
        print(MenuFormat.DIVIDER_EQUAL.value)

    @classmethod
    def display_exit(cls) -> None:
        print(cls.EXIT_MESSAGE)

    @classmethod
    def display_quiz_list(cls, quizzes: list[Quiz]) -> None:  # 목록 출력
        print(MenuFormat.NEWLINE.value)
        title = cls.QUIZ_LIST.format(len(quizzes))
        print(f"{MenuFormat.PADDING.value}{title}")
        print(MenuFormat.DIVIDER_DASH.value)
        for i, quiz in enumerate(quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print(MenuFormat.DIVIDER_DASH.value)
        print(MenuFormat.NEWLINE.value)

    @classmethod
    def display_message(cls, message: str) -> None:
        print(message)

    @classmethod
    def display_best_score(cls, best_score: BestScore) -> None:
        # 🏆 최고 점수: 80점 (5문제 중 4문제 정답)
        print(MenuFormat.NEWLINE.value)
        if best_score is None:
            print(cls.NO_BEST_SCORE)
        else:
            print(
                cls.BEST_SCORE.format(
                    score=best_score.score,
                    total=best_score.total,
                    correct=best_score.correct,
                )
            )
        print(MenuFormat.NEWLINE.value)

    @classmethod
    def display_add_quiz_success_result(cls) -> None:
        print(MenuFormat.NEWLINE.value)
        print(cls.ADD_QUIZ_COMPLETE_MESSAGE)
        print(MenuFormat.NEWLINE.value)

    @classmethod
    def display_add_quiz_start(cls) -> None:
        print(MenuFormat.NEWLINE.value)
        print(cls.ADD_QUIZ)
        print(MenuFormat.NEWLINE.value)

    @classmethod
    def display_quiz_start(cls, total_quiz_count: int) -> None:
        print(MenuFormat.NEWLINE.value)
        print(cls.QUIZ_START.format(total=total_quiz_count))
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.DIVIDER_EQUAL.value)

    @classmethod
    def display_quiz(cls, quiz: Quiz, quiz_number: int) -> None:
        print(cls.QUESTION_NUMBER.format(number=quiz_number))
        print(quiz.question)
        print(MenuFormat.NEWLINE.value)

        for i, choice in enumerate(quiz.choices, start=1):
            print(f"{i}. {choice}")

        print(MenuFormat.NEWLINE.value)

    @classmethod
    def display_no_quiz(cls) -> None:
        print(cls.NO_QUIZ)
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.DIVIDER_DASH.value)

    @classmethod
    def display_correct(cls) -> None:
        print(cls.CORRECT)
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.DIVIDER_DASH.value)

    @classmethod
    def display_incorrect(cls, correct_answer: int) -> None:
        print(cls.INCORRECT)
        print(cls.CORRECT_ANSWER.format(answer=correct_answer))
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.DIVIDER_DASH.value)

    @classmethod
    def display_quiz_result(cls, user_score: dict, is_new_record: bool) -> None:
        print(MenuFormat.DIVIDER_EQUAL.value)
        print(cls.RESULT_SCORE.format(**user_score))

        if is_new_record:
            print(cls.NEW_RECORD)
        print(MenuFormat.DIVIDER_EQUAL.value)
        print(MenuFormat.NEWLINE.value)
        print(MenuFormat.NEWLINE.value)
