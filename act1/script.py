import glob
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

files = glob.glob("*.txt")

for file in range(len(files)):
	list = []
	input = open(files[file], "r")
	lines = input.readlines()

	for line in lines:
	    list.append(float(line))

	plt.figure(len(lines))
	plt.title("Time Vs. Requests")
	plt.xlabel("Number of requests")
	plt.ylabel("Time taken (seconds)")
	plt.grid(True)
	plt.plot(list)

plt.show()
