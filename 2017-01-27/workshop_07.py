from pyplasm import *
from larlib import *

def createWindow(Xarray, Yarray, Zarray, boolArray, Xglass, Zglass):
	"""
	Args:
	:param Xarray: a list of distances on x axis
	:param Yarray: a list of distances on y axis
	:param Zarray: a list of distances on z axis
	:param boolArray: a three dimensional matrix of occupancy
	:param Xglass: x coordinate of the glass on the window
	:param Zglass: z coordinate of the glass on the window

	Returns:
	a second order function
	"""
	def createWindow2(dimensions):
		"""
		Args:
		:param dimensions: dimension of the cube that contais the window

		Returns:
		an HPC object that represts a window
		"""
		(dx, dy, dz) = dimensions
		window = []

		x = 0
		for i in range (0, len(boolArray)) :
			y = 0
			for j in range (0, len(boolArray[i])):
				z = 0
				for k in range(0, len(boolArray[i][j])):
					if(boolArray[i][j][k]):
						cell = []
						if(Zarray[k] == Zglass and Xarray[i] == Xglass):
							cell = CUBOID([Xarray[i], Yarray[j], Zarray[k]])
						else:
							cell = COLOR([0.709, 0.709, 0.709])(CUBOID([Xarray[i], Yarray[j], Zarray[k]]))	
						window.append(T([1,2,3])([x,y,z])(cell))
					z += Zarray[k]
				y += Yarray[j]
			x += Xarray[i]

		window = STRUCT(window)
		window = S([1,2,3])([dx, dy, dz])(window)
		return window
	return createWindow2

def createDoor(Xarray, Yarray, Zarray, boolArray, Xglass, Zglass):
	"""
	Args:
	:param Xarray: a list of distances on x axis
	:param Yarray: a list of distances on y axis
	:param Zarray: a list of distances on z axis
	:param boolArray: a three dimensional matrix of occupancy
	:param Xglass: x coordinate of the glass on the door
	:param Zglass: z coordinate of the glass on the door

	Returns:
	a second order function
	"""
	def createDoor2(dimensions):
		"""
		Args:
		:param dimensions: dimension of the cube that contais the door

		Returns:
		an HPC object that represts a door
		"""
		(dx, dy, dz) = dimensions
		door = []

		x = 0
		for i in range (0, len(boolArray)) :
			y = 0
			for j in range (0, len(boolArray[i])):
				z = 0
				for k in range(0, len(boolArray[i][j])):
					if(boolArray[i][j][k]):
						cell = []
						if(Zarray[k] == Zglass and Xarray[i] == Xglass):
							cell = CUBOID([Xarray[i], Yarray[j], Zarray[k]])
						else:
							cell = COLOR([0.325, 0.207, 0.176])(CUBOID([Xarray[i], Yarray[j], Zarray[k]]))	
						door.append(T([1,2,3])([x,y,z])(cell))
					z += Zarray[k]
				y += Yarray[j]
			x += Xarray[i]

		door = STRUCT(door)
		door = S([1,2,3])([dx, dy, dz])(door)
		return door
	return createDoor2

if __name__ == "__main__":
	dx = 5.0
	dy = 5.0
	dz = 5.0
	dimensions = (dx, dy, dz)
	doorXarray = [0.20, 0.5, 0.20]
	doorYarray = [0.02, 0.04, 0.02]
	doorZarray = [0.20, 0.5, 0.015, 0.5, 0.015, 0.5, 0.015, 0.5, 0.20]

	doorBoolArray = [
		[
			[True, True, True, True, True, True, True, True, True], #X1, Y1, Zi
			[True, True, True, True, True, True, True, True, True], #X1, Y2, Zi
			[True, True, True, True, True, True, True, True, True] #X1, Y3, Zi
		],
		[
			[True, False, True, False, True, False, True, False, True], #X2, Y1, Zi
			[True, True, True, True, True, True, True, True, True], #X2, Y2, Zi
			[True, False, True, False, True, False, True, False, True] #X2, Y3, Zi
		],
		[
			[True, True, True, True, True, True, True, True, True], #X3, Y1, Zi
			[True, True, True, True, True, True, True, True, True], #X3, Y2, Zi
			[True, True, True, True, True, True, True, True, True] #X3, Y3, Zi
		]
	]

	windowXarray = [0.1, 0.4, 0.1, 0.4, 0.1]
	windowYarray = [0.02, 0.04, 0.02]
	windowZarray = [0.1, 0.95, 0.1]

	windowBoolArray = [
		[
			[True, True, True], #X1, Y1, Zi
			[True, True, True], #X1, Y2, Zi
			[True, True, True], #X1, Y3, Zi
		],
		[
			[True, False, True], #X2, Y1, Zi
			[True, True, True], #X2, Y2, Zi
			[True, False, True], #X2, Y3, Zi
		],
		[
			[True, True, True], #X3, Y1, Zi
			[True, True, True], #X3, Y2, Zi
			[True, True, True], #X3, Y3, Zi
		],
		[
			[True, False, True], #X4, Y1, Zi
			[True, True, True], #X4, Y2, Zi
			[True, False, True], #X4, Y3, Zi
		],
		[
			[True, True, True], #X5, Y1, Zi
			[True, True, True], #X5, Y2, Zi
			[True, True, True], #X5, Y3, Zi
		]
	]


	door = createDoor(doorXarray, doorYarray, doorZarray, doorBoolArray, doorXarray[1], doorZarray[1])(dimensions)
	window = createWindow(windowXarray, windowYarray, windowZarray, windowBoolArray, windowXarray[1], windowZarray[1])(dimensions)
	VIEW(door)
	VIEW(window)