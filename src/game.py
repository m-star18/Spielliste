import os
import io
import subprocess
import uuid

import PySimpleGUI as sg
from PIL import Image, ImageTk

from const import (
    FONT_SIZE,
    NUMBER_DATA_PER,
    IMAGE_DATA_NUMBER,
    SITE_DATA_NUMBER,
    EXEC_DATA_NUMBER,
    HARD_DATA_NUMBER,
)


class GameData:

    def __init__(self, key, game_list):
        self.id = key
        self.name = game_list[0]
        self.genre = game_list[1]
        self.date_birth = game_list[2]
        self.company = game_list[3]
        self.point = game_list[4]
        self.image_site = game_list[5]
        self.site = game_list[6]
        self.exec_site = game_list[7]
        self.hard = game_list[8]

        if self.id == '':
            self.id = str(uuid.uuid4())

        if self.image_site == '':
            self.image_site = os.path.abspath('assets/no-image.png')
        self.image = Image.open(self.image_site)

        if self.site == '':
            self.site = 'site'

        if self.exec_site == '':
            self.exec_site = 'exec'

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
            window['site'].update('エラー: romファイルが指定されていません')
        elif self.exec_site == 'exec':
            window['site'].update('エラー: 実行ファイルが指定されていません')

        else:
            subprocess.Popen([rf"{self.exec_site}", rf"{self.site}"], shell=True)
            exit()

    def details_menu(self):
        layout_details = [
            [sg.Image(data=self.get_img_data(first=True)),
             ],
            [sg.Text('ハード', size=(10, 1), font=FONT_SIZE),
             sg.Image(filename=self.hard, size=(50, 50)),
             ],
            [sg.Text('ゲーム名', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.name, size=(50, 1), font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.genre, size=(50, 1), font=FONT_SIZE),
             ],
            [sg.Text('発売年', size=(10, 1), font=FONT_SIZE),
             sg.Text(f'{self.date_birth}年', size=(50, 1), font=FONT_SIZE),
             ],
            [sg.Text('会社名', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.company, size=(50, 1), font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=(10, 1), font=FONT_SIZE),
             sg.Text(self.point, size=(50, 1), font=FONT_SIZE),
             ],
            [sg.CloseButton('戻る', size=(30, 1), font=FONT_SIZE, key='Exit'),
             sg.Button(button_text='実行', size=(30, 1), font=FONT_SIZE),
             ],
            [sg.Text('', size=(60, 1), font=FONT_SIZE, key='site'),
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
            [sg.Text('ハード', size=(10, 2), font=FONT_SIZE),
             sg.Button(image_filename='assets/hard_icon/fc.gif', image_size=(50, 50), key='ファミコン'),
             sg.Button(image_filename='assets/hard_icon/sfc.gif', image_size=(50, 50), key='スーパーファミコン'),
             sg.Button(image_filename='assets/hard_icon/MSX.gif', image_size=(50, 50), key='MSX'),
             sg.Button(image_filename='assets/hard_icon/MSX2.gif', image_size=(50, 50), key='MSX2'),
             sg.Button(image_filename='assets/hard_icon/n64.gif', image_size=(50, 50), key='ニンテンドー64'),
             sg.Button(image_filename='assets/hard_icon/gba.gif', image_size=(50, 50), key='ゲームボーイアドバンス'),
             sg.Button(image_filename='assets/hard_icon/pce.gif', image_size=(50, 50), key='pcエンジン'),
             sg.Button(image_filename='assets/hard_icon/md.gif', image_size=(50, 50), key='メガドライブ'),
             sg.Button(image_filename='assets/hard_icon/nds.gif', image_size=(50, 50), key='ニンテンドーds'),
             sg.Button(image_filename='assets/hard_icon/gc.gif', image_size=(50, 50), key='ゲームキューブ'),
             sg.Button(image_filename='assets/hard_icon/ps.gif', image_size=(50, 50), key='プレステーション'),
             sg.Button(image_filename='assets/hard_icon/psp.gif', image_size=(50, 50), key='psp'),
             ],
            [sg.Text('タイトル', size=(10, 2), font=FONT_SIZE),
             sg.Input(default_text=self.name, size=(58, 2), font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=(10, 2), font=FONT_SIZE),
             sg.InputCombo(default_value=self.genre, values=genre_data, size=(57, 1),
                           font=FONT_SIZE),
             ],
            [sg.Text('発売年', size=(10, 2), font=FONT_SIZE),
             sg.Input(default_text=self.date_birth, size=(58, 2), font=FONT_SIZE),
             ],
            [sg.Text('会社名', size=(10, 2), font=FONT_SIZE),
             sg.InputCombo(default_value=self.company, values=company_name_data, size=(57, 1),
                           font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=(10, 2), font=FONT_SIZE),
             sg.Input(default_text=self.point, size=(58, 2), font=FONT_SIZE),
             ],
            [sg.FileBrowse(button_text='画像を選択してください', size=(67, 1), font=FONT_SIZE, key=IMAGE_DATA_NUMBER,
                           file_types=(('Image Files', '*.png'),)),
             ],
            [sg.FileBrowse(button_text='romファイルを選択してください', size=(67, 1), font=FONT_SIZE, key=SITE_DATA_NUMBER),
             ],
            [sg.FileBrowse(button_text='実行ファイルを選択してください', size=(67, 1), font=FONT_SIZE, key=EXEC_DATA_NUMBER),
             ],
            [sg.Button(button_text='追加', size=(32, 1), font=FONT_SIZE, key=add_key),
             sg.CloseButton('戻る', size=(32, 1), font=FONT_SIZE, key='Exit'),
             ],
            [sg.Text('', size=(68, 1), font=FONT_SIZE, key='INPUT')]
        ]

        return sg.Window('作成メニュー').Layout(layout_add)

    def update_data(self, window):
        while True:
            event, new_game_data = window.Read()
            # print(event, new_game_data)

            if event is None or event == 'Exit':
                break

            # When hardware is selected
            if event != '追加':
                self.hard = event
                window['INPUT'].update(f'{self.hard}を入力しました')
                continue

            if new_game_data[IMAGE_DATA_NUMBER] == '':
                new_game_data[IMAGE_DATA_NUMBER] = self.image_site

            if new_game_data[SITE_DATA_NUMBER] == '':
                new_game_data[SITE_DATA_NUMBER] = self.site

            if new_game_data[EXEC_DATA_NUMBER] == '':
                new_game_data[EXEC_DATA_NUMBER] = self.exec_site

            # Don't require "site" to be entered.
            for i in range(NUMBER_DATA_PER - 1):
                if new_game_data[i] == '':
                    window['INPUT'].update('入力忘れがあります')
                    break

            else:
                window.close()
                new_game_data[HARD_DATA_NUMBER] = self.hard
                key = list(new_game_data.values())
                return key

    def update_details(self, window):
        while True:
            event, _ = window.Read()
            if event is None or event == 'Exit':
                break

            self.run_data(window)
