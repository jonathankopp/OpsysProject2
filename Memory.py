class Memory:
	def __init__(self, numFrames, memorySize, tMemMove):
		self.numFrames = numFrames
		self.memorySize = memorySize
		self.tMemMove = tMemMove
		self.memory = ['.' for i in range(memorySize)]
		self.running = [] 	# Running process
		self.ready = []			# Ready processes

	def __str__(self):
		ret = '=' * self.numFrames + "\n"
		i = 0
		for frame in self.memory:
			if i == self.numFrames:
				ret+= "\n"
				i = 0
			ret += frame
			i += 1
		ret += "\n"
		ret += '=' * self.numFrames
		return ret



	def isDone(self):
		return len(self.running) == 0 and len(self.ready) == 0

	def add(self, process, time):
		self.ready.append(process)

	def checkDefrag(self, process):
		# count the number of free frames and check if there are enough to place process after defragmentation
		return len([frame for frame in self.memory if frame == '.']) >= process.memorySize

	def defrag(self):
		# compact memory to only processes
		defrag = [frame for frame in self.memory if frame != '.']
		# add free space to the end of memory
		defrag = defrag + ['.' for i in range(self.memorySize - len(defrag))]
		# set defraged memory to memory
		self.memory = defrag
		# update the startFrame index for each process in memory and count number of frames moved
		numFramesMoved = 0
		processesMoved = []
		for process in self.running:
			newStartFrame = self.memory.index(process.name)
			if not process.startFrame == newStartFrame:
				numFramesMoved += process.memorySize
				process.startFrame = newStartFrame
				processesMoved.append(process.name)
		return numFramesMoved, sorted(processesMoved)

class firstFitMemory(Memory):
	def __init__(self, numFrames, memorySize, tMemMove):
		super().__init__(numFrames, memorySize, tMemMove)
		self.type = "(Contiguous -- First-Fit)"

	def update(self, time):
		# for all running processes
		for process in sorted(self.running, key=lambda process: process.name):
			# Decrement time left for process
			process.runTime -= 1
			# logic to remove memory
			if process.runTime == 0:
				for i in range(process.memorySize):
					self.memory[process.startFrame + i] = '.'
				print("time {}ms: Process {} removed:".format(time, process.name))
				print(str(self))
				self.running.remove(process)
		# for all processes ready to be added to memory
		for process in sorted(self.ready, key=lambda process: process.name):
			print("time {}ms: Process {} arrived (requires {} frames)".format(time, process.name, process.memorySize))
			self.ready.remove(process)
			# logic to place memory
			free = 0
			for i in range(len(self.memory)):
				if self.memory[i] == '.':
					free += 1
				else:
					free = 0
				if free == process.memorySize:
					process.startFrame = i - process.memorySize + 1
					break
			# if there isn't a memory memory chunk large enough
			if free < process.memorySize:
				# check if defrag will create a memory chunk large enough
				if self.checkDefrag(process):
					# if yes, defrag memory and set the start index to the first open memory index
					print("time {}ms: Cannot place process {} -- starting defragmentation".format(time, process.name))
					numFramesMoved, processesMoved = self.defrag()
					# update the time
					# since everything stops while defragging, the time can be changed within this function with no problems
					time += self.tMemMove * numFramesMoved
					process.startFrame = self.memory.index('.')
					print("time {}ms: Defragmentation complete (moved {} frames: {})".format(time, numFramesMoved, ', '.join(processesMoved)))
				else:
					# if no, do not place the process and continue
					print("time {}ms: Cannot place process {} -- skipped!".format(time, process.name))
					continue
			self.running.append(process)
			# write the process into memory using the start index found above
			for i in range(process.memorySize):
				self.memory[process.startFrame + i] = process.name
			print("time {}ms: Placed process {}:".format(time, process.name))
			print(str(self))
		return time

	def add(self, process, time):
		super().add(process, time)

	def checkDefrag(self, process):
		return super().checkDefrag(process)

	def defrag(self):
		return super().defrag()

class nextFitMemory(Memory):
	def __init__(self, numFrames, memorySize, tMemMove):
		super().__init__(numFrames, memorySize, tMemMove)
		self.type = "(Contiguous -- Next-Fit)"
		self.memIndex = 0

	def update(self, time):
		# for all running processes
		for process in sorted(self.running, key=lambda process: process.name):
			# Decrement time left for process
			process.runTime -= 1
			# logic to remove memory
			if process.runTime == 0:
				for i in range(process.memorySize):
					self.memory[process.startFrame + i] = '.'
				print("time {}ms: Process {} removed:".format(time, process.name))
				print(str(self))
				self.running.remove(process)
		# for all processes ready to be added to memory
		for process in sorted(self.ready, key=lambda process: process.name):
			print("time {}ms: Process {} arrived (requires {} frames)".format(time, process.name, process.memorySize))
			self.ready.remove(process)
			# logic to place memory
			free = 0
			for i in range(len(self.memory)):
				if self.memory[(i + self.memIndex) % self.memorySize] == '.' and not (i + self.memIndex) % self.memorySize == self.memorySize - 1:
					free += 1
				else:
					free = 0
				if free == process.memorySize:
					process.startFrame = ((i + self.memIndex) % self.memorySize) - process.memorySize + 1
					self.memIndex = ((i + self.memIndex) % self.memorySize) + 1
					break
			# if there isn't a memory memory chunk large enough
			if free < process.memorySize:
				# check if defrag will create a memory chunk large enough
				if self.checkDefrag(process):
					# if yes, defrag memory and set the start index to the first open memory index
					print("time {}ms: Cannot place process {} -- starting defragmentation".format(time, process.name))
					numFramesMoved, processesMoved = self.defrag()
					# update the time
					# since everything stops while defragging, the time can be changed within this function with no problems
					time += self.tMemMove * numFramesMoved
					process.startFrame = self.memory.index('.')
					print("time {}ms: Defragmentation complete (moved {} frames: {})".format(time, numFramesMoved, ', '.join(processesMoved)))
				else:
					# if no, do not place the process and continue
					print("time {}ms: Cannot place process {} -- skipped!".format(time, process.name))
					continue
			self.running.append(process)
			# write the process into memory using the start index found above
			for i in range(process.memorySize):
				self.memory[process.startFrame + i] = process.name
			print("time {}ms: Placed process {}:".format(time, process.name))
			print(str(self))
		return time

	def add(self, process, time):
		super().add(process, time)

	def checkDefrag(self, process):
		return super().checkDefrag(process)

	def defrag(self):
		return super().defrag()

