import PySimpleGUI as sg
import operator

from saves import Saves

from game import GameData
from menu import MainMenu
from const.app import (
    GAME_DATA_NUMBER,
    GENRE_NAME_DATA_NUMBER,
    DATE_BIRTH_DATA_NUMBER,
    COMPANY_NAME_DATA_NUMBER,
    HARD_DATA_NUMBER,
    NUMBER_DATA_PER,
    FONT_SIZE,
)


class App:

    def __init__(self, number=0, keys=None, word=''):
        if keys is None:
            keys = ['全て'] * 4

        Saves.current_dbname = 'spielliste'
        self.save_data = Saves()
        self.game_list = []
        self.keys = keys
        self.search_word = word
        self.get_load_data()
        self.sum_number = len(self.game_list)
        self.flag = None

        if self.sum_number >= number * 10:
            self.number = number
        else:
            self.number = 0

        self.window = MainMenu(self.number, self.sum_number, self.game_list, self.get_genre_data(),
                               self.get_date_birth_data(), self.get_company_data(),
                               ).show(self.search_word)

    def get_load_data(self):
        load_data = [[key] + self.save_data.load(key) for key in self.save_data.keys()]
        # sorted by [hard -> name -> genre -> company -> date]
        load_data = sorted(load_data, key=operator.itemgetter(HARD_DATA_NUMBER + 1,
                                                              GAME_DATA_NUMBER + 1,
                                                              GENRE_NAME_DATA_NUMBER + 1,
                                                              COMPANY_NAME_DATA_NUMBER + 1,
                                                              DATE_BIRTH_DATA_NUMBER + 1))
        for data in load_data:
            key = data[0]
            values = data[1:]
            # Refine search
            if self.search_word != values[0][:len(self.search_word)]:
                continue

            for k, v in zip(self.keys, values[1:]):
                # "hard" is the last thing on your mind.
                if k != '全て' and k != v and k != values[-1]:
                    break
            else:
                self.game_list.append(GameData(key, self.save_data.load(key)))

    def get_genre_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(GameData(key, self.save_data.load(key)).genre)

        return res

    def get_date_birth_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(GameData(key, self.save_data.load(key)).date_birth)

        return res

    def get_company_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(GameData(key, self.save_data.load(key)).company)

        return res

    def add_game_data(self, key):
        self.save_data.save(key[0], key[1:])
        self.reload_game_data()

    def delete_game_data(self, key):
        self.save_data.delete(key)
        # To reflect that the data was loss.
        self.reload_game_data()

    def change_page_number(self, event):
        if event == 'next':
            self.number += 1
        else:
            self.number -= 1
        self.reload_game_data()

    def reload_game_data(self):
        self.window.close()
        self.__init__(number=self.number, keys=self.keys, word=self.search_word)

    def run_edit(self, game):
        self.flag = None
        key = game.update_data(self.get_genre_data(), self.get_company_data())

        if key:
            key = [game.id] + key
            self.add_game_data(key)
            # Keep the program closed for a safe screen transition.
            return

    def run_detail(self, game):
        self.flag = None
        window = game.details_menu()
        game.update_details(window)

    def run_delete(self, game):
        del_flag = sg.popup_ok_cancel(f'{game.name}を削除しますか？', font=FONT_SIZE)
        if del_flag == 'OK':
            self.delete_game_data(game.id)
        # Keep the program closed for a safe screen transition.
        return

    def run_add(self):
        edit_data = [''] * NUMBER_DATA_PER
        new_game_data = GameData(edit_data[0], edit_data[1:])
        key = new_game_data.update_data(self.get_genre_data(), self.get_company_data())

        if key:
            key = [new_game_data.id] + key
            self.add_game_data(key)
            return

    def change_key_check(self, event, values):
        check_data_number = [GENRE_NAME_DATA_NUMBER, DATE_BIRTH_DATA_NUMBER, COMPANY_NAME_DATA_NUMBER, HARD_DATA_NUMBER]
        for i, data_number in enumerate(check_data_number):
            if event == data_number:
                self.keys[i] = values[data_number]
                self.reload_game_data()

        if event == 'search':
            self.search_word = values[0]
            self.reload_game_data()

    def get_event_check(self, event, values):
        self.change_key_check(event, values)

        if event == 'next' or event == 'previous':
            self.change_page_number(event)

        elif event == 'オールクリア':
            self.window.close()
            self.__init__()

        # When narrowing down the list, the value becomes an integer.
        if type(event) is int:
            return

        for game in self.game_list:
            if event[:-1] == game.id:
                self.flag = event[:-1]
                self.window['INPUT'].update(f'{game.name}を選択中')

            elif self.flag == game.id:
                if event == '詳細':
                    self.run_detail(game)

                elif event == '削除':
                    self.run_delete(game)

                elif event == '編集':
                    self.run_edit(game)

            # Play game...
            elif 'Play' in event and event[4:] == game.id:
                game.run_data(self.window)

        if event == '新規':
            self.run_add()

        elif event == '詳細' or event == '新規' or event == '編集' or event == '削除':
            self.window['INPUT'].update('ゲームを選択してください')
