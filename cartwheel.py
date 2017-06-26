#! /usr/bin/python

import sys
import os
import math
import datetime
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ControlWindow
import SceneWindow

class MainControlWindow(QMainWindow, ControlWindow.Ui_ControlWindow):
	
	"""
	This is the main window of the program.
	"""
	
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		ControlWindow.Ui_ControlWindow.__init__(self, parent)
		
		# Build the main window using the setupUi method generated by Qt Designer
		self.setupUi(self)

		# Grab the current date for the filename
		now = datetime.datetime.now()
		dateStr = '-'.join([str(now.year), str(now.month), str(now.day)])
		timeStr = ''.join(['%02d' % now.hour, '%02d' % now.minute, '%02d' % now.second])
		self.fname_prefix = '_'.join([dateStr, timeStr])

		# Start with the "invert" action unchecked
		self.action_invert.setChecked(False)

		# Create the window that will show the scene
		self.sceneWindow = MainSceneWindow(parent=self)
		self.sceneWindow.show()
		
		# Connections
		self.connect(self.action_invert, SIGNAL("toggled(bool)"), self.sceneWindow.updateProperties)
		self.connect(self.scale_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateProperties)
		self.connect(self.innerRadius_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateProperties)
		self.connect(self.thickness_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateProperties)
		self.connect(self.aVelocity_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateParameters)
		self.connect(self.distance_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateParameters)
		self.connect(self.diameter_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateParameters)
		self.connect(self.density_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateParameters)
		self.connect(self.viscosity_doubleSpinBox, SIGNAL("valueChanged(double)"), self.sceneWindow.updateParameters)
		self.connect(self.engage_pushButton, SIGNAL("clicked()"), self.sceneWindow.startRotation)
		self.connect(self.record_pushButton, SIGNAL("clicked()"), self.saveData)

	def saveData(self):
		"""
		Save parameters to disk
		"""
		
		fname = self.fname_prefix + '_WheelTest' + '.dat' 
		if os.path.isfile(fname):
			# Open in append mode
			file = open(fname, 'a')
		else:
			# Open in write mode (create the file) and write header
			file = open(fname, 'w')
			
			scaleHead = 'Scale'
			thicknessHead = 'Thickness'
			angularVelocityHead = 'AngularVelocity (rps)'
			distanceHead = 'Distance (um)'
			densityHead = 'Density (g/cm3)'
			diameterHead = 'Particle diameter (um)'
			viscosityHead = 'Viscosity (mPa s)'
			linearVelocityHead = 'Linear velocity (um/s)'
			depHead = 'DEP (pN)'
			centripetalForceHead = 'Centripetal force (pN)'
			header = '\t'.join(['# ' + scaleHead, thicknessHead, angularVelocityHead, distanceHead, densityHead, diameterHead, viscosityHead, linearVelocityHead, depHead, centripetalForceHead])
			file.write('# The Wheel test\n')
			file.write(header + '\n\n')
		
		# Write the values
		scale = str(self.scale_doubleSpinBox.value())
		thickness = str(self.thickness_doubleSpinBox.value())
		angularVelocity = str(self.aVelocity_doubleSpinBox.value())	# rps
		distance = str(self.distance_doubleSpinBox.value())			# um
		density = str(self.density_doubleSpinBox.value())			# g/cm3
		diameter = str(self.diameter_doubleSpinBox.value())			# um
		viscosity = str(self.viscosity_doubleSpinBox.value())		# mPa s
		linearVelocity = str(self.lVelocity_LCDNumber.value())		# um/s
		dep = str(self.DEPForce_LCDNumber.value())					# pN
		centripetalForce = str(self.cForce_LCDNumber.value())		# pN
		recordLine = '\t'.join([scale, thickness, angularVelocity, distance, density, diameter, viscosity, linearVelocity, dep, centripetalForce])
		file.write(recordLine + '\n')
			
		file.close()
		
		self.statusbar.showMessage("Saved to file " + fname)


