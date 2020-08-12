import PySimpleGUI as sg
from PIL import Image
import os

from file import open_file
from check import event_check
from menu import main_menu, create_summary
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


class GameData:

    def __init__(self, key, game_list):
        self.name = key
        self.genre = game_list[0]
        self.date_birth = game_list[1]
        self.company = game_list[2]
        self.point = game_list[3]
        self.image_site = game_list[4]
        self.site = game_list[5]

        if self.image_site != '':
            self.image = Image.open(self.image_site)

    def image_resize(self):
        image_size = self.image.resize((500, 500))
        image_size.save(self.image)

    def run_data(self, window):
        if self.site == 'site':
            window['site'].update('エラー: 実行ファイルが指定されていません')

        else:
            os.system("xdg-open '" + self.site + "'")
            exit()

    def details_menu(self):
        self.image_resize()

        layout_details = [
            [sg.Image(self.image),
             ],
            [sg.Text('ゲーム名', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.name, size=(17, 1), font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.genre, size=(17, 1), font=FONT_SIZE),
             ],
            [sg.Text('発売年', size=(10, 1), font=FONT_SIZE),
             sg.Text(f'{self.date_birth}年', size=(17, 1), font=FONT_SIZE),
             ],
            [sg.Text('会社名', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.company, size=(17, 1), font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.point, size=(17, 1), font=FONT_SIZE),
             ],
            [sg.CloseButton('戻る', size=(13, 1), font=FONT_SIZE, key='Exit'),
             sg.Button(button_text='実行', size=(13, 1), font=FONT_SIZE, key='site'),
             ],
            [sg.Text('', size=(29, 1), font=FONT_SIZE),
             ],
        ]

        return sg.Window(f'{self.name}の詳細').Layout(layout_details)

    def add_menu(self):
        genre_data = ['シューティング', 'アクション', 'アドベンチャー', 'ロールプレイング', 'パズル',
                      'レース', 'シュミレーション', 'スポーツ', 'オープンワールド', 'ボード',
                      ]
        company_name_data = ['任天堂', 'コナミ', 'エニックス', 'ナムコ', 'ソニー']

        # Edit and Add are determined by key
        if self.point == '':
            self.point = '0'
            add_key = '追加'
        else:
            add_key = 'edit'

        layout_add = [
            [sg.Text('タイトル', size=(10, 2), font=FONT_SIZE),
             sg.Input(default_text=self.name, size=(20, 2), font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=(10, 2), font=FONT_SIZE),
             sg.InputCombo(default_value=self.genre, values=genre_data, size=(20, 1),
                           font=FONT_SIZE),
             ],
            [sg.Text('発売年', size=(10, 2), font=FONT_SIZE),
             sg.Input(default_text=self.date_birth, size=(20, 2), font=FONT_SIZE),
             ],
            [sg.Text('会社名', size=(10, 2), font=FONT_SIZE),
             sg.InputCombo(default_value=self.company, values=company_name_data, size=(20, 1),
                           font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=(10, 2), font=FONT_SIZE),
             sg.Input(default_text=self.point, size=(20, 2), font=FONT_SIZE),
             ],
            [sg.FileBrowse(button_text='画像を選択してください', size=(30, 1), font=FONT_SIZE, key=IMAGE_DATA_NUMBER,
                           file_types=(('Image Files', '*.png'),)),
             ],
            [sg.FileBrowse(button_text='実行ファイルを選択してください', size=(30, 1), font=FONT_SIZE, key=SITE_DATA_NUMBER),
             ],
            [sg.Button(button_text='追加', size=(15, 1), font=FONT_SIZE, key=add_key),
             sg.CloseButton('戻る', size=(15, 1), font=FONT_SIZE, key='Exit'),
             ],
            [sg.Text('', size=(30, 1), font=FONT_SIZE, key='INPUT')]
        ]

        return sg.Window('作成メニュー').Layout(layout_add)

    def update_data(self, window):
        while True:
            event, new_game_data = window.Read()
            key = list(new_game_data.values())

            if event is None or event == 'Exit':
                break

            if new_game_data[SITE_DATA_NUMBER] == '':
                new_game_data[SITE_DATA_NUMBER] = 'site'

            if event == 'edit':
                if new_game_data[IMAGE_DATA_NUMBER] == '':
                    new_game_data[IMAGE_DATA_NUMBER] = self.image_site

                if new_game_data[SITE_DATA_NUMBER] == '':
                    new_game_data[SITE_DATA_NUMBER] = self.site

            for i in range(NUMBER_DATA_PER):
                if new_game_data[i] == '':
                    window['INPUT'].update('入力忘れがあります')
                    break

            else:
                return key


    def update_details(self, window):
        while True:
            event, = window.Read()
            if event is None:
                break

            self.run_data(window)


