from enum import Enum


class ErrorMessage(Enum):
    EMPTY_INPUT = "⚠️  입력이 없습니다. {}-{} 사이의 정수를 입력하세요."
    INVALID_TYPE = "⚠️  정수 변환에 실패했습니다. {}-{} 사이의 정수를 입력하세요."
    OUT_OF_RANGE = "⚠️  잘못된 입력입니다. {}-{} 사이의 숫자를 입력해주세요."
