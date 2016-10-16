from pyplasm import *
from larlib import *

def buildStructure(beamSection, pillarSection, pillarDistances, beamDistances) :

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

	return STRUCT([pillarComplete, beamComplete])



beamSection = (0.3, 0.3)
pillarSection = (0.3, 0.3)
pillarDistances = [2.5, 2, 3, 0.5, 1.5]
beamDistances = [2, 1, 0.5]

structure = buildStructure(beamSection, pillarSection, pillarDistances, beamDistances)

VIEW(structure)