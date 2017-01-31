from pyplasm import *
from workshop_03 import *
from workshop_04 import *
from workshop_07 import *

import csv

def stairs(dimension, stepDimension):
	"""
	Args:
	:param dimension: vector dimensions of the cube
	:param dimension: vector dimensions of the single step

	Returns:
	an HPC object representing a stair
	"""
	stair = ggpl_floatingStair(dimension, stepDimension)
	return stair


def roof(vertex, cells):
	"""
	Args:
	:param vertex: set of verts
	:param cell: set of cells

	Returns:
	an HPC object representing a roof
	"""
	roof = ggpl_buildRoof(vertex, cells)

	return roof


def door(doorDimensions):
	"""
	Args:
	:param doorDimensions: dimensions of the door

	Returns:
	an HPC object representing a door
	"""
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

	door = createDoor(doorXarray, doorYarray, doorZarray, doorBoolArray, doorXarray[1], doorZarray[1])(doorDimensions)
	return door

def window(windowDimensions):
	"""
	Args:
	:param windowDimensions: dimensions of the window

	Returns:
	an HPC object representing a window
	"""
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

	window = createWindow(windowXarray, windowYarray, windowZarray, windowBoolArray, windowXarray[1], windowZarray[1])(windowDimensions)
	return window

def plan():
	"""
	Returns:
	an HPC object representing a plan of the building
	"""
	with open("internalWalls.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		internalWalls = []
		for row in reader :
			internalWalls.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
		internalWalls = STRUCT(internalWalls)
		internalWalls = OFFSET([0, 0, 100.0])(internalWalls)
		internalWalls = OFFSET([0, 5.0, 0])(internalWalls)
		internalWalls = OFFSET([5.0, 0, 0])(internalWalls)
		internalWalls = COLOR([0.96, 0.87, 0.70])(internalWalls)
		#VIEW(internalWalls)

		
	with open("windows.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		i = 1
		j = 0
		for row in reader :
			if(i == 1 or i == 2 or i == 5 or i == 6 or i == 7 or i == 8):
				xi = float(row[0])
				yi = float(row[1])
				xf = float(row[2])
				windowDimensions = [xf-xi-4.0, xf-xi-10.0, 53.0]
				windowElement = window(windowDimensions)
				lowerWall = CUBOID([xf-xi+2.0, 5.0, 20.0])
				lowerWall = COLOR([0.96, 0.87, 0.70])(lowerWall)
				upperWall = CUBOID([xf-xi+2.0, 5.0, 20.0])
				upperWall = COLOR([0.96, 0.87, 0.70])(upperWall)
				windowElement = T(1)(2.0)(windowElement)
				windowElement = STRUCT([lowerWall, T(3)(20.0), windowElement, T(3)(61.0), upperWall])
				if(j == 0):
					house = STRUCT([internalWalls, T(1)(xi), T(2)(yi), windowElement])
					j = j + 1
				else:
					house = STRUCT([house, internalWalls, T(1)(xi), T(2)(yi), windowElement])
				i = i + 1

			else:
				if(i == 3 or i == 4):
					xi = float(row[0])
					yi = float(row[1])
					yf = float(row[3])
					windowDimensions = [yf-yi-5.0, yf-yi-3.5, 53.0]
					windowElement = window(windowDimensions)

					lowerWall = CUBOID([5.0, yf-yi+2.0, 20.0])
					lowerWall = COLOR([0.96, 0.87, 0.70])(lowerWall)
					upperWall = CUBOID([5.0, yf-yi+2.0, 20.0])
					upperWall = COLOR([0.96, 0.87, 0.70])(upperWall)
					lowerWall = R([2, 1])(PI/2.0)(lowerWall)
					upperWall = R([2, 1])(PI/2.0)(upperWall)

					windowElement = T(1)(2.0)(windowElement)
					windowElement = T(2)(-5.0)(windowElement)
					windowElement = STRUCT([lowerWall, T(3)(20.0), windowElement, T(3)(61.0), upperWall])
					windowElement = R([2, 1])(-PI/2.0)(windowElement)

					house = STRUCT([house, internalWalls, T(1)(xi), T(2)(yi), windowElement])
					i = i + 1
				else:
					if(i == 9):
						xi = float(row[0])
						yi = float(row[1])
						yf = float(row[3])
						windowDimensions = [yf-yi-7.0, yf-yi-3.5, 53.0]
						windowElement = window(windowDimensions)

						lowerWall = CUBOID([5.0, yf-yi+2.0, 20.0])
						lowerWall = COLOR([0.96, 0.87, 0.70])(lowerWall)
						upperWall = CUBOID([5.0, yf-yi+2.0, 20.0])
						upperWall = COLOR([0.96, 0.87, 0.70])(upperWall)

						lowerWall = R([2, 1])(PI/2.0)(lowerWall)
						upperWall = R([2, 1])(PI/2.0)(upperWall)

						windowElement = T(1)(2.0)(windowElement)
						windowElement = T(2)(-5.0)(windowElement)
						windowElement = STRUCT([lowerWall, T(3)(20.0), windowElement, T(3)(61.0), upperWall])

						windowElement = T(2)(-0.5)(windowElement)
						windowElement = R([2, 1])(-PI/2.0)(windowElement)

						house = STRUCT([house, internalWalls, T(1)(xi), T(2)(yi), windowElement])
						i = i + 1
		#VIEW(house)

	with open("doors.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		i = 0
		for row in reader :
			xi = float(row[0])
			yi = float(row[1])
			yf = float(row[3])
			doorDimensions = [yf-yi+5.0, yf-yi-10.0, 34.0]
			doorElement = door(doorDimensions)
			doorElement = R([2, 1])(-PI/2.0)(doorElement)
			doorElement = T(2)(2.0)(doorElement)
			doorElement = T(1)(4.0)(doorElement)
			upperWall = CUBOID([5.0, yf-yi, 20.0])
			upperWall = COLOR([0.96, 0.87, 0.70])(upperWall)
			doorElement = STRUCT([doorElement, T(3)(81.0), upperWall])

			house = STRUCT([house, internalWalls, T(1)(xi), T(2)(yi), doorElement])
		#VIEW(house)

	with open("floor.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		verts = []
		cells = [[1, 2, 3, 4]]
		i = 0
		for row in reader :
			if(i == 0):
				x = float(row[0])
				y = float(row[1])
				elem = [x, y]
				verts.append(elem)
			if(i == 1):
				x = float(row[0])
				y = float(row[1])
				elem = [x, y]
				verts.append(elem)
			if(i == 2):
				x = float(row[0])
				y = float(row[1])
				elem = [x, y]
				verts.append(elem)
			if(i == 3):
				x = float(row[2])
				y = float(row[3])
				elem = [x, y]
				verts.append(elem)
			i = i + 1
		
		floor = TEXTURE("floor_texture.JPG") (MKPOL([verts, cells, None]))

	house = STRUCT([house, floor])

	#VIEW(house)

	return house

def house(building):
	"""
	Args:
	:param building: an HPC object representig a two floor building

	Returns:
	an HPC object representing a complete building
	"""

	with open("roof.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		verts = []
		cells = [[1, 2, 5], [2, 3, 6, 5], [3, 4, 6], [4, 1, 5, 6]]
		i = 1
		for row in reader :
			if(i == 1):
				x = float(row[0])
				y = float(row[1])
				z = 0.0
				elem = [x-30.0, y-30.0, z]
				verts.append(elem)
			if(i == 2):
				x = float(row[0])
				y = float(row[1])
				z = 0.0
				elem = [x+30.0, y-30.0, z]
				verts.append(elem)
			if(i == 3):
				x = float(row[0])
				y = float(row[1])
				z = 0.0
				elem = [x+30.0, y+30.0, z]
				verts.append(elem)
			if(i == 4):
				x = float(row[2])
				y = float(row[3])
				z = 0.0
				elem = [x-30.0, y+30.0, z]
				verts.append(elem)
			if(i == 5):
				x = float(row[0])
				y = float(row[1])
				z = 100.0
				elem = [x, y, z]
				verts.append(elem)
			if(i == 6):
				x = float(row[0])
				y = float(row[1])
				z = 100.0
				elem = [x, y, z]
				verts.append(elem)	
			i = i + 1

		roofElem = roof(verts, cells)
		roofElem = TEXTURE("roof_texture.jpg")(roofElem)

		stairElem = stairs((55, 65, 100), (30, 8.1, 3))
		stairElem = T(1)(100.0)(stairElem)
		stairElem = T(2)(376.0)(stairElem)
		house = STRUCT([building, stairElem])

		house = STRUCT([house, T(3)(200.0) ,roofElem])

	return house

def ggpl_multistorey_house():
	"""
	Returns:
	an HPC object representing a multistorey house
	"""

	plan1 = plan()
	plan2 = plan()
	building = STRUCT([plan1, T(3)(100.0) ,plan2])
	#VIEW(building)
	multistorey_house = house(building)
	return multistorey_house

if __name__ == '__main__':
	result = ggpl_multistorey_house()
	#VIEW(result)
