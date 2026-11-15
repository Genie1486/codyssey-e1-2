from common.enums.error_type import ErrorType
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
        output_view.display_error(ErrorType.KEYBOARD_INTERRUPT)
    except EOFError:
        output_view.display_error(ErrorType.EOF_ERROR)
    except Exception as e:
        # ← 예상 못한 심각한 오류만 여기서 처리
        output_view.display_error(ErrorType.UNEXPECTED_ERROR, str(e))
    finally:
        output_view.display_exit()
