from database import get_db


def get_all_sessions():
    """Get all quiz sessions ordered by round number descending."""
    db = get_db()
    cursor = db.execute(
        'SELECT session_id, round_number, total_count, correct_count FROM QuizSessions ORDER BY round_number DESC'
    )
    return cursor.fetchall()


def get_wrong_answers(session_id):
    """Get all wrong answers for a session with question and answer details."""
    db = get_db()

    cursor = db.execute("""
        SELECT
            ua.session_id,
            ua.question_id,
            ua.selected_answer,
            q.question_text,
            q.correct_answer,
            q.explanation,
            GROUP_CONCAT(a.option_label || ': ' || a.option_text, ' | ') as options
        FROM UserAnswers ua
        JOIN Questions q ON ua.question_id = q.question_id
        LEFT JOIN Answers a ON q.question_id = a.question_id
        WHERE ua.session_id = ? AND ua.is_correct = 0
        GROUP BY ua.question_id
        ORDER BY ua.question_id
    """, [session_id])

    return cursor.fetchall()


def get_session_info(session_id):
    """Get specific session information."""
    db = get_db()
    cursor = db.execute(
        'SELECT session_id, round_number, total_count, correct_count FROM QuizSessions WHERE session_id = ?',
        [session_id]
    )
    return cursor.fetchone()
