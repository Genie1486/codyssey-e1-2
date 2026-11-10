import unittest
from model.quiz import Quiz


class TestQuizModel(unittest.TestCase):

    def test_quiz_create_with_all_fields(self):
        """모든 속성을 입력했을 때 Quiz 객체가 올바르게 생성되는지 확인"""
        quiz = Quiz(
            question="1번 문제입니다.",
            choices=["보기1", "보기2", "보기3", "보기4"],
            answer=3,
            hint="힌트입니다.",
        )
        self.assertEqual(quiz.question, "1번 문제입니다.")
        self.assertEqual(quiz.choices[0], "보기1")
        self.assertEqual(quiz.choices[1], "보기2")
        self.assertEqual(quiz.choices[2], "보기3")
        self.assertEqual(quiz.choices[3], "보기4")
        self.assertEqual(quiz.answer, 3)
        self.assertEqual(quiz.hint, "힌트입니다.")

    def test_quiz_create_without_hint_uses_default(self):
        """hint 속성을 입력하지 않아도 Quiz 객체가 올바르게 생성되는지 확인"""
        quiz = Quiz(
            question="1번 문제입니다.",
            choices=["보기1", "보기2", "보기3", "보기4"],
            answer=3,
        )
        self.assertEqual(quiz.hint, "힌트가 등록되지 않았습니다.")

    def test_quiz_create_with_no_args_uses_all_defaults(self):
        """모든 속성을 입력하지 않아도 Quiz 객체가 올바르게 생성되는지 확인"""
        quiz = Quiz()
        self.assertEqual(quiz.question, "")
        self.assertEqual(len(quiz.choices), 0)
        self.assertEqual(quiz.answer, 0)
        self.assertEqual(quiz.hint, "힌트가 등록되지 않았습니다.")

    def test_check_answer_correct(self):
        """check_answer 메서드 동작확인: 정답일 때"""
        quiz = Quiz(question="1+1?", choices=["1", "2", "3"], answer=1)
        self.assertTrue(quiz.check_answer(1))

    def test_check_answer_wrong(self):
        """check_answer 메서드 동작확인: 오답일 때"""
        quiz = Quiz(question="1+1?", choices=["1", "2", "3"], answer=1)
        self.assertFalse(quiz.check_answer(0))


if __name__ == "__main__":
    unittest.main()
