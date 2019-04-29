class Process:
	def __init__(self, name, memorySize, arrivalTime, runTime):
		self.name = name
		self.memorySize = memorySize
		self.arrivalTime = arrivalTime
		self.runTime = runTime
		self.startFrame = None
		
	def __str__(self):
		return "P[" + self.name + " " + str(self.memorySize) + " " + str(self.arrivalTime) + " " + str(self.runTime) + "]"
