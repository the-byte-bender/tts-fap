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
        panel.SetSizerAndFit(main_sizer)
        self.CenterOnScreen()
