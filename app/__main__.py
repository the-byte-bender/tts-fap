import wx
from app.providers import providers
from app.main_screen import MainScreen

if __name__ == "__main__":
    app = wx.App()
    main_screen = MainScreen(tts_providers=providers)
    main_screen.Show()
    app.MainLoop()
