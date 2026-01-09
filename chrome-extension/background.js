// Анимация circle-loader и управление иконкой (всё в одном файле)
let loaderIntervalId = null;
let loaderAngle = 0; // в радианах
const supportsOffscreen = typeof OffscreenCanvas !== 'undefined';

function createCanvas(size) {
  const canvas = new (typeof OffscreenCanvas !== 'undefined' ? OffscreenCanvas : ImageData)(size, size);
  // Для OffscreenCanvas доступен 2d контекст, для ImageData — нет. Но сюда мы попадаем только если supportsOffscreen=true.
  // Этот конструктор вызовется только при OffscreenCanvas, иначе используем fallback badge.
  const ctx = canvas.getContext ? canvas.getContext('2d') : null;
  return { canvas, ctx };
}

function drawLoaderFrame(ctx, size, angle) {
  if (!ctx) return;
  ctx.clearRect(0, 0, size, size);

  const center = size / 2;
  const radius = Math.floor(size * 0.35);
  const line = Math.max(2, Math.floor(size * 0.12));

  ctx.beginPath();
  ctx.strokeStyle = '#e5e7eb';
  ctx.lineWidth = line;
  ctx.arc(center, center, radius, 0, Math.PI * 2);
  ctx.stroke();

  ctx.beginPath();
  ctx.strokeStyle = '#0ea5e9';
  ctx.lineCap = 'round';
  ctx.lineWidth = line;
  const span = Math.PI * 0.9;
  ctx.arc(center, center, radius, angle, angle + span);
  ctx.stroke();
}

function drawDefaultWIcon(ctx, size) {
  if (!ctx) return;
  ctx.clearRect(0, 0, size, size);
  ctx.fillStyle = '#ffffff';
  ctx.fillRect(0, 0, size, size);
  ctx.fillStyle = '#111827';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  const fontSize = Math.floor(size * 0.75);
  ctx.font = `bold ${fontSize}px system-ui, -apple-system, Segoe UI, Roboto, Arial`;
  ctx.fillText('W', size / 2, Math.floor(size * 0.55));
}

async function startLoaderIcon() {
  try { chrome.action.setTitle({ title: 'Добавление слова…' }); } catch {}

  if (!supportsOffscreen) {
    try {
      chrome.action.setBadgeText({ text: '…' });
      chrome.action.setBadgeBackgroundColor({ color: '#0ea5e9' });
    } catch {}
    return;
  }

  if (loaderIntervalId) return;

  const sizes = [16, 19, 32, 38];
  const canvases = sizes.map(createCanvas);

  const render = () => {
    loaderAngle = (loaderAngle + Math.PI / 12) % (Math.PI * 2);
    const imageData = {};
    for (let i = 0; i < sizes.length; i++) {
      drawLoaderFrame(canvases[i].ctx, sizes[i], loaderAngle);
      imageData[sizes[i]] = canvases[i].ctx.getImageData(0, 0, sizes[i], sizes[i]);
    }
    try { chrome.action.setIcon({ imageData }); } catch {}
  };

  render();
  loaderIntervalId = setInterval(render, 100);
}

async function stopLoaderIcon() {
  if (loaderIntervalId) {
    clearInterval(loaderIntervalId);
    loaderIntervalId = null;
  }

  if (!supportsOffscreen) {
    try {
      chrome.action.setBadgeText({ text: '' });
      chrome.action.setTitle({ title: 'Готово' });
    } catch {}
    return;
  }

  const sizes = [16, 19, 32, 38];
  const canvases = sizes.map(createCanvas);
  const imageData = {};
  for (let i = 0; i < sizes.length; i++) {
    drawDefaultWIcon(canvases[i].ctx, sizes[i]);
    imageData[sizes[i]] = canvases[i].ctx.getImageData(0, 0, sizes[i], sizes[i]);
  }
  try {
    chrome.action.setIcon({ imageData });
    chrome.action.setTitle({ title: 'Готово' });
  } catch {}
}

function setProcessingUI(active) {
  if (active) startLoaderIcon(); else stopLoaderIcon();
}

// Константы
const FETCH_TIMEOUT = 10000; // 10 секунд
const MIN_WORD_LENGTH = 1;
const MAX_WORD_LENGTH = 500;

// Флаг для предотвращения множественных одновременных запросов
let isProcessing = false;

// Создание контекстного меню при установке расширения
function ensureContextMenu() {
  try {
    chrome.contextMenus.removeAll(() => {
      const _ = chrome.runtime.lastError;
      chrome.contextMenus.create({
        id: 'addWordToDictionary',
        title: 'Добавить "%s" в словарь',
        contexts: ['selection']
      }, () => {
        if (chrome.runtime.lastError) {
          console.error('Ошибка при создании контекстного меню:', chrome.runtime.lastError);
        }
      });
    });
  } catch (error) {
    console.error('Ошибка при создании контекстного меню:', error);
  }
}

