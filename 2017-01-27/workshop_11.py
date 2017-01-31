from pyplasm import *
from workshop_10 import *

def road():
	road = CUBOID([3500.0, 700.0, 10.0])
	road = TEXTURE("road_texture.jpg")(road)
	road = T(2)(-1500.0)(road)
	road = T(1)(-3200.0)(road)
	road = T(3)(-12.0)(road)

	return road


def curvedRoad(dx, dy):
	verts = [[0, 1000], [125, 500], [437.5, 500], [425, 0]]
	polyline = POLYLINE(verts)

	roadHeight = 5.0
	
	roadwidth = 250.0

	road = PROD([BEZIERSTRIPE([verts, roadwidth, 24]), QUOTE([roadHeight])])
	road = TEXTURE("road_texture.jpg")(road)
	road = COLOR(BROWN)(road)
	road = T(3)(20.0)(road)
	road = T(1)(-600.0)(road)
	road = T(2)(-850.0)(road)
	#VIEW(STRUCT([road]))
	return road

def houseArea():
	with open("floor.lines", "rb") as file:
		reader = csv.reader(file, delimiter = ",")
		i = 0
		for row in reader :
			if(i == 0):
				xi = float(row[0])
				xf = float(row[2])
			if(i == 1):
				yi = float(row[1])
				yf = float(row[3])
			i = i + 1 
		dimensionX = xf - xi
		dimensionY = yf - yi
		area = TEXTURE("grass_texture.jpg")(CUBOID([dimensionX + 700.0, dimensionY + 1200.0, 20.0]))
		area = T(1)(-950.0)(area)
		area = T(2)(-800.0)(area)

		road = curvedRoad(dimensionX, dimensionY)
		area = STRUCT([area, road])
		#VIEW(area)

	return area

def multistoreyHouse():
	multistoreyHouse = ggpl_multistorey_house()

	return multistoreyHouse

def ggpl_suburbian_neighborhood():
	multi = multistoreyHouse()
	area = houseArea()
	multi = R([2, 1])(-PI/2.0)(multi)
	house = STRUCT([multi, T(3)(-30.0), area])
	roadElem = road()
	side1 = STRUCT([house, T(1) (1100.0) , house, T(1)(1100.0), house, roadElem])
	house = R([2,1])(PI)(house)
	side2 = STRUCT([house, T(1) (1100.0) , house, T(1)(1100.0), house])
	side2 = T(1)(-750.0)(side2)
	suburbian_neighborhood = STRUCT([side1, T(2)(-2300.0), side2])
	#VIEW(suburbian_neighborhood)
	return suburbian_neighborhood

if __name__ == '__main__':
	suburbian_neighborhood = ggpl_suburbian_neighborhood()
	VIEW(suburbian_neighborhood)