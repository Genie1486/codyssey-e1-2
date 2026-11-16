# common/error_type.py
from enum import Enum


class ResultType(Enum):
    """프로그램 전체의 결과 타입 관리"""

    # 파일 불러오기, 파일 저장
    DATA_LOAD_COMPLETE = "DATA_LOAD_COMPLETE"
    DATA_SAVE_COMPLETE = "DATA_SAVE_COMPLETE"
    NO_QUIZZES = "NO_QUIZZES"

    # 사용자 입력 관련
    KEYBOARD_INTERRUPT = "USER_INTERRUPT"
    EOF_ERROR = "EOF_ERROR"

    # 데이터 관련
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_CORRUPTED = "FILE_CORRUPTED"
    FILE_IO_ERROR = "FILE_IO_ERROR"
    INVALID_DATA = "INVALID_DATA"

    # 기타
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"

    def get_message(self) -> str:
        """에러 타입별 메시지 반환"""
        messages = {
            ResultType.DATA_LOAD_COMPLETE: "데이터 로드 완료",
            ResultType.DATA_SAVE_COMPLETE: "데이터 저장 완료",
            ResultType.NO_QUIZZES: "퀴즈 개수 0개",
            ResultType.KEYBOARD_INTERRUPT: "사용자가 프로그램을 중단했습니다.",
            ResultType.EOF_ERROR: "입력 스트림이 종료되었습니다.",
            ResultType.FILE_NOT_FOUND: "필요한 파일을 찾을 수 없습니다.",
            ResultType.FILE_CORRUPTED: "파일이 손상되었습니다. 파일을 다시 확인해주세요.",
            ResultType.FILE_IO_ERROR: "파일 읽기/쓰기 중 오류가 발생했습니다.",
            ResultType.INVALID_DATA: "데이터 형식이 올바르지 않습니다.",
            ResultType.UNEXPECTED_ERROR: "예상치 못한 오류가 발생했습니다.",
        }
        return messages.get(self, "알 수 없는 오류입니다.")
