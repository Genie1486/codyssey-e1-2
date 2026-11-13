# main.py
from controller.quiz_game import QuizGame
from service.quiz_service import QuizService
from view import InputView, OutputView
import os

if __name__ == "__main__":
    # 객체 조립 (main.py가 책임짐)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "state.json")

    try:
        game = QuizGame(
            quiz_service=QuizService(file_path),
            input_view=InputView(),
            output_view=OutputView(),
        )
        game.run()
    except KeyboardInterrupt:
        print("\n\n사용자가 프로그램을 중단했습니다.")
        print("프로그램을 종료합니다.")
    except EOFError:
        print("\n\n입력 스트림이 종료되었습니다.")
        print("프로그램을 종료합니다.")
        # 자동화 테스트나 파이프 실행 시 안전 종료
