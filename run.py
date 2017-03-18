from sys import argv

from server import create_app
from smartmirror import Bot

from _thread import start_new_thread

from PyQt5.QtWidgets import QApplication
try:
    from PyQt5.QtWebKitWidgets import QWebView
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView

def start_server(a=None, b=None):
    create_app().run(debug=True, use_reloader=False, host="0.0.0.0", port=80)

if __name__ == "__main__":

    server_thread = start_new_thread(start_server, (None,None))
    if(len(argv) > 1):
        if(argv[1] == 'write'):
            from speech import write
            speech = write

    app = QApplication([])
    win = QWebView()
    win.show()
    win.loadFinished.connect(lambda ok: print("finish", ok))
    win.loadProgress.connect(lambda p: print("progress", p))
    win.loadStarted.connect(lambda: print("started"))
    bot = Bot(speech)
    bot.page_changed.connect(lambda url: print("Url changed", url))
    bot.page_changed.connect(win.load)
    bot.start()
    app.exec_()
