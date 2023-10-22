import tempfile
import threading
import time
from typing import Any, Iterable
import wave
import pyaudio
import pyttsx3 as tts
from .provider import TTSProvider, on_done_callback_type


class SAPIProvider(TTSProvider):
    human_readable_name = "Microsoft SAPI"

    def __init__(self):
        self.paused = False
        self.temp = tempfile.mktemp()
        self.engine = tts.Engine()
        self.pyaudio = pyaudio.PyAudio()
        self.on_done_speaking: on_done_callback_type | None = None
        self.stream: pyaudio.Stream | None = None
        self.open_wave: wave.Wave_read | None = None
        self.running = True
        self.thread = None
        self.start_loop()

    def new_stream_from_file(self, filename: str):
        self.close_stream()
        self.open_wave = wave.open(filename)
        self.stream = self.pyaudio.open(
            self.open_wave.getframerate(),
            self.open_wave.getnchannels(),
            pyaudio.get_format_from_width(self.open_wave.getsampwidth()),
            output=True,
        )

    def close_stream(self):
        if self.stream is not None:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.open_wave:
            self.open_wave.close()
            self.open_wave = None

    def loop(self):
        while self.running:
            if (
                self.paused
                or not self.open_wave
                or not self.stream
                or not self.stream.is_active()
            ):
                time.sleep(0.02)
                continue
            frames_to_write = self.stream.get_write_available()
            if frames_to_write > 0:
                frames_will_be_written = self.open_wave.readframes(frames_to_write)
                if not frames_will_be_written:
                    if callable(self.on_done_speaking):
                        self.on_done_speaking(True)
                    self.close_stream()
                    continue
                self.stream.write(frames_will_be_written)

    def start_loop(self):
        self.stop_loop()
        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop_loop(self):
        if self.thread is not None:
            self.running = False
            self.thread.join()
            self.thread = None

    def speak(self, text: str, on_done_callback: on_done_callback_type):
        self.close_stream()
        self.paused = False
        self.engine.save_to_file(text, self.temp)
        self.engine.runAndWait()
        self.on_done_speaking = on_done_callback
        self.new_stream_from_file(self.temp)

    def stop(self):
        if self.open_wave:
            self.open_wave.setpos(self.open_wave.getnframes())

    def save_to_file(
        self, text: str, filepath: str, on_done_callback: on_done_callback_type
    ):
        self.engine.save_to_file(text, filepath)
        self.engine.runAndWait()
        on_done_callback(True)

    def get_rate(self) -> int:
        return self.engine.getProperty("rate")

    def set_rate(self, rate: int):
        self.engine.setProperty("rate", rate)

    def get_volume(self) -> float:
        return self.engine.getProperty("volume")

    def set_volume(self, volume: float):
        self.engine.setProperty("volume", volume)

    def get_voices(self) -> Iterable[tuple[str, Any]]:
        for voice in self.engine.getProperty("voices"):
            yield voice.name, voice.id

    def get_voice(self) -> Any:
        return self.engine.getProperty("voice")

    def set_voice(self, voice: Any):
        self.engine.setProperty("voice", voice)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
