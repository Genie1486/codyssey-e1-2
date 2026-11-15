# common/error_type.py
from enum import Enum


class ErrorType(Enum):
    """프로그램 전체의 에러 타입 관리"""

    # 사용자 입력 관련
    KEYBOARD_INTERRUPT = "USER_INTERRUPT"
    EOF_ERROR = "EOF_ERROR"

    # 데이터 관련
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    INVALID_DATA = "INVALID_DATA"

    # 기타
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"

    def get_message(self) -> str:
        """에러 타입별 메시지 반환"""
        messages = {
            ErrorType.KEYBOARD_INTERRUPT: "사용자가 프로그램을 중단했습니다.",
            ErrorType.EOF_ERROR: "입력 스트림이 종료되었습니다.",
            ErrorType.FILE_NOT_FOUND: "필요한 파일을 찾을 수 없습니다.",
            ErrorType.INVALID_DATA: "데이터 형식이 올바르지 않습니다.",
            ErrorType.UNEXPECTED_ERROR: "예상치 못한 오류가 발생했습니다.",
        }
        return messages.get(self, "알 수 없는 오류입니다.")
