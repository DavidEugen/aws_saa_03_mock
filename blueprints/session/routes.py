from flask import request, jsonify
from blueprints.session import session_bp
from blueprints.session.queries import save_answer
from blueprints.quiz.queries import get_question_data


@session_bp.route('/<session_id>/<int:q_index>/answer', methods=['POST'])
def submit_answer(session_id, q_index):
    """Submit answer for a question."""
    data = request.get_json()

    if not data or 'question_id' not in data or 'selected_answer' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    question_id = data['question_id']
    selected_answer = data['selected_answer']

    # Get question data
    question = get_question_data(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404

    # Check if answer is correct
    correct_answer = question['correct_answer']

    # For multi-select questions, compare as comma-separated values
    if question['is_multi_select']:
        # Sort both answers and compare
        selected_sorted = ','.join(sorted([x.strip().upper() for x in selected_answer.split(',')]))
        correct_sorted = ','.join(sorted([x.strip().upper() for x in correct_answer.split(',')]))
        is_correct = selected_sorted == correct_sorted
    else:
        # Single select: simple comparison
        is_correct = selected_answer.upper() == correct_answer.upper()

    # Save answer
    save_answer(session_id, question_id, selected_answer, is_correct)

    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': question['explanation']
    })
