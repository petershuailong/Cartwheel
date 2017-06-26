from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Viewport(QGraphicsView):
	"""
	This is a subclass of QGraphicsView that adds behavior to its mouseMoveEvent function
	"""
	
	def __init__(self, parent=None):
		QGraphicsView.__init__(self, parent)
		self.setMouseTracking(True)
		
	def mouseMoveEvent(self, event):
		"""
		What to do when the mouse is moved within the viewport
		"""

		QGraphicsView.mouseMoveEvent(self, event)
		
		# Grab the position of the mouse and convert it to scene coordinates
		sceneCoordinates = self.mapToScene(event.pos())
		x = sceneCoordinates.x()
		y = sceneCoordinates.y()

		# Show in the status bar
		self.parent().parent().statusbar.showMessage("Current mouse position: " + str(x) + ", " + str(y))
		self.parent().parent().parent().statusbar.showMessage("Current mouse position: " + str(x) + ", " + str(y))
