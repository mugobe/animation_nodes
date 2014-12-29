import bpy, time
from bpy.types import Node
from animation_nodes.mn_node_base import AnimationNode
from animation_nodes.mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling
from animation_nodes.utils.mn_mesh_utils import *
from animation_nodes.mn_cache import *

cacheIdentifier = "Object Mesh Data"

class mn_ObjectMeshInfo(Node, AnimationNode):
	bl_idname = "mn_ObjectMeshInfo"
	bl_label = "Object Mesh Info"
	outputUseParameterName = "useOutput"
	
	usePerObjectCache = bpy.props.BoolProperty(name = "Use Cache", default = False, description = "Warning: Modifications to the data will overwrite the cache.")
	
	def init(self, context):
		forbidCompiling()
		self.inputs.new("mn_ObjectSocket", "Object").showName = False
		self.outputs.new("mn_PolygonListSocket", "Polygons")
		self.outputs.new("mn_VertexListSocket", "Vertices")
		self.outputs.new("mn_MeshDataSocket", "Mesh Data")
		allowCompiling()
		
	def draw_buttons(self, context, layout):
		layout.prop(self, "usePerObjectCache")
		
	def getInputSocketNames(self):
		return {"Object" : "object"}
	def getOutputSocketNames(self):
		return {"Polygons" : "polygons",
				"Vertices" : "vertices",
				"Mesh Data" : "meshData"}
		
	def execute(self, object, useOutput):
		if getattr(object, "type", None) != "MESH": 
			return [], [], MeshData()
		
		cache = self.getInitializedCache()
		
		polygons = []
		vertices = []
		meshData = MeshData()
		
		if useOutput["Polygons"]:		
			polygons = cacheFunctionResult(cache, object.name + "POLYGONS", getPolygonsFromMesh, [object.data], self.usePerObjectCache)
		if useOutput["Vertices"]:
			vertices = cacheFunctionResult(cache, object.name + "VERTICES", getVerticesFromMesh, [object.data], self.usePerObjectCache)
		if useOutput["Mesh Data"]:
			meshData = cacheFunctionResult(cache, object.name + "MESH_DATA", getMeshDataFromMesh, [object.data], self.usePerObjectCache)
			
		return polygons, vertices, meshData
		
	def getInitializedCache(self):
		cache = getLongTimeCache(cacheIdentifier)
		if cache is None:
			cache = {}
			setLongTimeCache(cacheIdentifier, cache)
		return cache
		
		
def getPolygonsFromMesh(mesh):
	polygons = []
	for polygon in mesh.polygons:
		vertices = []
		for vertex_index in polygon.vertices:
			vertices.append(Vertex.fromMeshVertex(mesh.vertices[vertex_index]))
		polygons.append(Polygon(vertices, polygon.area, polygon.center.copy(), polygon.normal.copy(), polygon.material_index))
	return polygons
	
	
def getVerticesFromMesh(mesh):
	vertices = []
	for vertex in mesh.vertices:
		vertices.append(Vertex.fromMeshVertex(vertex))
	return vertices
	
	
def getMeshDataFromMesh(mesh):
	vertices = getVertexLocationsFromMesh(mesh)
	edges = getEdgesIndicesFromMesh(mesh)
	polygons = getPolygonsIndicesFromMesh(mesh)
	return MeshData(vertices, edges, polygons)	
	
def getVertexLocationsFromMesh(mesh):
	return [vertex.co.copy() for vertex in mesh.vertices]
	
def getEdgesIndicesFromMesh(mesh):
	edgesIndices = []
	for edge in mesh.edges:
		edgesIndices.append((edge.vertices[0], edge.vertices[1]))
	return edgesIndices
	
def getPolygonsIndicesFromMesh(mesh):
	polygonsIndices = []
	for polygon in mesh.polygons:
		polygonsIndices.append(polygon.vertices[:])
	return polygonsIndices	


