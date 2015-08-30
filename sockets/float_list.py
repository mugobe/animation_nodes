import bpy
from .. base_types.socket import AnimationNodeSocket

class FloatListSocket(bpy.types.NodeSocket, AnimationNodeSocket):
    bl_idname = "an_FloatListSocket"
    bl_label = "Float List Socket"
    dataType = "Float List"
    allowedInputTypes = ["Float List", "Integer List"]
    drawColor = (0.4, 0.2, 0.9, 1.0)

    def getValue(self):
        return []

    def getValueCode(self):
        return "[]"

    def getCopyStatement(self):
        return "value[:]"
