# data/default_quizzes.py
"""
기본 TOEIC 문법 퀴즈 데이터
Quiz 객체로 생성하여 관리
"""

from model.quiz import Quiz

DEFAULT_QUIZZES = [
    Quiz(
        question="The manager requested that all employees _______ the mandatory training session next Monday.",
        choices=["attend", "attends", "attended", "will attend"],
        answer=1,
        hint="request, suggest, insist, recommend 등의 동사 뒤에 오는 that절에서는 동사원형을 써요! (가정법 현재 / 당위성의 should 생략)",
    ),
    Quiz(
        question="The new policy will be implemented _______ all departments have reviewed and approved the proposal.",
        choices=["despite", "once", "although", "so that"],
        answer=2,
        hint="빈칸 앞뒤 문맥을 살펴보세요. '~하고 나면 / ~하자마자' 라는 시간의 접속사가 필요해요!",
    ),
    Quiz(
        question="The report _______ by the research team was presented to the board of directors yesterday.",
        choices=["compile", "compiling", "compiled", "to compile"],
        answer=3,
        hint="명사(report)를 뒤에서 꾸며주는 분사를 골라야 해요. report와 compile의 관계가 능동인지 수동인지 생각해보세요!",
    ),
    Quiz(
        question="She finished the project _______ than anyone had expected.",
        choices=["more quickly", "most quickly", "much quickly", "as quickly"],
        answer=1,
        hint="than이 있으면 비교급이 필요해요! quickly는 부사라서 more를 붙여 비교급을 만들어요 😊",
    ),
    Quiz(
        question="Please submit your application form _______ the deadline on Friday.",
        choices=["until", "during", "by", "for"],
        answer=3,
        hint="마감 기한을 나타낼 때 쓰는 전치사를 고르세요! '~까지 (완료)'의 의미예요.",
    ),
]


def load_default_quizzes():
    """
    기본 퀴즈 데이터 반환

    Returns:
        list: Quiz 객체 리스트

    Example:
        >>> quizzes = load_default_quizzes()
        >>> len(quizzes)
        5
        >>> quizzes[0].answer
        1
    """
    return DEFAULT_QUIZZES
