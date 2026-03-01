import secrets
from database import get_db


def create_session(total_count):
    """Create a new quiz session."""
    db = get_db()
    session_id = secrets.token_hex(6)

    # Get next round number
    cursor = db.execute('SELECT MAX(round_number) as max_round FROM QuizSessions')
    result = cursor.fetchone()
    round_number = (result['max_round'] or 0) + 1

    # Insert session
    db.execute(
        'INSERT INTO QuizSessions (session_id, round_number, total_count, correct_count) VALUES (?, ?, ?, ?)',
        [session_id, round_number, total_count, 0]
    )
    db.commit()

    return session_id


def save_answer(session_id, question_id, selected_answer, is_correct):
    """Save user answer for a question."""
    db = get_db()

    db.execute(
        'INSERT INTO UserAnswers (session_id, question_id, selected_answer, is_correct, is_skipped) VALUES (?, ?, ?, ?, ?)',
        [session_id, question_id, selected_answer, int(is_correct), 0]
    )

    # Update session correct count
    db.execute(
        'UPDATE QuizSessions SET correct_count = correct_count + ? WHERE session_id = ?',
        [int(is_correct), session_id]
    )

    db.commit()


def get_session_info(session_id):
    """Get session information."""
    db = get_db()
    cursor = db.execute(
        'SELECT session_id, round_number, total_count, correct_count FROM QuizSessions WHERE session_id = ?',
        [session_id]
    )
    return cursor.fetchone()
