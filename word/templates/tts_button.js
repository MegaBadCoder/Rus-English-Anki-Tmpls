// Функция для создания кнопки TTS (синтез речи)
function createTTSButton(text) {
    var utterance = new SpeechSynthesisUtterance(text);
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
    if (americanVoices.length === 0) {
        americanVoices = voices.filter(voice => voice.lang === 'en-US');
    }
    if (americanVoices.length > 0) {
        utterance.voice = americanVoices[0];
    }
    speechSynthesis.speak(utterance);
}

