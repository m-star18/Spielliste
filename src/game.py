import os
import io

import PySimpleGUI as sg
from PIL import Image, ImageTk

from const import (
    FONT_SIZE,
    NUMBER_DATA_PER,
    IMAGE_DATA_NUMBER,
    SITE_DATA_NUMBER,
)


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

    def get_img_data(self, maxsize=(500, 500), first=False):
        """
        Generate image data using PIL
        """
        self.image = Image.open(self.image_site)
        self.image.thumbnail(maxsize)
        if first:  # tkinter is inactive the first time
            bio = io.BytesIO()
            self.image.save(bio, format="PNG")
            del self.image
            return bio.getvalue()
        return ImageTk.PhotoImage(self.image)

    def run_data(self, window):
        if self.site == 'site':
            window['site'].update('エラー: 実行ファイルが指定されていません')

        else:
            os.system(f"xdg-open '{self.site}'")
            exit()

    def details_menu(self):
        layout_details = [
            [sg.Image(data=self.get_img_data(first=True)),
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

            if event is None or event == 'Exit':
                break

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
                window.close()
                key = list(new_game_data.values())
                return key

    def update_details(self, window):
        while True:
            event, _ = window.Read()
            if event is None or event == 'Exit':
                break

            self.run_data(window)
