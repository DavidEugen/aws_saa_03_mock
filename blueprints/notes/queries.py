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
            q.explanation
        FROM UserAnswers ua
        JOIN Questions q ON ua.question_id = q.question_id
        WHERE ua.session_id = ? AND ua.is_correct = 0
        ORDER BY ua.question_id
    """, [session_id])

    wrong_answers = cursor.fetchall()

    # Add options list for each wrong answer
    result = []
    for answer in wrong_answers:
        answer_dict = dict(answer)

        # Get all options for this question
        options_cursor = db.execute("""
            SELECT option_label, option_text
            FROM Answers
            WHERE question_id = ?
            ORDER BY option_label
        """, [answer_dict['question_id']])

        options_list = []
        for opt in options_cursor.fetchall():
            options_list.append({
                'option_label': opt['option_label'],
                'option_text': opt['option_text']
            })

        answer_dict['options_list'] = options_list
        result.append(answer_dict)

    return result


def get_session_info(session_id):
    """Get specific session information."""
    db = get_db()
    cursor = db.execute(
        'SELECT session_id, round_number, total_count, correct_count FROM QuizSessions WHERE session_id = ?',
        [session_id]
    )
    return cursor.fetchone()