class bestFitMemory(Memory):
	def __init__(self, numFrames, memorySize, tMemMove):
		super().__init__(numFrames, memorySize, tMemMove)
		self.type = "(Contiguous -- Best-Fit)"
		# freeChunks structure is {indexOfStart: sizeOfChunk}
		self.freeChunks = {}
		self.memIndex = 0

	def update(self, time):
		# for all running processes
		for process in sorted(self.running, key=lambda process: process.name):
			# Decrement time left for process
			process.runTime -= 1
			# logic to remove memory
			if process.runTime == 0:
				for i in range(process.memorySize):
					self.memory[process.startFrame + i] = '.'
				print("time {}ms: Process {} removed:".format(time, process.name))
				print(str(self))
				self.running.remove(process)
		# for all processes ready to be added to memory
		for process in sorted(self.ready, key=lambda process: process.name):
			print("time {}ms: Process {} arrived (requires {} frames)".format(time, process.name, process.memorySize))
			self.ready.remove(process)
			# logic to place memory
			free = 0
			# update the freeChunks dict
			self.updateFreeChunks()
			# returns the best fit location and the size of the best fit memory fragment
			if(len(list(self.freeChunks.keys())) > 0):
				startIndex,chunkSize = self.bestFitHelp(process)
			else:
				# if no, do not place the process and continue
				print("time {}ms: Cannot place process {} -- skipped!".format(time, process.name))
				continue
			# if there is a chunk of memory that can fit this process
			if(not startIndex is None):
				process.startFrame = startIndex
				# self.memIndex = ((i + self.memIndex) % self.memorySize) + 1
			
			# if there isn't a memory memory chunk large enough
			else:
				# check if defrag will create a memory chunk large enough
				if self.checkDefrag(process):
					# if yes, defrag memory and set the start index to the first open memory index
					print("time {}ms: Cannot place process {} -- starting defragmentation".format(time, process.name))
					numFramesMoved, processesMoved = self.defrag()
					# update the time
					# since everything stops while defragging, the time can be changed within this function with no problems
					time += self.tMemMove * numFramesMoved
					process.startFrame = self.memory.index('.')
					print("time {}ms: Defragmentation complete (moved {} frames: {})".format(time, numFramesMoved, ', '.join(processesMoved)))
				else:
					# if no, do not place the process and continue
					print("time {}ms: Cannot place process {} -- skipped!".format(time, process.name))
					continue
			self.running.append(process)
			# write the process into memory using the start index found above
			for i in range(process.memorySize):
				self.memory[process.startFrame + i] = process.name
			print("time {}ms: Placed process {}:".format(time, process.name))
			print(str(self))
		return time

	def bestFitHelp(self,process):
		bestFit = None
		bestSize = None

		for startIndex in self.freeChunks.keys():
			# print("Start "+str(startIndex)+" size "+str(self.freeChunks[startIndex]))
			if(bestFit is None and self.freeChunks[startIndex] >= process.memorySize):
				bestFit = startIndex
				bestSize = self.freeChunks[startIndex]
				continue
			if(process.memorySize <= self.freeChunks[startIndex] and self.freeChunks[startIndex]<=bestSize):
				if(self.freeChunks[startIndex] ==  bestSize):
					if(startIndex > bestFit):
						continue
				bestFit = startIndex
				bestSize = self.freeChunks[startIndex]
		# print(bestFit,bestSize)
		return bestFit,bestSize







	def updateFreeChunks(self):
		lastFrame = None
		index = 0
		self.freeChunks = {}
		sFrame = 0
		lastWasFree = False
		i = 0
		for currentFrame in self.memory:
			# print(currentFrame," ",lastWasFree," ",sFrame)
			if(currentFrame == '.'):
				# if its a the top of the memory segmant
				# the check if its still focused on the same memory segmant
				if(lastWasFree):
					self.freeChunks[sFrame] += 1

				# if the current frame is free but its the start of a new memory segmant
				else:
					sFrame = index
					self.freeChunks[sFrame] = 1
				lastWasFree = True
			else:
				lastWasFree = False
			index+=1

	def add(self, process, time):
		super().add(process, time)

	def checkDefrag(self, process):
		return super().checkDefrag(process)

	def defrag(self):
		return super().defrag()

	def findFreeChunks(self):
		return super.findFreeChunks()

class nonContiguousMemory(Memory):
	def __init__(self, numFrames, memorySize, tMemMove):
		super().__init__(numFrames, memorySize, tMemMove)
		self.type = "(Non-Contiguous)"
