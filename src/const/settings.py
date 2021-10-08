import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# menu.py
HEAD_HARD_SIZE = eval(os.environ.get("HEAD_HARD_SIZE"))
HEAD_NAME_SIZE = eval(os.environ.get("HEAD_NAME_SIZE"))
NAME_SIZE = eval(os.environ.get("NAME_SIZE"))
SPACE_SIZE = eval(os.environ.get("SPACE_SIZE"))
TITLE_SIZE = eval(os.environ.get("TITLE_SIZE"))
INPUT_SIZE = eval(os.environ.get("INPUT_SIZE"))
PREVIOUS_SIZE = eval(os.environ.get("PREVIOUS_SIZE"))
PREVIOUS_SPACE_SIZE = eval(os.environ.get("PREVIOUS_SPACE_SIZE"))
CONFIG_SIZE = eval(os.environ.get("CONFIG_SIZE"))
DEFAULT_SIZE = eval(os.environ.get("DEFAULT_SIZE"))
INFO_TXT_SIZE = eval(os.environ.get("INFO_TXT_SIZE"))
INFO_INPUT_SIZE = eval(os.environ.get("INFO_INPUT_SIZE"))

# game.py
# detail
DETAIL_GENRE_SIZE = eval(os.environ.get("DETAIL_GENRE_SIZE"))
DETAIL_TEXT_SIZE = eval(os.environ.get("DETAIL_TEXT_SIZE"))
DETAIL_BUTTON_SIZE = eval(os.environ.get("DETAIL_BUTTON_SIZE"))
DETAIL_SITE_SIZE = eval(os.environ.get("DETAIL_SITE_SIZE"))
# add_menu
MENU_GENRE_SIZE = eval(os.environ.get("MENU_GENRE_SIZE"))
MENU_BROWSE_SIZE = eval(os.environ.get("MENU_BROWSE_SIZE"))
MENU_BUTTON_SIZE = eval(os.environ.get("MENU_BUTTON_SIZE"))
MENU_TEXT_GENRE_SIZE = eval(os.environ.get("MENU_TEXT_GENRE_SIZE"))
MENU_TEXT_INPUT_SIZE = eval(os.environ.get("MENU_TEXT_INPUT_SIZE"))
MENU_DATE_INPUT_SIZE = eval(os.environ.get("MENU_DATE_INPUT_SIZE"))
MENU_SITE_SIZE = eval(os.environ.get("MENU_SITE_SIZE"))
