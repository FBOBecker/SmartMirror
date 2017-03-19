import os
from sys import argv, executable

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

    euid = os.geteuid()
    if euid != 0:
        print("Script not started as root. Running sudo..")
        args = ['sudo', executable] + argv + [os.environ]
        os.execlpe('sudo', *args)
    print('Running. Your euid is', euid)

    if("--h" in argv):
        help_mode()

    server_thread = start_new_thread(start_server, (None, None))

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
    try:
        bot.run()
    finally:
        bot.close_browser()
