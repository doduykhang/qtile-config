from libqtile import widget
from ..Constant.Constant import *

from subprocess import CompletedProcess, run
from libqtile.widget import base

class Music(base.ThreadPoolText):
    """
    A widget to interact with spotify via dbus.
    """

    defaults = [
        ("play_icon", "", "icon to display when playing music"),
        ("pause_icon", "", "icon to display when music paused"),
        ("update_interval", 0.5, "polling rate in seconds"),
        ("format", "{track}", "Spotify display format"),
    ]

    def __init__(self, **config) -> None:
        base.ThreadPoolText.__init__(self, text="", **config)
        self.add_defaults(Music.defaults)
        self.add_callbacks(
            {
                "Button1": self.toggle_music,
            }
        )

    def _is_proc_running(self, proc_name: str) -> bool:
        # create regex pattern to search for to avoid similar named processes
        pattern = proc_name + "$"

        # pgrep will return a string of pids for matching processes
        proc_out = run(["pgrep", "-fli", pattern], capture_output=True).stdout.decode(
            "utf-8"
        )

        # empty string means nothing started
        is_running = proc_out != ""

        return is_running

    def poll(self) -> str:
        """Poll content for the text box"""
        vars = {}
        if self.playing:
            vars["icon"] = self.play_icon
        else:
            vars["icon"] = self.pause_icon

        vars["artist"] = ""
        vars["track"] = self.song_title

        return self.format.format(**vars)

    def toggle_music(self) -> None:
        run(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause",
            shell=True,
        )

    def get_proc_output(self, proc: CompletedProcess) -> str:
        if proc.stderr.decode("utf-8") != "":
            return (
                ""
                if "org.mpris.MediaPlayer2.chrome" in proc.stderr.decode("utf-8")
                else proc.stderr.decode("utf-8")
            )

        output = proc.stdout.decode("utf-8").rstrip()
        return output

    @property
    def _meta(self) -> str:
        proc = run(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata'",
            shell=True,
            capture_output=True,
        )

        output: str = proc.stdout.decode("utf-8").replace("'", "ʼ").rstrip()
        return "" if ("org.mpris.MediaPlayer2.chrome" in output) else output

    @property
    def artist(self) -> str:
        proc: CompletedProcess = run(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'Metadata' | grep -m1 'xesam:artist' -b2 | tail -n 1 | grep -o '\".*\"' | sed 's/\"//g' | sed -e 's/&/and/g'",
            shell=True,
            capture_output=True,
        )

        output = self.get_proc_output(proc)
        return output

    @property
    def url(self) -> str:
        proc = run(
            f"echo '{self._meta}' | grep -m1 'mpris:artUrl' -b1 | tail -n1 | grep -o '\".*\"' | sed 's/\"//g' | sed -e 's/&/and/g'",
            shell=True,
            capture_output=True,
        )

        output: str = self.get_proc_output(proc)
        return output

    @property
    def song_title(self) -> str:
        proc: CompletedProcess = run(
            f"echo '{self._meta}' | grep -m1 'xesam:title' -b1 | tail -n1 | grep -o '\".*\"' | sed 's/\"//g' | sed -e 's/&/and/g'",
            shell=True,
            capture_output=True,
        )

        output = self.get_proc_output(proc)
        return output

    @property
    def album(self) -> str:
        proc = run(
            f"echo '{self._meta}' | grep -m1 'xesam:album' -b1 | tail -n1 | grep -o '\".*\"' | sed 's/\"//g' | sed -e 's/&/and/g'",
            shell=True,
            capture_output=True,
        )

        output: str = self.get_proc_output(proc)
        return output

    @property
    def playing(self) -> bool:
        play = run(
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.chrome /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Get string:'org.mpris.MediaPlayer2.Player' string:'PlaybackStatus' | grep -o Playing",
            shell=True,
            capture_output=True,
        ).stdout.decode("utf-8")

        is_running = play != ""
        return is_running

widgets = [
    widget.GroupBox(
        fontsize=fontSize,
        margin_y=3,
        margin_x=6,
        padding_y=6,
        padding_x=6,
        borderwidth=4,
        active=highlightColor,
        # does not have window open text color
        inactive="aaaaaa",
        rounded=True,
        highlight_color="1F2122",
        highlight_method="line",
        this_current_screen_border=highlightColor,
        other_current_screen_border="1F2122",
        other_screen_border="1F2122"
    ),

    widget.Spacer(),
    widget.TextBox(text=" ", foreground=[
                   "#FF679A", "#FFCDAC"], fontsize="16"),
    Music(
        fontsize=fontSize,
        foreground=["#FF679A", "#FFCDAC"]
    ),
    widget.Spacer(),
    widget.Spacer(length=20),
    widget.TextBox(text="墳 ", foreground=[
        "#00BBDC", "#99CDFF"], fontsize="16"),
    widget.PulseVolume(
        fontsize=fontSize,
        foreground=["#00BBDC", "#99CDFF"]
    ),
    widget.Spacer(length=20),
    widget.TextBox(text="", foreground=["#FF7721", "#FFA9CC"], fontsize="16"),
    widget.Memory(
        fontsize=fontSize,
        measure_mem="G",
        foreground=["#FF7721", "#FFA9CC"]
    ),
    widget.Spacer(length=20),
    widget.TextBox(text=" ", foreground=[
        "#0077DD", "#9AEEDE"], fontsize="16"),
    widget.Clock(
        format="%d/%m/%y %H:%M",
        foreground=["#0077DD", "#9AEEDE"]
    ),
    widget.TextBox(text=" ", foreground=[
        "#0077DD", "#9AEEDE"], fontsize="16"),
]
