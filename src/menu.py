import PySimpleGUI as sg

from image_resize import get_img_data
from const.app import (
    FONT_SIZE,
    GENRE_NAME_DATA_NUMBER,
    DATE_BIRTH_DATA_NUMBER,
    COMPANY_NAME_DATA_NUMBER,
    HARD_DATA_NUMBER,
    ONE_COLUMN_LENGTH,
    TITLE,
    THEME,
)


class MainMenu:
    HEADINGS_NAME = ['ゲーム名', 'ジャンル', '発売日', '会社名', 'ハード名']
    BUTTON_NAME = ['新規', '編集', '詳細', '削除', '検索', 'オールクリア']
    HARD_NAME = {'ファミコン': 'fc', 'スーパーファミコン': 'sfc', 'MSX': 'MSX', 'MSX2': 'MSX2',
                 'ニンテンドー64': 'n64', 'ゲームボーイアドバンス': 'gba', 'PCエンジン': 'pce',
                 'メガドライブ': 'md', 'ニンテンドーDS': 'nds', 'ゲームキューブ': 'gc',
                 'プレステーション': 'ps', 'PSP': 'psp',
                 }
    HEAD_HARD_SIZE = (10, 1)
    HEAD_NAME_SIZE = (51, 1)
    NAME_SIZE = (50, 1)
    SPACE_SIZE = (12, 1)
    TITLE_SIZE = (50, 1)
    INPUT_SIZE = (30, 1)
    PREVIOUS_SIZE = (59, 1)
    PREVIOUS_SPACE_SIZE = (61, 1)
    CONFIG_SIZE = (28, 1)
    DEFAULT_SIZE = (18, 1)
    INFO_TXT_SIZE = (40, 1)
    INFO_INPUT_SIZE = (80, 1)

    def __init__(self, number, sum_number, game_list, genre, date_birth, company):
        self.number = number * 10
        self.sum_number = sum_number
        self.game_list = game_list
        self.genre = sorted(list(set(genre))) + ['全て']
        self.date_birth = sorted(list(set(date_birth))) + ['全て']
        self.company = sorted(list(set(company))) + ['全て']
        self.hard = sorted(list(self.HARD_NAME.keys())) + ['全て']
        sg.theme(THEME)

    def show(self, input_text):
        previous_page = []
        next_page = []

        headings = [
            [sg.ButtonMenu(button_text=self.HEADINGS_NAME[4], menu_def=['', self.hard],
                           size=self.HEAD_HARD_SIZE, font=FONT_SIZE, key=HARD_DATA_NUMBER),
             sg.Text(text=self.HEADINGS_NAME[0], size=self.HEAD_NAME_SIZE, font=FONT_SIZE),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[1], menu_def=['', self.genre],
                           size=self.DEFAULT_SIZE, font=FONT_SIZE, key=GENRE_NAME_DATA_NUMBER),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[2], menu_def=['', self.date_birth],
                           size=self.DEFAULT_SIZE, font=FONT_SIZE, key=DATE_BIRTH_DATA_NUMBER),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[3], menu_def=['', self.company],
                           size=self.DEFAULT_SIZE, font=FONT_SIZE, key=COMPANY_NAME_DATA_NUMBER),
             ]
        ]

        layout = [
            [sg.Text(text=TITLE, size=self.TITLE_SIZE, font=FONT_SIZE),
             sg.Input(size=self.INPUT_SIZE, font=FONT_SIZE, default_text=input_text),
             sg.Button(button_text=self.BUTTON_NAME[4], size=self.DEFAULT_SIZE, font=FONT_SIZE, key='search'),
             sg.Button(button_text=self.BUTTON_NAME[5], size=self.DEFAULT_SIZE, font=FONT_SIZE),
             ]
        ]
        layout += headings

        for game in self.game_list[self.number:self.number + ONE_COLUMN_LENGTH]:
            if game.site == 'site':
                button_color = ('white', 'black')

            else:
                button_color = ('black', 'white')

            layout += [
                [sg.Image(data=get_img_data(f'assets/hard_icon/{self.HARD_NAME[game.hard]}.png',
                                            maxsize=(50, 50),
                                            first=True),
                          key=game.id,
                          ),
                 sg.Text(size=self.SPACE_SIZE),
                 sg.Button(game.name, size=self.NAME_SIZE, font=FONT_SIZE, button_color=button_color, key=game.id),
                 sg.Text(game.genre, size=self.DEFAULT_SIZE, font=FONT_SIZE),
                 sg.Text(game.date_birth, size=self.DEFAULT_SIZE, font=FONT_SIZE),
                 sg.Text(game.company, size=self.DEFAULT_SIZE, font=FONT_SIZE),
                 ]
            ]
        # Determine if you need a button
        if self.number > 0:
            previous_page = [sg.Submit(button_text='前の10件', size=self.PREVIOUS_SIZE, font=FONT_SIZE, key='previous')]

        if self.sum_number > self.number + ONE_COLUMN_LENGTH:
            # Adjust the position by putting in a space
            if self.number == 0:
                previous_page = [sg.Text(' ', size=self.PREVIOUS_SPACE_SIZE, font=FONT_SIZE)]

            next_page = [sg.Submit(button_text='次の10件', size=self.PREVIOUS_SIZE, font=FONT_SIZE, key='next')]
            next_number = self.number + ONE_COLUMN_LENGTH

        else:
            next_number = self.sum_number

        layout += [previous_page + next_page,
                   [sg.Button(button_text=self.BUTTON_NAME[0], size=self.CONFIG_SIZE, font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[1], size=self.CONFIG_SIZE, font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[2], size=self.CONFIG_SIZE, font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[3], size=self.CONFIG_SIZE, font=FONT_SIZE),
                    ],
                   [sg.Text(f'{self.sum_number}件のうち、{self.number}から{next_number}件を表示しています',
                            size=self.INFO_TXT_SIZE, font=FONT_SIZE),
                    sg.Text('', size=self.INFO_INPUT_SIZE, font=FONT_SIZE, key='INPUT')],
                   ]

        return sg.Window(TITLE).Layout(layout)
