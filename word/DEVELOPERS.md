# Документация для разработчиков

## Архитектура проекта

### Структура файлов

```
word/
├── generate_words_deck.py   # Основной скрипт генерации
├── words.csv                 # База данных слов
├── requirements.txt          # Зависимости Python
├── generate.bat / .sh        # Скрипты запуска
├── README.md                 # Пользовательская документация
├── DEVELOPERS.md             # Эта документация
└── templates/                # Шаблоны для карточек
    ├── README.md             # Документация по шаблонам
    ├── styles.css            # CSS стили
    ├── tts_button.js         # JavaScript для TTS
    ├── check_answer.js       # JavaScript для проверки ответов
    ├── card_en_to_rus_front.html
    ├── card_en_to_rus_back.html
    ├── card_rus_to_en_front.html
    ├── card_rus_to_en_back.html
    ├── card_example_front.html
    └── card_example_back.html
```

## Основные компоненты

### 1. TemplateLoader (класс)

**Назначение:** Загрузка шаблонов из внешних файлов

**Методы:**
- `load_file(filename)` - загружает любой файл
- `load_css()` - загружает CSS стили
- `load_js()` - загружает и объединяет JavaScript файлы
- `load_card_template(front_file, back_file)` - загружает HTML шаблоны

**Пример использования:**
```python
loader = TemplateLoader()
css = loader.load_css()
template = loader.load_card_template("front.html", "back.html")
```

### 2. create_card_models()

**Назначение:** Создает модели карточек Anki

**Возвращает:** Список из 3 моделей:
1. EN → RUS (ID: 1707392319)
2. RUS → EN (ID: 1707392320)
3. Example Practice (ID: 1707392321)

**Особенности:**
- JavaScript встраивается в CSS (требование Anki)
- Каждая модель имеет уникальный ID
- Модели содержат 6 полей

### 3. load_words_from_csv()

**Назначение:** Загружает слова из CSV файла

**Формат CSV:**
```csv
word,transcription,translation,example_en,example_ru,audio_url
```

**Возвращает:** Список словарей с ключами:
- word
- transcription
- translation
- example_en
- example_ru
- audio_url

### 4. create_deck()

**Назначение:** Создает колоду Anki с карточками

**Параметры:**
- `words` - список слов (из load_words_from_csv)
- `deck_name` - название колоды

**Возвращает:** Объект genanki.Deck

## Структура данных

### Модель карточки (genanki.Model)

```python
model = genanki.Model(
    model_id,              # Уникальный ID (int)
    name,                  # Название модели (str)
    fields=[...],          # Поля карточки (list of dict)
    templates=[...],       # Шаблоны (list of dict)
    css=css_string         # CSS + JavaScript (str)
)
```

### Поля карточки

```python
fields = [
    {"name": "Word"},         # Английское слово
    {"name": "Transcription"}, # Транскрипция
    {"name": "Translation"},   # Перевод
    {"name": "ExampleEn"},    # Пример EN
    {"name": "ExampleRu"},    # Пример RU
    {"name": "AudioUrl"},     # URL аудио
]
```

### Шаблон карточки

```python
template = {
    "name": "Card Name",  # Название шаблона
    "qfmt": html_front,   # HTML лицевой стороны
    "afmt": html_back,    # HTML обратной стороны
}
```

## JavaScript API

### Функции в tts_button.js

```javascript
createTTSButton(text)
```
Воспроизводит текст через синтез речи.

**Параметры:**
- `text` (string) - текст для озвучки

**Особенности:**
- Выбирает американский английский голос
- Скорость: 0.8
- Высота тона: 1.0

### Функции в check_answer.js

```javascript
checkTranslationAnswer(feedbackId, storageKey, userAnswer, correctAnswer)
```
Проверяет перевод слова (EN → RUS).

**Параметры:**
- `feedbackId` - ID элемента для отображения результата
- `storageKey` - ключ localStorage для очистки
- `userAnswer` - ответ пользователя
- `correctAnswer` - правильный ответ

**Особенности:**
- Поддерживает множественные ответы через `;`
- Игнорирует регистр
- Очищает localStorage после проверки

```javascript
checkWordAnswer(feedbackId, storageKey, userAnswer, correctAnswer)
```
Проверяет английское слово (RUS → EN).

**Параметры:** аналогично `checkTranslationAnswer`

**Особенности:**
- Строгая проверка (точное совпадение)
- Игнорирует регистр

