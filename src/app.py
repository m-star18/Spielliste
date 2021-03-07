from saves import Saves

from game import GameData
from menu import MainMenu
from const import (
    GENRE_NAME_DATA_NUMBER,
    DATE_BIRTH_DATA_NUMBER,
    COMPANY_NAME_DATA_NUMBER,
    NUMBER_DATA_PER,
)


class App:

    def __init__(self, number=0, keys=None, word=''):
        if keys is None:
            keys = ['全て'] * 3

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
                               ).show('', '')

    def get_load_data(self):
        for key in sorted(self.save_data.keys()):
            # Refine search
            for k, v in zip(self.keys, self.save_data.load(key)):
                if k != '全て' and k != v:
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

    def change_key_check(self, event, values):
        if event == GENRE_NAME_DATA_NUMBER:
            self.keys[0] = values[GENRE_NAME_DATA_NUMBER]

        elif event == DATE_BIRTH_DATA_NUMBER:
            self.keys[1] = values[DATE_BIRTH_DATA_NUMBER]

        elif event == COMPANY_NAME_DATA_NUMBER:
            self.keys[2] = values[COMPANY_NAME_DATA_NUMBER]

        elif event == 'search':
            self.search_word = values[0]
            self.reload_game_data()

    def get_event_check(self, event, values):
        edit_data = [''] * NUMBER_DATA_PER

        self.change_key_check(event, values)

        if event == 'next' or event == 'previous':
            self.change_page_number(event)

        elif event == '再読込':
            self.reload_game_data()

        for i in range(self.sum_number):
            if event == self.game_list[i].name:
                self.flag = event
                self.window['INPUT'].update(f'{event}を選択中')

            elif self.flag == self.game_list[i].name:
                if event == '詳細':
                    window = self.game_list[i].details_menu()
                    self.game_list[i].update_details(window)

                elif event == '削除':
                    self.delete_game_data(self.game_list[i].name)

                elif event == '編集':
                    window = self.game_list[i].add_menu()
                    key = self.game_list[i].update_data(window)

                    if key:
                        self.add_game_data(key)

        if event == '追加':
            new_game_data = GameData(edit_data[0], edit_data[1:])
            window = new_game_data.add_menu()
            key = new_game_data.update_data(window)

            if key:
                self.add_game_data(key)

        elif event == '詳細' or event == '追加' or event == '編集' or event == '削除':
            self.window['INPUT'].update('ゲームを選択してください')
