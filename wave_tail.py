import maya.cmds as cmds
import math

MIN_OFFSET = -math.pi
MAX_OFFSET = math.pi


def start():
    WaveTail()


class UiArray:
    def __init__(self, elem_class, ui_root):
        self.elem = elem_class
        self.root = ui_root
        self.elems = {}

    def new_element(self, name, *arg, **kwargs):
        if name not in self.elems:
            cmds.setParent(self.root)
            new_elem = self.elem(name, self.delete_element, *arg, **kwargs)
            self.elems[name] = new_elem

    def delete_element(self, name):
        del self.elems[name]


class ParamsButton:
    def __init__(self, name, close_callback):
        self.name = name
        self.id = cmds.button(name, command=lambda _ : self.delete())
        self.close_callback = close_callback

    def delete(self):
        cmds.deleteUI(self.id)
        self.close_callback(self.name)


class WaveTail:

    def __init__(self):
        self.win = cmds.window(title="Wave Tail", widthHeight=(500, 170), sizeable=False)
        self.frequency = 5.
        self.strength = 5.
        self.offset = 5.
        self.base_offset = 0.

        self.rotate_f = lambda a, obj : cmds.rotate(a, 0, 0, obj)

        layout = cmds.paneLayout(configuration='vertical2')
        # Left column
        cmds.columnLayout()
        self.frequency_slider_id = cmds.floatSliderGrp(label="Frequency", cw=[1, 60], field=True, minValue=-0., maxValue=10., value=0., dragCommand=lambda _ : (self.set_frequency(_), self.update_selection()), changeCommand=lambda _ : (self.set_frequency(_), self.update_selection()))
        self.strength_slider_id = cmds.floatSliderGrp(label="Strength", cw=[1, 60], field=True, minValue=0., maxValue=10., value=5., dragCommand=lambda _ : (self.set_strength(_), self.update_selection()), changeCommand=lambda _ : (self.set_strength(_), self.update_selection()))
        self.offset_slider_id = cmds.floatSliderGrp(label="Offset", cw=[1, 60], field=True, minValue=MIN_OFFSET, maxValue=MAX_OFFSET, value=MAX_OFFSET / 2., dragCommand=lambda _ : (self.set_offset(_), self.update_selection()), changeCommand=lambda _ : (self.set_offset(_), self.update_selection()))
        self.base_offset_slider_id = cmds.floatSliderGrp(label="Base Offset", cw=[1, 60], field=True, minValue=-2., maxValue=2., value=0., dragCommand=lambda _ : (self.set_base_offset(_), self.update_selection()), changeCommand=lambda _ : (self.set_base_offset(_), self.update_selection()))
        self.axis_buttons_id = cmds.radioButtonGrp(labelArray3=["X", "Y", "Z"], numberOfRadioButtons=3, sl=1,
                                                   onCommand1=lambda _ : (self.set_rotate_function(lambda a, obj : cmds.rotate(a, 0, 0, obj)), self.update_selection()),
                                                   onCommand2=lambda _ : (self.set_rotate_function(lambda a, obj : cmds.rotate(0, a, 0, obj)), self.update_selection()),
                                                   onCommand3=lambda _ : (self.set_rotate_function(lambda a, obj : cmds.rotate(0, 0, a, obj)), self.update_selection()))
        self.sort_button_id = cmds.button("Sort Controllers", align="center", command=lambda _ : self.sort_controllers())
        self.mirror_button_id = cmds.button("Mirror", align="center", command=lambda _ : (self.mirror_axis(), self.update_selection()))

        # Right column
        cmds.setParent(layout)
        ccl = cmds.columnLayout(adjustableColumn=1)
        cmds.rowLayout(nc=3)
        self.new_button_id = cmds.button("NEW")
        text = cmds.textField(width=100)

        cmds.setParent(ccl)
        cmds.frameLayout(borderVisible=1, labelVisible=0, h=130)
        scroll = cmds.scrollLayout(cr=1)
        params_root = cmds.columnLayout()
        saved_params = UiArray(ParamsButton, params_root)

        cmds.button(self.new_button_id, e=1, command=(lambda _ : saved_params.new_element(cmds.textField(text, text=1, q=1))))

        cmds.showWindow(self.win)

    def set_rotate_function(self, f): self.rotate_f = f

    def set_offset(self, offset): self.offset = offset

    def set_frequency(self, freq): self.frequency = freq

    def set_strength(self, str): self.strength = str

    def set_base_offset(self, offset): self.base_offset = offset

    def update_selection(self):
        """
        Rotates every selected object according to UI options, drawing a shape from the FK chain
        """

        selected_objs = cmds.ls(sl=True, long=True)

        if not selected_objs:
            return

        l = len(selected_objs)

        first, tail = selected_objs[0], selected_objs[1:]
        r = self.base_offset * self.strength * 10.
        self.rotate_f(r, first)

        for i, obj in enumerate(tail):
            r = math.sin((i + 1) / l * self.frequency + self.offset * 1) * self.strength * 5.
            self.rotate_f(r, obj)

    def sort_controllers(self):
        """
        Sorts selected Maya objects from top hierarchy to bottom
        """

        selected_objs = cmds.ls(sl=True, long=True)

        if not selected_objs:
            return

        objs_children = {}
        for o in selected_objs:
            objs_children[o] = cmds.listRelatives(cmds.listRelatives(o, p=True)[0], ad=True)
        selected_objs.sort(key=lambda a : len(objs_children[a]), reverse=True)
        cmds.select(clear=True)
        cmds.select(selected_objs)

    def mirror_axis(self):
        """
        Mirrors the FK tail shape
        """

        new_offset = (self.offset + math.pi - MIN_OFFSET) % (MAX_OFFSET - MIN_OFFSET) + MIN_OFFSET
        cmds.floatSliderGrp(self.offset_slider_id, edit=True, value=new_offset)
        self.offset = new_offset
        new_base_offset = -self.base_offset
        cmds.floatSliderGrp(self.base_offset_slider_id, edit=True, value=new_base_offset)
        self.base_offset = new_base_offset


WaveTail()
