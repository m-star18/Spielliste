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
from const.settings import (
    HEAD_HARD_SIZE,
    HEAD_NAME_SIZE,
    NAME_SIZE,
    SPACE_SIZE,
    TITLE_SIZE,
    INPUT_SIZE,
    PREVIOUS_SIZE,
    PREVIOUS_SPACE_SIZE,
    CONFIG_SIZE,
    DEFAULT_SIZE,
    INFO_TXT_SIZE,
    INFO_INPUT_SIZE,
)


class MainMenu:
    HEADINGS_NAME = ['ゲーム名', 'ジャンル', '発売日', '会社名', 'ハード名']
    BUTTON_NAME = ['新規', '編集', '詳細', '削除', '検索', 'オールクリア']
    HARD_NAME = {'ファミコン': 'fc', 'スーパーファミコン': 'sfc', 'MSX': 'MSX', 'MSX2': 'MSX2',
                 'ニンテンドー64': 'n64', 'ゲームボーイアドバンス': 'gba', 'PCエンジン': 'pce',
                 'メガドライブ': 'md', 'ニンテンドーDS': 'nds', 'ゲームキューブ': 'gc',
                 'プレステーション': 'ps', 'PSP': 'psp',
                 }

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
                           size=HEAD_HARD_SIZE, font=FONT_SIZE, key=HARD_DATA_NUMBER),
             sg.Text(text=self.HEADINGS_NAME[0], size=HEAD_NAME_SIZE, font=FONT_SIZE),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[1], menu_def=['', self.genre],
                           size=DEFAULT_SIZE, font=FONT_SIZE, key=GENRE_NAME_DATA_NUMBER),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[2], menu_def=['', self.date_birth],
                           size=DEFAULT_SIZE, font=FONT_SIZE, key=DATE_BIRTH_DATA_NUMBER),
             sg.ButtonMenu(button_text=self.HEADINGS_NAME[3], menu_def=['', self.company],
                           size=DEFAULT_SIZE, font=FONT_SIZE, key=COMPANY_NAME_DATA_NUMBER),
             ]
        ]

        layout = [
            [sg.Text(text=TITLE, size=TITLE_SIZE, font=FONT_SIZE),
             sg.Input(size=INPUT_SIZE, font=FONT_SIZE, default_text=input_text),
             sg.Button(button_text=self.BUTTON_NAME[4], size=DEFAULT_SIZE, font=FONT_SIZE, key='search'),
             sg.Button(button_text=self.BUTTON_NAME[5], size=DEFAULT_SIZE, font=FONT_SIZE),
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
                 sg.Text(size=SPACE_SIZE),
                 sg.Button(game.name, size=NAME_SIZE, font=FONT_SIZE, button_color=button_color, key=game.id),
                 sg.Text(game.genre, size=DEFAULT_SIZE, font=FONT_SIZE),
                 sg.Text(game.date_birth, size=DEFAULT_SIZE, font=FONT_SIZE),
                 sg.Text(game.company, size=DEFAULT_SIZE, font=FONT_SIZE),
                 ]
            ]
        # Determine if you need a button
        if self.number > 0:
            previous_page = [sg.Submit(button_text='前の10件', size=PREVIOUS_SIZE, font=FONT_SIZE, key='previous')]

        if self.sum_number > self.number + ONE_COLUMN_LENGTH:
            # Adjust the position by putting in a space
            if self.number == 0:
                previous_page = [sg.Text(' ', size=PREVIOUS_SPACE_SIZE, font=FONT_SIZE)]

            next_page = [sg.Submit(button_text='次の10件', size=PREVIOUS_SIZE, font=FONT_SIZE, key='next')]
            next_number = self.number + ONE_COLUMN_LENGTH

        else:
            next_number = self.sum_number

        layout += [previous_page + next_page,
                   [sg.Button(button_text=self.BUTTON_NAME[0], size=CONFIG_SIZE, font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[1], size=CONFIG_SIZE, font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[2], size=CONFIG_SIZE, font=FONT_SIZE),
                    sg.Button(button_text=self.BUTTON_NAME[3], size=CONFIG_SIZE, font=FONT_SIZE),
                    ],
                   [sg.Text(f'{self.sum_number}件のうち、{self.number}から{next_number}件を表示しています',
                            size=INFO_TXT_SIZE, font=FONT_SIZE),
                    sg.Text('', size=INFO_INPUT_SIZE, font=FONT_SIZE, key='INPUT')],
                   ]

        return sg.Window(TITLE).Layout(layout)
