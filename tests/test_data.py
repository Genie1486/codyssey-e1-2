import unittest
from data.default_quizzes import load_default_quizzes
from model.quiz import Quiz


class TestData(unittest.TestCase):
    def test_default_quizzes(self):
        """load_load_defualt_quizzes 메서드 동작확인 : 기본 퀴즈 데이터 잘 불러와지는 지 확인"""
        # Given, When : 퀴즈 데이터 불러오기
        quizzes = load_default_quizzes()

        # Then : 기본 퀴즈 데이터 확인
        # 1️⃣ 개수 확인
        self.assertEqual(len(quizzes), 5)

        # 2️⃣ 모두 Quiz 객체인지 확인
        for quiz in quizzes:
            self.assertIsInstance(quiz, Quiz)

        # 3️⃣ 각 퀴즈가 필수 속성을 가지는지 확인
        self.assertTrue(hasattr(quizzes[0], "question"))
        self.assertTrue(hasattr(quizzes[0], "choices"))
        self.assertTrue(hasattr(quizzes[0], "answer"))
        self.assertTrue(hasattr(quizzes[0], "hint"))


if __name__ == "__main__":
    unittest.main()
