class QuizRepositoryError(Exception):
    """Repository 계층의 기본 예외"""

    pass


class QuizFileNotFoundError(QuizRepositoryError):
    """파일이 없을 때"""

    pass


class QuizFileCorruptedError(QuizRepositoryError):
    """파일이 손상되었을 때 (JSON 파싱 실패)"""

    pass


class QuizFileIOError(QuizRepositoryError):
    """읽기/쓰기 중 발생한 IO 에러"""

    pass
