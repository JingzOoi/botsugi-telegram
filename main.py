from utils.construct import construct_path
from utils.dataIO import dataIO
from telegram.ext import CommandHandler, Updater, Filters
import os
import logging
import subprocess
import asyncio
import time

logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.CONFIG = dataIO.load_json(construct_path("resources", "config.json"))
        self.UPDATER = Updater(token=self.CONFIG["telegram"]["token"], use_context=True)

    def is_owner(self, update):
        return update.effective_user.id == self.CONFIG["telegram"]["owner"]

    def add_command(self, func):
        try:
            self.UPDATER.dispatcher.add_handler(CommandHandler(func.__name__, func, filters=Filters.user(user_id=self.CONFIG["telegram"]["owner"])))
        except Exception as e:
            print(f"[ERROR] Failed to add command {func.__name__}: {e}")

    def online(self):
        self.UPDATER.start_polling()
        self.UPDATER.idle()
        print("[ONLINE] Waiting for commands...")


bot = Bot()


@bot.add_command
def start(update, ctx):
    return ctx.bot.send_message(chat_id=update.effective_chat.id, text="Welcome back.")


@bot.add_command
def ready(update, ctx):
    return ctx.bot.send_message(chat_id=update.effective_chat.id, text="Botsugi is my name, and ready is my game.")


def bot_exit():
    os._exit(0)


@bot.add_command
def quit(update, ctx):
    with open('quit.txt', 'w', encoding="utf8") as f:
        f.write('.')
    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Shutting down.")
    print("[SHUTDOWN] Ending processes...")
    return bot_exit()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.online)
    except Exception as e:
        print(f"[ERROR] An exception has occured: {e}")
    finally:
        print("Weiting untill restart...")
        time.sleep(60)
