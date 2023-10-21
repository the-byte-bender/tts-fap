import wx
from app.main_screen import MainScreen

if __name__ == "__main__":
    app = wx.App()
    main_screen = MainScreen()
    main_screen.Show()
    app.MainLoop()
