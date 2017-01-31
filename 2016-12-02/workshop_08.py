from pyplasm import *
import csv

def ggpl_house():
	"""
	Returns:
	an HPC object that represents an house
	"""

	with open("internalWalls.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		internalWalls = []
		for row in reader :
			internalWalls.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
		internalWalls = STRUCT(internalWalls)
		internalWalls = OFFSET([0, 0, 100])(internalWalls)
		internalWalls = OFFSET([0, 10, 0])(internalWalls)
		internalWalls = OFFSET([10, 0, 0])(internalWalls)
		

	with open("windows.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		windows = []
		upperWall = []
		lowerWall = []
		for row in reader :
			windows.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
			upperWall.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
			lowerWall.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
		
		windows = STRUCT(windows)
		windows = OFFSET([0, 0, 50])(windows)
		windows = OFFSET([0, 10, 0])(windows)
		windows = OFFSET([10, 0, 0])(windows)
		windows = T(3)(25)(windows)
		windows = COLOR(BLUE)(windows)
		upperWall = STRUCT(upperWall)
		upperWall = OFFSET([0, 0, 25])(upperWall)
		upperWall = OFFSET([0, 10, 0])(upperWall)
		upperWall = OFFSET([10, 0, 0])(upperWall)
		upperWall = T(3)(75)(upperWall)
		lowerWall = STRUCT(lowerWall)
		lowerWall = OFFSET([0, 0, 25])(lowerWall)
		lowerWall = OFFSET([0, 10, 0])(lowerWall)
		lowerWall = OFFSET([9, 0, 0])(lowerWall)
		windows = STRUCT([windows, lowerWall, upperWall])


	with open("doors.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		doors = []
		upperWall = []
		for row in reader :
			doors.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
			upperWall.append(POLYLINE([[float(row[0]), float(row[1])],[float(row[2]), float(row[3])]]))
		
		doors = STRUCT(doors)
		doors = OFFSET([0, 0, 80])(doors)
		doors = OFFSET([0, 10, 0])(doors)
		doors = OFFSET([10, 0, 0])(doors)
		doors = COLOR([0.588, 0.29, 0])(doors)
		upperWall = STRUCT(upperWall)
		upperWall = OFFSET([0, 0, 20])(upperWall)
		upperWall = OFFSET([0, 10, 0])(upperWall)
		upperWall = OFFSET([10, 0, 0])(upperWall)
		upperWall = T(3)(80)(upperWall)
	
		doors = STRUCT([doors, upperWall])

	with open("floor.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		floor = []
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

	house = STRUCT([internalWalls, windows, doors, floor])
	return house

if __name__ == '__main__':
	house = ggpl_house()
	VIEW(house)