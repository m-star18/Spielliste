import PySimpleGUI as sg

from file import open_file
from check import event_check
from menu import main_menu, create_summary, Gamedata
from saves import Saves
from const import (
    FONT_SIZE,
    GAME_NAME_DATA_NUMBER,
    GENRE_NAME_DATA_NUMBER,
    DATE_BIRTH_DATA_NUMBER,
    COMPANY_NAME_DATA_NUMBER,
    HIGHEST_SCORE_DATA_NUMBER,
    IMAGE_DATA_NUMBER,
    SITE_DATA_NUMBER,
    NUMBER_DATA_PER,
    ONE_COLUMN_LENGTH,
)


def main(game_list_data=None, sum_number_data=0, event_data='', number_data=0, input_text='', values_data=None,
         genre_data=None, date_birth_data=None, company_data=None):
    if game_list_data is None:
        game_list_data, sum_number_data, event_data = open_file()

    if values_data is None:
        values_data = {}

    if (genre_data or date_birth_data or company_data) is None:
        genre_data, date_birth_data, company_data = create_summary(game_list_data, sum_number_data)

    sg.theme("Topanga")

    window = main_menu(sum_number_data, game_list_data, number_data, input_text, values_data, genre_data,
                       date_birth_data, company_data)

    while True:
        event, values = window.Read()
        window['INPUT'].update('{0}を選択中'.format(event))

        if event is None:
            exit()

        event_data = event_check(event, values, values_data, game_list_data, number_data, event_data, sum_number_data,
                                 window)


class App:

    def __init__(self):
        Saves.current_dbname = 'spielliste'
        self.save_data = Saves()
        self.game_list = []
        self.number = 0
        self.load_data()
        self.sum_number = len(self.game_list)

        self.window = MainMenu(self.number, self.sum_number, self.game_list, self.genre_data(),
                               self.date_birth_data(), self.company_data(),
                               ).show('', '')

    def load_data(self):
        for key in self.save_data.keys():
            self.game_list.append(Gamedata(self.save_data.load(key)))

    def genre_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(Gamedata(self.save_data.load(key)).genre)

        return res

    def date_birth_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(Gamedata(self.save_data.load(key)).date_birth)

        return res

    def company_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(Gamedata(self.save_data.load(key)).company)

        return res


if __name__ == "__main__":
    main()
