from pyplasm import *
from larlib import *

def createStructure(vertex, cells):
	"""
	creates roof
	Args:
	:param vertex: set of vertices 
	:param cells: set of cells

	Returns:
	3D value of type HPC representing the bone structure of the roof
	"""
	structure = MKPOL([vertex, cells, None])
	structure = SKELETON(1)(structure)
	structure = OFFSET([0.2, 0.2, 0.2])(structure)
	return structure

def createFaces(vertex, cells):
	"""
	creates faces of the roof
	Args:
	:param vertex: set of vertices 
	:param cells: set of cells

	Returns:
	3D value of type HPC representing the faces of the roof
	"""
	faces = MKPOL([vertex, cells, None])
	faces = OFFSET([1.0, 1.0, 1.0])(faces)
	faces = COLOR(BROWN)(faces)
	return faces

def ggpl_buildRoof(vertex, cells) :
	"""
	creates roof
	Args:
	:param vertex: set of vertices 
	:param cells: set of cells

	Returns:
	3D value of type HPC representing the roof
	"""
	structure = createStructure(vertex, cells)
	faces = createFaces(vertex, cells)
	roof = STRUCT([faces, T(3)(-0.2), structure])
	return roof

if __name__ == '__main__':
	vertex = [(0.0, 0.0, 0.0), (16.0, 0.0, 0.0), (13.0, 12.5, 6.0), (3.0, 12.5, 6.0), (16.0, 25.0, 0.0), (0.0, 25.0, 0.0)]
	cells = [[1, 2, 3, 4], [1, 4, 6], [2, 3, 5], [3, 4, 5, 6]]
	result = ggpl_buildRoof(vertex, cells)
	VIEW(result)	