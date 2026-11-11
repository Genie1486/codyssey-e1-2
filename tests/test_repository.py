import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from exceptions.repository_exceptions import (
    QuizFileCorruptedError,
    QuizFileIOError,
    QuizFileNotFoundError,
)
from model import Quiz, BestScore
from repository.quiz_repository import QuizRepository


# ============ 파일 I/O 테스트 ============
class TestQuizRepositoryFileIO(unittest.TestCase):

    def setUp(self):
        test_dir = Path(__file__).parent
        self.test_file = test_dir / "test_state.json"
        self.repo = QuizRepository(str(self.test_file))

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_load_data_raises_not_found_when_file_missing(self):
        """파일이 없을 때 QuizFileNotFoundError 발생"""
        with self.assertRaises(QuizFileNotFoundError):
            self.repo._load_data()

    def test_load_data_raises_corrupted_when_json_invalid(self):
        """JSON이 깨졌을 때 QuizFileCorruptedError 발생"""
        with open(self.test_file, "w") as f:
            f.write('{"quizzes": [')

        with self.assertRaises(QuizFileCorruptedError):
            self.repo._load_data()

    def test_load_data_raises_io_error_when_read_fails(self):
        """읽기 중 IOError 발생 시 QuizFileIOError 발생"""
        with patch("builtins.open", side_effect=IOError("읽기 실패")):
            with self.assertRaises(QuizFileIOError):
                self.repo._load_data()

    def test_save_data_raises_io_error_when_open_fails(self):
        """open() 실패 시 QuizFileIOError 발생"""
        test_data = {"quizzes": [], "best_score": 0}

        with patch("builtins.open", side_effect=IOError("파일 열기 실패")):
            with self.assertRaises(QuizFileIOError):
                self.repo._save_data(test_data)

    def test_save_data_raises_io_error_when_dump_fails(self):
        """json.dump() 실패 시 QuizFileIOError 발생"""
        test_data = {"quizzes": [], "best_score": 0}

        with patch("json.dump", side_effect=IOError("디스크 쓰기 실패")):
            with self.assertRaises(QuizFileIOError):
                self.repo._save_data(test_data)


# ============ Quiz CRUD 테스트 ============
class TestQuizRepositoryQuizCRUD(unittest.TestCase):

    def setUp(self):
        self.repo = QuizRepository("")

    def test_get_all_quizzes_returns_quiz_list(self):
        """퀴즈 데이터가 있을 때 Quiz 객체 리스트 반환"""
        fake_data = {
            "quizzes": [
                {
                    "id": 1,
                    "question": "Choose the correct word.",
                    "choices": ["run", "runs", "ran", "running"],
                    "answer": 2,
                }
            ]
        }

        with patch.object(self.repo, "_load_data", return_value=fake_data):
            result = self.repo.get_all_quizzes()

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Quiz)

    def test_get_all_quizzes_returns_empty_list_when_no_quizzes(self):
        """퀴즈가 없을 때 빈 리스트 반환"""
        fake_data = {"quizzes": []}

        with patch.object(self.repo, "_load_data", return_value=fake_data):
            result = self.repo.get_all_quizzes()

        self.assertEqual(len(result), 0)

    def test_create_quiz_saves_new_quiz(self):
        """create_quiz가 _load_data와 _save_data를 올바르게 호출"""
        fake_data = {"quizzes": []}
        fake_quiz = MagicMock()
        fake_quiz.to_dict.return_value = {
            "question": "Test",
            "choices": ["a", "b", "c", "d"],
            "answer": 1,
        }

        with patch.object(
            self.repo, "_load_data", return_value=fake_data
        ), patch.object(self.repo, "_save_data") as mock_save:
            self.repo.save_quiz(fake_quiz)

        expected_data = {
            "quizzes": [
                {
                    "question": "Test",
                    "choices": ["a", "b", "c", "d"],
                    "answer": 1,
                }
            ]
        }
        mock_save.assert_called_once_with(expected_data)


# ============ BestScore CRUD 테스트 ============
class TestQuizRepositoryBestScoreCRUD(unittest.TestCase):

    def setUp(self):
        self.repo = QuizRepository("")

    def test_get_best_score_returns_score(self):
        """get_best_score() 동작 확인"""
        fake_data = {
            "quizzes": [],
            "best_score": {"score": 80, "correct": 4, "total": 5},
        }

        with patch.object(self.repo, "_load_data", return_value=fake_data):
            best_score = self.repo.get_best_score()

        self.assertEqual(best_score.score, 80)

    def test_get_best_score_returns_zero_when_no_key(self):
        """best_score 키가 없을 때 기본값 0 반환"""
        fake_data = {"quizzes": []}

        with patch.object(
            self.repo, "_load_data", return_value=fake_data
        ), patch.object(self.repo, "_save_data") as mock_save:
            result = self.repo.get_best_score()

        self.assertEqual(result.score, 0)

        expected_data = {
            "quizzes": [],
            "best_score": {"score": 0, "correct": 0, "total": 0},
        }
        mock_save.assert_called_once_with(expected_data)

    def test_update_best_score_saves_new_score(self):
        """update_best_score()가 새로운 score를 저장하는 지 확인"""
        fake_data = {"quizzes": [], "best_score": {"score": 100}}
        fake_best_score = MagicMock()
        fake_best_score.to_dict.return_value = {"score": 80, "correct": 4, "total": 5}

        with patch.object(
            self.repo, "_load_data", return_value=fake_data
        ), patch.object(self.repo, "_save_data") as mock_save:
            self.repo.save_best_score(fake_best_score)

        expected_data = {
            "quizzes": [],
            "best_score": {"score": 80, "correct": 4, "total": 5},
        }
        mock_save.assert_called_once_with(expected_data)


if __name__ == "__main__":
    unittest.main()
