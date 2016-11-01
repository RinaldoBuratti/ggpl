from pyplasm import *
from larlib import *
import csv

def search(string, char): 
    """
    Function to search a character in a string 

    Args:
    string: a string in which we have to find the character char
    char: a character

    Returns:
    An index corresponding to the position of the character within the string

    """   
    
    index = 0 
    while index < len(string): 
        if string[index] == char: 
            return index
        index = index + 1 
    return -1 


def loadDataFromCsv(string):
    """
    Function to load the contenct of a csv file

    Returns:
    A set of element's list

    """   
    with open(string,'r') as f:
        dati=csv.reader(f, delimiter=':', quotechar=' ')
        #my_list = map(tuple, dati)
        frameDistances = []				#per la traslazione sull'asse x
        yDistances = []				#per la traslazione sull'asse y
        zDistances = []				#per la traslazione sull'asse z
        beamsSections = []
        beamsDistances = []
        pillarsSections = []
        pillarsDistances = []

        for line in dati:
            if(len(line) == 1):
                s = line[0]
                frameDistances.extend([float(s[0:search(s,",")])])
                s = s[search(s,",")+1:len(s)]
                yDistances.extend([float(s[0:search(s,",")])])
                zDistances.extend([float(s[search(s,",")+1:len(s)])])
            else:
                pillarsDistances.append(line[0])
                beamsDistances.append(line[1])
                pillarsSections.append(line[2])
                beamsSections.append(line[3])


        tmp = []
        for i in range (0, len(pillarsDistances)):
            el2 = []
            for j in range (0, len(pillarsDistances[i])):
                if(j%2 == 0):
                    el2.extend([float(pillarsDistances[i][j])])
            tmp.append(el2)
        pillarsDistances = tmp

        tmp = []
        for i in range (0, len(beamsDistances)):
            el2 = []
            for j in range (0, len(beamsDistances[i])):
                if(j%2 == 0):
                    el2.extend([float(beamsDistances[i][j])])
            tmp.append(el2)
        beamsDistances = tmp

        ps= []
        val = search(pillarsSections[0], ",")
        for i in range(0,len(pillarsSections)):
            tmp = pillarsSections[i]
            px = float(tmp[0:val])
            py = float(tmp[val+1:len(tmp)])
            p = (px,py)
            ps.append(p)
        pillarsSections = ps

        bs= []
        val = search(beamsSections[0], ",")
        for i in range(0,len(beamsSections)):
            tmp = beamsSections[i]
            bx = float(tmp[0:val])
            by = float(tmp[val+1:len(tmp)])
            b = (bx,by)
            bs.append(b)
        beamsSections = bs

    return (pillarsDistances, beamsDistances, pillarsSections, beamsSections, frameDistances)


def buildFrame(beamSection, pillarSection, pillarDistances, beamDistances) :
	"""

	Creates a parametric frame in reinforced concrete

	Args:
    :param beamSize: given dimensions of beam section
    :param pillarSize: given dimensions of pillar section
    :param beamDistances: distances between axes of the pillars
    :param pillarDistances: interstory heights
    
    Returns: 
    3D value of type HPC representing a single frame of the building
    
    """

	(bx, bz) = beamSection
	(px, py) = pillarSection

	#pillar creation

	pillarX = []
	for i in range(0, len(pillarDistances)):
		pillarX.extend([py, -pillarDistances[i]])
	pillarX.extend([py])

	pillarY = []
	for i in range(0, len(beamDistances)):
		pillarY.extend([beamDistances[i], -bz])

	pillarSimple = PROD([QUOTE(pillarX), QUOTE(pillarY)])
	pillarComplete = PROD([pillarSimple, Q(px)])

	#beam creations

	beamX = []
	for i in range(0, len(pillarDistances)):
		if i == 0 or i == len(pillarDistances) - 1 :
			beamSize = pillarDistances[i] + py + py/2.0
		else:
			beamSize = pillarDistances[i] + py
		beamX.extend([beamSize])

	beamY = []
	for i in range(0, len(beamDistances)):
		beamY.extend([-beamDistances[i], bz])

	beamSimple = PROD([QUOTE(beamX), QUOTE(beamY)])
	beamComplete = PROD([beamSimple, Q(bx)])

	structure = STRUCT([pillarComplete, beamComplete])
	structure = R([1,2])(PI/2.0)(structure)
	return R([1,3])(-PI/2.0)(structure)
	