chrome.runtime.onInstalled.addListener(() => {
  ensureContextMenu();
});

chrome.runtime.onStartup.addListener(() => {
  ensureContextMenu();
});

// Создаём меню сразу при загрузке сервис-воркера (полезно при ручной перезагрузке расширения)
ensureContextMenu();

// Обработка клика по контекстному меню
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === 'addWordToDictionary') {
    const selectedText = info.selectionText?.trim();

    if (!selectedText) {
      showNotification('Ошибка', 'Не выделен текст для добавления');
      return;
    }

    // Валидация длины слова
    if (selectedText.length < MIN_WORD_LENGTH || selectedText.length > MAX_WORD_LENGTH) {
      showNotification('Ошибка', `Длина текста должна быть от ${MIN_WORD_LENGTH} до ${MAX_WORD_LENGTH} символов`);
      return;
    }

    // Защита от множественных одновременных запросов
    if (isProcessing) {
      showNotification('Информация', 'Запрос уже обрабатывается, подождите...');
      return;
    }

    await sendWordToN8n(selectedText);
  }
});

// Функция отправки слова в n8n
async function sendWordToN8n(word) {
  isProcessing = true;
  setProcessingUI(true);
  
  try {
    // Получаем сохраненный URL из storage
    const result = await chrome.storage.sync.get(['n8nUrl']);
    const n8nUrl = result.n8nUrl;

    if (!n8nUrl) {
      showNotification('Ошибка', 'URL n8n не настроен. Откройте расширение для настройки.');
      return;
    }

    // Валидация URL
    try {
      new URL(n8nUrl);
    } catch (urlError) {
      showNotification('Ошибка', 'Неверный формат URL. Проверьте настройки расширения.');
      return;
    }

    // Создаем AbortController для таймаута
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT);
    try {
      // Отправляем запрос в n8n
      const response = await fetch(n8nUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          word: word,
          timestamp: new Date().toISOString()
        }),
        signal: controller.signal
      });

      if (response.ok) {
        console.log('Слово успешно отправлено:', word);
        showNotification('Успех', `Слово "${word}" добавлено в словарь`);
      } else {
        const errorText = await response.text().catch(() => '');
        throw new Error(`HTTP ${response.status}${errorText ? ': ' + errorText.substring(0, 100) : ''}`);
      }
    } finally {
      clearTimeout(timeoutId);
    }
  } catch (error) {
    console.error('Ошибка при отправке слова:', error);
    
    let errorMessage = 'Не удалось отправить слово в n8n';
    
    if (error.name === 'AbortError') {
      errorMessage = 'Превышено время ожидания ответа от сервера';
    } else if (error instanceof TypeError || error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
      errorMessage = 'Ошибка сети. Проверьте подключение к интернету';
    } else if (error.message.includes('HTTP')) {
      errorMessage = `Ошибка сервера: ${error.message}`;
    }
    
    showNotification('Ошибка', errorMessage);
  } finally {
    isProcessing = false;
    setProcessingUI(false);
  }
}

// Вспомогательная функция для показа уведомлений с обработкой ошибок
function showNotification(title, message) {
  chrome.notifications.create({
    type: 'basic',
    iconUrl: chrome.runtime.getURL('icon.png'),
    title: title,
    message: message
  }).catch(error => {
    // Если иконка не найдена, создаем без неё
    console.warn('Не удалось создать уведомление с иконкой:', error);
    chrome.notifications.create({
      type: 'basic',
      title: title,
      message: message
    }).catch(err => {
      console.error('Не удалось создать уведомление:', err);
    });
  });
}

// Обработка сообщений из popup
chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
  if (request.action === 'addWord') {
    const word = request.word;

    if (!word) {
      sendResponse({ success: false, error: 'Не указано слово для добавления' });
      return;
    }

    // Валидация длины слова
    if (word.length < MIN_WORD_LENGTH || word.length > MAX_WORD_LENGTH) {
      sendResponse({ success: false, error: `Длина текста должна быть от ${MIN_WORD_LENGTH} до ${MAX_WORD_LENGTH} символов` });
      return;
    }

    // Защита от множественных одновременных запросов
    if (isProcessing) {
      sendResponse({ success: false, error: 'Запрос уже обрабатывается, подождите...' });
      return;
    }

    try {
      await sendWordToN8n(word);
      sendResponse({ success: true });
    } catch (error) {
      sendResponse({ success: false, error: 'Ошибка при отправке слова' });
    }
  }

  // Возвращаем true для асинхронных ответов
  return true;
});
