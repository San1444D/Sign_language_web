from email.mime import audio
import whisper
import base64
import io
from gtts import gTTS
from gtts.lang import tts_langs
import soundfile as sf
from scipy.signal import resample
from deep_translator import GoogleTranslator
from pydub import AudioSegment

from .config import SHARED_MODEL, logger


class SpeechProcessor:
    # Class-level attribute to store the shared Whisper model
    _model = None

    def __init__(self):
        """
        Initialize the SpeechProcessor with a shared Whisper model.

        :param model_name: The name of the Whisper model to load. Default is 'base'.
        """
        self._model = SHARED_MODEL
        self.orginal_text = None
        self.translated_text = None
        self.audio_base64 = None

    def text_to_speech(
        self, text: str, language: str = "en", slow: bool = False
    ) -> str:
        """
        Convert text to speech and return the audio as a Base64 string.

        :param text: The text to convert to speech.
        :param language: The language in which to convert the text. Default is 'en'.
        :param slow: If True, the speech will be slower. Default is False.
        :return: Base64 encoded audio string.
        """
        tts = gTTS(text=text, lang=language, slow=slow)
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)
        audio_b64 = base64.b64encode(audio_stream.read()).decode("utf-8")
        return audio_b64

    def speech_to_text(self, audio_base64: str) -> tuple:
        """
        Transcribe audio from a Base64 string using the Whisper model.

        :param audio_base64: The Base64 encoded audio to transcribe.
        :return: A tuple containing the **transcribed text** and **detected language**.
        :rtype: tuple (str, str)
        """
        try:
            # Decode the Base64 audio
            audio_stream = io.BytesIO(base64.b64decode(audio_base64))

            # Convert audio to WAV format using pydub
            audio = AudioSegment.from_file(audio_stream)
            # logger.info(f"Audio properties - Channels: {audio.channels}, Frame rate: {audio.frame_rate}, Duration: {audio.duration_seconds}s")
            wav_stream = io.BytesIO()
            audio.export(wav_stream, format="wav")
            wav_stream.seek(0)

            # Read the WAV audio using soundfile
            audio_data, sample_rate = sf.read(wav_stream, dtype="float32")
            if sample_rate != 16000:
                audio_data = resample(audio_data, int(len(audio_data) * 16000 / sample_rate)).astype("float32")

            # Transcribe the audio using Whisper
            result = self._model.transcribe(audio_data, fp16=False)
            return result["text"], result["language"]
        except Exception as e:
            logger.error(f"Error in speech_to_text: {e}")
            return None, None

    def translate(self, text: str, target_language: str = "en") -> str:
        """
        Translate the given text to the target language.

        :param text: The text to translate.
        :param target_language: The target language code (default is 'en') (e.g., 'fr' for French).
        :return: Translated text.
        """
        try:
            translator = GoogleTranslator(source="auto", target=target_language)
            return translator.translate(text)
        except Exception as e:
            logger.error(f"Error in translate: {e}")
            return None

    def get_google_supported_languages(self):
        """
        Return a dict of supported languages for translation.

        :return: dict of supported languages {'lang_name': 'lang_id'}.
        """
        return GoogleTranslator().get_supported_languages(as_dict=True)

    def get_gtts_supported_languages(self):
        """
        Return a dict of supported languages for text-to-speech.

        :return: dict of supported languages {'lang_name': 'lang_id'}.
        """
        return tts_langs()

    def get_whisper_supported_languages(self):
        """
        Return a dict of supported languages for speech recognition.

        :return: dict of supported languages {'lang_name': 'lang_id'}.
        """
        return whisper.tokenizer.LANGUAGES

