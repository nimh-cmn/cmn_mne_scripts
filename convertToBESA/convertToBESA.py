#!/env/python3

import argparse
import os
import numpy as np
import pandas as pd

def main():
	parser = argparse.ArgumentParser()
	
	parser.add_argument(
		'--inputFile',
		help='File to convert from EGI text to BESA text',
		nargs=1,
	)
	parser.add_argument(
		'--output',
		help='Filename for output as BESA text',
		nargs=1,
	)
	parser.add_argument(
		'--baseline',
		help='Number of datapoints in baseline',
		nargs=1,
	)
	parser.add_argument(
		'--srate',
		help='Sampling Rate of EEG',
		nargs=1,
	)
		
	args = parser.parse_args()
	#print(args)
	
	#get the input file and read into pandas
	#print ("input: " + args.inputFile[0])
	
	eegData = pd.read_table(args.inputFile[0], sep='\t', header=None)
	rotatedData = eegData.transpose()
	
	dataPoints = eegData.shape[0]
	eegSensors = eegData.shape[1]
	#print(eegData.shape)
	
	sampleRate = float(args.srate[0]) / 1000.00
	print(sampleRate)
	
	#build output string
	print("Npts= " + str(dataPoints) + " TSB= -" + str(args.baseline[0]) + 
		" DI= " + str(sampleRate) + " SB= 1.000 SC= 200.0 Nchan= " + str(eegSensors) +
		" SegmentName= Segment1")
		
	#dataString = rotatedData.to_csv(sep=' ', )
		
	
	with open(args.output[0], 'w') as f:
		f.write("Npts= " + str(dataPoints) + " TSB= -" + str(args.baseline[0]) + 
		" DI= " + str(sampleRate) + " SB= 1.000 SC= 200.0 Nchan= " + str(eegSensors) +
		" SegmentName= Segment1\n")
		#f.write(" ".join([ f"E{i:03}"  for i in range(0,257)]))
		f.write(" ".join([ f"E{i}"  for i in range(1,258)]))
		f.write("\n")
		
	rotatedData.to_csv(args.output[0], sep=' ', index=False, header=False, mode='a')

if __name__ == '__main__':
	main()