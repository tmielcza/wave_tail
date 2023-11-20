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

        self.rotate_f = lambda a, obj : cmds.rotate(a, 0, 0, obj)

        cmds.columnLayout()
        cmds.floatSliderGrp(label="Frequency", field=True, minValue=0.0, maxValue=10.0, value=5., dragCommand=lambda _ : (self.set_frequency(_), self.rotate()))
        cmds.floatSliderGrp(label="Strength", field=True, minValue=0.0, maxValue=10.0, value=5., dragCommand=lambda _ : (self.set_strength(_), self.rotate()))
        cmds.floatSliderGrp(label="Offset", field=True, minValue=0.0, maxValue=10.0, value=5., dragCommand=lambda _ : (self.set_offset(_), self.rotate()))
        cmds.floatSliderGrp(label="Base Offset", field=True, minValue=-2., maxValue=2., value=0., dragCommand=lambda _ : (self.set_base_offset(_), self.rotate()))
        cmds.radioButtonGrp(labelArray3=['x', 'y', 'z'], numberOfRadioButtons=3, sl=1,
                            onCommand1=lambda _ : self.set_rotate_function(lambda a, obj : cmds.rotate(a, 0, 0, obj)),
                            onCommand2=lambda _ : self.set_rotate_function(lambda a, obj : cmds.rotate(0, a, 0, obj)),
                            onCommand3=lambda _ : self.set_rotate_function(lambda a, obj : cmds.rotate(0, 0, a, obj))),
        cmds.button("Sort Controllers", align="center", command=lambda _ : self.sort_controllers())

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
        new_order = []
        for o in selected_objs:
            objs_children[o] = cmds.listRelatives(cmds.listRelatives(o, p=True)[0], f=True, ad=True)
        for o in selected_objs:
            i = 0
            for n in new_order:
                if o not in objs_children[n]:
                    break
                i += 1
            new_order.insert(i, o)
        cmds.select(clear=True)
        cmds.select(new_order)

WaveTail()
