from flask import render_template
from blueprints.notes import notes_bp
from blueprints.notes.queries import get_all_sessions, get_wrong_answers, get_session_info


@notes_bp.route('', methods=['GET'])
def all_sessions():
    """Display all quiz sessions."""
    sessions = get_all_sessions()
    return render_template('notes.html', sessions=sessions)


@notes_bp.route('/<session_id>', methods=['GET'])
def session_notes(session_id):
    """Display wrong answers for a session."""
    session_info = get_session_info(session_id)

    if not session_info:
        return render_template('notes.html', sessions=[])

    wrong_answers = get_wrong_answers(session_id)

    return render_template(
        'session_notes.html',
        session=session_info,
        wrong_answers=wrong_answers
    )