class App:

    def __init__(self):
        Saves.current_dbname = 'spielliste'
        self.save_data = Saves()
        self.game_list = []
        self.number = 0
        self.get_load_data()
        self.sum_number = len(self.game_list)
        self.flag = None

        self.window = MainMenu(self.number, self.sum_number, self.game_list, self.get_genre_data(),
                               self.get_date_birth_data(), self.get_company_data(),
                               ).show('', '')

    def get_load_data(self):
        for key in self.save_data.keys():
            print(key, self.save_data.load(key))
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
        self.__init__()

    def get_event_check(self, event):
        edit_data = [''] * NUMBER_DATA_PER

        if event == 'next' or event == 'previous':
            self.change_page_number(event)

        elif event == '再読込':
            self.reload_game_data()

        for i in range(self.sum_number):
            print(event, self.flag)
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

    def show(self, input_text, values_data):
        previous_page = []
        next_page = []

        headings = [
            [sg.Text(text=self.HEADINGS_NAME[0], size=(20, 1), font=FONT_SIZE),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[1], menu_def=['', self.genre], size=(14, 1), font=FONT_SIZE,
                           key=GENRE_NAME_DATA_NUMBER),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[2], menu_def=['', self.date_birth], size=(14, 1),
                           font=FONT_SIZE, key=DATE_BIRTH_DATA_NUMBER),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[3], menu_def=['', self.company], size=(14, 1), font=FONT_SIZE,
                           key=COMPANY_NAME_DATA_NUMBER),
             ]
        ]

        if len(values_data) != 0 and values_data[0] == input_text:
            input_text = ''

        layout = [
            [sg.Text(size=(13, 1)),
             sg.Input(size=(20, 1), font=FONT_SIZE, default_text=input_text),
             sg.Button(button_text=self.BUTTON_NAME[4], size=(20, 1), font=FONT_SIZE, key='search'),
             sg.Button(button_text=self.BUTTON_NAME[5], size=(13, 1), font=FONT_SIZE),
             ]
        ]
        layout += headings

        for game in self.game_list:
            if game.site == 'site':
                button_color = ('white', 'black')

            else:
                button_color = ('black', 'white')

            layout += [
                [sg.Button(game.name, size=(19, 1), font=FONT_SIZE, button_color=button_color),
                 sg.Text(game.genre, size=(15, 1), font=FONT_SIZE),
                 sg.Text(game.date_birth + '年', size=(15, 1), font=FONT_SIZE),
                 sg.Text(game.company, size=(15, 1), font=FONT_SIZE),
                 ]
            ]
        # Determine if you need a button
        if self.number > 0:
            previous_page = [sg.Submit(button_text='前の10件', size=(33, 1), font=FONT_SIZE, key='previous')]

        if self.sum_number > (self.number + 1) * ONE_COLUMN_LENGTH:
            # Adjust the position by putting in a space
            if self.number == 0:
                previous_page = [sg.Text(' ', size=(32, 1), font=FONT_SIZE)]

            next_page = [sg.Submit(button_text='次の10件', size=(33, 1), font=FONT_SIZE, key='next')]
            next_number = self.number + ONE_COLUMN_LENGTH

        else:
            next_number = self.sum_number

        layout += [previous_page + next_page,
                   [sg.Button(button_text=self.BUTTON_NAME[0], size=(15, 1), font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[1], size=(15, 1), font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[2], size=(15, 1), font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[3], size=(15, 1), font=FONT_SIZE),
                    ],
                   [sg.Text(f'{self.sum_number}件のうち、　{self.number}から{next_number}件を表示しています',
                            size=(40, 1), font=FONT_SIZE),
                    sg.Text('', size=(30, 1), font=FONT_SIZE, key='INPUT')],
                   ]

        return sg.Window('Game menu').Layout(layout)


if __name__ == "__main__":
    a = App()
    while True:
        event, values = a.window.Read()
        a.window['INPUT'].update('{0}を選択中'.format(event))
        a.get_event_check(event)

        if event is None:
            exit()
