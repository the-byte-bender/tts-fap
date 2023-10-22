from typing import Callable, Any, Iterable

on_done_callback_type = Callable[[bool], None]


class TTSProvider:
    human_readable_name: str = "Dummy TTS provider"

    def speak(self, text: str, on_done_callback: on_done_callback_type):
        """Will be called when requesting to speak new text. This function should handle speaking the text and it should call the callback given to it when the utterance is complete, passing it True if the text has finished speaking successfully, False if an error prevented it from speaking to completion."""
        raise NotImplementedError()

    def stop(self):
        """Called when requesting to stop the current speech. The callback given when the speak function is called must be called when the speech is stopped."""
        raise NotImplementedError()

    def save_to_file(
        self, text: str, filepath: str, on_done_callback: on_done_callback_type
    ):
        """Will be called when requesting to save the text to a file. This function should handle saving the text given to the file path, and it should call the callback given to it when the operation is complete, passing it True if the text has saved successfully, False if an error prevented it from saving to completion."""
        raise NotImplementedError()

    def get_rate(self) -> int:
        """Returns the current speech rate in words per minute"""
        raise NotImplementedError()

    def set_rate(self, rate: int):
        """Set the speech rate (in words per minute) for all next utterances"""
        raise NotImplementedError()

    def get_volume(self) -> float:
        """Returns volume, as a float between 0.0 and 1.0(inclusive)"""
        raise NotImplementedError()

    def set_volume(self, volume: float):
        """Set the volume (as float between 0.0 and 1.0 (inclusive)) for all next utterances"""
        raise NotImplementedError()

    def get_voices(self) -> Iterable[tuple[str, Any]]:
        """Returns a list of supported, usable voices as an iterable of tuples where each tuple contains a human-readable name of the voice and an ID of the voice. The ID will be passed to set_voice() when the user chooses it."""
        raise NotImplementedError()

    def get_voice(self) -> Any:
        """Returns the ID of the currently set voice"""
        raise NotImplementedError()

    def set_voice(self, voice: Any):
        """Sets the current voice. Voice is a valid Voice ID previously returned from get_voices"""
        raise NotImplementedError()

    def pause(self):
        """Called when requesting the current speech to be paused"""
        raise NotImplementedError()

    def resume(self):
        """Called when requesting the currently paused speech to be resumed"""
        raise NotImplementedError()
