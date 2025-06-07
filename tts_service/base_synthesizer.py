import io
from abc import ABC, abstractmethod
from pydub import AudioSegment, effects

class BaseSynthesizer(ABC):

    def supported_languages(self):
        """Returns supported languages."""
        pass

    @abstractmethod
    def has_lan(self, language: str):
        """Check if the synthesizer supports the given language."""
        pass

    @abstractmethod
    def synthesize(self, language: str, text: str):
        """Synthesize audio from the given text."""
        pass

    @staticmethod
    def _normalize_audio(wav_io: io.BytesIO) -> io.BytesIO:
        segment = AudioSegment.from_file(wav_io, format="wav")
        normalized = effects.normalize(segment)

        output = io.BytesIO()
        normalized.export(output, format="wav")
        output.seek(0)

        return output
