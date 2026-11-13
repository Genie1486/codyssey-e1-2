from view import InputView, OutputView
from service.quiz_service import QuizService
from model.quiz import Quiz
from constants.menu import Menu
from constants.error_message import QuizMessage


class QuizGame:
    def __init__(
        self, quiz_service: QuizService, input_view: InputView, output_view: OutputView
    ):
        self.quiz_service = quiz_service
        self.input_view = input_view
        self.output_view = output_view

    def run(self):
        while True:
            self.show_menu()  # 이미 만들어둔 메서드 활용!
            choice = self._get_choice()

            if choice == Menu.EXIT.number:
                self.output_view.display_exit()
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
        self.output_view.display_menu(display_names)

    def _get_choice(self) -> int:
        min_val, max_val = Menu.number_range()
        return self.input_view.get_menu_choice(min_val, max_val)

    def show_quiz_list(self) -> None:
        quizzes, message = self.quiz_service.get_all_quizzes()
        if message:
            self.output_view.display_message(message)
        self.output_view.display_quiz_list(quizzes)

    def show_best_score(self) -> None:
        best_score, message = self.quiz_service.get_best_score()
        if message:
            self.output_view.display_message(message)
        self.output_view.display_best_score(best_score)

    def add_quiz(self) -> None:
        # 1. 시작 메시지
        self.output_view.display_add_quiz_start()

        # 2. 입력받기
        quiz_data = self.input_view.get_quiz_input()

        # 3. 서비스 처리
        is_success = self.quiz_service.add_quiz(quiz_data)

        if is_success:
            self.output_view.display_add_quiz_success_result()
        else:
            self.output_view.display_message(QuizMessage.ADD_FAILED.value)

    def play_quiz(self) -> None:
        quizzes, _ = self.quiz_service.get_all_quizzes()

        self.output_view.display_quiz_start(len(quizzes))

        if len(quizzes) == 0:
            self.output_view.display_no_quiz()
            return

        problem_count = self.input_view.get_quiz_count(1, len(quizzes))

        selected_quizzes = self.quiz_service.get_quizzes_by_count(
            quizzes, problem_count
        )

        user_correct, hint_view_cnt = self._play_all_quizzes(selected_quizzes)

        self._display_and_save_result(
            user_correct, len(selected_quizzes), hint_view_cnt
        )

    # ===== 헬퍼메서드 =====

    def _play_all_quizzes(self, quizzes):
        """모든 퀴즈 풀기"""
        user_correct = 0
        hint_view_cnt = 0

        for i, quiz in enumerate(quizzes, start=1):
            is_correct, hint_viewed = self._play_single_quiz(quiz, i)

            if is_correct:
                user_correct += 1
            if hint_viewed:
                hint_view_cnt += 1

        return user_correct, hint_view_cnt

    def _play_single_quiz(self, quiz: Quiz, question_number: int) -> tuple:
        """1개 퀴즈 풀기"""
        self.output_view.display_quiz(quiz, question_number)

        user_answer, hint_viewed = self._get_user_answer(quiz)

        if self.quiz_service.is_correct(quiz, user_answer):
            self.output_view.display_correct()
            return True, hint_viewed
        else:
            self.output_view.display_incorrect(quiz.answer)
            return False, hint_viewed

    def _get_user_answer(self, quiz: Quiz):
        """사용자 답변 입력받기 (힌트 처리 포함)"""
        hint_viewed = False

        if not quiz.has_hint():
            return self.input_view.get_quiz_answer(1, 4), hint_viewed

        while True:
            user_input = self.input_view.get_quiz_answer_or_hint(0, 4)

            # 힌트 요청 (0 입력)
            if user_input == 0:
                if not hint_viewed:
                    self.output_view.display_hint(quiz.hint)
                    hint_viewed = True
                else:
                    self.output_view.display_hint_aleady_viewed()
                continue

            # 정답 입력 (1~4)
            return user_input, hint_viewed

    def _display_and_save_result(
        self, user_correct: int, total_quiz_count: int, hint_view_cnt: int
    ):
        """결과 표시 및 저장"""
        user_score = self.quiz_service.calculate_score(
            user_correct, total_quiz_count, hint_view_cnt
        )
        is_update_best_score = self.quiz_service.update_best_score_if_needed(user_score)
        self.output_view.display_quiz_result(user_score, is_update_best_score)
