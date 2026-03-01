from flask import render_template, request, redirect, url_for, session
from blueprints.quiz import quiz_bp
from blueprints.quiz.queries import get_categories, get_questions_by_filters, get_question_data
from blueprints.session.queries import create_session


@quiz_bp.route('/setup', methods=['GET'])
def setup():
    """Display quiz setup page."""
    categories = get_categories()
    return render_template('setup.html', categories=categories)


@quiz_bp.route('/start', methods=['POST'])
def start():
    """Start a quiz session with selected filters."""
    # Get form data
    selected_categories = request.form.getlist('categories')
    num_questions = request.form.get('num_questions', '10')

    try:
        num_questions = int(num_questions)
        if num_questions < 1:
            num_questions = 10
    except ValueError:
        num_questions = 10

    # Parse keyword groups
    keyword_groups = []
    group_count = int(request.form.get('group_count', '0'))

    for i in range(group_count):
        keywords = request.form.getlist(f'group_{i}_keywords')
        keywords = [k.strip() for k in keywords if k.strip()]
        if keywords:
            keyword_groups.append(keywords)

    # Convert category_ids to integers
    category_ids = []
    try:
        category_ids = [int(cat) for cat in selected_categories]
    except ValueError:
        pass

    if not category_ids:
        # No categories selected, redirect back
        return redirect(url_for('quiz.setup'))

    # Get filtered questions
    question_ids = get_questions_by_filters(category_ids, keyword_groups, num_questions)

    if not question_ids:
        # No questions found, redirect back
        return redirect(url_for('quiz.setup'))

    # Create session
    session_id = create_session(len(question_ids))

    # Store question IDs in Flask session
    session['quiz_session_id'] = session_id
    session['question_ids'] = question_ids

    # Redirect to first question
    return redirect(url_for('quiz.show_question', session_id=session_id, q_index=0))


@quiz_bp.route('/<session_id>/<int:q_index>', methods=['GET'])
def show_question(session_id, q_index):
    """Display a question."""
    # Verify session matches
    if session.get('quiz_session_id') != session_id:
        return redirect(url_for('quiz.setup'))

    question_ids = session.get('question_ids', [])

    if q_index < 0 or q_index >= len(question_ids):
        return redirect(url_for('notes.session_notes', session_id=session_id))

    question_id = question_ids[q_index]
    question_data = get_question_data(question_id)

    if not question_data:
        return redirect(url_for('quiz.setup'))

    return render_template(
        'quiz.html',
        session_id=session_id,
        q_index=q_index,
        total_questions=len(question_ids),
        question=question_data
    )
