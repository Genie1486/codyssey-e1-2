# main.py
from controller.quiz_game import QuizGame

if __name__ == "__main__":

    try:
        game = QuizGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\n사용자가 프로그램을 중단했습니다.")
        print("프로그램을 종료합니다.")
    except EOFError:
        print("\n\n입력 스트림이 종료되었습니다.")
        print("프로그램을 종료합니다.")
        # 자동화 테스트나 파이프 실행 시 안전 종료
