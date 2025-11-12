# Константы модели
MODEL_ID = 1707392319
MODEL_NAME = "English Words"

# Названия шаблонов
TEMPLATE_EN_TO_RUS = "EN to RUS"
TEMPLATE_RUS_TO_EN = "RUS to EN"

# Названия полей
FIELD_WORD = "Word"
FIELD_TRANSCRIPTION = "Transcription"
FIELD_TRANSLATION = "Translation"
FIELD_EXAMPLE_EN = "ExampleEn"
FIELD_EXAMPLE_RU = "ExampleRu"
FIELD_AUDIO_URL = "AudioUrl"

# Файлы шаблонов
TEMPLATE_FILES = {
    "en_to_rus": ("card_en_to_rus_front.html", "card_en_to_rus_back.html"),
    "rus_to_en": ("card_rus_to_en_front.html", "card_rus_to_en_back.html"),
}

# Настройки по умолчанию
DEFAULT_OUTPUT_FILE = "english_words.apkg"
DEFAULT_DECK_NAME = "English Words"
TEMPLATES_DIR = "templates"

# Количество шаблонов карточек
NUM_TEMPLATES = 2
