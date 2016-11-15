from pyplasm import *
from larlib import *

def createLegs(dimension):
	'''
	creates legs of the desk

	Args:
	:param dimension: dimension of the cube that contains the desk

	Returns:
	3D value of type HPC representing the legs of a desk
	'''
	(dx, dy, dz) = dimension
	legs = []
	leg = CYLINDER([0.04, dz])(1000)
	leg = COLOR(GRAY)(leg)
	leg = T(1)(0.06)(leg)
	leg = T(2)(0.06)(leg)
	legs.extend([leg])
	leg2 = T(1)(dx-0.1)(leg)
	legs.extend([leg2])
	leg3 = T(2)(dy-0.13)(leg)
	legs.extend([leg3])
	leg4 = T(1)(dx-0.1)(leg)
	leg4 = T(2)(dy-0.13)(leg4)
	legs.extend([leg4])

	legs = STRUCT(legs)
	return legs


def createBaseStructure(dimension):
	'''
	creates the structure under the table of the desk

	Args:
	:param dimension: dimension of the cube that contains the desk

	Returns:
	3D value of type HPC representing the structure under the table of a desk
	'''
	(dx, dy, dz) = dimension
	baseStructure = []
	baseX1 = CUBOID([dx-0.09, 0.05, 0.05])
	baseX1 = COLOR(GRAY)(baseX1)
	baseX2 = CUBOID([dx-0.09, 0.05, 0.05])
	baseX2 = COLOR(GRAY)(baseX2)
	baseY1 = CUBOID([0.05, dy-0.09, 0.05])
	baseY1 = COLOR(GRAY)(baseY1)
	baseY2 = CUBOID([0.05, dy-0.09, 0.05])
	baseY2 = COLOR(GRAY)(baseY2)

	baseX1 = T(1)(0.04)(baseX1)
	baseX1 = T(2)(0.04)(baseX1)
	baseX1 = T(3)(dz-0.05)(baseX1)
	baseX2 = T(1)(0.04)(baseX2)
	baseX2 = T(2)(dy-0.1)(baseX2)
	baseX2 = T(3)(dz-0.05)(baseX2)
	baseY1 = T(1)(0.04)(baseY1)
	baseY1 = T(2)(0.04)(baseY1)
	baseY1 = T(3)(dz-0.05)(baseY1)
	baseY2 = T(1)(dx-0.08)(baseY2)
	baseY2 = T(2)(0.04)(baseY2)
	baseY2 = T(3)(dz-0.05)(baseY2)

	baseStructure.extend([baseX1])
	baseStructure.extend([baseX2])
	baseStructure.extend([baseY1])
	baseStructure.extend([baseY2])

	baseStructure = STRUCT(baseStructure)
	return baseStructure

def createTable(dimension):	
	'''
	creates the table of the desk

	Args:
	:param dimension: dimension of the cube that contains the desk

	Returns:
	3D value of type HPC representing the table of a desk
	'''
	(dx, dy, dz) = dimension
	table = CUBOID([dx, dy, 0.025])
	table = COLOR(GREEN)(table)
	table = T(3)(dz)(table)
	return table
def ggpl_desk(dimension):
	'''
	creates a desk

	Args:
	:param dimension: dimension of the cube that contains the desk

	Returns:
	3D value of type HPC representing a desk
	'''
	(dx, dy, dz) = dimension
	legs = createLegs(dimension)
	baseStructure = createBaseStructure(dimension)
	table = createTable(dimension)
	desk = STRUCT([legs, baseStructure, table])
	return desk

if __name__ == "__main__":
	dimension = (0.8, 1.25, 1.3)
	desk = ggpl_desk(dimension)
	VIEW(desk)
