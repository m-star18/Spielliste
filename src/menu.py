import os

import PySimpleGUI as sg
from PIL import Image

from file import image_resize
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


def game_list_sort(game_list_data, sum_number_data):
    game_name_list_data = [''] * sum_number_data
    sorted_game_list_data = [''] * (sum_number_data * NUMBER_DATA_PER)

    for i in range(sum_number_data):
        game_name_list_data[i] = game_list_data[i * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER]

    sorted_game_name_list_data = sorted(game_name_list_data)

    for i in range(sum_number_data):
        for j in range(sum_number_data):

            if sorted_game_name_list_data[i] == game_name_list_data[j]:
                for k in range(NUMBER_DATA_PER):
                    sorted_game_list_data[i * NUMBER_DATA_PER + k] = game_list_data[j * NUMBER_DATA_PER + k]

                break

    return sorted_game_list_data


def create_summary(game_list_data, sum_number_data):
    genre_data = [''] * sum_number_data
    date_birth_data = [0] * sum_number_data
    company_data = [''] * sum_number_data

    for i in range(sum_number_data):
        genre_data[i] = game_list_data[i * NUMBER_DATA_PER + GENRE_NAME_DATA_NUMBER]
        date_birth_data[i] = game_list_data[i * NUMBER_DATA_PER + DATE_BIRTH_DATA_NUMBER]
        company_data[i] = game_list_data[i * NUMBER_DATA_PER + COMPANY_NAME_DATA_NUMBER]

    genre_data = sorted(list((set(genre_data))))
    date_birth_data = sorted(list(set(date_birth_data)))
    company_data = sorted(list(set(company_data)))

    return genre_data, date_birth_data, company_data


def main_menu(sum_number_data, game_list_data, number_data, input_text, values_data, genre_data, date_birth_data,
              company_data):
    now_page_number = ONE_COLUMN_LENGTH * number_data
    next_page_number = sum_number_data
    previous_page = []
    next_page = []

    game_list_data = game_list_sort(game_list_data, sum_number_data)

    headings = [
        [sg.Text('ゲーム名', size=(20, 1), font=FONT_SIZE),
         sg.ButtonMenu(button_text='ジャンル', menu_def=['', genre_data], size=(14, 1), font=FONT_SIZE, key=GENRE_NAME_DATA_NUMBER),
         sg.ButtonMenu(button_text='発売年', menu_def=['', date_birth_data], size=(14, 1), font=FONT_SIZE, key=DATE_BIRTH_DATA_NUMBER),
         sg.ButtonMenu(button_text='会社名', menu_def=['', company_data], size=(14, 1), font=FONT_SIZE, key=COMPANY_NAME_DATA_NUMBER),
         ]
    ]

    if len(values_data) != 0 and values_data[0] == input_text:
        input_text = ''

    layout = [
        [sg.Text(size=(13, 1)),
         sg.Input(size=(20, 1), font=FONT_SIZE, default_text=input_text),
         sg.Button(button_text='検索', size=(20, 1), font=FONT_SIZE, key='search'),
         sg.Button('再読込', size=(13, 1), font=FONT_SIZE),
         ]
    ]
    layout += headings

    for i in range(now_page_number, now_page_number + min(ONE_COLUMN_LENGTH, sum_number_data - now_page_number)):
        if game_list_data[i * NUMBER_DATA_PER + SITE_DATA_NUMBER] == 'site':
            button_color = ('white', 'black')

        else:
            button_color = ('black', 'white')

        layout += [
            [sg.Button(game_list_data[i * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER], size=(19, 1), font=FONT_SIZE, button_color=button_color),
             sg.Text(game_list_data[i * NUMBER_DATA_PER + GENRE_NAME_DATA_NUMBER], size=(15, 1), font=FONT_SIZE),
             sg.Text(game_list_data[i * NUMBER_DATA_PER + DATE_BIRTH_DATA_NUMBER] + '年', size=(15, 1), font=FONT_SIZE),
             sg.Text(game_list_data[i * NUMBER_DATA_PER + COMPANY_NAME_DATA_NUMBER], size=(15, 1), font=FONT_SIZE),
             ]
        ]
    # Determine if you need a button
    if number_data > 0:
        previous_page = [sg.Submit(button_text='前の10件', size=(33, 1), font=FONT_SIZE, key='previous')]

    if sum_number_data > now_page_number + ONE_COLUMN_LENGTH:
        # Adjust the position by putting in a space
        if now_page_number == 0:
            previous_page = [sg.Text(' ', size=(32, 1), font=FONT_SIZE)]

        next_page = [sg.Submit(button_text='次の10件', size=(33, 1), font=FONT_SIZE, key='next')]
        next_page_number = now_page_number + ONE_COLUMN_LENGTH

    layout += [previous_page + next_page,
               [sg.Button('追加', size=(15, 1), font=FONT_SIZE),
                sg.Button('編集', size=(15, 1), font=FONT_SIZE),
                sg.Button('詳細', size=(15, 1), font=FONT_SIZE),
                sg.Button('削除', size=(15, 1), font=FONT_SIZE),
                ],
               [sg.Text('{0}件のうち、　{1}から{2}件を表示しています'.format(sum_number_data, now_page_number, next_page_number), size=(40, 1), font=FONT_SIZE),
                sg.Text('', size=(30, 1), font=FONT_SIZE, key='INPUT')],
               ]

    return sg.Window('Game menu').Layout(layout)


