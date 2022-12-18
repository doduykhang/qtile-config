from ..Group.Group import groups
from ..Constant.Constant import *
from ..Widgets.Widgets import widgets
from libqtile import bar, widget
from libqtile.config import Screen

f_screens = []
for i, group in enumerate(groups):
    f_screens.append(
        Screen(
            top=bar.Bar( 
                [
                    *widgets
                ],
                32,
                opacity=0.95,
                background="1F2122",
            ),
            x=1920*i,
            y=0,
            width=1920,
            height=1080
        ),
    )

my_screen = [
        Screen(
            top=bar.Bar( 
                [
                    *widgets
                ],
                32,
                opacity=0.95,
                background="1F2122",
            ),
            x=1920*2,
            y=0,
            width=1920,
            height=1080
        ),
        Screen(
            top=bar.Bar( 
                [
                    *widgets
                ],
                32,
                opacity=0.95,
                background="1F2122",
            ),
            x=1920*1,
            y=0,
            width=1920,
            height=1080
        ),
]

