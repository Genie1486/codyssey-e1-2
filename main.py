from common.enums.error_type import ResultType
from controller.quiz_game import QuizGame
from repository.quiz_repository import QuizRepository
from service.quiz_service import QuizService
from view import InputView, OutputView

if __name__ == "__main__":
    try:
        input_view = InputView()
        output_view = OutputView()
        quiz_repository = QuizRepository()
        quiz_service = QuizService(quiz_repository)

        game = QuizGame(quiz_service, input_view, output_view)
        game.run()
    except KeyboardInterrupt:
        # Ctrl+C로 종료
        output_view.display_error(ResultType.KEYBOARD_INTERRUPT)
    except EOFError:
        # Ctrl+Z로 인한 일시 중지 후 재개 시에도 정상 종료
        output_view.display_error(ResultType.EOF_ERROR)
    except Exception as e:
        # ← 예상 못한 심각한 오류만 여기서 처리
        output_view.display_error(ResultType.UNEXPECTED_ERROR, str(e))
    finally:
        game.finalize_game()  # 안전 저장
        output_view.display_exit()
