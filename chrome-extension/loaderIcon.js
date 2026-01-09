// Анимация circle-loader на иконке и восстановление иконки "W"
let loaderIntervalId = null;
let loaderAngle = 0; // в радианах
const supportsOffscreen = typeof OffscreenCanvas !== 'undefined';

function createCanvas(size) {
  const canvas = new OffscreenCanvas(size, size);
  const ctx = canvas.getContext('2d');
  return { canvas, ctx };
}

function drawLoaderFrame(ctx, size, angle) {
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
  try {
    chrome.action.setTitle({ title: 'Добавление слова…' });
  } catch {}

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
    try {
      chrome.action.setIcon({ imageData });
    } catch {}
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
  if (active) {
    startLoaderIcon();
  } else {
    stopLoaderIcon();
  }
}

// Экспорт в глобальную область для importScripts
self.setProcessingUI = setProcessingUI;