```javascript
displayExampleAnswer(feedbackId, storageKey, userAnswer, correctAnswer)
```
Отображает ответ для практики с примерами.

**Параметры:** аналогично предыдущим функциям

**Особенности:**
- Не проверяет правильность, только показывает оба варианта

## CSS классы

### Основные классы

- `.card` - контейнер карточки
- `.word` - английское слово
- `.transcription` - транскрипция
- `.translation` - перевод
- `.example` - контейнер примера
- `.example-en` - английский пример
- `.example-ru` - русский пример

### Классы состояния

- `.feedback` - контейнер для обратной связи
- `.correct` - правильный ответ
- `.incorrect` - неправильный ответ
- `.input-correct` - input с правильным ответом
- `.input-incorrect` - input с неправильным ответом

## Расширение функционала

### Добавление нового типа карточки

1. Создайте HTML шаблоны:
   - `card_new_type_front.html`
   - `card_new_type_back.html`

2. Добавьте модель в `create_card_models()`:
```python
new_template = loader.load_card_template(
    "card_new_type_front.html",
    "card_new_type_back.html"
)

model_new = genanki.Model(
    1707392322,  # Новый уникальный ID
    "English Words - New Type",
    fields=[...],
    templates=[{
        "name": "New Type",
        "qfmt": new_template["front"],
        "afmt": new_template["back"],
    }],
    css=full_css,
)
```

3. Добавьте модель в возвращаемый список

### Добавление новых полей

1. Обновите CSV файл с новой колонкой
2. Обновите `load_words_from_csv()`:
```python
"new_field": row["new_field"].strip() if "new_field" in row else ""
```

3. Добавьте поле в модели:
```python
fields=[
    # ... существующие поля
    {"name": "NewField"},
]
```

4. Используйте в HTML шаблонах:
```html
<div>{{NewField}}</div>
```

### Добавление новых JavaScript функций

1. Создайте новый файл в `templates/` (например, `my_function.js`)
2. Обновите `TemplateLoader.load_js()`:
```python
def load_js(self):
    tts_js = self.load_file("tts_button.js")
    check_js = self.load_file("check_answer.js")
    my_js = self.load_file("my_function.js")
    return f"{tts_js}\n\n{check_js}\n\n{my_js}"
```

## Отладка

### Проверка шаблонов

```python
loader = TemplateLoader()
print(loader.load_css())  # Проверка CSS
print(loader.load_js())   # Проверка JS
```

### Проверка генерации

```bash
python generate_words_deck.py words.csv -o test.apkg
```

### Проверка в Anki

1. Импортируйте колоду
2. Tools → Preferences → Review → Show debug console
3. Изучайте карточки и смотрите на ошибки в консоли

## Соглашения о коде

1. **Python:**
   - PEP 8 стиль
   - Docstrings для всех функций
   - UTF-8 кодировка

2. **HTML:**
   - Правильная вложенность
   - Semantic HTML

3. **CSS:**
   - BEM или простая структура
   - Комментарии для сложных стилей

4. **JavaScript:**
   - ES5 синтаксис (для совместимости с Anki)
   - Комментарии для функций
   - Избегать глобальных переменных

## Тестирование

### Тест загрузки шаблонов
```python
loader = TemplateLoader()
assert loader.load_css() != ""
assert loader.load_js() != ""
```

### Тест создания моделей
```python
models = create_card_models()
assert len(models) == 3
assert all(hasattr(m, 'fields') for m in models)
```

### Тест загрузки слов
```python
words = load_words_from_csv("words.csv")
assert len(words) > 0
assert all('word' in w for w in words)
```

## Производительность

- Загрузка файлов выполняется один раз при создании моделей
- CSV файл читается построчно (эффективно для больших файлов)
- genanki создает архив в памяти (быстро, но может потреблять RAM)

## Известные ограничения

1. **JavaScript в Anki:**
   - Ограниченный доступ к Web APIs
   - Нет импорта модулей ES6
   - Должен быть встроен в CSS

2. **Шаблоны Mustache:**
   - Нет логики в шаблонах
   - Только простые подстановки переменных

3. **genanki:**
   - Не поддерживает медиа файлы напрямую
   - Требует уникальные ID моделей

## Контакты и поддержка

При возникновении вопросов или нахождении ошибок:
1. Проверьте документацию
2. Посмотрите примеры в коде
3. Создайте issue в репозитории

