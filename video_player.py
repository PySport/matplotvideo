from enum import Enum
from typing import Callable

import cv2, numpy as np
import sys
from time import sleep, time

from matplotlib.backend_bases import FigureCanvasBase
from matplotlib.figure import Figure

# https://github.com/maximus009/VideoPlayer/blob/master/new_test_3.py


class FrameChange(Enum):
    NoChange = 0
    Next = 1
    Seek = 2


class CV2VideoPlayer:
    KEY_CODE_STOP = 27
    KEY_CODE_TOGGLE_PLAY = 32
    KEY_CODE_PREV_FRAME = ord('a')
    KEY_CODE_NEXT_FRAME = ord('d')

    CMD_NEXT_FRAME = "next"
    CMD_NOOP = "noop"

    # __cap:
    __frame_count: int
    __fps: int
    __on_frame_callback: Callable
    __on_stop_callback: Callable
    __previous_frame_display_timestamp: float
    __window_name: str = 'VideoPlayer'

    def __init__(self, filename: str, on_frame: Callable, on_stop: Callable):
        self.__cap = cv2.VideoCapture(filename)

        self.__frame_count = int(self.__cap.get(cv2.cv2.CAP_PROP_FRAME_COUNT))
        self.__fps = self.__cap.get(cv2.cv2.CAP_PROP_FPS)

        self.__playback_rate = 1.0

        self.__current_frame = 0
        self.__on_frame_callback = on_frame
        self.__on_stop_callback = on_stop
        self.__previous_frame_display_timestamp = 0

        self.__status = 'play'

        self.__setup_ui()

    def __setup_ui(self):
        def on_change_frame(x):
            self.__current_frame = x
            if self.__status == 'paused':
                self.__status = 'seek_frame'

        def on_change_playback_rate(x):
            if x == 0:
                x = 1
            self.__playback_rate = x / 100.

        cv2.namedWindow(self.__window_name)
        cv2.createTrackbar('Frame', self.__window_name, 0, self.__frame_count - 1, on_change_frame)
        cv2.setTrackbarPos('Frame', self.__window_name, 0)

        cv2.createTrackbar('Playback Speed', self.__window_name, 1, 400, on_change_playback_rate)
        cv2.setTrackbarPos('Playback Speed', self.__window_name, int(self.__playback_rate * 100))

    def __handle_keyboard_input(self):
        key = cv2.waitKey(1)
        if key == self.KEY_CODE_TOGGLE_PLAY:
            if self.__status == 'paused':
                self.__status = 'play'
            else:
                self.__status = 'paused'
        elif key == self.KEY_CODE_PREV_FRAME:
            self.__status = 'prev_frame'
        elif key == self.KEY_CODE_NEXT_FRAME:
            self.__status = 'next_frame'
        elif key == self.KEY_CODE_STOP:
            self.stop()

    def __calculate_current_frame(self) -> FrameChange:
        if self.__status == 'play':
            if self.__current_frame == self.__frame_count:
                self.__status = 'paused'
                return FrameChange.NoChange

            now = time()
            if self.__previous_frame_display_timestamp == 0:
                self.__previous_frame_display_timestamp = now
                return FrameChange.NoChange

            frame_display_time = 1 / self.__fps / self.__playback_rate
            time_delta = now - self.__previous_frame_display_timestamp

            frame_delta = int(time_delta / frame_display_time)

            if frame_delta > 0:
                self.__current_frame += frame_delta
                self.__previous_frame_display_timestamp = now
                if frame_delta > 1:
                    return FrameChange.Seek
                else:
                    return FrameChange.Next
        elif self.__status == 'next_frame':
            if self.__current_frame < self.__frame_count:
                self.__current_frame += 1
                self.__status = 'paused'
                return FrameChange.Next
        elif self.__status == 'prev_frame':
            if self.__current_frame > 0:
                self.__current_frame -= 1
                self.__status = 'paused'
                return FrameChange.Seek
        elif self.__status == 'seek_frame':
            self.__status = 'paused'
            return FrameChange.Seek
        elif self.__status == 'paused':
            self.__previous_frame_display_timestamp = 0

        return FrameChange.NoChange

    def __show_current_frame(self):
        ret, im = self.__cap.read()
        r = 750.0 / im.shape[1]
        dim = (750, int(im.shape[0] * r))
        im = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)
        cv2.imshow(self.__window_name, im)

    def on_timer(self):
        if self.__status == "stopped":
            return

        self.__handle_keyboard_input()
        frame_change = self.__calculate_current_frame()

        if frame_change == FrameChange.NoChange:
            return
        elif frame_change == FrameChange.Next:
            pass  # by default capture reads next frame
        elif frame_change == FrameChange.Seek:
            self.__cap.set(cv2.cv2.CAP_PROP_POS_FRAMES, self.__current_frame)

        self.__show_current_frame()
        cv2.setTrackbarPos('Frame', self.__window_name, self.__current_frame)
        self.__on_frame_callback(self.__current_frame)

    def stop(self):
        del self.__cap
        cv2.destroyWindow(self.__window_name)
        self.__status = "stopped"
        self.__on_stop_callback()


def attach_video_player(figure: Figure, filename: str, on_frame: Callable = None):
    timer = None

    def on_stop():
        timer.stop()

    video_player = CV2VideoPlayer(filename, on_frame, on_stop)

    timer = figure.canvas.new_timer(interval=1,
                                    callbacks=[(video_player.on_timer, [], {})])
    timer.start()
