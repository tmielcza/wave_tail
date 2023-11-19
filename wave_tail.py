import maya.cmds as cmds
import math

def start():
    WaveTail()

class WaveTail:

    def __init__(self):
        self.win = cmds.window(title="Wave Tail", widthHeight=(500,200))
        self.frequency = 5.
        self.strength = 5.
        self.offset = 5.
        self.base_offset = 0.
        cmds.columnLayout()
        cmds.floatSliderGrp(label="Frequency",field=True,minValue=0.0,maxValue=10.0,value=5., dragCommand = lambda _ : (self.set_frequency(_), self.rotate()))
        cmds.floatSliderGrp(label="Strength",field=True,minValue=0.0,maxValue=10.0,value=5., dragCommand=lambda _ : (self.set_strength(_), self.rotate()))
        cmds.floatSliderGrp(label="Offset",field=True,minValue=0.0,maxValue=10.0,value=5., dragCommand=lambda _ : (self.set_offset(_), self.rotate()))
        cmds.floatSliderGrp(label="Base Offset",field=True,minValue=-2.,maxValue=2.,value=0., dragCommand=lambda _ : (self.set_base_offset(_), self.rotate()))
        cmds.showWindow(self.win)

    def set_offset(self, offset): self.offset = offset

    def set_frequency(self, freq): self.frequency = freq

    def set_strength(self, str): self.strength = str

    def set_base_offset(self, offset): self.base_offset = offset

    def rotate(self):
        selected_objs = cmds.ls(sl=True, long=True)
        l = len(selected_objs)

        first, tail = selected_objs[0], selected_objs[1:]
        r = self.base_offset * self.strength * 10.
        cmds.rotate(0, r, 0, first)

        for i, obj in enumerate(tail):
            r = math.sin((i + 1) / l * self.frequency + self.offset * 1) * self.strength * 5.
            print ("test" + str(i / l) + "| r = " + str(r))
            cmds.rotate(0, r, 0, obj)

WaveTail()