def details_menu(game_list_data, number):
    image = Image.open(game_list_data[number * NUMBER_DATA_PER + IMAGE_DATA_NUMBER])
    image_resize(image, game_list_data, number)

    layout_details = [
        [sg.Image(game_list_data[number * NUMBER_DATA_PER + IMAGE_DATA_NUMBER]),
         ],
        [sg.Text('ゲーム名', size=(10, 1), font=FONT_SIZE),
         sg.Text(game_list_data[number * NUMBER_DATA_PER + GAME_NAME_DATA_NUMBER], size=(17, 1), font=FONT_SIZE),
         ],
        [sg.Text('ジャンル', size=(10, 1), font=FONT_SIZE),
         sg.Text(game_list_data[number * NUMBER_DATA_PER + GENRE_NAME_DATA_NUMBER], size=(17, 1), font=FONT_SIZE),
         ],
        [sg.Text('発売年', size=(10, 1), font=FONT_SIZE),
         sg.Text(game_list_data[number * NUMBER_DATA_PER + DATE_BIRTH_DATA_NUMBER] + '年', size=(17, 1), font=FONT_SIZE),
         ],
        [sg.Text('会社名', size=(10, 1), font=FONT_SIZE),
         sg.Text(game_list_data[number * NUMBER_DATA_PER + COMPANY_NAME_DATA_NUMBER], size=(17, 1), font=FONT_SIZE),
         ],
        [sg.Text('最高得点', size=(10, 1), font=FONT_SIZE),
         sg.Text(game_list_data[number * NUMBER_DATA_PER + HIGHEST_SCORE_DATA_NUMBER], size=(17, 1), font=FONT_SIZE),
         ],
        [sg.CloseButton('戻る', size=(13, 1), font=FONT_SIZE, key='Exit'),
         sg.Button(button_text='実行', size=(13, 1), font=FONT_SIZE, key=number * NUMBER_DATA_PER + SITE_DATA_NUMBER),
         ],
        [sg.Text('', size=(29, 1), font=FONT_SIZE, key='site'),
         ],
    ]

    return sg.Window(game_list_data[number * NUMBER_DATA_PER] + 'の詳細').Layout(layout_details)


def add_menu(item_name, edit_data):
    layout_add = []
    genre_data = ['シューティング', 'アクション', 'アドベンチャー', 'ロールプレイング', 'パズル',
                  'レース', 'シュミレーション', 'スポーツ', 'オープンワールド', 'ボード',
                  ]
    company_name_data = ['任天堂', 'コナミ', 'エニックス', 'ナムコ', 'ソニー']
    # Edit and Add are determined by key
    if not edit_data:
        edit_data = [''] * NUMBER_DATA_PER
        edit_data[HIGHEST_SCORE_DATA_NUMBER] = '0'
        add_key = '追加'

    else:
        add_key = 'edit'

    layout_add += [
        [sg.Text(item_name[GAME_NAME_DATA_NUMBER], size=(10, 2), font=FONT_SIZE),
         sg.Input(default_text=edit_data[GAME_NAME_DATA_NUMBER], size=(20, 2), font=FONT_SIZE),
         ],
        [sg.Text(item_name[GENRE_NAME_DATA_NUMBER], size=(10, 2), font=FONT_SIZE),
         sg.InputCombo(default_value=edit_data[GENRE_NAME_DATA_NUMBER], values=genre_data, size=(20, 1), font=FONT_SIZE),
         ],
        [sg.Text(item_name[DATE_BIRTH_DATA_NUMBER], size=(10, 2), font=FONT_SIZE),
         sg.Input(default_text=edit_data[DATE_BIRTH_DATA_NUMBER], size=(20, 2), font=FONT_SIZE),
         ],
        [sg.Text(item_name[COMPANY_NAME_DATA_NUMBER], size=(10, 2), font=FONT_SIZE),
         sg.InputCombo(default_value=edit_data[COMPANY_NAME_DATA_NUMBER], values=company_name_data, size=(20, 1), font=FONT_SIZE),
         ],
        [sg.Text(item_name[HIGHEST_SCORE_DATA_NUMBER], size=(10, 2), font=FONT_SIZE),
         sg.Input(default_text=edit_data[HIGHEST_SCORE_DATA_NUMBER], size=(20, 2), font=FONT_SIZE),
         ],
        [sg.FileBrowse(button_text='画像を選択してください', size=(30, 1), font=FONT_SIZE, key=IMAGE_DATA_NUMBER, file_types=(('Image Files', '*.png'),)),
         ],
        [sg.FileBrowse(button_text='実行ファイルを選択してください', size=(30, 1), font=FONT_SIZE, key=SITE_DATA_NUMBER),
         ],
        [sg.Button(button_text='追加', size=(15, 1), font=FONT_SIZE, key=add_key),
         sg.CloseButton('戻る', size=(15, 1), font=FONT_SIZE, key='Exit'),
         ],
        [sg.Text('', size=(30, 1), font=FONT_SIZE, key='INPUT')]
    ]

    return sg.Window('作成メニュー').Layout(layout_add)


class GameData:

    def __init__(self, game_list):
        self.name = game_list[0]
        self.genre = game_list[1]
        self.date_birth = game_list[2]
        self.company = game_list[3]
        self.point = game_list[4]
        self.image_site = game_list[5]
        self.site = game_list[6]
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
        image_resize()

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
            event, values = window.Read()

            if event is None or event == 'Exit':
                break

            if values[SITE_DATA_NUMBER] == '':
                values[SITE_DATA_NUMBER] = 'site'

            if event == 'edit':
                if values[IMAGE_DATA_NUMBER] == '':
                    values[IMAGE_DATA_NUMBER] = self.image_site

                if values[SITE_DATA_NUMBER] == '':
                    values[SITE_DATA_NUMBER] = self.site

            for i in range(NUMBER_DATA_PER):
                if values[i] == '':
                    window['INPUT'].update('入力忘れがあります')
                    break

            else:
                window.close()
                return values, event

    def update_details(self, window):
        while True:
            event, = window.Read()
            if event is None:
                break

            self.run_data(window)
