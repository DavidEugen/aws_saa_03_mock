// Quiz page JavaScript

const checkAnswerButton = document.getElementById('checkAnswerButton');
const answerForm = document.getElementById('answerForm');
const resultSection = document.getElementById('resultSection');

checkAnswerButton.addEventListener('click', async function(e) {
    e.preventDefault();

    // Get selected answer
    let selectedAnswer = null;

    if (questionData.is_multi_select) {
        // Multi-select: collect all checked values
        const checked = document.querySelectorAll('input[name="answer"]:checked');
        if (checked.length === 0) {
            alert('최소 1개 이상 선택해주세요.');
            return;
        }
        selectedAnswer = Array.from(checked).map(c => c.value).join(',');
    } else {
        // Single select: get the checked value
        const checked = document.querySelector('input[name="answer"]:checked');
        if (!checked) {
            alert('답을 선택해주세요.');
            return;
        }
        selectedAnswer = checked.value;
    }

    // Prepare data
    const questionId = document.querySelector('input[name="question_id"]').value;
    const data = {
        question_id: parseInt(questionId),
        selected_answer: selectedAnswer
    };

    try {
        // Submit answer
        const response = await fetch(
            `/session/${questionData.session_id}/${questionData.q_index}/answer`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            }
        );

        if (!response.ok) {
            throw new Error('Failed to submit answer');
        }

        const result = await response.json();

        // Display result
        displayResult(result);

    } catch (error) {
        console.error('Error:', error);
        alert('답안 제출에 실패했습니다.');
    }
});

function displayResult(result) {
    const resultStatus = document.getElementById('resultStatus');
    const resultDetails = document.getElementById('resultDetails');

    // Set status
    if (result.is_correct) {
        resultStatus.className = 'result-status correct';
        resultStatus.textContent = '✓ 정답입니다!';
    } else {
        resultStatus.className = 'result-status incorrect';
        resultStatus.textContent = '✗ 오답입니다.';
    }

    // Set details
    let detailsHtml = '<div class="detail-row">';
    detailsHtml += '<span class="detail-label">정답:</span>';
    detailsHtml += `<span>${result.correct_answer}</span></div>`;
    detailsHtml += '<div class="detail-row"><span class="detail-label">해설:</span></div>';
    detailsHtml += `<div style="margin-left: 0; padding-left: 80px;">${result.explanation}</div>`;

    resultDetails.innerHTML = detailsHtml;

    // Show result section and hide answer form
    answerForm.style.display = 'none';
    resultSection.classList.remove('hidden');

    // Disable check button
    checkAnswerButton.disabled = true;
}

// Next button
document.getElementById('nextButton').addEventListener('click', function(e) {
    e.preventDefault();

    const nextIndex = questionData.q_index + 1;

    if (nextIndex < questionData.total_questions) {
        // Load next question
        window.location.href = `/quiz/${questionData.session_id}/${nextIndex}`;
    } else {
        // Quiz completed, go to session notes
        window.location.href = `/notes/${questionData.session_id}`;
    }
});
