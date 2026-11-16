from common.constants.output_message import OutputMessage
from common.enums.error_type import ResultType
from common.constants.menu_format import MenuFormat
from common.enums.menu import Menu
from model import Quiz, BestScore, ScoreHistory


class OutputView:
    TITLE = "🎯 나만의 퀴즈 게임 🎯"
    QUIZ_LIST = "등록된 퀴즈 목록 (총 {}개)"
    ADD_QUIZ = "📌 새로운 퀴즈를 추가합니다."
    ADD_QUIZ_COMPLETE = "✅ 퀴즈가 추가되었습니다!"
    ADD_QUIZ_FAILED = "⚠️  퀴즈 추가 실패하였습니다."
    DELETE_QUIZ = "📋 퀴즈 삭제"
    DELETE_QUIZ_COMPLETE = "✅ 퀴즈가 삭제되었습니다!"
    DELETE_QUIZ_FAILED = "❌ 퀴즈 삭제에 실패했습니다."
    DELETE_QUIZ_FORMAT = "🗑️  [{number}] {question}"
    QUIZ_START = "📝 퀴즈를 시작합니다! (총 {total}문제)"
    QUESTION_NUMBER = "[문제 {number}]"
    CORRECT = "✅ 정답입니다!"
    INCORRECT = "❌ 오답입니다!"
    CORRECT_ANSWER = "정답: {answer}번"
    RESULT_SCORE_HEADER = "🏆 결과: {total}문제 중 {correct}문제 정답!"
    RESULT_SCORE_BODY = "힌트 본 횟수: {hint_view_cnt}회 ({hint_view_cnt}*10 점 차감)\n총점: {score:.1f}점"
    NEW_RECORD = "🎉 새로운 최고 점수입니다!"
    NO_QUIZ = "등록된 퀴즈가 없습니다."
    NO_BEST_SCORE = "아직 최고 점수가 없습니다."
    BEST_SCORE = "🏆 최고 점수: {score:.1f}점 ({total}문제 중 {correct}문제 정답)"
    EXIT_MESSAGE = "프로그램을 종료합니다."
    HINT_NOTICE = "💡 이 문제는 힌트가 있습니다."
    HINT = "💡 힌트: {hint}"
    HINT_ALREADY_VIEWED = "이미 힌트를 봤습니다"
    DATA_SAVE_FAILED = "데이터 저장 실패"
    DATA_LOAD_FAILED = "데이터 로드 실패"
    SCORE_HISTORY_HEADER = "📜 게임 기록 히스토리 (총 {count}회)"
    SCORE_HISTORY_EMPTY = "아직 플레이한 게임 기록이 없습니다."
    SCORE_HISTORY_ITEM = (
        "[{index}] {played_at} | {total}문제 중 {correct}문제 정답 | {score:.1f}점"
    )
    SAVE_HISTORY_COMPLETE = "✅ 게임 기록이 저장되었습니다!"
    SAVE_HISTORY_FAILED = "❌ 게임 기록 저장에 실패했습니다."

    def _display_header(self) -> None:
        print(MenuFormat.NEWLINE)
        print(MenuFormat.DIVIDER_EQUAL)
        print(f"{MenuFormat.PADDING}{self.TITLE}")
        print(MenuFormat.DIVIDER_EQUAL)

    def display_menu(
        self,
        quiz_count: int,
        best_scoer: float,
        is_first_loading: bool,
        has_existing_data: bool,
    ) -> None:
        self._display_header()

        if is_first_loading and has_existing_data:
            self._display_saved_data_loaded(quiz_count, best_scoer)

        if is_first_loading and not has_existing_data:
            self._display_basic_data_loaded(quiz_count, best_scoer)

        menus = [menu.display_name for menu in Menu]

        for i, menu in enumerate(menus, start=1):
            print(f"{i}. {menu}")

        print(MenuFormat.DIVIDER_EQUAL)

    def display_exit(self) -> None:
        print(self.EXIT_MESSAGE)

    def display_quiz_list(
        self, quizzes: list[Quiz], header: str = None
    ) -> None:  # 목록 출력
        print(MenuFormat.NEWLINE)

        if header is None:
            header = self.QUIZ_LIST.format(len(quizzes))

        print(header)

        print(MenuFormat.NEWLINE)

        if len(quizzes) == 0:
            self._display_no_quiz()
            return

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
        print(MenuFormat.DIVIDER_EQUAL)
        if best_score is None:
            print(self.NO_BEST_SCORE)
        else:
            print(self.BEST_SCORE.format(**best_score.to_dict()))
        print(MenuFormat.DIVIDER_EQUAL)
        print(MenuFormat.NEWLINE)

    def display_score_histories(self, histories: list[ScoreHistory]) -> None:
        print(self.SCORE_HISTORY_HEADER.format(count=len(histories)))

        print(MenuFormat.DIVIDER_DASH)

        if not histories:
            print(self.SCORE_HISTORY_EMPTY)
            print(MenuFormat.DIVIDER_DASH)
            return

        for i, history in enumerate(histories, start=1):
            print(self.SCORE_HISTORY_ITEM.format(index=i, **history.to_dict()))

        print(MenuFormat.DIVIDER_DASH)

    def display_add_quiz_result(self, success: bool) -> None:
        print(MenuFormat.NEWLINE)
        if success:
            print(self.ADD_QUIZ_COMPLETE)
        else:
            print(self.ADD_QUIZ_FAILED)
        print(MenuFormat.NEWLINE)

    def _display_add_quiz_success_result(self) -> None:
        print(MenuFormat.NEWLINE)
        print(self.ADD_QUIZ_COMPLETE)
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

        if total_quiz_count == 0:
            self._display_no_quiz()

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

    def _display_no_quiz(self) -> None:
        print(MenuFormat.DIVIDER_DASH)
        print(self.NO_QUIZ)
        print(MenuFormat.DIVIDER_DASH)

    def display_single_quiz_result(self, is_correct: bool, answer: str):
        print(MenuFormat.NEWLINE)
        if is_correct:
            print(self.CORRECT)
        else:
            print(self.INCORRECT)
            print(self.CORRECT_ANSWER.format(answer=answer))
        print(MenuFormat.NEWLINE)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.DIVIDER_DASH)

    def display_quiz_result(self, user_score: dict, is_new_record: bool) -> None:

        print(MenuFormat.DIVIDER_EQUAL)

        print(self.RESULT_SCORE_HEADER.format(**user_score))
        print(self.RESULT_SCORE_BODY.format(**user_score))

        if is_new_record:
            print(self.NEW_RECORD)
        print(MenuFormat.DIVIDER_EQUAL)
        print(MenuFormat.NEWLINE)
        print(MenuFormat.NEWLINE)

    def display_hint_result(self, hint: str, is_viewed: bool) -> None:
        """힌트 표시"""
        print(MenuFormat.NEWLINE)
        if is_viewed:
            print(self.HINT_ALREADY_VIEWED)
            return

        print(self.HINT.format(hint=hint))

    def display_error(self, error_type: ResultType, detail: str = "") -> None:
        """에러 메시지 출력"""
        message = error_type.get_message()

        print(f"\n{message}")

        if detail:
            print(f"   상세: {detail}")

    def _display_saved_data_loaded(self, quiz_count, best_score) -> None:
        print(
            OutputMessage.SAVED_DATA_LOAD_MESSAGE.format(
                quiz_count=quiz_count, best_score=best_score
            )
        )
        print(MenuFormat.DIVIDER_EQUAL)

    def _display_basic_data_loaded(self, quiz_count, best_score) -> None:
        print(
            OutputMessage.DEFAULT_DATA_LOAD_MESSAGE.format(
                quiz_count=quiz_count, best_score=best_score
            )
        )
        print(MenuFormat.DIVIDER_EQUAL)

    def display_save_result(self, is_success: bool, result: ResultType) -> None:
        # 실패는 IO에러 일 때만 발생할듯
        print(MenuFormat.NEWLINE)
        if not is_success:
            print(self.DATA_SAVE_FAILED)

        print(result.get_message())

    def display_init_result(self, is_success: bool, result: ResultType) -> None:
        if not is_success:
            print(self.DATA_LOAD_FAILED)

        print(result.get_message())

    def display_delete_confirmation(self, number: int, question: str):
        print(MenuFormat.NEWLINE)
        print(self.DELETE_QUIZ_FORMAT.format(**locals()))

    def display_delete_result(self, result: bool):
        print(MenuFormat.NEWLINE)
        if result:
            print(self.DELETE_QUIZ_COMPLETE)
        else:
            print(self.DELETE_QUIZ_FAILED)

    def display_save_history_result(self, is_saved: bool) -> None:
        print(MenuFormat.NEWLINE)
        if is_saved:
            print(self.SAVE_HISTORY_COMPLETE)
        else:
            print(self.SAVE_HISTORY_FAILED)
