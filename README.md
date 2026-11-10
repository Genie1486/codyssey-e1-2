# E1-2 컴퓨터에게 명령 내리는 말(파이썬) 처음 배우기 


## 1. 프로젝트 개요

## 2. 퀴즈 주제와 선정 이유

## 3. 실행 방법

## 4. 기능 목록

## 5. 파일구조

```bash
quiz_game_app/
│
├── 📄 main.py # 애플리케이션 진입점
├── 📄 state.json # 게임 상태 데이터 저장소 (점수, 히스토리)
│
├── 📁 model/ # 📊 데이터 모델 (MVC - Model)
│       ├── init.py
│       ├── quiz.py # Quiz 클래스 (문제 데이터)
│       └── history.py # History 클래스 (게임 기록 데이터)
│
├── 📁 repository/ # 💾 데이터 접근 계층
│       ├── init.py
│       └── quiz_repository.py # JSON ↔ Model 변환 (CRUD 작업)
│
├── 📁 service/ # ⚙️ 비즈니스 로직 계층
│       ├── init.py
│       └── quiz_service.py # 검증, 게임 로직, 점수 계산
│
├── 📁 view/ # 🖥️ 사용자 인터페이스 (MVC - View)
│       ├── init.py
│       ├── input_view.py # 사용자 입력 처리
│       └── output_view.py # 결과 출력
│
├── 📁 controller/ # 🎮 게임 흐름 제어 (MVC - Controller)
│       ├── init.py
│       └── quiz_game.py # 게임 진행 흐름 조율
│
└── 📁 tests/ # ✅ 단위 테스트
        ├── init.py
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