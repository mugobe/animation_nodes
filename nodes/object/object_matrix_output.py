import bpy
from bpy.props import *
from ... events import executionCodeChanged
from ... base_types.node import AnimationNode

outputItems = [	("BASIS", "Basis", ""),
                ("LOCAL", "Local", ""),
                ("PARENT INVERSE", "Parent Inverse", ""),
                ("WORLD", "World", "") ]

class ObjectMatrixOutputNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_ObjectMatrixOutputNode"
    bl_label = "Object Matrix Output"

    outputType = EnumProperty(items = outputItems, update = executionCodeChanged, default = "WORLD")

    def create(self):
        self.inputs.new("an_ObjectSocket", "Object", "object").showName = False
        self.inputs.new("an_MatrixSocket", "Matrix", "matrix")
        self.outputs.new("an_ObjectSocket", "Object", "outObject")

    def draw(self, layout):
        layout.prop(self, "outputType", text = "Type")

    def getExecutionCode(self):
        t = self.outputType
        lines = []
        lines.append("if object is not None:")
        if t == "BASIS": lines.append("    object.matrix_basis = matrix")
        if t == "LOCAL": lines.append("    object.matrix_local = matrix")
        if t == "PARENT INVERSE": lines.append("    object.matrix_parent_inverse = matrix")
        if t == "WORLD": lines.append("    object.matrix_world = matrix")
        lines.append("outObject = object")
        return lines
