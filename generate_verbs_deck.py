#!/usr/bin/env python3
import argparse
import csv
import genanki
import random
import sys
from pathlib import Path


def create_tts_button(text):
    js_code = f"""
    var utterance = new SpeechSynthesisUtterance('{text}');
    utterance.lang = 'en-US';
    utterance.rate = 0.8;
    utterance.pitch = 1.0;
    var voices = speechSynthesis.getVoices();
    var americanVoices = voices.filter(voice =>
        voice.lang === 'en-US' && (
            voice.name.includes('Google US English') ||
            voice.name.includes('Microsoft David') ||
            voice.name.includes('Microsoft Mark') ||
            voice.name.includes('Microsoft Zira') ||
            voice.name.includes('Alex') ||
            voice.name.includes('Samantha') ||
            voice.name.includes('American') ||
            (voice.name.includes('English') && voice.name.includes('United States'))
        )
    );
    if (americanVoices.length === 0) {{
        americanVoices = voices.filter(voice => voice.lang === 'en-US');
    }}
    if (americanVoices.length > 0) {{
        utterance.voice = americanVoices[0];
    }}
    speechSynthesis.speak(utterance);
    """
    return f'<button onclick="{js_code}" style="background: #4CAF50; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">🔊</button>'


def create_check_function(correct_answer, input_id):
    return f"""
    function checkAnswer_{input_id}() {{
        var input = document.getElementById('{input_id}');
        var feedback = document.getElementById('feedback_{input_id}');
        var userAnswer = input.value.trim().toLowerCase();
        var correctAnswer = '{correct_answer}'.toLowerCase();

        if (userAnswer === correctAnswer) {{
            input.className = 'input-correct';
            feedback.className = 'feedback correct';
            feedback.innerHTML = '✓ Правильно!';
            feedback.style.display = 'block';
        }} else {{
            input.className = 'input-incorrect';
            feedback.className = 'feedback incorrect';
            feedback.innerHTML = '✗ Неправильно. Правильный ответ: {correct_answer}';
            feedback.style.display = 'block';
        }}
    }}
    """


def create_back_check_function(correct_answer, input_id):
    return f"""
    function checkAnswerBack_{input_id}() {{
        var input = document.getElementById('{input_id}');
        var feedback = document.getElementById('back_feedback_{input_id}');
        var userAnswer = input.value.trim().toLowerCase();
        var correctAnswer = '{correct_answer}'.toLowerCase();

        if (userAnswer === correctAnswer) {{
            input.className = 'input-correct';
            feedback.className = 'feedback correct';
            feedback.innerHTML = '✓ Правильно!';
            feedback.style.display = 'block';
        }} else {{
            input.className = 'input-incorrect';
            feedback.className = 'feedback incorrect';
            feedback.innerHTML = '✗ Неправильно. Правильный ответ: {correct_answer}';
            feedback.style.display = 'block';
        }}
    }}
    """


