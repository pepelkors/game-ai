#!/usr/bin/env python
# ? from https://github.com/kevinhughes27/TensorKart/blob/master/utils.py
# ? kept the xbox controller code

import vgamepad as vg

from inputs import get_gamepad
import math
import threading
import cv2
import numpy as np

import datetime


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.lastStart = datetime.datetime.now()
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(
            target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    # TODO: set this to the shapes that are used in the game~
    def read(self):
        '''
        returns a list of the buttons that are pressed
        returns Y A X B ThumbStickLeft ThumbStickRight ThumbStick
        '''

        noteUp = self.Y  # xbox Y button
        noteDown = self.A  # xbox A button
        noteLeft = self.X  # xbox X button
        noteRight = self.B  # xbox B button
        slideLeft = 1 if self.LeftJoystickX < -0.6 else 0
        slideRight = 1 if self.LeftJoystickX > 0.6 else 0
        heartNote = 1 if (abs(self.LeftJoystickX) + abs(self.LeftJoystickY) +
                          abs(self.RightJoystickX) + abs(self.RightJoystickY)) > 0.6 else 0

        return [noteUp, noteDown, noteLeft, noteRight, slideLeft, slideRight, heartNote]

    def dump(self):
        if self.LeftTrigger == 1 and self.RightTrigger == 1 and self.LeftBumper == 1 and self.RightBumper == 1:
            elapsed = datetime.datetime.now() - self.lastStart
            if (elapsed.total_seconds() > 2):
                self.lastStart = datetime.datetime.now()
                return True
        return False

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / \
                        XboxController.MAX_JOY_VAL  # normalize between -1 and 1

                elif event.code == 'ABS_Z':
                    self.LeftTrigger = 1 if (
                        (event.state / XboxController.MAX_TRIG_VAL) > 0.6) else 0  # 0 or 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = 1 if (
                        (event.state / XboxController.MAX_TRIG_VAL) > 0.6) else 0  # 0 or 1

                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.Y = event.state
                elif event.code == 'BTN_WEST':
                    self.X = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state


def edgeFrame(frame):
    # change size to 960 x 540
    processedImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # for now we are just turning it into greyscale and do some edge detection
    processedImage = cv2.Canny(processedImage, threshold1=200, threshold2=300)

    meanValue = np.mean(frame)
    return processedImage, meanValue


def accuracyFrame(frame):
    accuracyImage = frame[frame.shape[0]-23: frame.shape[0],
                          frame.shape[1]-612:frame.shape[1]-333]
    return accuracyImage


def whitePixelCenter(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)[1]
    frame = cv2.bitwise_and(frame, frame, mask=binary)

    whitePixels = np.where(frame == 255)
    whitePixCenter = np.mean(whitePixels[1])

    # now we need to find how far from the actual center the white pixels are
    # 160 is the x center of the image, so we subtract the white pixel center from 160 and take abs value
    distFromCenter = abs(472 - whitePixCenter)
    return whitePixCenter


def rewardCalculator(averageX, previousX):
    # this calculates if the change is towards the center (472) or away from the center
    # we just need to find how far from the center of the image the white pixels are

    # just find the raw distance from the center for average and previous
    current = abs(averageX - 472)
    previous = abs(previousX - 472)
    change = previous - current
    return change


def scoreFrame(frame):
    # the score is in the top right corner
    scoreImage = frame[20: 45, frame.shape[1]-180: frame.shape[1]-55]
    return scoreImage


class GamePad(object):
    def __init__(self):
        self.state = [0, 0, 0, 0, 0, 0, 0]
        self.vg = vg.VX360Gamepad()
        pass

    def update(self, state):
        self.state = state

        # get the first 4 buttons from the state
        stateButtons = state[0:4]
        buttons = [vg.XUSB_BUTTON.XUSB_GAMEPAD_Y, vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
                   vg.XUSB_BUTTON.XUSB_GAMEPAD_X, vg.XUSB_BUTTON.XUSB_GAMEPAD_B]

        for i, j in zip(buttons, stateButtons):
            self.vg.press_button(i, j)

        # left slide
        if (state[4] == 1):
            self.vg.left_joystick_float(-1)
        else:
            self.vg.left_joystick_float(0)

        # right slide and heart note
        if (state[5] == 1 or state[6] == 1):
            self.vg.right_joystick_float(1)
        else:
            self.vg.right_joystick_float(0)

        # push changes
        self.vg.update()

    def reset(self):
        self.state = [0, 0, 0, 0, 0, 0, 0]

        # get the first 4 buttons from the state
        stateButtons = self.state[0:4]
        buttons = [vg.XUSB_BUTTON.XUSB_GAMEPAD_Y, vg.XUSB_BUTTON.XUSB_GAMEPAD_A,
                   vg.XUSB_BUTTON.XUSB_GAMEPAD_X, vg.XUSB_BUTTON.XUSB_GAMEPAD_B]

        for i, j in zip(buttons, stateButtons):
            self.vg.press_button(i, j)

        self.vg.left_joystick_float(0)
        self.vg.right_joystick_float(0)
        self.vg.update()

    def read(self):
        return self.state
