#!/bin/bash
# Скрипт для генерации Anki колоды из CSV файла

# Установка зависимостей (если нужно)
# pip install -r requirements.txt

# Генерация колоды
python3 generate_words_deck.py words.csv -o english_words.apkg -n "English Words"

echo "Колода создана! Импортируйте файл english_words.apkg в Anki."

