# Copyright (c) 2026 AnonymousX1025
# Licensed under the MIT License.
# This file is part of AnonXMusic

import math
from pyrogram import enums, types
from anony.core.youtube import time_to_seconds

class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton
        self.styles = {
            "default": enums.ButtonStyle.DEFAULT,
            "primary": enums.ButtonStyle.PRIMARY,
            "success": enums.ButtonStyle.SUCCESS,
            "danger": enums.ButtonStyle.DANGER,
            "status": enums.ButtonStyle.DEFAULT,
            "nav": enums.ButtonStyle.DEFAULT,
            "link": enums.ButtonStyle.DEFAULT,
            "menu": enums.ButtonStyle.PRIMARY,
            "media": enums.ButtonStyle.PRIMARY,
            "play": enums.ButtonStyle.SUCCESS,
            "setting": enums.ButtonStyle.PRIMARY,
            "enabled": enums.ButtonStyle.SUCCESS,
            "disabled": enums.ButtonStyle.DANGER,
        }

    def _button(self, text: str, category: str = "default", **kwargs):
        return self.ikb(
            text=text,
            style=self.styles.get(category, enums.ButtonStyle.DEFAULT),
            **kwargs,
        )

    # --- AAPKE PURANE FUNCTIONS KAA NAYA CONVERTED STYLE ---

    def track_markup(self, _, videoid, user_id, channel, fplay) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self._button(text=_["P_B_1"], category="success", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
                    self._button(text=_["P_B_2"], category="primary", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
                ],
                [
                    self._button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {videoid}|{user_id}")
                ]
            ]
        )

    def stream_markup_timer(self, _, chat_id, played, dur) -> types.InlineKeyboardMarkup:
        played_sec = time_to_seconds(played)
        duration_sec = time_to_seconds(dur)
        percentage = (played_sec / duration_sec) * 100 if duration_sec > 0 else 0
        umm = min(math.floor(percentage / 10), 9)

        # Dynamic progress bar logic (optimized)
        bar_list = ["—"] * 10
        bar_list[umm] = "◉"
        bar = "".join(bar_list)

        return self.ikm(
            [
                [
                    self._button(text=f"{played} {bar} {dur}", category="status", callback_data="GetTimer")
                ],
                [   
                    self._button(text="▷", category="success", callback_data=f"ADMIN Resume|{chat_id}"),
                    self._button(text="II", category="primary", callback_data=f"ADMIN Pause|{chat_id}"),
                    self._button(text="↻", category="default", callback_data=f"ADMIN Replay|{chat_id}"),
                    self._button(text="‣‣I", category="primary", callback_data=f"ADMIN Skip|{chat_id}"),
                    self._button(text="▢", category="danger", callback_data=f"ADMIN Stop|{chat_id}")
                ]
            ]
        )

    def stream_markup(self, _, chat_id) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self._button(text="▷", category="success", callback_data=f"ADMIN Resume|{chat_id}"),
                    self._button(text="II", category="primary", callback_data=f"ADMIN Pause|{chat_id}"),
                    self._button(text="↻", category="default", callback_data=f"ADMIN Replay|{chat_id}"),
                    self._button(text="‣‣I", category="primary", callback_data=f"ADMIN Skip|{chat_id}"),
                    self._button(text="▢", category="danger", callback_data=f"ADMIN Stop|{chat_id}")
                ]
            ]
        )

    def playlist_markup(self, _, videoid, user_id, ptype, channel, fplay) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self._button(text=_["P_B_1"], category="success", callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
                    self._button(text=_["P_B_2"], category="primary", callback_data=f"AnonyPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}")
                ],
                [
                    self._button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {videoid}|{user_id}")
                ]
            ]
        )

    def livestream_markup(self, _, videoid, user_id, mode, channel, fplay) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self._button(text=_["P_B_3"], category="success", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}")
                ],
                [
                    self._button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {videoid}|{user_id}")
                ]
            ]
        )

    def slider_markup(self, _, videoid, user_id, query, query_type, channel, fplay) -> types.InlineKeyboardMarkup:
        query = f"{query[:20]}"
        return self.ikm(
            [
                [
                    self._button(text=_["P_B_1"], category="success", callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
                    self._button(text=_["P_B_2"], category="primary", callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
                ],
                [
                    self._button(text="◁", category="default", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
                    self._button(text=_["CLOSE_BUTTON"], category="danger", callback_data=f"forceclose {query}|{user_id}"),
                    self._button(text="▷", category="default", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}")
                ]
            ]
        )