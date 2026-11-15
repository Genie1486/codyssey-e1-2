from common.constants.output_message import OutputMessage
from common.enums.error_type import ResultType
from common.constants.menu_format import MenuFormat
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
    RESULT_SCORE_HEADER = "🏆 결과: {total}문제 중 {correct}문제 정답!"
    RESULT_SCORE_BODY = "힌트 본 횟수: {hint_view_cnt}회 ({hint_view_cnt}*10 점 차감)\n총점: {score:.1f}점"
    NEW_RECORD = "🎉 새로운 최고 점수입니다!"
    NO_QUIZ = "퀴즈가 없습니다."
    NO_BEST_SCORE = "아직 최고 점수가 없습니다."
    BEST_SCORE = "🏆 최고 점수: {score:.1f}점 ({total}문제 중 {correct}문제 정답)"
    EXIT_MESSAGE = "프로그램을 종료합니다."
    HINT_NOTICE = "💡 이 문제는 힌트가 있습니다."
    HINT = "💡 힌트: {hint}"
    HINT_ALREADY_VIEWED = "이미 힌트를 봤습니다"

    def display_header(self) -> None:
        print(MenuFormat.DIVIDER_EQUAL)
        print(f"{MenuFormat.PADDING}{self.TITLE}")
        print(MenuFormat.DIVIDER_EQUAL)

    def display_menu(self, menus: list[str]) -> None:
        for i, menu in enumerate(menus, start=1):
            print(f"{i}. {menu}")
        print(MenuFormat.DIVIDER_EQUAL)

    def display_exit(self) -> None:
        print(self.EXIT_MESSAGE)

    def display_quiz_list(self, quizzes: list[Quiz]) -> None:  # 목록 출력
        print(MenuFormat.NEWLINE)
        title = self.QUIZ_LIST.format(len(quizzes))
        print(f"{MenuFormat.PADDING}{title}")
        print(MenuFormat.DIVIDER_DASH)
        for i, quiz in enumerate(quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print(MenuFormat.DIVIDER_DASH)
        print(MenuFormat.NEWLINE)

    def display_message(self, message: str) -> None:
        print(message)

    def display_best_score(self, best_score: BestScore) -> None:
        # 🏆 최고 점수: 80점 (5문제 중 4문제 정답)
        print(MenuFormat.NEWLINE)
        if best_score is None:
            print(self.NO_BEST_SCORE)
        else:
            print(
                self.BEST_SCORE.format(
                    score=best_score.score,
                    total=best_score.total,
                    correct=best_score.correct,
                )
            )
        print(MenuFormat.NEWLINE)

    def display_add_quiz_success_result(self) -> None:
        print(MenuFormat.NEWLINE)
        print(self.ADD_QUIZ_COMPLETE_MESSAGE)
        print(MenuFormat.NEWLINE)

    def display_add_quiz_start(self) -> None:
        print(MenuFormat.NEWLINE)
        print(self.ADD_QUIZ)
        print(MenuFormat.NEWLINE)

    def display_quiz_start(self, total_quiz_count: int) -> None:
        print(MenuFormat.NEWLINE)
        print(self.QUIZ_START.format(total=total_quiz_count))
        print(MenuFormat.NEWLINE)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.DIVIDER_EQUAL)

    def display_quiz(self, quiz: Quiz, quiz_number: int) -> None:
        print(MenuFormat.NEWLINE)
        print(self.QUESTION_NUMBER.format(number=quiz_number))
        print(quiz.question)
        print(MenuFormat.NEWLINE)

        for i, choice in enumerate(quiz.choices, start=1):
            print(f"{i}. {choice}")

        print(MenuFormat.NEWLINE)
        if quiz.has_hint():
            print(self.HINT_NOTICE)

    def display_no_quiz(self) -> None:
        print(self.NO_QUIZ)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.DIVIDER_DASH)

    def display_correct(self) -> None:
        print(self.CORRECT)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.DIVIDER_DASH)

    def display_incorrect(self, correct_answer: int) -> None:
        print(self.INCORRECT)
        print(self.CORRECT_ANSWER.format(answer=correct_answer))
        print(MenuFormat.NEWLINE)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.DIVIDER_DASH)

    def display_quiz_result(self, user_score: dict, is_new_record: bool) -> None:

        print(MenuFormat.DIVIDER_EQUAL)

        print(
            self.RESULT_SCORE_HEADER.format(
                total=user_score["total"], correct=user_score["correct"]
            )
        )
        print(
            self.RESULT_SCORE_BODY.format(
                hint_view_cnt=user_score["hint_view_cnt"],
                score=user_score["score"],
            )
        )

        if is_new_record:
            print(self.NEW_RECORD)
        print(MenuFormat.DIVIDER_EQUAL)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.NEWLINE)

    def display_hint(self, hint: str) -> None:
        """힌트 표시"""
        print(MenuFormat.NEWLINE)
        print(self.HINT.format(hint=hint))

    def display_hint_aleady_viewed(self) -> None:
        """이미 힌트를 봤음을 표시"""
        print(self.HINT_ALREADY_VIEWED)

    def display_error(self, error_type: ResultType, detail: str = "") -> None:
        """에러 메시지 출력"""
        message = error_type.get_message()

        print(f"\n\n{message}")

        if detail:
            print(f"   상세: {detail}")

    def display_saved_data_loaded(self, quiz_count, best_score) -> None:
        print(
            OutputMessage.SAVED_DATA_LOAD_MESSAGE.format(
                quiz_count=quiz_count, best_score=best_score
            )
        )
        print(MenuFormat.DIVIDER_EQUAL)

    def display_basic_data_loaded(self, quiz_count, best_score) -> None:
        print(
            OutputMessage.DEFAULT_DATA_LOAD_MESSAGE.format(
                quiz_count=quiz_count, best_score=best_score
            )
        )
        print(MenuFormat.DIVIDER_EQUAL)
