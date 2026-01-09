// Загружаем сохраненные настройки при открытии popup
document.addEventListener('DOMContentLoaded', async () => {
  const result = await chrome.storage.sync.get(['n8nUrl']);
  if (result.n8nUrl) {
    document.getElementById('n8nUrl').value = result.n8nUrl;
  }
});

// Обработка сохранения настроек
document.getElementById('saveBtn').addEventListener('click', async () => {
  const n8nUrl = document.getElementById('n8nUrl').value.trim();
  const statusDiv = document.getElementById('status');

  // Валидация URL
  if (!n8nUrl) {
    showStatus('Пожалуйста, введите URL', 'error');
    return;
  }

  try {
    // Проверяем, что это валидный URL
    new URL(n8nUrl);

    // Сохраняем настройки
    await chrome.storage.sync.set({ n8nUrl: n8nUrl });

    showStatus('Настройки успешно сохранены!', 'success');

    // Скрываем сообщение через 2 секунды
    setTimeout(() => {
      statusDiv.style.display = 'none';
    }, 2000);
  } catch (error) {
    showStatus('Неверный формат URL. Пожалуйста, введите правильный URL', 'error');
  }
});

// Функция отображения статуса
function showStatus(message, type) {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = message;
  statusDiv.className = `status ${type}`;
  statusDiv.style.display = 'block';
}

// Обработка добавления слова
document.getElementById('addWordBtn').addEventListener('click', async () => {
  const word = document.getElementById('wordInput').value.trim();
  const wordStatusDiv = document.getElementById('wordStatus');

  if (!word) {
    showWordStatus('Пожалуйста, введите слово', 'error');
    return;
  }

  // Валидация длины слова
  if (word.length < 1 || word.length > 500) {
    showWordStatus('Длина слова должна быть от 1 до 500 символов', 'error');
    return;
  }

  try {
    // Отправляем сообщение в background script
    const response = await chrome.runtime.sendMessage({ action: 'addWord', word: word });

    if (response.success) {
      showWordStatus(`Слово "${word}" успешно добавлено в словарь!`, 'success');
      document.getElementById('wordInput').value = ''; // Очищаем поле
    } else {
      showWordStatus(response.error || 'Ошибка при добавлении слова', 'error');
    }
  } catch (error) {
    showWordStatus('Ошибка при добавлении слова: ' + error.message, 'error');
  }
});

// Функция отображения статуса для слова
function showWordStatus(message, type) {
  const wordStatusDiv = document.getElementById('wordStatus');
  wordStatusDiv.textContent = message;
  wordStatusDiv.className = `status ${type}`;
  wordStatusDiv.style.display = 'block';

  // Скрываем сообщение через 3 секунды
  setTimeout(() => {
    wordStatusDiv.style.display = 'none';
  }, 3000);
}
