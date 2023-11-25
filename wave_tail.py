import maya.cmds as cmds
import math

MIN_OFFSET = -math.pi
MAX_OFFSET = math.pi

def start():
    WaveTail()

class WaveTail:

    def __init__(self):
        self.win = cmds.window(title="Wave Tail", widthHeight=(500,200))
        self.frequency = 5.
        self.strength = 5.
        self.offset = 5.
        self.base_offset = 0.

        self.rotate_f = lambda a, obj : cmds.rotate(a, 0, 0, obj)

        cmds.columnLayout()
        self.frequency_slider_id = cmds.floatSliderGrp(label="Frequency", field=True, minValue=-0., maxValue=10., value=0., dragCommand=lambda _ : (self.set_frequency(_), self.rotate()), changeCommand=lambda _ : (self.set_frequency(_), self.rotate()))
        self.strength_slider_id = cmds.floatSliderGrp(label="Strength", field=True, minValue=0., maxValue=10., value=5., dragCommand=lambda _ : (self.set_strength(_), self.rotate()), changeCommand=lambda _ : (self.set_strength(_), self.rotate()))
        self.offset_slider_id = cmds.floatSliderGrp(label="Offset", field=True, minValue=MIN_OFFSET, maxValue=MAX_OFFSET, value=MAX_OFFSET / 2., dragCommand=lambda _ : (self.set_offset(_), self.rotate()), changeCommand=lambda _ : (self.set_offset(_), self.rotate()))
        self.base_offset_slider_id = cmds.floatSliderGrp(label="Base Offset", field=True, minValue=-2., maxValue=2., value=0., dragCommand=lambda _ : (self.set_base_offset(_), self.rotate()), changeCommand=lambda _ : (self.set_base_offset(_), self.rotate()))
        self.axis_buttons_id = cmds.radioButtonGrp(labelArray3=["X", "Y", "Z"], numberOfRadioButtons=3, sl=1,
                                                   onCommand1=lambda _ : (self.set_rotate_function(lambda a, obj : cmds.rotate(a, 0, 0, obj)), self.rotate()),
                                                   onCommand2=lambda _ : (self.set_rotate_function(lambda a, obj : cmds.rotate(0, a, 0, obj)), self.rotate()),
                                                   onCommand3=lambda _ : (self.set_rotate_function(lambda a, obj : cmds.rotate(0, 0, a, obj)), self.rotate()))
        self.sort_button_id = cmds.button("Sort Controllers", align="center", command=lambda _ : self.sort_controllers())
        self.mirror_button_id = cmds.button("Mirror", align="center", command=lambda _ : (self.mirror_axis(), self.rotate()))

        cmds.showWindow(self.win)

    def set_rotate_function(self, f): self.rotate_f = f

    def set_offset(self, offset): self.offset = offset

    def set_frequency(self, freq): self.frequency = freq

    def set_strength(self, str): self.strength = str

    def set_base_offset(self, offset): self.base_offset = offset

    def rotate(self):
        selected_objs = cmds.ls(sl=True, long=True)
        l = len(selected_objs)

        first, tail = selected_objs[0], selected_objs[1:]
        r = self.base_offset * self.strength * 10.
        self.rotate_f(r, first)

        for i, obj in enumerate(tail):
            r = math.sin((i + 1) / l * self.frequency + self.offset * 1) * self.strength * 5.
            self.rotate_f(r, obj)

    def sort_controllers(self):
        selected_objs = cmds.ls(sl=True, long=True)
        objs_children = {}
        for o in selected_objs:
            objs_children[o] = cmds.listRelatives(cmds.listRelatives(o, p=True)[0], ad=True)
        selected_objs.sort(key=lambda a : len(objs_children[a]), reverse=True)
        cmds.select(clear=True)
        cmds.select(selected_objs)

    def mirror_axis(self):
        new_offset = (self.offset + math.pi - MIN_OFFSET) % (MAX_OFFSET - MIN_OFFSET) + MIN_OFFSET
        cmds.floatSliderGrp(self.offset_slider_id, edit=True, value=new_offset)
        self.offset = new_offset
        new_base_offset = -self.base_offset
        cmds.floatSliderGrp(self.base_offset_slider_id, edit=True, value=new_base_offset)
        self.base_offset = new_base_offset

WaveTail()