def buildAllFrames(beamSection, pillarSection, pillarDistances, beamDistances, frameDistances) :
	"""
	Build multiple frames

	Args:
	:param beamSize: given dimensions of beam section
    :param pillarSize: given dimensions of pillar section
    :param beamDistances: distances between axes of the pillars
    :param pillarDistances: interstory heights
    :param frameDistances: distances between frames
    
    Returns: 
    3D value of type HPC representing the frames of the building

	"""
	allFrames = []
	framesHeight = []
	framesWidth = []
	for i in range(0, len(frameDistances)):
		temp = 0
		currentPillarDistances = pillarDistances[i]
		currentBeamDistances = beamDistances[i]
		
		for j in range(0, len(currentBeamDistances)):
			temp = temp + currentBeamDistances[j]
		framesHeight.extend([temp])

		temp = 0
		for j in range(0, len(currentPillarDistances)):
			temp = temp + currentPillarDistances[j]
		framesWidth.extend([temp])

		currentPillarSection = pillarSection[i]
		currentBeamSection = beamSection[i]

		frame = buildFrame(currentBeamSection, currentPillarSection, currentPillarDistances, currentBeamDistances)
		allFrames.extend([T(1) (frameDistances[i]), frame])
	return (STRUCT(allFrames), framesHeight, framesWidth)

def buildBeamsBetweenFrames(beamSection, pillarSection, pillarDistances, beamDistances, frameDistances, heights, widths):
	"""
	Build beams between frames

	Args:
	:param beamSize: given dimensions of beam section
    :param pillarSize: given dimensions of pillar section
    :param beamDistances: distances between axes of the pillars
    :param pillarDistances: interstory heights
    :param frameDistances: distances between frames
    
    Returns: 
    3D value of type HPC representing the internal beams of the building

	"""
	planes = []
	dist = 0
	for j in range(0, len(frameDistances)-1):
		minHeight = 0
		if(heights[j] <= heights[j+1]):
			minHeight = j
		else:
			minHeight = j+1

		minWidth = 0
		if(widths[j] <= widths[j+1]):
			minWidth = j
		else:
			minWidth = j+1

		(by, bz) = beamSection[minHeight]
		(px, py) = pillarSection[minWidth]
		bx = frameDistances[j+1]
		yDistances = pillarDistances[minWidth]
		zDistances = beamDistances[minHeight]

		if(j == 0):
			dist = px

		el = PROD([Q(bx), Q(by)])
		el = PROD([el, Q(bz)])
		el = STRUCT([el])

		tmp = []
		for i in range(0, len(yDistances)):
			tmp.extend([el, T(2)(yDistances[i]+py)])
		tmp.extend([el])
		tmp = STRUCT(tmp)

		floors = []
		pred = 0
		for i in range(0, len(zDistances)):
			floors.extend([T(3)(zDistances[i] + pred), tmp])
			pred = bz
		floors = STRUCT(floors)

		planes.extend([T(1)(dist), floors])
		dist = bx

	planes = STRUCT(planes)
	return planes

def ggpl_bone_structure(filename):
	"""
	creates a bone structure of a building
	Args:
	:param filename: the name of a .csv file that contais input values

	Returns:
	3D value of type HPC representing the bone structure of a building
	"""
	values = loadDataFromCsv(filename)
	beamSection = values[3]
	pillarSection = values[2]
	pillarDistances = values[0]
	beamDistances = values[1]
	frameDistances = values[4]

	(allFrames, heights, widths) = buildAllFrames(beamSection, pillarSection, pillarDistances, beamDistances, frameDistances)
	allBeams = buildBeamsBetweenFrames(beamSection, pillarSection, pillarDistances, beamDistances, frameDistances, heights, widths)
	

	structure = buildStructure(allFrames, allBeams)

	return structure

def buildStructure(frames, floorsBeams):
	structure = STRUCT([frames, floorsBeams])
	return structure


if __name__ == "__main__":
	structure = ggpl_bone_structure('frame_data_438537.csv')
	VIEW(structure)