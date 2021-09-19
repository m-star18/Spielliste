import os
import subprocess
import uuid

import PySimpleGUI as sg
from PIL import Image

from image_resize import get_img_data
from const.app import (
    FONT_SIZE,
    ICON_SIZE,
    NUMBER_DATA_PER,
    IMAGE_DATA_NUMBER,
    SITE_DATA_NUMBER,
    EXEC_DATA_NUMBER,
    HARD_DATA_NUMBER,
)
from const.game import (
    GAME_DETAIL_BUTTON_SIZE,
    GAME_DETAIL_GENRE_SIZE,
    GAME_DETAIL_TEXT_SIZE,
    GAME_DETAIL_SITE_SIZE,
    GAME_MENU_GENRE_SIZE,
    GAME_MENU_SITE_SIZE,
    GAME_MENU_BUTTON_SIZE,
    GAME_MENU_BROWSE_SIZE,
    GAME_MENU_TEXT_GENRE_SIZE,
    GAME_MENU_TEXT_INPUT_SIZE,
)


class GameData:
    HARD_NAME = {'ファミコン': 'fc', 'スーパーファミコン': 'sfc', 'MSX': 'MSX', 'MSX2': 'MSX2',
                 'ニンテンドー64': 'n64', 'ゲームボーイアドバンス': 'gba', 'pcエンジン': 'pce',
                 'メガドライブ': 'md', 'ニンテンドーds': 'nds', 'ゲームキューブ': 'gc',
                 'プレステーション': 'ps', 'psp': 'psp',
                 }

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
            [sg.Image(data=get_img_data(self.image_site, first=True)),
             ],
            [sg.Text('ハード', size=GAME_DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Image(data=get_img_data(f'assets/hard_icon/{self.HARD_NAME[self.hard]}.png',
                                        maxsize=ICON_SIZE,
                                        first=True)
                      ),
             ],
            [sg.Text('ゲーム名', size=GAME_DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.name, size=GAME_DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=GAME_DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.genre, size=GAME_DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('発売年', size=GAME_DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(f'{self.date_birth}年', size=GAME_DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('会社名', size=GAME_DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.company, size=GAME_DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=GAME_DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.point, size=GAME_DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.CloseButton('戻る', size=GAME_DETAIL_BUTTON_SIZE, font=FONT_SIZE, key='Exit'),
             sg.Button(button_text='実行', size=GAME_DETAIL_BUTTON_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('', size=GAME_DETAIL_SITE_SIZE, font=FONT_SIZE, key='site'),
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
            [sg.Text('ハード', size=GAME_MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.Button(image_filename='assets/hard_icon/fc.png', image_size=ICON_SIZE, key='ファミコン'),
             sg.Button(image_filename='assets/hard_icon/sfc.png', image_size=ICON_SIZE, key='スーパーファミコン'),
             sg.Button(image_filename='assets/hard_icon/MSX.png', image_size=ICON_SIZE, key='MSX'),
             sg.Button(image_filename='assets/hard_icon/MSX2.png', image_size=ICON_SIZE, key='MSX2'),
             sg.Button(image_filename='assets/hard_icon/n64.png', image_size=ICON_SIZE, key='ニンテンドー64'),
             sg.Button(image_filename='assets/hard_icon/gba.png', image_size=ICON_SIZE, key='ゲームボーイアドバンス'),
             sg.Button(image_filename='assets/hard_icon/pce.png', image_size=ICON_SIZE, key='pcエンジン'),
             sg.Button(image_filename='assets/hard_icon/md.png', image_size=ICON_SIZE, key='メガドライブ'),
             sg.Button(image_filename='assets/hard_icon/nds.png', image_size=ICON_SIZE, key='ニンテンドーds'),
             sg.Button(image_filename='assets/hard_icon/gc.png', image_size=ICON_SIZE, key='ゲームキューブ'),
             sg.Button(image_filename='assets/hard_icon/ps.png', image_size=ICON_SIZE, key='プレステーション'),
             sg.Button(image_filename='assets/hard_icon/psp.png', image_size=ICON_SIZE, key='psp'),
             ],
            [sg.Text('タイトル', size=GAME_MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.Input(default_text=self.name, size=GAME_MENU_TEXT_INPUT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=GAME_MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.InputCombo(default_value=self.genre, values=genre_data, size=GAME_MENU_TEXT_GENRE_SIZE,
                           font=FONT_SIZE),
             ],
            [sg.Text('発売年', size=GAME_MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.Input(default_text=self.date_birth, size=GAME_MENU_TEXT_INPUT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('会社名', size=GAME_MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.InputCombo(default_value=self.company, values=company_name_data, size=GAME_MENU_TEXT_GENRE_SIZE,
                           font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=GAME_MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.Input(default_text=self.point, size=GAME_MENU_TEXT_INPUT_SIZE, font=FONT_SIZE),
             ],
            [sg.FileBrowse(button_text='画像を選択してください', size=GAME_MENU_BROWSE_SIZE, font=FONT_SIZE, key=IMAGE_DATA_NUMBER,
                           file_types=(('Image Files', '*.png'),)),
             ],
            [sg.FileBrowse(button_text='romファイルを選択してください', size=GAME_MENU_BROWSE_SIZE, font=FONT_SIZE,
                           key=SITE_DATA_NUMBER),
             ],
            [sg.FileBrowse(button_text='実行ファイルを選択してください', size=GAME_MENU_BROWSE_SIZE, font=FONT_SIZE,
                           key=EXEC_DATA_NUMBER),
             ],
            [sg.Button(button_text='追加', size=GAME_MENU_BUTTON_SIZE, font=FONT_SIZE, key=add_key),
             sg.CloseButton('戻る', size=GAME_MENU_BUTTON_SIZE, font=FONT_SIZE, key='Exit'),
             ],
            [sg.Text('', size=GAME_MENU_SITE_SIZE, font=FONT_SIZE, key='INPUT')]
        ]

        return sg.Window('作成メニュー').Layout(layout_add)

    def update_data(self, window):
        while True:
            event, new_game_data = window.Read()
            # print(event, new_game_data)

            if event is None or event == 'Exit':
                break

            # When hardware is selected
            print(event)
            if event != '追加' and event != 'edit':
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
            # Reduce the number of loops by one since Hard is a button.
            for i in range(NUMBER_DATA_PER - 2):
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
