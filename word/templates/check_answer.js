// Функция проверки ответа для карточки EN -> RUS
window.checkTranslationAnswer = function(feedbackId, storageKey, userAnswer, correctAnswer) {
    var feedback = document.getElementById(feedbackId);
    if (!feedback) {
        console.error('Element with id "' + feedbackId + '" not found');
        return;
    }
    
    userAnswer = userAnswer.trim().toLowerCase();
    correctAnswer = correctAnswer.toLowerCase();
    
    // Разрешаем несколько вариантов ответа через точку с запятой
    var correctAnswers = correctAnswer.split(';').map(a => a.trim());
    var isCorrect = correctAnswers.some(answer => 
        userAnswer === answer || userAnswer.includes(answer)
    );

    if (isCorrect) {
        feedback.className = 'feedback correct';
        feedback.innerHTML = '✓ Правильно! Ваш ответ: ' + userAnswer;
        feedback.style.display = 'block';
    } else {
        feedback.className = 'feedback incorrect';
        feedback.innerHTML = '✗ Неправильно.<br>Ваш ответ: ' + (userAnswer || '(пусто)') + '<br>Правильный ответ: ' + correctAnswer;
        feedback.style.display = 'block';
    }
    localStorage.removeItem(storageKey);
};

// Функция проверки ответа для карточки RUS -> EN
window.checkWordAnswer = function(feedbackId, storageKey, userAnswer, correctAnswer) {
    var feedback = document.getElementById(feedbackId);
    if (!feedback) {
        console.error('Element with id "' + feedbackId + '" not found');
        return;
    }
    
    userAnswer = userAnswer.trim().toLowerCase();
    correctAnswer = correctAnswer.toLowerCase();

    if (userAnswer === correctAnswer) {
        feedback.className = 'feedback correct';
        feedback.innerHTML = '✓ Правильно! Ваш ответ: ' + userAnswer;
        feedback.style.display = 'block';
    } else {
        feedback.className = 'feedback incorrect';
        feedback.innerHTML = '✗ Неправильно.<br>Ваш ответ: ' + (userAnswer || '(пусто)') + '<br>Правильный ответ: ' + correctAnswer;
        feedback.style.display = 'block';
    }
    localStorage.removeItem(storageKey);
};

// Функция отображения ответа для практики с примерами
window.displayExampleAnswer = function(feedbackId, storageKey, userAnswer, correctAnswer) {
    var feedback = document.getElementById(feedbackId);
    if (!feedback) {
        console.error('Element with id "' + feedbackId + '" not found');
        return;
    }
    
    if (userAnswer.trim()) {
        feedback.className = 'feedback';
        feedback.innerHTML = '<strong>Ваш ответ:</strong><br>' + userAnswer + '<br><br><strong>Правильный ответ:</strong><br>' + correctAnswer;
        feedback.style.display = 'block';
        feedback.style.background = '#e3f2fd';
        feedback.style.color = '#1565c0';
        feedback.style.border = '2px solid #90caf9';
    }
    localStorage.removeItem(storageKey);
};