def create_card_models():
    css = """
    .card {
        font-family: Arial, sans-serif;
        font-size: 20px;
        text-align: center;
        color: black;
        background-color: white;
        padding: 20px;
    }
    .front {
        font-size: 24px;
        margin-bottom: 20px;
    }
    .transcription {
        color: #666;
        font-style: italic;
        font-size: 16px;
    }
    .translation {
        color: #333;
        font-size: 18px;
        margin-top: 15px;
    }
    .example {
        color: #555;
        font-size: 16px;
        font-style: italic;
        margin-top: 10px;
    }
    input[type="text"] {
        font-size: 20px;
        padding: 10px;
        border: 2px solid #ddd;
        border-radius: 5px;
        width: 200px;
        text-align: center;
    }
    .verb-form {
        display: inline-block;
        margin: 0 10px;
    }
    .check-btn {
        background: #2196F3;
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 5px;
        cursor: pointer;
        margin-left: 10px;
        font-size: 16px;
    }
    .check-btn:hover {
        background: #1976D2;
    }
    .feedback {
        margin-top: 15px;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        display: none;
    }
    .correct {
        background: #4CAF50;
        color: white;
    }
    .incorrect {
        background: #f44336;
        color: white;
    }
    .input-correct {
        border-color: #4CAF50 !important;
        background-color: #e8f5e8;
    }
    .input-incorrect {
        border-color: #f44336 !important;
        background-color: #ffeaea;
    }
    """

    # Model 1: Infinitive → Past Participle (need Past Simple)
    model1 = genanki.Model(
        1607392319,
        "Irregular Verbs - Inf to PP",
        fields=[
            {"name": "Infinitive"},
            {"name": "PastSimple"},
            {"name": "PastParticiple"},
            {"name": "TransInf"},
            {"name": "TransPS"},
            {"name": "TransPP"},
            {"name": "Translation"},
            {"name": "ExampleEn"},
            {"name": "ExampleRu"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": """
                <div class="front">
                    <div class="verb-form">{{Infinitive}} <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                    <span> - </span>
                    <input type="text" id="input1" placeholder="?" oninput="localStorage.setItem('userAnswer1_{{Infinitive}}_{{PastSimple}}', this.value)" onblur="localStorage.setItem('userAnswer1_{{Infinitive}}_{{PastSimple}}', this.value)">
                    <span> - </span>
                    <div class="verb-form">{{PastParticiple}} <span class="transcription">{{TransPP}}</span> """
                + create_tts_button("{{PastParticiple}}")
                + """</div>
                </div>
                <script>
                window.addEventListener('beforeunload', function() {
                    var input = document.getElementById('input1');
                    if (input) localStorage.setItem('userAnswer1', input.value);
                });
                </script>
                """,
                "afmt": """
                <div class="front">
                    <div class="verb-form">{{Infinitive}} <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form"><strong>{{PastSimple}}</strong> <span class="transcription">{{TransPS}}</span> """
                + create_tts_button("{{PastSimple}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form">{{PastParticiple}} <span class="transcription">{{TransPP}}</span> """
                + create_tts_button("{{PastParticiple}}")
                + """</div>
                </div>
                <div class="translation">{{Translation}}</div>
                <div class="example">{{ExampleEn}}<br>{{ExampleRu}}</div>
                <hr>
                <div style="margin-top: 15px;">
                    <div id="check_feedback1" class="feedback"></div>
                </div>
                <script>
                (function() {
                    var feedback = document.getElementById('check_feedback1');
                    var userAnswer = localStorage.getItem('userAnswer1_{{Infinitive}}_{{PastSimple}}') || '';
                    userAnswer = userAnswer.trim().toLowerCase();
                    var correctAnswer = '{{PastSimple}}'.toLowerCase();

                    if (userAnswer === correctAnswer) {
                        feedback.className = 'feedback correct';
                        feedback.innerHTML = '✓ Правильно! Ваш ответ: ' + userAnswer;
                        feedback.style.display = 'block';
                    } else {
                        feedback.className = 'feedback incorrect';
                        feedback.innerHTML = '✗ Неправильно.<br>Ваш ответ: ' + (userAnswer || '(пусто)') + '<br>Правильный ответ: {{PastSimple}}';
                        feedback.style.display = 'block';
                    }
                    localStorage.removeItem('userAnswer1_{{Infinitive}}_{{PastSimple}}');
                })();
                </script>
                """,
            },
        ],
        css=css,
    )

    # Model 2: Past Simple + Past Participle → Infinitive
    model2 = genanki.Model(
        1607392320,
        "Irregular Verbs - PS+PP to Inf",
        fields=[
            {"name": "Infinitive"},
            {"name": "PastSimple"},
            {"name": "PastParticiple"},
            {"name": "TransInf"},
            {"name": "TransPS"},
            {"name": "TransPP"},
            {"name": "Translation"},
            {"name": "ExampleEn"},
            {"name": "ExampleRu"},
        ],
        templates=[
            {
                "name": "Card 2",
                "qfmt": """
                <div class="front">
                    <input type="text" id="input2" placeholder="?" oninput="localStorage.setItem('userAnswer2_{{Infinitive}}_{{PastSimple}}', this.value)" onblur="localStorage.setItem('userAnswer2_{{Infinitive}}_{{PastSimple}}', this.value)">
                    <span> - </span>
                    <div class="verb-form">{{PastSimple}} <span class="transcription">{{TransPS}}</span> """
                + create_tts_button("{{PastSimple}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form">{{PastParticiple}} <span class="transcription">{{TransPP}}</span> """
                + create_tts_button("{{PastParticiple}}")
                + """</div>
                </div>
                <script>
                window.addEventListener('beforeunload', function() {
                    var input = document.getElementById('input2');
                    if (input) localStorage.setItem('userAnswer2', input.value);
                });
                </script>
                """,
                "afmt": """
                <div class="front">
                    <div class="verb-form"><strong>{{Infinitive}}</strong> <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form">{{PastSimple}} <span class="transcription">{{TransPS}}</span> """
                + create_tts_button("{{PastSimple}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form">{{PastParticiple}} <span class="transcription">{{TransPP}}</span> """
                + create_tts_button("{{PastParticiple}}")
                + """</div>
                </div>
                <div class="translation">{{Translation}}</div>
                <div class="example">{{ExampleEn}}<br>{{ExampleRu}}</div>
                <hr>
                <div style="margin-top: 15px;">
                    <div id="check_feedback2" class="feedback"></div>
                </div>
                <script>
                (function() {
                    var feedback = document.getElementById('check_feedback2');
                    var userAnswer = localStorage.getItem('userAnswer2_{{Infinitive}}_{{PastSimple}}') || '';
                    userAnswer = userAnswer.trim().toLowerCase();
                    var correctAnswer = '{{Infinitive}}'.toLowerCase();

                    if (userAnswer === correctAnswer) {
                        feedback.className = 'feedback correct';
                        feedback.innerHTML = '✓ Правильно! Ваш ответ: ' + userAnswer;
                        feedback.style.display = 'block';
                    } else {
                        feedback.className = 'feedback incorrect';
                        feedback.innerHTML = '✗ Неправильно.<br>Ваш ответ: ' + (userAnswer || '(пусто)') + '<br>Правильный ответ: {{Infinitive}}';
                        feedback.style.display = 'block';
                    }
                    localStorage.removeItem('userAnswer2_{{Infinitive}}_{{PastSimple}}');
                })();
                </script>
                """,
            },
        ],
        css=css,
    )

    # Model 3: Infinitive + Past Simple → Past Participle
    model3 = genanki.Model(
        1607392321,
        "Irregular Verbs - Inf+PS to PP",
        fields=[
            {"name": "Infinitive"},
            {"name": "PastSimple"},
            {"name": "PastParticiple"},
            {"name": "TransInf"},
            {"name": "TransPS"},
            {"name": "TransPP"},
            {"name": "Translation"},
            {"name": "ExampleEn"},
            {"name": "ExampleRu"},
        ],
        templates=[
            {
                "name": "Card 3",
                "qfmt": """
                <div class="front">
                    <div class="verb-form">{{Infinitive}} <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form">{{PastSimple}} <span class="transcription">{{TransPS}}</span> """
                + create_tts_button("{{PastSimple}}")
                + """</div>
                    <span> - </span>
                    <input type="text" id="input3" placeholder="?" oninput="localStorage.setItem('userAnswer3_{{Infinitive}}_{{PastSimple}}', this.value)" onblur="localStorage.setItem('userAnswer3_{{Infinitive}}_{{PastSimple}}', this.value)">
                </div>
                <script>
                window.addEventListener('beforeunload', function() {
                    var input = document.getElementById('input3');
                    if (input) localStorage.setItem('userAnswer3', input.value);
                });
                </script>
                """,
                "afmt": """
                <div class="front">
                    <div class="verb-form">{{Infinitive}} <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form">{{PastSimple}} <span class="transcription">{{TransPS}}</span> """
                + create_tts_button("{{PastSimple}}")
                + """</div>
                    <span> - </span>
                    <div class="verb-form"><strong>{{PastParticiple}}</strong> <span class="transcription">{{TransPP}}</span> """
                + create_tts_button("{{PastParticiple}}")
                + """</div>
                </div>
                <div class="translation">{{Translation}}</div>
                <div class="example">{{ExampleEn}}<br>{{ExampleRu}}</div>
                <hr>
                <div style="margin-top: 15px;">
                    <div id="check_feedback3" class="feedback"></div>
                </div>
                <script>
                (function() {
                    var feedback = document.getElementById('check_feedback3');
                    var userAnswer = localStorage.getItem('userAnswer3_{{Infinitive}}_{{PastSimple}}') || '';
                    userAnswer = userAnswer.trim().toLowerCase();
                    var correctAnswer = '{{PastParticiple}}'.toLowerCase();

                    if (userAnswer === correctAnswer) {
                        feedback.className = 'feedback correct';
                        feedback.innerHTML = '✓ Правильно! Ваш ответ: ' + userAnswer;
                        feedback.style.display = 'block';
                    } else {
                        feedback.className = 'feedback incorrect';
                        feedback.innerHTML = '✗ Неправильно.<br>Ваш ответ: ' + (userAnswer || '(пусто)') + '<br>Правильный ответ: {{PastParticiple}}';
                        feedback.style.display = 'block';
                    }
                    localStorage.removeItem('userAnswer3_{{Infinitive}}_{{PastSimple}}');
                })();
                </script>
                """,
            },
        ],
        css=css,
    )

    # Model 4: EN → RUS
    model4 = genanki.Model(
        1607392322,
        "Irregular Verbs - EN to RUS",
        fields=[
            {"name": "Infinitive"},
            {"name": "PastSimple"},
            {"name": "PastParticiple"},
            {"name": "TransInf"},
            {"name": "TransPS"},
            {"name": "TransPP"},
            {"name": "Translation"},
            {"name": "ExampleEn"},
            {"name": "ExampleRu"},
        ],
        templates=[
            {
                "name": "Card 4",
                "qfmt": """
                <div class="front">
                    <div class="verb-form">{{Infinitive}} <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                    <br><br>
                    <input type="text" id="input4" placeholder="Перевод на русский" oninput="localStorage.setItem('userAnswer4_{{Infinitive}}_{{Translation}}', this.value)" onblur="localStorage.setItem('userAnswer4_{{Infinitive}}_{{Translation}}', this.value)">
                </div>
                <script>
                window.addEventListener('beforeunload', function() {
                    var input = document.getElementById('input4');
                    if (input) localStorage.setItem('userAnswer4', input.value);
                });
                </script>
                """,
                "afmt": """
                <div class="front">
                    <div class="verb-form">{{Infinitive}} <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                </div>
                <div class="translation"><strong>{{Translation}}</strong></div>
                <div class="example">{{ExampleEn}}<br>{{ExampleRu}}</div>
                <hr>
                <div>{{PastSimple}} <span class="transcription">{{TransPS}}</span> """
                + create_tts_button("{{PastSimple}}")
                + """ | {{PastParticiple}} <span class="transcription">{{TransPP}}</span> """
                + create_tts_button("{{PastParticiple}}")
                + """</div>
                <hr>
                <div style="margin-top: 15px;">
                    <div id="check_feedback4" class="feedback"></div>
                </div>
                <script>
                (function() {
                    var feedback = document.getElementById('check_feedback4');
                    var userAnswer = localStorage.getItem('userAnswer4_{{Infinitive}}_{{Translation}}') || '';
                    userAnswer = userAnswer.trim().toLowerCase();
                    var correctAnswer = '{{Translation}}'.toLowerCase();

                    if (userAnswer === correctAnswer) {
                        feedback.className = 'feedback correct';
                        feedback.innerHTML = '✓ Правильно! Ваш ответ: ' + userAnswer;
                        feedback.style.display = 'block';
                    } else {
                        feedback.className = 'feedback incorrect';
                        feedback.innerHTML = '✗ Неправильно.<br>Ваш ответ: ' + (userAnswer || '(пусто)') + '<br>Правильный ответ: {{Translation}}';
                        feedback.style.display = 'block';
                    }
                    localStorage.removeItem('userAnswer4_{{Infinitive}}_{{Translation}}');
                })();
                </script>
                """,
            },
        ],
        css=css,
    )

    # Model 5: RUS → EN
    model5 = genanki.Model(
        1607392323,
        "Irregular Verbs - RUS to EN",
        fields=[
            {"name": "Infinitive"},
            {"name": "PastSimple"},
            {"name": "PastParticiple"},
            {"name": "TransInf"},
            {"name": "TransPS"},
            {"name": "TransPP"},
            {"name": "Translation"},
            {"name": "ExampleEn"},
            {"name": "ExampleRu"},
        ],
        templates=[
            {
                "name": "Card 5",
                "qfmt": """
                <div class="front">
                    <div class="translation">{{Translation}}</div>
                    <br><br>
                    <input type="text" id="input5" placeholder="English translation" oninput="localStorage.setItem('userAnswer5_{{Infinitive}}_{{Translation}}', this.value)" onblur="localStorage.setItem('userAnswer5_{{Infinitive}}_{{Translation}}', this.value)">
                </div>
                <script>
                window.addEventListener('beforeunload', function() {
                    var input = document.getElementById('input5');
                    if (input) localStorage.setItem('userAnswer5', input.value);
                });
                </script>
                """,
                "afmt": """
                <div class="front">
                    <div class="translation">{{Translation}}</div>
                </div>
                <div class="verb-form"><strong>{{Infinitive}}</strong> <span class="transcription">{{TransInf}}</span> """
                + create_tts_button("{{Infinitive}}")
                + """</div>
                <div class="example">{{ExampleEn}}<br>{{ExampleRu}}</div>
                <hr>
                <div>{{PastSimple}} <span class="transcription">{{TransPS}}</span> """
                + create_tts_button("{{PastSimple}}")
                + """ | {{PastParticiple}} <span class="transcription">{{TransPP}}</span> """
                + create_tts_button("{{PastParticiple}}")
                + """</div>
                <hr>
                <div style="margin-top: 15px;">
                    <div id="check_feedback5" class="feedback"></div>
                </div>
                <script>
                (function() {
                    var feedback = document.getElementById('check_feedback5');
                    var userAnswer = localStorage.getItem('userAnswer5_{{Infinitive}}_{{Translation}}') || '';
                    userAnswer = userAnswer.trim().toLowerCase();
                    var correctAnswer = '{{Infinitive}}'.toLowerCase();

                    if (userAnswer === correctAnswer) {
                        feedback.className = 'feedback correct';
                        feedback.innerHTML = '✓ Правильно! Ваш ответ: ' + userAnswer;
                        feedback.style.display = 'block';
                    } else {
                        feedback.className = 'feedback incorrect';
                        feedback.innerHTML = '✗ Неправильно.<br>Ваш ответ: ' + (userAnswer || '(пусто)') + '<br>Правильный ответ: {{Infinitive}}';
                        feedback.style.display = 'block';
                    }
                    localStorage.removeItem('userAnswer5_{{Infinitive}}_{{Translation}}');
                })();
                </script>
                """,
            },
        ],
        css=css,
    )

    return [model1, model2, model3, model4, model5]


def load_verbs_from_csv(csv_file):
    verbs = []
    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                verbs.append(
                    {
                        "infinitive": row["infinitive"].strip(),
                        "past_simple": row["past_simple"].strip(),
                        "past_participle": row["past_participle"].strip(),
                        "transcription_inf": row["transcription_inf"].strip(),
                        "transcription_ps": row["transcription_ps"].strip(),
                        "transcription_pp": row["transcription_pp"].strip(),
                        "translation": row["translation"].strip(),
                        "example_en": row["example_en"].strip(),
                        "example_ru": (
                            row["example_ru"].strip() if "example_ru" in row else ""
                        ),
                    }
                )
    except FileNotFoundError:
        print(f"Error: File {csv_file} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    return verbs


def create_deck(verbs, deck_name="Irregular English Verbs"):
    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, deck_name)

    models = create_card_models()

    for verb in verbs:
        for i, model in enumerate(models):
            note = genanki.Note(
                model=model,
                fields=[
                    verb["infinitive"],
                    verb["past_simple"],
                    verb["past_participle"],
                    verb["transcription_inf"],
                    verb["transcription_ps"],
                    verb["transcription_pp"],
                    verb["translation"],
                    verb["example_en"],
                    verb["example_ru"],
                ],
            )
            deck.add_note(note)

    return deck


def main():
    parser = argparse.ArgumentParser(
        description="Generate Anki deck for irregular English verbs"
    )
    parser.add_argument("csv_file", help="Path to CSV file with verb data")
    parser.add_argument(
        "-o", "--output", default="irregular_verbs.apkg", help="Output deck file name"
    )
    parser.add_argument(
        "-n", "--name", default="Irregular English Verbs", help="Deck name"
    )

    args = parser.parse_args()

    if not Path(args.csv_file).exists():
        print(f"Error: CSV file '{args.csv_file}' does not exist.")
        sys.exit(1)

    print(f"Loading verbs from {args.csv_file}...")
    verbs = load_verbs_from_csv(args.csv_file)
    print(f"Loaded {len(verbs)} verbs.")

    print("Creating Anki deck...")
    deck = create_deck(verbs, args.name)

    print(f"Generating {args.output}...")
    genanki.Package(deck).write_to_file(args.output)

    print(
        f"Successfully created {args.output} with {len(verbs) * 5} cards ({len(verbs)} verbs x 5 card types)"
    )


if __name__ == "__main__":
    main()
