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
    DATE_BIRTH_DATA_NUMBER,
    IMAGE_DATA_NUMBER,
    SITE_DATA_NUMBER,
    EXEC_DATA_NUMBER,
    HARD_DATA_NUMBER,
)


class GameData:
    HARD_NAME = {'ファミコン': 'fc', 'スーパーファミコン': 'sfc', 'MSX': 'MSX', 'MSX2': 'MSX2',
                 'ニンテンドー64': 'n64', 'ゲームボーイアドバンス': 'gba', 'pcエンジン': 'pce',
                 'メガドライブ': 'md', 'ニンテンドーds': 'nds', 'ゲームキューブ': 'gc',
                 'プレステーション': 'ps', 'psp': 'psp',
                 }
    # detail
    DETAIL_GENRE_SIZE = (10, 1)
    DETAIL_TEXT_SIZE = (50, 1)
    DETAIL_BUTTON_SIZE = (30, 1)
    DETAIL_SITE_SIZE = (60, 1)
    # add_menu
    MENU_GENRE_SIZE = (10, 2)
    MENU_BROWSE_SIZE = (67, 1)
    MENU_BUTTON_SIZE = (32, 1)
    MENU_TEXT_GENRE_SIZE = (57, 1)
    MENU_TEXT_INPUT_SIZE = (58, 2)
    MENU_DATE_INPUT_SIZE = (19, 2)
    MENU_SITE_SIZE = (68, 1)

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
            [sg.Text('ハード', size=self.DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Image(data=get_img_data(f'assets/hard_icon/{self.HARD_NAME[self.hard]}.png',
                                        maxsize=ICON_SIZE,
                                        first=True)
                      ),
             ],
            [sg.Text('ゲーム名', size=self.DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.name, size=self.DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=self.DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.genre, size=self.DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('発売日', size=self.DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(f'{self.date_birth}', size=self.DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('会社名', size=self.DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.company, size=self.DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=self.DETAIL_GENRE_SIZE, font=FONT_SIZE),
             sg.Text(self.point, size=self.DETAIL_TEXT_SIZE, font=FONT_SIZE),
             ],
            [sg.CloseButton('戻る', size=self.DETAIL_BUTTON_SIZE, font=FONT_SIZE, key='Exit'),
             sg.Button(button_text='実行', size=self.DETAIL_BUTTON_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('', size=self.DETAIL_SITE_SIZE, font=FONT_SIZE, key='site'),
             ],
        ]

        return sg.Window(f'{self.name}の詳細').Layout(layout_details)

    def add_menu(self, genre, company, input_txt=''):
        # If the year and date are not entered
        if self.date_birth == '':
            self.date_birth = '//'
        elif self.date_birth.count('/') != 2:
            self.date_birth = '//'

        genre_data = sorted(list(set(genre)))
        company_name_data = sorted(list(set(company)))
        year, month, day = self.date_birth.split('/')

        # Edit and Add are determined by key
        if self.point == '':
            self.point = '0'
            add_key = '追加'
        else:
            add_key = 'edit'

        hard_layout1 = [sg.Text('ハード', size=self.MENU_GENRE_SIZE, font=FONT_SIZE)]
        hard_layout2 = [sg.Text('', size=self.MENU_GENRE_SIZE, font=FONT_SIZE)]

        for i, (key, value) in enumerate(self.HARD_NAME.items()):
            if self.hard == key:
                button_color = ('white', 'black')

            else:
                button_color = ('black', 'white')
            if i % 2 == 0:
                hard_layout1.append(sg.Button(image_filename=f'assets/hard_icon/{value}.png', image_size=ICON_SIZE,
                                              key=key, button_color=button_color))
            else:
                hard_layout2.append(sg.Button(image_filename=f'assets/hard_icon/{value}.png', image_size=ICON_SIZE,
                                              key=key, button_color=button_color))

        layout_add = [
            hard_layout1,
            hard_layout2,
            [sg.Text('タイトル', size=self.MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.Input(default_text=self.name, size=self.MENU_TEXT_INPUT_SIZE, font=FONT_SIZE),
             ],
            [sg.Text('ジャンル', size=self.MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.InputCombo(default_value=self.genre, values=genre_data, size=self.MENU_TEXT_GENRE_SIZE,
                           font=FONT_SIZE),
             ],
            [sg.Text('発売日', size=self.MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.Input(default_text=year, size=self.MENU_DATE_INPUT_SIZE, font=FONT_SIZE),
             sg.Text('/', font=FONT_SIZE),
             sg.Input(default_text=month, size=self.MENU_DATE_INPUT_SIZE, font=FONT_SIZE, key='month'),
             sg.Text('/', font=FONT_SIZE),
             sg.Input(default_text=day, size=self.MENU_DATE_INPUT_SIZE, font=FONT_SIZE, key='day'),
             ],
            [sg.Text('会社名', size=self.MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.InputCombo(default_value=self.company, values=company_name_data, size=self.MENU_TEXT_GENRE_SIZE,
                           font=FONT_SIZE),
             ],
            [sg.Text('最高得点', size=self.MENU_GENRE_SIZE, font=FONT_SIZE),
             sg.Input(default_text=self.point, size=self.MENU_TEXT_INPUT_SIZE, font=FONT_SIZE),
             ],
            [sg.FileBrowse(button_text='画像を選択してください', size=self.MENU_BROWSE_SIZE, font=FONT_SIZE,
                           key=IMAGE_DATA_NUMBER, file_types=(('Image Files', '*.png'),)),
             ],
            [sg.FileBrowse(button_text='romファイルを選択してください', size=self.MENU_BROWSE_SIZE, font=FONT_SIZE,
                           key=SITE_DATA_NUMBER),
             ],
            [sg.FileBrowse(button_text='実行ファイルを選択してください', size=self.MENU_BROWSE_SIZE, font=FONT_SIZE,
                           key=EXEC_DATA_NUMBER),
             ],
            [sg.Button(button_text='追加', size=self.MENU_BUTTON_SIZE, font=FONT_SIZE, key=add_key),
             sg.CloseButton('戻る', size=self.MENU_BUTTON_SIZE, font=FONT_SIZE, key='Exit'),
             ],
            [sg.Text(input_txt, size=self.MENU_SITE_SIZE, font=FONT_SIZE, key='INPUT')]
        ]

        self.window = sg.Window('作成メニュー').Layout(layout_add)

    def update_data(self, genre, company):
        self.add_menu(genre, company)
        while True:
            event, new_game_data = self.window.Read()
            # print(event, new_game_data)

            # Button select
            new_game_data[HARD_DATA_NUMBER] = self.hard

            if event is None or event == 'Exit':
                break

            if (new_game_data[DATE_BIRTH_DATA_NUMBER].isdigit() and
                    new_game_data["month"].isdigit() and new_game_data["day"].isdigit()):
                new_game_data[DATE_BIRTH_DATA_NUMBER] = (f'{new_game_data[DATE_BIRTH_DATA_NUMBER]}/'
                                                         f'{new_game_data.pop("month")}/'
                                                         f'{new_game_data.pop("day")}')
            else:
                self.window.close()
                # delete from dict
                new_game_data.pop("month")
                new_game_data.pop("day")
                self.__init__(self.id, list(new_game_data.values()))
                self.add_menu(genre, company, input_txt='エラー: 整数を入力してください')
                continue

            # When hardware is selected
            if event != '追加' and event != 'edit':
                self.hard = event
                self.window.close()
                self.__init__(self.id, list(new_game_data.values()))
                self.add_menu(genre, company, input_txt=f'{self.hard}を入力しました')
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
                    self.window.close()
                    self.__init__(self.id, list(new_game_data.values()))
                    self.add_menu(genre, company, input_txt='入力忘れがあります')
                    break

            else:
                self.window.close()
                key = list(new_game_data.values())
                return key

    def update_details(self, window):
        while True:
            event, _ = window.Read()
            if event is None or event == 'Exit':
                break

            self.run_data(window)
