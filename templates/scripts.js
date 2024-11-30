$(document).ready(function () {
    const $chatBody = $('#chat-body');
    const $userInput = $('#user-input');
    const $submitBtn = $('#submit-btn');
    const $suggestedQuestions = $('.suggested-questions .btn');

    function addMessage(message, type) {
        const messageElement = $(`
            <div class="message ${type} d-flex">
                ${message}
            </div>
        `);
        $chatBody.append(messageElement);
        scrollToBottom();
    }

    function scrollToBottom() {
        $chatBody.scrollTop($chatBody[0].scrollHeight);
    }

    function submitQuestion(query) {
        $userInput.val('');
        addMessage(query, 'user');
        addMessage('Searching for an answer...', 'bot');

        $.ajax({
            url: '/ask',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ user_query: query }),
            success: function (response) {
                $chatBody.find('.message.bot:last').html(`
                    <div class="w-100">
                        <strong>Answer:</strong> ${response.answer}
                        <div class="mt-2 d-flex align-items-center">
                            <span class="me-2">Was this helpful?</span>
                            <button class="feedback-btn text-success me-2" data-feedback="up">
                                <i class="bi bi-hand-thumbs-up"></i>
                            </button>
                            <button class="feedback-btn text-danger" data-feedback="down">
                                <i class="bi bi-hand-thumbs-down"></i>
                            </button>
                        </div>
                    </div>
                `);

                if (response.similar_questions && response.similar_questions.length) {
                    const relatedQuestionsHtml = response.similar_questions
                        .slice(0, 3)
                        .map(q => `
                            <li class="list-group-item list-group-item-action related-question" data-question="${q.question}">
                                ${q.question}
                            </li>
                        `)
                        .join('');

                    addMessage(`
                        <div class="w-100">
                            <strong>Related Questions:</strong>
                            <ul class="list-group related-questions mt-2">
                                ${relatedQuestionsHtml}
                            </ul>
                        </div>
                    `, 'bot');
                }
                scrollToBottom();
            },
            error: function () {
                $chatBody.find('.message.bot:last').html(`
                    <span class="text-danger">
                        <i class="bi bi-exclamation-triangle me-2"></i>
                        An unexpected error occurred.
                    </span>
                `);
            }
        });
    }

    $submitBtn.on('click', function () {
        const query = $userInput.val().trim();
        if (query) submitQuestion(query);
    });

    $userInput.on('keypress', function (e) {
        if (e.which === 13) {
            const query = $(this).val().trim();
            if (query) submitQuestion(query);
        }
    });

    $suggestedQuestions.on('click', function () {
        const question = $(this).text();
        $userInput.val(question);
        submitQuestion(question);
    });

    $chatBody.on('click', '.related-question', function () {
        const question = $(this).data('question');
        $userInput.val(question);
        submitQuestion(question);
    });
});
