import wx


class MainScreen(wx.Frame):
    def __init__(self, parrent: wx.Window | None = None):
        super().__init__(parrent, title="TTS Free app")
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
        buttons_sizer.Add(self.play_button, wx.RIGHT)
        self.stop_button = wx.Button(panel, label="S&top")
        self.stop_button.Hide()
        buttons_sizer.Add(self.stop_button)
        self.export_button = wx.Button(panel, label="&Export")
        buttons_sizer.Add(self.export_button, wx.RIGHT)
        main_sizer.Add(buttons_sizer)
        self.voice_label = wx.StaticText(panel, label="Voice")
        main_sizer.Add(self.voice_label)
        self.voice_ctrl = wx.Choice(panel)
        main_sizer.Add(self.voice_ctrl)
        self.speech_rate_label = wx.StaticText(
            panel, label="Speech rate (words per minute)"
        )
        main_sizer.Add(self.speech_rate_label)
        self.speech_rate_ctrl = wx.SpinCtrl(panel, max=1000, value="200")
        main_sizer.Add(self.speech_rate_ctrl)
        self.volume_label = wx.StaticText(panel, label="Volume")
        main_sizer.Add(self.volume_label)
        self.volume_ctrl = wx.Slider(panel, value=100)
        main_sizer.Add(self.volume_ctrl)
        panel.SetSizerAndFit(main_sizer)
        self.CenterOnScreen()
