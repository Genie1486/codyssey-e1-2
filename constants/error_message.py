from enum import Enum


class ErrorMessage(Enum):
    EMPTY_INPUT = "⚠️  입력이 없습니다. {}-{} 사이의 정수를 입력하세요."
    INVALID_TYPE = "⚠️  정수 변환에 실패했습니다. {}-{} 사이의 정수를 입력하세요."
    OUT_OF_RANGE = "⚠️  잘못된 입력입니다. {}-{} 사이의 숫자를 입력해주세요."


class QuizMessage(Enum):
    FILE_NOT_FOUND = (
        "⚠️  퀴즈 파일을 찾을 수 없습니다.\n📝 기본 퀴즈로 초기화합니다...\n"
    )
    FILE_CORRUPTED = "⚠️  퀴즈 파일이 손상되었습니다.\n📝 기본 퀴즈로 복구합니다...\n"
    FILE_IO_ERROR = "⚠️  파일 읽기 오류가 발생했습니다.\n📝 기본 퀴즈로 복구합니다...\n"
    NO_QUIZZES = "📝 저장된 퀴즈가 없습니다.\n📝 기본 퀴즈로 초기화합니다...\n"
