# Word to Dictionary - Chrome Extension

Расширение для Chrome, которое позволяет быстро добавлять выделенные слова в словарь через n8n webhook.

## Установка

1. Откройте Chrome и перейдите по адресу `chrome://extensions/`
2. Включите "Режим разработчика" (Developer mode) в правом верхнем углу
3. Нажмите кнопку "Загрузить распакованное расширение" (Load unpacked)
4. Выберите папку `chrome-extension`

## Настройка

1. Создайте в n8n workflow с Webhook триггером:
   - Метод: POST
   - Путь: любой (например, `/add-word`)
   - Webhook будет получать JSON: `{ "word": "слово", "timestamp": "2024-01-01T12:00:00.000Z" }`

2. Скопируйте URL вашего webhook (например: `https://your-n8n.com/webhook/add-word`)

3. Кликните на иконку расширения в Chrome
4. Вставьте URL webhook в поле "URL webhook n8n"
5. Нажмите "Сохранить"

## Использование

1. Выделите любое слово или фразу на веб-странице
2. Нажмите правую кнопку мыши
3. Выберите "Добавить [выделенный текст] в словарь"
4. Получите уведомление об успешной отправке

## Структура проекта

```
chrome-extension/
├── manifest.json       # Конфигурация расширения
├── background.js       # Service worker для контекстного меню
├── popup.html          # Интерфейс настроек
├── popup.js            # Логика настроек
├── icon128.svg         # Иконка расширения
└── README.md           # Инструкции
```

## Пример n8n workflow

1. **Webhook Node**:
   - Метод: POST
   - Путь: `/add-word`

2. **Function Node** (опционально - обработка данных):
   ```javascript
   const word = $input.item.json.body.word;
   const timestamp = $input.item.json.body.timestamp;

   return {
     word: word,
     timestamp: timestamp
   };
   ```

3. **Дальнейшие действия**:
   - Сохранение в базу данных
   - Отправка в Google Sheets
   - Добавление в Notion
   - И т.д.

## Примечания

- Расширение отправляет POST запрос с JSON телом
- Данные включают выделенное слово и метку времени
- Уведомления показываются при успешной/неуспешной отправке
- URL webhook хранится в синхронизированном хранилище Chrome

## Иконки

Для правильной работы расширения нужны иконки в форматах PNG:
- icon16.png (16x16)
- icon48.png (48x48)
- icon128.png (128x128)

Вы можете конвертировать icon128.svg в PNG используя онлайн-конвертеры или Photoshop/GIMP.
