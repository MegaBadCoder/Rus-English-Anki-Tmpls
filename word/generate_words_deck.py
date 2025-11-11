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


def inject_js_to_html(html, js_code):
    """Вставляет JavaScript код в начало HTML"""
    if not js_code:
        return html
    return f"<script>\n{js_code}\n</script>\n{html}"


class TemplateLoader:
    """Класс для загрузки шаблонов из файлов"""

    def __init__(self, templates_dir="templates"):
        self.templates_dir = Path(__file__).parent / templates_dir

    def load_file(self, filename):
        """Загружает содержимое файла"""
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
        """Загружает CSS стили"""
        return self.load_file("styles.css")

    def load_js(self):
        """Загружает JavaScript код"""
        check_js = self.load_file("check_answer.js")
        return check_js

    def load_card_template(self, front_file, back_file):
        """Загружает HTML шаблоны для карточки"""
        return {
            "front": self.load_file(front_file),
            "back": self.load_file(back_file),
        }


def create_card_model():
    """Создает одну модель карточек с несколькими шаблонами для Anki"""
    loader = TemplateLoader()

    # Загружаем общие ресурсы
    css = loader.load_css()
    js_code = loader.load_js()

    # Загружаем шаблоны карточек
    en_to_rus = loader.load_card_template(
        "card_en_to_rus_front.html", "card_en_to_rus_back.html"
    )
    rus_to_en = loader.load_card_template(
        "card_rus_to_en_front.html", "card_rus_to_en_back.html"
    )
    example = loader.load_card_template(
        "card_example_front.html", "card_example_back.html"
    )

    # Одна модель с несколькими шаблонами
    # Каждый шаблон создает свой тип карточки из одних и тех же полей
    model = genanki.Model(
        1707392319,  # Один ID для всей модели
        "English Words",  # Одно название модели
        fields=[
            {"name": "Word"},
            {"name": "Transcription"},
            {"name": "Translation"},
            {"name": "ExampleEn"},
            {"name": "ExampleRu"},
            {"name": "AudioUrl"},
        ],
        templates=[
            # Шаблон 1: EN → RUS (English word to Russian translation)
            {
                "name": "EN to RUS",
                "qfmt": inject_js_to_html(en_to_rus["front"], js_code),
                "afmt": inject_js_to_html(en_to_rus["back"], js_code),
            },
            # Шаблон 2: RUS → EN (Russian translation to English word)
            {
                "name": "RUS to EN",
                "qfmt": inject_js_to_html(rus_to_en["front"], js_code),
                "afmt": inject_js_to_html(rus_to_en["back"], js_code),
            },
        ],
        css=css,
    )

    return model


def load_words_from_csv(csv_file):
    """Загружает слова из CSV файла"""
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
                        "example_ru": (
                            row["example_ru"].strip() if "example_ru" in row else ""
                        ),
                        "audio_url": (
                            row["audio_url"].strip() if "audio_url" in row else ""
                        ),
                    }
                )
    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file} не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        sys.exit(1)

    return words


def create_deck(words, deck_name="English Words", shuffle=False):
    """Создает колоду Anki с карточками слов

    Args:
        words: Список слов для создания карточек
        deck_name: Название колоды
        shuffle: Если True, карточки будут перемешаны случайным образом
    """
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, deck_name)

    # Используем одну модель с несколькими шаблонами
    model = create_card_model()

    # Создаем все Note сначала
    notes = []
    for word in words:
        # Одна Note автоматически создаст карточки для всех шаблонов модели
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
        # Для каждого слова будет создано 2 карточки (по одной на каждый шаблон)

    # Перемешиваем карточки, если нужно
    if shuffle:
        random.shuffle(notes)
        print("Карточки перемешаны случайным образом.")

    # Добавляем карточки в колоду
    for note in notes:
        deck.add_note(note)

    return deck


def main():
    parser = argparse.ArgumentParser(
        description="Генератор Anki колоды для изучения английских слов"
    )
    parser.add_argument("csv_file", help="Путь к CSV файлу со словами")
    parser.add_argument(
        "-o", "--output", default="english_words.apkg", help="Имя выходного файла"
    )
    parser.add_argument("-n", "--name", default="English Words", help="Название колоды")
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

    # Подсчитываем количество карточек: каждая Note создает карточки для всех шаблонов
    num_templates = 2  # EN to RUS, RUS to EN
    total_cards = len(words) * num_templates

    print(
        f"Успешно создана колода {args.output} с {total_cards} карточками "
        f"({len(words)} слов x {num_templates} шаблонов в одной модели)"
    )


if __name__ == "__main__":
    main()
