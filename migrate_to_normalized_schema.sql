PRAGMA foreign_keys = OFF;

-- 1. Create Categories table
CREATE TABLE Categories (
  category_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create Questions table
CREATE TABLE Questions (
  question_id INTEGER PRIMARY KEY,
  category_id INTEGER,
  question_text TEXT NOT NULL,
  is_multi_select INTEGER NOT NULL DEFAULT 0,
  correct_answer TEXT NOT NULL,
  explanation TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- 3. Create Answers table
CREATE TABLE Answers (
  answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  question_id INTEGER NOT NULL,
  option_label TEXT NOT NULL,
  option_text TEXT NOT NULL,
  FOREIGN KEY (question_id) REFERENCES Questions(question_id),
  UNIQUE (question_id, option_label)
);

-- 4. Create QuizSessions table
CREATE TABLE QuizSessions (
  session_id TEXT PRIMARY KEY,
  round_number INTEGER,
  total_count INTEGER NOT NULL DEFAULT 0,
  correct_count INTEGER NOT NULL DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. Create UserAnswers table
CREATE TABLE UserAnswers (
  user_answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  question_id INTEGER NOT NULL,
  selected_answer TEXT NOT NULL,
  is_skipped INTEGER NOT NULL DEFAULT 0,
  is_correct INTEGER NOT NULL,
  attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES QuizSessions(session_id),
  FOREIGN KEY (question_id) REFERENCES Questions(question_id)
);

-- 6. Migrate Categories: extract unique categories from questions table
INSERT INTO Categories (name)
SELECT DISTINCT category FROM questions
WHERE category IS NOT NULL AND length(trim(category)) > 0
ORDER BY category;

-- Add default '미분류' category for any NULL values
INSERT OR IGNORE INTO Categories (name) VALUES ('미분류');

-- 7. Migrate Questions: preserve question_id and connect to Categories
INSERT INTO Questions (question_id, category_id, question_text, is_multi_select, correct_answer, explanation, created_at)
SELECT
  q.id,
  COALESCE(c.category_id, (SELECT category_id FROM Categories WHERE name = '미분류')),
  q.question_text,
  q.is_multi_select,
  q.answer,
  q.explanation,
  CURRENT_TIMESTAMP
FROM questions q
LEFT JOIN Categories c ON c.name = q.category;

-- 8. Migrate Answers: normalize option_a through option_f into rows
INSERT INTO Answers (question_id, option_label, option_text)
SELECT id, 'A', option_a FROM questions WHERE option_a IS NOT NULL AND length(trim(option_a)) > 0;

INSERT INTO Answers (question_id, option_label, option_text)
SELECT id, 'B', option_b FROM questions WHERE option_b IS NOT NULL AND length(trim(option_b)) > 0;

INSERT INTO Answers (question_id, option_label, option_text)
SELECT id, 'C', option_c FROM questions WHERE option_c IS NOT NULL AND length(trim(option_c)) > 0;

INSERT INTO Answers (question_id, option_label, option_text)
SELECT id, 'D', option_d FROM questions WHERE option_d IS NOT NULL AND length(trim(option_d)) > 0;

INSERT INTO Answers (question_id, option_label, option_text)
SELECT id, 'E', option_e FROM questions WHERE option_e IS NOT NULL AND length(trim(option_e)) > 0;

INSERT INTO Answers (question_id, option_label, option_text)
SELECT id, 'F', option_f FROM questions WHERE option_f IS NOT NULL AND length(trim(option_f)) > 0;

-- 9. Migrate QuizSessions: direct copy from sessions table
INSERT INTO QuizSessions (session_id, round_number, total_count, correct_count, created_at)
SELECT session_id, round_number, total_count, correct_count, created_at FROM sessions;

-- 10. Migrate UserAnswers: copy from attempts and derive is_skipped field
INSERT INTO UserAnswers (user_answer_id, session_id, question_id, selected_answer, is_skipped, is_correct, attempted_at)
SELECT
  id,
  session_id,
  question_id,
  selected_answer,
  CASE WHEN selected_answer = 'Z' THEN 1 ELSE 0 END AS is_skipped,
  is_correct,
  attempted_at
FROM attempts;

-- 11. Rename old tables with _backup suffix for preservation
ALTER TABLE questions RENAME TO questions_backup;
ALTER TABLE sessions RENAME TO sessions_backup;
ALTER TABLE attempts RENAME TO attempts_backup;

PRAGMA foreign_keys = ON;
