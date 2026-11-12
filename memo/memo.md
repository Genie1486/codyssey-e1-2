**순서대로 가자!** 🎯

---

## 추천 순서

### 1️⃣ **InputView에 퀴즈 입력 메서드 추가**
   - `input_quiz_data()` 또는 비슷한 이름
   - 문제, 선택지 4개, 정답, 힌트 입력받기
   - 입력값 검증 포함

### 2️⃣ **Service에 퀴즈 추가 메서드 추가**
   - `add_quiz()` 메서드
   - 받은 데이터로 Quiz 객체 생성
   - Repository에 저장

### 3️⃣ **Repository에 퀴즈 저장 메서드 추가**
   - `save_quiz()` 메서드 (기존 `save_quizzes()`와 다름)
   - 새 퀴즈를 기존 퀴즈 리스트에 추가
   - state.json에 저장

### 4️⃣ **Controller에 라우팅 추가**
   - 메뉴에서 "퀴즈 추가" 선택 시 호출
   - InputView → Service → Repository 연결

### 5️⃣ **OutputView에 메시지 추가**
   - 성공/실패 메시지 출력

---

**1번부터 시작할까?** InputView 수정하는 거부터! 💪