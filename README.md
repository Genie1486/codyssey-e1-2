# E1-2 컴퓨터에게 명령 내리는 말(파이썬) 처음 배우기 


## 1. 프로젝트 개요

## 2. 퀴즈 주제와 선정 이유

### 1️⃣ 개인 학습 필요성
- 현재 TOEIC 공부 중이며, 프로젝트를 마무리 후 **실제 학습 도구**로 활용 가능
- 게임 히스토리 기능으로 학습 동기 부여 가능
- **매일 지정 시간 카톡 알람**으로 학습 습관 형성

### 2️⃣ 시장 기회 발굴
- 기존 TOEIC 앱(산타토익 등)은 월 6만원대의 높은 비용
- 본 프로젝트를 기반으로 **저가형 학습 솔루션** 개발 가능
- 추후 AI 기술 접목으로 **차별화된 서비스** 구현 계획

### 3️⃣ 기술 확장성 (AI 기반 맞춤형 학습)
- **Phase 1**: 문법 모의고사 진행 후 오답 기록하는 시스템 구현
- **Phase 2**: 틀린 문제 유형 분석 & 통계
- **Phase 3**: AI 기반 유사 문제 자동 생성 및 추천
  - 예: "관계대명사 오답" → AI가 같은 유형의 새로운 문제 생성 → 반복 학습
- **Phase 4**: 웹/모바일 서비스화

### 4️⃣ 사회적 가치
- 오답 → 분석 → 맞춤형 재학습의 **선순환 구조**로 학습 격차 해소
- 저비용 고효율 학습 플랫폼으로 **교육 접근성 개선**

## 3. 실행 방법

## 4. 기능 목록

## 5. 파일구조

```bash
quiz_game_app/
│
├── 📄 main.py # 애플리케이션 진입점
├── 📄 state.json # 게임 상태 데이터 저장소 (점수, 히스토리)
│
├── 📁 data/ # 📦 기본 데이터
│       ├── __init__.py
│       └── default_quizzes.py # 기본 퀴즈 데이터 (하드코딩)
│
├── 📁 model/ # 📊 데이터 모델 (MVC - Model)
│       ├── __init__.py
│       ├── quiz.py # Quiz 클래스 (문제 데이터)
│       └── history.py # History 클래스 (게임 기록 데이터)
│
├── 📁 repository/ # 💾 데이터 접근 계층
│       ├── __init__.py
│       └── quiz_repository.py # JSON ↔ Model 변환 (CRUD 작업)
│
├── 📁 service/ # ⚙️ 비즈니스 로직 계층
│       ├── __init__.py
│       └── quiz_service.py # 검증, 게임 로직, 점수 계산
│
├── 📁 view/ # 🖥️ 사용자 인터페이스 (MVC - View)
│       ├── __init__.py
│       ├── input_view.py # 사용자 입력 처리
│       └── output_view.py # 결과 출력
│
├── 📁 controller/ # 🎮 게임 흐름 제어 (MVC - Controller)
│       ├── __init__.py
│       └── quiz_game.py # 게임 진행 흐름 조율
│
└── 📁 tests/ # ✅ 단위 테스트
        ├── __init__.py
        ├── test_model.py
        ├── test_repository.py
        ├── test_service.py
        ├── test_view.py
        └── test_controller.py
```

```bash
🏗️ MVC 패턴 아키텍처
시각화 자료 
```


### 책임 분담
| 계층 | 파일 | 책임 |
|------|------|------|
| **Model** | `quiz.py`, `history.py` | 데이터 구조 정의 |
| **Repository** | `quiz_repository.py` | JSON ↔ Model 변환, CRUD |
| **Service** | `quiz_service.py` | 검증, 비즈니스 로직, 점수 계산 |
| **View** | `input_view.py`, `output_view.py` | 사용자 입출력 |
| **Controller** | `quiz_game.py` | 게임 흐름 조율 |




## 6. 데이터 파일 설명 (state.json 경로, 역할, 스키마)


```json
{
    "quizzes": [
        {
            "id": 1,
            "question": "The manager requested that all employees _______ the mandatory training session next Monday.",
            "choices": [
                "attend",
                "attends",
                "attended",
                "will attend"
            ],
            "answer": 0,
            "hint": "request, suggest, insist, recommend 등의 동사 뒤에 오는 that절에서는 동사원형을 써요!"
        },
        {
            "id": 2,
            "question": "The new policy will be implemented _______ all departments have reviewed and approved the proposal.",
            "choices": [
                "despite",
                "once",
                "although",
                "so that"
            ],
            "answer": 1
        }
    ],
    "best_score": {
        "score": 0,
        "correct": 0,
        "total": 0
    },
    "score_history": [
        {
            "date": "2024-01-15",
            "time": "14:30:45",
            "correct": 3,
            "total": 5,
            "score": 60
        }
    ]
}
```

## 7. 트러블 슈팅
- 테스트 코드 도입(main.py에서 테스트 코드 만들었는데... 코드를 보존하고 싶었음)