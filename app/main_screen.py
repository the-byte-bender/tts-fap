import wx
from .providers.provider import TTSProvider
from .speech_state import SpeechState


class MainScreen(wx.Frame):
    def __init__(
        self, parrent: wx.Window | None = None, tts_providers: list[TTSProvider] = None
    ):
        super().__init__(parrent, title="TTS Free app")
        tts_providers = tts_providers or []
        self.tts_providers = tts_providers
        self.current_provider: TTSProvider | None = None
        self.voices = []
        self.speech_state: SpeechState = SpeechState.STOPPED
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_input_label = wx.StaticText(panel, label="Your text")
        main_sizer.Add(self.text_input_label)
        self.text_input_ctrl = wx.TextCtrl(
            panel, style=wx.TE_MULTILINE | wx.TE_DONTWRAP
        )
        main_sizer.Add(self.text_input_ctrl, wx.EXPAND | wx.ALL)
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.play_button = wx.Button(panel, label="&Speak")
        self.play_button.Bind(wx.EVT_BUTTON, self.on_speak)
        buttons_sizer.Add(self.play_button, wx.RIGHT)
        self.stop_button = wx.Button(panel, label="S&top")
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop)
        self.stop_button.Hide()
        buttons_sizer.Add(self.stop_button)
        self.export_button = wx.Button(panel, label="&Export")
        buttons_sizer.Add(self.export_button, wx.RIGHT)
        main_sizer.Add(buttons_sizer)
        self.engine_label = wx.StaticText(panel, label="Engine")
        main_sizer.Add(self.engine_label)
        self.engine_ctrl = wx.Choice(
            panel, choices=[i.human_readable_name for i in self.tts_providers]
        )
        #self.engine_ctrl.Bind(wx.EVT_CHOICE, self.on_engine_change)
        if self.tts_providers:
            self.engine_ctrl.SetSelection(0)
            self.current_provider = self.tts_providers[0]
        main_sizer.Add(self.engine_ctrl)
        self.voice_label = wx.StaticText(panel, label="Voice")
        main_sizer.Add(self.voice_label)
        self.voice_ctrl = wx.Choice(panel)
        #self.voice_ctrl.Bind(wx.EVT_CHOICE, self.on_voice_changed)
        main_sizer.Add(self.voice_ctrl)
        self.speech_rate_label = wx.StaticText(
            panel, label="Speech rate (words per minute)"
        )
        main_sizer.Add(self.speech_rate_label)
        self.speech_rate_ctrl = wx.SpinCtrl(panel, max=1000, value="200")
        #self.speech_rate_ctrl.Bind(wx.EVT_SPINCTRL, self.on_speech_rate_changed)
        main_sizer.Add(self.speech_rate_ctrl)
        self.volume_label = wx.StaticText(panel, label="Volume")
        main_sizer.Add(self.volume_label)
        self.volume_ctrl = wx.Slider(panel, value=100)
        #self.volume_ctrl.Bind(wx.EVT_SLIDER, self.on_volume_changed)
        main_sizer.Add(self.volume_ctrl)
        self.update_config_from_engine()
        panel.SetSizerAndFit(main_sizer)
        self.CenterOnScreen()

    def update_config_from_engine(self):
        if self.current_provider is None:
            return
        self.voices = []
        self.voices = list(self.current_provider.get_voices())
        self.volume_ctrl.SetValue(int(self.current_provider.get_volume() * 100))
        self.speech_rate_ctrl.SetValue(str(self.current_provider.get_rate()))
        self.voice_ctrl.Clear()
        for voice_name, voice_id in self.voices:
            self.voice_ctrl.Append(voice_name, voice_id)
        if self.voices:
            selected_voice = self.current_provider.get_voice()
            for index, voice in enumerate(self.voices):
                voice_name, voice_id = voice
                if voice_id == selected_voice:
                    self.voice_ctrl.SetSelection(index)
                    break

    def speak_done_callback(self, success):
        self.speech_state = SpeechState.STOPPED
        self.update_speak_state()

    def on_speak(self, event):
        if self.current_provider is None:
            return
        if self.speech_state== SpeechState.SPEAKING:
            self.current_provider.pause()
            self.speech_state = SpeechState.PAUSED
        elif self.speech_state == SpeechState.PAUSED:
            self.current_provider.resume()
            self.speech_state = SpeechState.SPEAKING
        elif text := self.text_input_ctrl.GetValue():
            self.current_provider.speak(text, self.speak_done_callback)
            self.speech_state = SpeechState.SPEAKING
        self.update_speak_state()

    def update_speak_state(self):
        states = {
            SpeechState.SPEAKING: ("Pau&se", True),
            SpeechState.PAUSED: ("Re&sume", True),
            SpeechState.STOPPED: ("&Speak", False),
        }
        play_button_label, show_stopped_button = states[self.speech_state]
        self.play_button.SetLabel(play_button_label)
        self.stop_button.Show(show_stopped_button)
    def on_stop(self, event):
        if self.current_provider is not None:
            self.current_provider.stop()
    