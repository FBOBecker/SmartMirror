import os
from sys import argv, executable, platform

from PyQt5.QtWidgets import QApplication
try:
    from PyQt5.QtWebKitWidgets import QWebView
except ImportError:
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView

from server import create_app
from smartmirror import Bot

from _thread import start_new_thread


def start_server(a=None, b=None):
    create_app().run(debug=True, use_reloader=False, host="0.0.0.0", port=80)


def exit_and_print_help(help_message):
    print(help_message + " For more help use file_name --h")
    exit()


def help_mode():
    with open("help.txt") as f:
        lines = f.readlines()
        for line in lines:
            print(line)
    exit()

if __name__ == "__main__":

    if platform != "win32":
        try:
            euid = os.geteuid()
            if euid != 0:
                print("Script not started as root. Running sudo..")
                args = ['sudo', executable] + argv + [os.environ]
                os.execlpe('sudo', *args)
            print('Running. Your euid is', euid)
        except Exception as e:
            pass

    if("--h" in argv):
        help_mode()

    server_thread = start_new_thread(start_server, (None, None))

    app = QApplication([])
    win = QWebView()
    win.showFullScreen()
    win.loadFinished.connect(lambda ok: print("finish", ok))
    win.loadProgress.connect(lambda p: print("progress", p))
    win.loadStarted.connect(lambda: print("started"))


    if(len(argv) == 1):
        bot = Bot()
    else:
        if(argv[1] == 'write'):
            from speech import write
            speech = write
            bot = Bot(speech)
        elif(argv[1] == 'voice'):
            from speech import speech
            bot = Bot(speech)
        else:
            help = "Unknown argument '" + argv[1] + "'."
            exit_and_print_help(help)
    
    bot.page_changed.connect(lambda url: print("Url changed", url))
    bot.page_changed.connect(win.load)
    
    try:
        bot.start()
        app.exec_()
    finally:
        bot.update_file()
