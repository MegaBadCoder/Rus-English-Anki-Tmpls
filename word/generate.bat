@echo off
REM Скрипт для генерации Anki колоды из CSV файла (Windows)

REM Установка зависимостей (если нужно)
REM pip install -r requirements.txt

REM Генерация колоды
python generate_words_deck.py words.csv -o english_words.apkg -n "English Words"

echo Колода создана! Импортируйте файл english_words.apkg в Anki.
pause

