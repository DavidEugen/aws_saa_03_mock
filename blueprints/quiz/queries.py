import random
from database import get_db


def get_categories():
    """Get all categories."""
    db = get_db()
    cursor = db.execute('SELECT category_id, name FROM Categories ORDER BY name')
    return cursor.fetchall()


def get_questions_by_filters(category_ids, keyword_groups, limit=10):
    """
    Get questions filtered by categories and keyword groups.

    Args:
        category_ids: List of category IDs to include
        keyword_groups: List of keyword groups, each group is a list of keywords
                       (AND within group, OR between groups)
        limit: Number of questions to return

    Returns:
        List of question IDs
    """
    db = get_db()

    if not category_ids:
        return []

    category_placeholders = ','.join('?' * len(category_ids))

    # If no keywords, get random questions from categories
    if not keyword_groups or all(not group for group in keyword_groups):
        query = f"""
            SELECT question_id FROM Questions
            WHERE category_id IN ({category_placeholders})
            ORDER BY RANDOM()
            LIMIT ?
        """
        cursor = db.execute(query, category_ids + [limit])
        return [row[0] for row in cursor.fetchall()]

    # Build queries for each keyword group (AND within group)
    union_queries = []
    params = []

    for group in keyword_groups:
        if not group:
            continue

        # Build WHERE clause for all keywords in this group (AND)
        where_conditions = []
        for keyword in group:
            where_conditions.append(f"""
                (q.question_text LIKE ?
                OR EXISTS (
                    SELECT 1 FROM Answers a
                    WHERE a.question_id = q.question_id
                    AND a.option_text LIKE ?
                ))
            """)

        where_clause = ' AND '.join(where_conditions)
        group_query = f"""
            SELECT q.question_id FROM Questions q
            WHERE q.category_id IN ({category_placeholders})
            AND {where_clause}
        """
        union_queries.append(group_query)

        # Add parameters for this group
        params.extend(category_ids)
        for keyword in group:
            search_term = f'%{keyword}%'
            params.extend([search_term, search_term])

    # Combine all group queries with UNION
    if union_queries:
        combined_query = ' UNION '.join(union_queries)
        full_query = f"""
            SELECT * FROM ({combined_query})
            ORDER BY RANDOM()
            LIMIT ?
        """
        params.append(limit)

        cursor = db.execute(full_query, params)
        return [row[0] for row in cursor.fetchall()]

    return []


def get_question_data(question_id):
    """Get question with all answers."""
    db = get_db()

    # Get question
    cursor = db.execute(
        'SELECT question_id, question_text, is_multi_select, correct_answer, explanation FROM Questions WHERE question_id = ?',
        [question_id]
    )
    question = cursor.fetchone()

    if not question:
        return None

    # Get answers
    cursor = db.execute(
        'SELECT answer_id, option_label, option_text FROM Answers WHERE question_id = ? ORDER BY option_label',
        [question_id]
    )
    answers = cursor.fetchall()

    return {
        'question_id': question['question_id'],
        'question_text': question['question_text'],
        'is_multi_select': question['is_multi_select'],
        'correct_answer': question['correct_answer'],
        'explanation': question['explanation'],
        'answers': answers
    }
