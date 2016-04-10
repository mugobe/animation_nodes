import bpy
from .... base_types.node import AnimationNode

class LineMeshNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_LineMeshNode"
    bl_label = "Line Mesh"

    def create(self):
        self.newInput("an_VectorSocket", "Start", "start")
        self.newInput("an_VectorSocket", "End", "end").value = (0, 0, 10)
        socket = self.newInput("an_IntegerSocket", "Steps", "steps")
        socket.value = 2
        socket.minValue = 2
        self.newOutput("an_VectorListSocket", "Vertices", "vertices")
        self.newOutput("an_EdgeIndicesListSocket", "Edge Indices", "edgeIndices")

    def execute(self, start, end, steps):
        steps = max(steps, 2)
        divisor = steps - 1
        vertices = [start * (1 - i / divisor) + end * i / divisor for i in range(steps)]
        edges = [(i, i + 1) for i in range(steps - 1)]
        return vertices, edges
