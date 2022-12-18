from libqtile import bar, widget

from libqtile.config import Screen

colors = ["#FF7721", "#FF679A", "#00BBDC", "#0077DD"]
bgColor = "#EE1166"
textColor = "#575279"
# have window open text color
activeColor = "#ffffff"
# does not have window open text color
inactiveColor = "#b3b1b1"
# border/line color
highlightColor = colors[1]
highlightTextColor = "#ffffff"
fontSize = 16

def wrapWidget(widgets, bgColor, icon=""):
    return [
        widget.TextBox(text="", foreground=bgColor, padding=0, fontsize="30"),
        widget.TextBox(
            text=icon,
            background=bgColor,
        ),
        *widgets,
        widget.TextBox(text=" ", foreground=bgColor,
                       padding=0, fontsize="30"),
    ]


def wrapWidget2(widgets, bgColor, fgColor, icon=""):
    return [
        widget.TextBox(
            text=" ", foreground=fgColor, background=bgColor, padding=0, fontsize="30"
        ),
        widget.TextBox(
            text=icon,
            background=fgColor,
        ),
        *widgets,
    ]


screensold = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    fontsize=fontSize,
                    margin_y=3,
                    margin_x=6,
                    padding_y=7,
                    padding_x=6,
                    borderwidth=4,
                    active=activeColor,
                    # does not have window open text color
                    inactive=inactiveColor,
                    rounded=False,
                    highlight_color=inactiveColor,
                    highlight_method="block",
                    this_current_screen_border=highlightColor,
                    block_highlight_text_color=highlightTextColor,
                ),
                widget.Spacer(),
                *(
                    wrapWidget2(
                        [
                            widget.PulseVolume(
                                fontsize=fontSize,
                                background=colors[2],
                            ),
                        ],
                        colors[1],
                        colors[2],
                        "墳",
                    )
                ),
                *(
                    wrapWidget2(
                        [
                            widget.Memory(
                                fontsize=fontSize,
                                background=colors[3],
                            ),
                        ],
                        colors[2],
                        colors[3],
                        "",
                    )
                ),
                *(
                    wrapWidget2(
                        [
                            widget.Clock(
                                format="%d/%m/%y %H:%M",
                                background=colors[0],
                            ),
                        ],
                        colors[3],
                        colors[0],
                        " ",
                    )
                ),
            ],
            32,
            opacity=0.95,
            background=bgColor,
            # margin=[8,2,0,2]
        ),
    ),
]
