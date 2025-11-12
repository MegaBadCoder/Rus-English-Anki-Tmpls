#!/usr/bin/env python3
"""
Генератор Anki колоды для изучения английских слов
Использует внешние файлы для CSS, JS и HTML шаблонов
"""
import argparse
import csv
import genanki
import random
import sys
from pathlib import Path

from constants import (
    DEFAULT_DECK_NAME,
    DEFAULT_OUTPUT_FILE,
    FIELD_AUDIO_URL,
    FIELD_EXAMPLE_EN,
    FIELD_EXAMPLE_RU,
    FIELD_TRANSCRIPTION,
    FIELD_TRANSLATION,
    FIELD_WORD,
    MODEL_ID,
    MODEL_NAME,
    NUM_TEMPLATES,
    TEMPLATE_EN_TO_RUS,
    TEMPLATE_FILES,
    TEMPLATE_RUS_TO_EN,
    TEMPLATES_DIR,
)


def inject_js_to_html(html, js_code):
    """Вставляет JavaScript код в начало HTML"""
    if not js_code:
        return html
    return f"<script>\n{js_code}\n</script>\n{html}"


class TemplateLoader:
    def __init__(self, templates_dir=TEMPLATES_DIR):
        self.templates_dir = Path(__file__).parent / templates_dir

    def load_file(self, filename):
        file_path = self.templates_dir / filename
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Ошибка: Файл {file_path} не найден.")
            sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении файла {file_path}: {e}")
            sys.exit(1)

    def load_css(self):
        return self.load_file("styles.css")

    def load_js(self):
        return self.load_file("check_answer.js")

    def load_card_template(self, front_file, back_file):
        return {
            "front": self.load_file(front_file),
            "back": self.load_file(back_file),
        }


def create_card_model():
    loader = TemplateLoader()

    css = loader.load_css()
    js_code = loader.load_js()

    en_to_rus = loader.load_card_template(*TEMPLATE_FILES["en_to_rus"])
    rus_to_en = loader.load_card_template(*TEMPLATE_FILES["rus_to_en"])

    model = genanki.Model(
        MODEL_ID,
        MODEL_NAME,
        fields=[
            {"name": FIELD_WORD},
            {"name": FIELD_TRANSCRIPTION},
            {"name": FIELD_TRANSLATION},
            {"name": FIELD_EXAMPLE_EN},
            {"name": FIELD_EXAMPLE_RU},
            {"name": FIELD_AUDIO_URL},
        ],
        templates=[
            {
                "name": TEMPLATE_EN_TO_RUS,
                "qfmt": inject_js_to_html(en_to_rus["front"], js_code),
                "afmt": inject_js_to_html(en_to_rus["back"], js_code),
            },
            {
                "name": TEMPLATE_RUS_TO_EN,
                "qfmt": inject_js_to_html(rus_to_en["front"], js_code),
                "afmt": inject_js_to_html(rus_to_en["back"], js_code),
            },
        ],
        css=css,
    )

    return model


def load_words_from_csv(csv_file):
    words = []
    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                words.append(
                    {
                        "word": row["word"].strip(),
                        "transcription": row["transcription"].strip(),
                        "translation": row["translation"].strip(),
                        "example_en": row["example_en"].strip(),
                        "example_ru": row.get("example_ru", "").strip(),
                        "audio_url": row.get("audio_url", "").strip(),
                    }
                )
    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        sys.exit(1)

    return words


def create_deck(words, deck_name=DEFAULT_DECK_NAME, shuffle=False):
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, deck_name)
    model = create_card_model()

    notes = []
    for word in words:
        note = genanki.Note(
            model=model,
            fields=[
                word["word"],
                word["transcription"],
                word["translation"],
                word["example_en"],
                word["example_ru"],
                word["audio_url"],
            ],
        )
        notes.append(note)

    if shuffle:
        random.shuffle(notes)
        print("Карточки перемешаны случайным образом.")

    for note in notes:
        deck.add_note(note)

    return deck


def main():
    parser = argparse.ArgumentParser(
        description="Генератор Anki колоды для изучения английских слов"
    )
    parser.add_argument("csv_file", help="Путь к CSV файлу со словами")
    parser.add_argument(
        "-o", "--output", default=DEFAULT_OUTPUT_FILE, help="Имя выходного файла"
    )
    parser.add_argument(
        "-n", "--name", default=DEFAULT_DECK_NAME, help="Название колоды"
    )
    parser.add_argument(
        "-s",
        "--shuffle",
        action="store_true",
        help="Перемешать карточки случайным образом",
    )

    args = parser.parse_args()

    if not Path(args.csv_file).exists():
        print(f"Ошибка: CSV файл '{args.csv_file}' не существует.")
        sys.exit(1)

    print(f"Загрузка слов из {args.csv_file}...")
    words = load_words_from_csv(args.csv_file)
    print(f"Загружено {len(words)} слов.")

    print("Создание Anki колоды...")
    deck = create_deck(words, args.name, shuffle=args.shuffle)

    print(f"Генерация {args.output}...")
    genanki.Package(deck).write_to_file(args.output)

    total_cards = len(words) * NUM_TEMPLATES
    print(
        f"Успешно создана колода {args.output} с {total_cards} карточками "
        f"({len(words)} слов x {NUM_TEMPLATES} шаблонов в одной модели)"
    )


if __name__ == "__main__":
    main()
