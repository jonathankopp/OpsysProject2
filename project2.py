import sys
from Memory import firstFitMemory, nextFitMemory, bestFitMemory, nonContiguousMemory
from Process import Process
import copy

def run(memory, processes, maxATime):
	time = 0
	print("time 0ms: Simulator started {}".format(memory.type))
	while not memory.isDone() or time <= maxATime:
		for process in processes:
			if process.arrivalTime == time:
				memory.add(process, time)
		newTime = memory.update(time)
		# if defragmentation occured
		if newTime > time:
			for process in [process for process in processes if process.arrivalTime > time]:
				# delay process arrival time by defragmentation time
				process.arrivalTime += newTime - time
		time = newTime + 1
	print("time {}ms: Simulator ended {}".format(time-1, memory.type))

if __name__ == '__main__':
	numFrames = int(sys.argv[1])
	memorySize = int(sys.argv[2])
	fName = sys.argv[3]
	tMemMove = int(sys.argv[4])

	maxATime = 0
	processes = []
	f = open(fName,"r")
	for line in f.readlines():
		line = line.replace("\n", "").split(" ")
		name = line[0]
		size = int(line[1])
		line = line[2:]
		for times in line:
			times = times.split("/")
			if int(times[0]) > maxATime:
				maxATime = int(times[0])
			processes.append(Process(name, size, int(times[0]), int(times[1])))

	## Contiguous -- First-Fit
	ffProcesses = copy.deepcopy(processes)
	memory = firstFitMemory(numFrames, memorySize, tMemMove)
	# run(memory, ffProcesses, maxATime)
	print()

	## Contiguous -- Next-Fit
	nfProcesses = copy.deepcopy(processes)
	memory = nextFitMemory(numFrames, memorySize, tMemMove)
	# run(memory, nfProcesses, maxATime)
	print()

	## Contiguous -- Best-Fit
	bfProcesses = copy.deepcopy(processes)
	memory = bestFitMemory(numFrames, memorySize, tMemMove)
	run(memory, bfProcesses, maxATime)
	print()

	## Non-Contiguous
	ncProcesses = copy.deepcopy(processes)
	memory = nonContiguousMemory(numFrames, memorySize, tMemMove)
	# run(memory, ncProcesses, maxATime)
	print()
