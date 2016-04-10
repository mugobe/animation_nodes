import bpy
from ... base_types.node import AnimationNode

class an_EdgesOfPolygonsNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_EdgesOfPolygonsNode"
    bl_label = "Edges of Polygons"

    def create(self):
        self.newInput("an_PolygonIndicesListSocket", "Polygons", "polygons")
        self.newOutput("an_EdgeIndicesListSocket", "Edges", "edges")

    def execute(self, polygons):
        edges = []
        for polygon in polygons:
            for i, index in enumerate(polygon):
                startIndex = polygon[i - 1]
                edge = (startIndex, index) if index > startIndex else (index, startIndex)
                edges.append(edge)
        return list(set(edges))
