from view import InputView, OutputView
from service.quiz_service import QuizService
from model.quiz import Quiz
from common.enums import Menu, ResultType
from common.constants.error_message import QuizMessage


class QuizGame:
    _has_existing_data = False
    _is_first_loading = True

    def __init__(
        self, quiz_service: QuizService, input_view: InputView, output_view: OutputView
    ):
        self.quiz_service = quiz_service
        self.input_view = input_view
        self.output_view = output_view

    def run(self):
        self._initialize_game()
        self._play_game()

    def _initialize_game(self):
        """저장된 데이터로 게임 초기화"""
        success, result = self.quiz_service.load_game_state()

        if success:
            self._has_existing_data = True

        self.output_view.display_message(result.get_message())

    def finalize_game(self):
        """게임 종료 시 데이터 저장"""
        success, result = self.quiz_service.save_game_state()
        self.output_view.display_message(result.get_message())

    def _play_game(self):
        while True:
            self._show_menu()  # 이미 만들어둔 메서드 활용!
            choice = self._get_choice()

            if choice == Menu.EXIT.number:
                # main.py에서 finally에서 종료메시지 출력
                break

            self._handle_menu(choice)

    def _handle_menu(self, choice: int):
        if choice == Menu.PLAY.number:
            self._play_quiz()
        elif choice == Menu.ADD.number:
            self._add_quiz()
        elif choice == Menu.LIST.number:
            self._show_quiz_list()
        elif choice == Menu.SCORE.number:
            self._show_best_score()
        elif choice == Menu.DELETE.number:
            self._delete_quiz()

    def _show_menu(self) -> None:
        self.output_view.display_header()
        quiz_count, best_score = self.quiz_service.get_quiz_count_and_best_score()

        if self._is_first_loading:
            self._is_first_loading = False
            if self._has_existing_data:
                self.output_view.display_saved_data_loaded(quiz_count, best_score)
            else:
                self.output_view.display_basic_data_loaded(quiz_count, best_score)

        display_names = [menu.display_name for menu in Menu]
        self.output_view.display_menu(display_names)

    def _get_choice(self) -> int:
        min_val, max_val = Menu.number_range()
        return self.input_view.get_menu_choice(min_val, max_val)

    def _show_quiz_list(self) -> None:
        quizzes = self.quiz_service.get_all_quizzes()
        self.output_view.display_quiz_list(quizzes)

    def _show_best_score(self) -> None:
        best_score = self.quiz_service.get_best_score()
        self.output_view.display_best_score(best_score)

    def _add_quiz(self) -> None:
        # 1. 시작 메시지
        self.output_view.display_add_quiz_start()

        # 2. 입력받기
        quiz_data = self.input_view.get_quiz_input()

        # 3. 서비스 처리
        is_success = self.quiz_service.add_quiz(quiz_data)

        if is_success:
            self.output_view.display_add_quiz_success_result()
        else:
            self.output_view.display_message(QuizMessage.QUIZ_ADD_FAILED)

    def _play_quiz(self) -> None:
        quizzes = self.quiz_service.get_all_quizzes()

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

    def _delete_quiz(self):
        quizzes = self.quiz_service.get_all_quizzes()
        self.output_view.display_quiz_list(quizzes, OutputView.DELETE_QUIZ)

        if len(quizzes) == 0:
            return

        delete_quiz_num = self.input_view.get_delete_quiz_num(1, len(quizzes))

        self.output_view.display_message(
            OutputView.DELETE_QUIZ_FORMAT.format(
                number=delete_quiz_num, question=quizzes[delete_quiz_num - 1].question
            )
        )
        yes_or_no = self.input_view.get_delete_confirm()

        if yes_or_no == "y":
            result = self.quiz_service.remove_quiz(quizzes[delete_quiz_num - 1])
            if result:
                self.output_view.display_message(OutputView.DELETE_QUIZ_COMPLETE)
            else:
                self.output_view.display_message(OutputView.DELETE_QUIZ_FAILED)