class MainSceneWindow(QMainWindow, SceneWindow.Ui_SceneWindow):
	"""
	This is the window that shows the scene
	"""
	
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		SceneWindow.Ui_SceneWindow.__init__(self, parent)
		
		# Build the window using the setupUi method generated by Qt Designer
		self.setupUi(self)

		# Create the scene and visualize it
		self.scene = self.createScene()
		self.graphicsView.setScene(self.scene)

	def createScene(self):
		"""
		Create the scene
		"""
		
		# Create the scene and set some basic properties
		scene = QGraphicsScene(parent=self)
		scene.setBackgroundBrush(Qt.black)
		thickness = self.parent().thickness_doubleSpinBox.value()
		pixelRadius_outer = 100
		pixelRadius_inner = self.parent().innerRadius_doubleSpinBox.value()
		pen = QPen(Qt.white, thickness)
		
		# Create the items
		outer_circle = QGraphicsEllipseItem(-pixelRadius_outer, -pixelRadius_outer, pixelRadius_outer*2, pixelRadius_outer*2)
		inner_circle = QGraphicsEllipseItem(-pixelRadius_inner, -pixelRadius_inner, pixelRadius_inner*2, pixelRadius_inner*2)
		vline = QGraphicsLineItem(0, -pixelRadius_outer, 0, pixelRadius_outer)
		hline = QGraphicsLineItem(-pixelRadius_outer, 0, pixelRadius_outer, 0)
		outer_circle.setPen(pen)
		inner_circle.setPen(pen)
		vline.setPen(pen)
		hline.setPen(pen)
		wheel = QGraphicsItemGroup()
		wheel.addToGroup(outer_circle)
		wheel.addToGroup(inner_circle)
		wheel.addToGroup(vline)
		wheel.addToGroup(hline)
		wheel.setFlags(QGraphicsItem.GraphicsItemFlags(1)) # Make the item movable
		wheel.setPos(QPointF(0, 0))
		
		# Add the items to the scene
		scene.addItem(wheel)
		
		# Create a running variable that will be used to determine the rotation angle of the wheel
		self.wheelAngle = 0.0
		
		# Make the calculations with the initial values
		self.updateParameters()
		
		return scene

	def updateProperties(self):
		"""
		Update the properties of the scene
		"""
		
		# Read the properties from the SpinBoxes
		thickness = self.parent().thickness_doubleSpinBox.value()
		scale = self.parent().scale_doubleSpinBox.value()
		innerRadius = self.parent().innerRadius_doubleSpinBox.value()
		
		# Set the background and foreground color according to the status of the "invert" menu
		if self.parent().action_invert.isChecked():
			self.scene.setBackgroundBrush(Qt.white)
			pen = QPen(Qt.black, thickness)
		else:
			self.scene.setBackgroundBrush(Qt.black)
			pen = QPen(Qt.white, thickness)
		
		for item in self.scene.items():
			try:
				item.setPen(pen)
			except AttributeError:
				pass
		
		self.scene.items()[-1].setScale(scale)
		self.scene.items()[2].setRect(-innerRadius, -innerRadius, innerRadius*2, innerRadius*2)

	def startRotation(self):
		"""
		Start the rotation of the wheel
		"""
		
		unitRotation = 0.1 # seconds
		timeline = QTimeLine(unitRotation * 1000)
		timeline.setFrameRange(0, 1)
		timeline.setUpdateInterval(1)
		timeline.setCurveShape(3)
		self.rotation = QGraphicsItemAnimation()
		self.rotation.setTimeLine(timeline)
		
		self.connect(timeline, SIGNAL("finished()"), self.startRotation)
		self.connect(self.parent().stop_pushButton, SIGNAL("clicked()"), timeline.stop)
		
		angularV = self.parent().aVelocity_doubleSpinBox.value()
		initial = self.wheelAngle
		if initial > 360:
			initial -= 360
		final = initial + angularV * 360 * unitRotation
		self.wheelAngle = final
		
		self.rotation.setRotationAt(0, initial)
		self.rotation.setRotationAt(1, final)
		self.rotation.setItem(self.scene.items()[-1])
		timeline.start()

	def updateParameters(self):
		"""
		Update the linear velocity, DEP and centripetal forces according to the	values of the parameters
		"""
		
		# Linear velocity
		aVelocity_SI = self.parent().aVelocity_doubleSpinBox.value() * 2 * math.pi	# rad/s
		lVelocity = aVelocity_SI * self.parent().distance_doubleSpinBox.value()		# In um/s
		self.parent().lVelocity_LCDNumber.display(lVelocity)
		
		# DEP, which, at constant velocity, will be exactly the same as the drag force (that is what we assume)
		viscosity_SI = self.parent().viscosity_doubleSpinBox.value() * 1e-3			# Pa s
		radius_SI = (self.parent().diameter_doubleSpinBox.value() / 2) * 1e-6		# m
		lVelocity_SI = lVelocity * 1e-6												# m/s
		DEP_SI = 6 * math.pi * viscosity_SI * radius_SI * lVelocity_SI				# N
		DEP = DEP_SI * 1e12															# pN
		self.parent().DEPForce_LCDNumber.display(DEP)
		
		# Centripetal force
		distance_SI = self.parent().distance_doubleSpinBox.value() * 1e-6			# m
		density_SI = self.parent().density_doubleSpinBox.value() * 1e3				# Kg/m3
		volume_SI = 4 * math.pi * radius_SI**3 / 3									# m3
		mass_SI = density_SI * volume_SI											# Kg
		cForce_SI = mass_SI * aVelocity_SI**2 * distance_SI							# In N
		cForce = cForce_SI * 1e12													# pN
		self.parent().cForce_LCDNumber.display(cForce)


def main():
	app = QApplication(sys.argv)
	#app.setStyle("plastique")
	controlWin = MainControlWindow()
	controlWin.show()
	app.exec_()

main()
