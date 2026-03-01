# AWS SAA-C03 Quiz App

Flask + Vanilla JavaScript로 구현된 AWS SAA-C03 시험 문제풀이 애플리케이션입니다.

## 기능

### 1. 문제 출제
- **카테고리 선택**: 10개 카테고리 중 선택 (전체선택, 전체해제 버튼 지원)
- **문제 수 선택**: 1~100개 문제 중 선택 (기본값: 10)
- **키워드 검색**:
  - AND 그룹 단위로 키워드 추가 (같은 그룹 내 키워드는 AND 조건)
  - 그룹 간은 OR 조건
  - 예시: (S3 AND VPC) OR (EC2) → S3과 VPC를 모두 포함하거나 EC2를 포함하는 문제
  - 검색 범위: 문제 텍스트 + 선택지 텍스트

### 2. 문제 풀이
- **단일/다중 선택**: 문제 유형에 따라 라디오버튼(단일) 또는 체크박스(다중) 표시
- **정답 확인**:
  - "정답 확인" 버튼으로 답안 제출
  - 정오답 여부와 정답, 해설 즉시 표시
  - 다중 선택 문제도 정확히 검사 (순서 무관)
- **진행률 표시**: 상단에 현재 문제/전체 문제 수와 프로그레스 바
- **다음 문제**: 마지막 문제 후 오답노트로 자동 이동

### 3. 오답노트
- **세션 목록**: 회차별 총 문제, 정답 수, 점수 표시
- **오답 상세보기**:
  - 틀린 문제만 필터링
  - 문제 텍스트, 내 답, 정답, 선택지, 해설 표시
  - 회차별 통계 표시

## 파일 구조

```
quiz_app_new/
├── app.py                          # Flask 앱 진입점
├── database.py                     # DB 연결 관리
├── requirements.txt                # 의존성
├── blueprints/
│   ├── quiz/                       # 문제 설정 및 출제
│   │   ├── __init__.py
│   │   ├── routes.py              # 라우트 (setup, start, show_question)
│   │   └── queries.py             # DB 쿼리 (categories, questions, filtering)
│   ├── session/                    # 세션 및 답안 관리
│   │   ├── __init__.py
│   │   ├── routes.py              # 라우트 (answer submission)
│   │   └── queries.py             # DB 쿼리 (create_session, save_answer)
│   └── notes/                      # 오답노트
│       ├── __init__.py
│       ├── routes.py              # 라우트 (all_sessions, session_notes)
│       └── queries.py             # DB 쿼리 (wrong_answers)
├── templates/
│   ├── base.html                  # 공통 레이아웃
│   ├── setup.html                 # 문제 설정 페이지
│   ├── quiz.html                  # 문제 풀이 페이지
│   ├── notes.html                 # 세션 목록
│   └── session_notes.html         # 오답 상세보기
└── static/
    ├── style.css                  # 스타일시트
    ├── setup.js                   # 키워드 그룹 관리
    └── quiz.js                    # 답안 제출 및 다음 이동
```

## 데이터베이스 스키마

```
Categories: category_id, name
Questions: question_id, category_id, question_text, is_multi_select, correct_answer, explanation
Answers: answer_id, question_id, option_label (A~F), option_text
QuizSessions: session_id, round_number, total_count, correct_count, created_at
UserAnswers: user_answer_id, session_id, question_id, selected_answer, is_correct, is_skipped
```

## 설치 및 실행

### 필수 요구사항
- Python 3.7+
- Flask 2.3.0+

### 설치
```bash
pip install -r requirements.txt
```

### 실행
```bash
python app.py
```

브라우저에서 `http://localhost:5000` 으로 접속하세요.

## 주요 API 라우트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/` | 홈 (setup으로 리다이렉트) |
| GET | `/quiz/setup` | 문제 설정 페이지 |
| POST | `/quiz/start` | 세션 생성 후 첫 문제로 이동 |
| GET | `/quiz/<session_id>/<q_index>` | 문제 표시 |
| POST | `/session/<session_id>/<q_index>/answer` | 답안 제출 (JSON 응답) |
| GET | `/notes` | 세션 목록 |
| GET | `/notes/<session_id>` | 세션 오답 목록 |

## 개발 참고사항

### 키워드 검색 로직
- 각 AND 그룹별로 SQL 서브쿼리 생성
- UNION으로 그룹 간 OR 결합
- 매개변수 바인딩으로 SQL Injection 방지

### 다중 선택 문제 처리
- correct_answer가 "A,B" 형태로 저장
- selected_answer도 "A,B" 형태로 전달받음
- 소팅 후 비교하여 순서 무관하게 정답 검사

### 세션 관리
- session_id: `secrets.token_hex(6)` (12자 랜덤 문자열)
- Flask session에 question_ids 리스트 저장
- 페이지 리로드 시에도 진행 상태 유지

## 테스트

```bash
python -c "from app import create_app; app = create_app(); print('App OK')"
```

## 라이센스

이 프로젝트는 교육 목적으로 제작되었습니다.
