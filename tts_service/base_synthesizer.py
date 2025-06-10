from abc import ABC, abstractmethod


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
