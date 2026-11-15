# test_quiz_service.py
import unittest
from unittest.mock import MagicMock, Mock, patch
from service.quiz_service import QuizService
from common.enums.error_type import ResultType


class TestLoadGameState(unittest.TestCase):

    def setUp(self):
        """각 테스트 실행 전 호출 - Mock repository로 QuizService 생성"""
        self.mock_repository = MagicMock()
        self.service = QuizService(self.mock_repository)

    def test_io_error_3회_발생시_False와_FILE_IO_ERROR_반환(self):
        # Given: load_data가 호출될 때마다 IOError 발생하도록 설정
        self.mock_repository.load_data.side_effect = IOError("디스크 읽기 실패")

        # When
        with patch("time.sleep"):  # ⏱️ 재시도 대기시간 0.5초 스킵
            success, result = self.service.load_game_state()

        # Then
        self.assertFalse(success)
        self.assertEqual(result, ResultType.FILE_IO_ERROR)

        # load_data 총 호출 횟수 검증 (최초 1번 + 재시도 3번 = 4번)
        self.assertEqual(self.mock_repository.load_data.call_count, 4)

    def test_2회_IOError_발생_후_3회차_성공(self):
        # given - 2회 IOError 발생 후 3회차에 성공하는 시나리오 설정
        mock_load_data = Mock()
        mock_load_data.side_effect = [IOError, IOError, None]
        self.mock_repository.load_data = mock_load_data

        # when - 대기시간 제거 후 load_data 실행
        with patch("time.sleep"):
            result = self.service.load_game_state()

        # then - 성공 반환값 확인
        self.assertEqual(result, (True, ResultType.DATA_LOAD_COMPLETE))
        # then - load_data 3회 호출 확인 (2회 실패 + 1회 성공)
        self.assertEqual(mock_load_data.call_count, 3)


if __name__ == "__main__":
    unittest.main()
