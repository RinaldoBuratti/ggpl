from pyplasm import *
from larlib import *
import math

def createStep(stepDimension):
	'''
	creates a step

	Args:
	:param stepDimension: dimension of a step

	Returns:
	3D value of type HPC representing a step
	'''
	(sx, sy, sz) = stepDimension
	step = CUBOID([sx, sy, sz])
	step = COLOR([0.61, 0.43, 0.31])(step)
	step = STRUCT([T(3)(sz), step])
	return step

def createPlatform(stepDimension):
	'''
	creates a platform

	Args:
	:param stepDimension: dimension of a step

	Returns:
	3D value of type HPC representing a platform
	'''
	(sx, sy, sz) = stepDimension
	platform = CUBOID([sx, sx, sz])
	platform = COLOR([0.61, 0.43, 0.31])(platform)
	platform = T(3)(sz)(platform)
	platform = STRUCT([platform])
	return platform

def createStair(dimension, stepDimension):
	'''
	creates a floating stair

	Args:
	:param dimension: dimension of a cube respect of the x, y and z axis
	:param stepDimension: dimension of a step

	Returns:
	3D value of type HPC representing a floating stair
	'''
	(sx, sy, sz) = stepDimension
	(x, y, z) = dimension

	step = createStep(stepDimension)
	stairX = []

	height = sz
	width = sy
	dStepZ = sz*2.0
	dStepY = (4.0/5.0)*sy

	for i in range(0, int(y)):
		if(height < z - (sz*2.0)):
			height = height + dStepZ
			width = width + dStepY
			stairX.extend([step, T(2)(dStepY), T(3)(dStepZ)])

	platformX = createPlatform(stepDimension)
	stairX.extend([platformX])
	width = width + sx -sy

	stairY = []
	if(height < z):
		for i in range(0, int(x-(sx*2.0))):
			if(height < z - (sz*4.0)):
				height = height + dStepZ
				stairY.extend([step, T(2)(dStepY), T(3)(dStepZ)])

	platformY = createPlatform(stepDimension)
	stairY.extend([platformY])

	stairY = STRUCT(stairY)
	stairY = R([1, 2])(-PI/2.0)(stairY)
	stairY = T(1)(sx)(stairY)
	stairY = T(2)(sx)(stairY)
	stairY = T(3)(sz*2.0)(stairY)
	
	stairX.extend([stairY])

	floatingStair = STRUCT(stairX)

	return floatingStair


def ggpl_floatingStair(dimension, stepDimension):
	'''
	creates a floating stair

	Args:
	:param dimension: dimension of a cube respect of the x, y and z axis
	:param stepDimension: dimension of a step

	Returns:
	3D value of type HPC representing a floating stair
	'''
	floatingStair = createStair(dimension, stepDimension)
	return floatingStair

if __name__ == '__main__':
	dimension = (15, 25, 30)
	stepDimension = (3, 0.8, 0.3)
	floatingStair = ggpl_floatingStair(dimension, stepDimension)
	VIEW(floatingStair)