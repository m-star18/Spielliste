import PySimpleGUI as sg

from file import open_file
from check import event_check
from menu import main_menu, create_summary, Gamedata
from saves import Saves


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
        self.get_load_data()
        self.sum_number = len(self.game_list)

        self.window = MainMenu(self.number, self.sum_number, self.game_list, self.get_genre_data(),
                               self.get_date_birth_data(), self.get_company_data(),
                               ).show('', '')

    def get_load_data(self):
        for key in self.save_data.keys():
            self.game_list.append(Gamedata(self.save_data.load(key)))

    def get_genre_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(Gamedata(self.save_data.load(key)).genre)

        return res

    def get_date_birth_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(Gamedata(self.save_data.load(key)).date_birth)

        return res

    def get_company_data(self):
        res = []
        for key in self.save_data.keys():
            res.append(Gamedata(self.save_data.load(key)).company)

        return res

    def add_game_data(self, key):
        self.save_data.save(key, self.save_data.load(key))
        self.__init__()

    def delete_game_data(self, key):
        self.save_data.delete(key)
        self.__init__()

    def change_page_number(self, event):
        if event == 'next':
            self.number += 1
        else:
            self.number -= 1
        self.window.close()
        self.__init__()

    def get_event_check(self, event, window):
        edit_data = []
        flag = None

        if event == 'next' or event == 'previous':
            self.change_page_number(event)

        elif event == '再読込':
            self.window.close()
            self.__init__()

        for i in range(self.sum_number):
            if event == self.game_list[i].name:
                flag = event
                self.window['INPUT'].update(f'{event}を選択中')

            elif flag == self.game_list[i].name:
                if event == '詳細':
                    window = self.game_list[i].details_menu()
                    self.game_list[i].update_details(window)

                elif event == '削除':
                    self.delete_game_data(self.game_list[i].name)

                elif event == '編集':
                    window = self.game_list[i].add_menu()
                    key, flag = self.game_list[i].update_data(window)

                    if flag:
                        self.add_game_data(key)
                    else:
                        self.delete_game_data(key)

        if event == '追加':
            new = Gamedata(edit_data)
            window = new.add_menu()
            key, flag = new.update_data(window)

            if flag:
                self.add_game_data(key)
            else:
                self.delete_game_data(key)

        elif event == '詳細' or event == '追加' or event == '編集' or event == '削除':
            window['INPUT'].update('ゲームを選択してください')


class MainMenu:
    HEADINGS_NAME = ['ゲーム名', 'ジャンル', '発売年', '会社名']
    BUTTON_NAME = ['追加', '編集', '詳細', '削除', '検索', '再読込']

    def __init__(self, number, sum_number, game_list, genre, date_birth, company):
        self.number = number
        self.sum_number = sum_number
        self.game_list = game_list
        self.genre = genre
        self.date_birth = date_birth
        self.company = company


if __name__ == "__main__":
    main()
