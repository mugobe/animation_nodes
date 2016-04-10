import bpy
from ... base_types.node import AnimationNode

class FloatToStringNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_FloatToStringNode"
    bl_label = "Float to Text"

    def create(self):
        self.newInput("an_FloatSocket", "Number", "number")
        socket = self.newInput("an_IntegerSocket", "Min Length", "minLength")
        socket.value = 10
        socket.minValue = 0
        socket = self.newInput("an_IntegerSocket", "Decimals", "decimals")
        socket.value = 3
        socket.minValue = 0
        self.newInput("an_BooleanSocket", "Insert Sign", "insertSign").value = False
        self.newOutput("an_StringSocket", "Text", "text")

    def execute(self, number, minLength, decimals, insertSign):
        sign = "+" if insertSign else ""

        formatString = "{" + ":{}0{}.{}f".format(sign, max(minLength, 0), max(decimals, 0)) + "}"
        return formatString.format(number)
