#!/usr/bin/env python
#? from https://github.com/kevinhughes27/TensorKart/blob/master/utils.py
#? kept the xbox controller code

from inputs import get_gamepad
import math
import threading


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
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

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    #TODO: set this to the shapes that are used in the game~
    def read(self):
        noteUp = self.Y #xbox Y button
        noteDown = self.A #xbox A button
        noteLeft = self.X # xbox X button
        noteRight = self.B #xbox B button
        slideLeft = 1 if self.LeftJoystickX < -0.6 else 0
        slideRight = 1 if self.LeftJoystickX > 0.6 else 0
        heartNote = 1 if (abs(self.LeftJoystickX) + abs(self.LeftJoystickY) + abs(self.RightJoystickX) + abs(self.RightJoystickY)) > 0.6 else 0

        return [noteUp, noteDown, noteLeft, noteRight, slideLeft, slideRight, heartNote]

    def dump(self):
        if self.LeftJoystickY == 0 and self.LeftJoystickX == 0:
            pass
        return False

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                    
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = 1 if ((event.state / XboxController.MAX_TRIG_VAL)>0.6) else 0 # 0 or 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = 1 if ((event.state / XboxController.MAX_TRIG_VAL)>0.6) else 0 # 0 or 1
                    
                    
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
