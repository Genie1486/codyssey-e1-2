from enum import Enum


class ErrorMessage(Enum):
    EMPTY_INPUT = "⚠️  입력이 없습니다."
    NUMBER_RANGE = "{}-{} 사이의 정수를 입력하세요."
    NOT_AN_INTEGER = "⚠️  정수 변환에 실패했습니다."
    OUT_OF_RANGE = "⚠️  범위에 맞지 않는 숫자입니다."


class QuizMessage(Enum):
    QUIZ_ADD_FAILED = "⚠️  퀴즈 추가 실패하였습니다."
    FILE_NOT_FOUND = (
        "⚠️  퀴즈 파일을 찾을 수 없습니다.\n📝 기본 퀴즈로 초기화합니다...\n"
    )
    FILE_CORRUPTED = "⚠️  퀴즈 파일이 손상되었습니다.\n📝 기본 퀴즈로 복구합니다...\n"
    FILE_IO_ERROR = "⚠️  파일 읽기 오류가 발생했습니다.\n📝 기본 퀴즈로 복구합니다...\n"
    NO_QUIZZES = "📝 저장된 퀴즈가 없습니다.\n📝 기본 퀴즈로 초기화합니다...\n"
