###############################################################################
# Project:     Benford's Law Fraud Detection Script
# Author:      Subject Zero
# Created:     04/11/2013
# Modififed:   04/23/2013
# Description:
# This Python script searches an arbitrary number of files for signs of
# creative accounting, then reports the results to the user in the form of
# multiple files. 
###############################################################################

import math
import os
import datetime
import os.path

def\
main(): #\=====================================================================
	
	now = str(datetime.datetime.now())

	#\ SET UP \----------------------------------------------------------------

	dataFiles = []
	lForgeryCoefficient = []

	# get the absolute path of main.py
	whereAmI = os.path.dirname(os.path.abspath(__file__))

	# get the file names within the directory
	fileCount = 0
	for root, dirs, files in os.walk(whereAmI):
		for file_ in files:
			if file_.endswith('.dat'):
				dataFiles.append(file_)
			fileCount += 1
			if(fileCount > 100):
				print 'File limit reached'
				break

	# sort the files into a more reasonable order
	dataFiles.sort()

	#\ DO WORK \---------------------------------------------------------------

	for fileName in dataFiles:
		# determine the forgery coefficient
		lForgeryCoefficient.append(GetForgeryCo(fileName))

	#\ OUTPUT THE RESULTS TO A FILE \------------------------------------------

	# open the error_log file
	if os.path.isfile('primary_report.txt') and\
		os.path.exists('primary_report.txt'):
		outHandle = open('primary_report.txt', 'a')
	else:
		outHandle = open('primary_report.txt', 'w')
		# output a heading
		outHandle.write(('*'*80)+'\n')
		outHandle.write('** BENFORDS LAW\n')
		outHandle.write('** PRIMARY REPORT\n')
		outHandle.write('** (FORGERY COEFFICIENTS)\n')
		outHandle.write('** '+now)
		outHandle.write(('*'*80)+'\n')

	# make a header and output it
	header = 'FILE NAME                   | FORGERY COEFFICIENT\n'
	print header
	outHandle.write(header)
	
	# horizontal spacer	
	print ('-'*28)+'+'+('-'*51)

	# print stuff
	for index in range(0, len(lForgeryCoefficient)):
		line = ('%-28s| %.3f\n') %\
			    (dataFiles[index], lForgeryCoefficient[index])
		print line
		outHandle.write(line)

	# close the file
	outHandle.close()

	# end main() \=============================================================


def\
GetForgeryCo(fileName): #\=====================================================

	#\ SETUP \-----------------------------------------------------------------
	
	# initial values
	digit = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	empiricalProb = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	benfordProb = [.301, .176, .125, .097, .079, .067, .058, .051, .046]
	benfordOffset = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	numsFound = 0
	errorLog = []
	now = str(datetime.datetime.now())

	# open input file with read access
	inHandle = open(fileName, 'r')

	#\ PROCESSING \------------------------------------------------------------

	# count digits
	line = 1
	for buffer in inHandle:
		buffer.strip('\n')
		try:
			test = int(buffer)
			digit[(int(buffer[0])) - 1] += 1
			numsFound += 1
		except:
			errorLog.append('Bad read in '+fileName+': line '+str(line)+'\n')
		line += 1			
			

	for x in range(0, 9):
		empiricalProb[x] = float(digit[x]) / numsFound

	# get Benford Offset
	for x in range(0, 9):
		benfordOffset[x] = abs(empiricalProb[x] - benfordProb[x])
		#benfordOffset[x] = abs(empiricalProb[x] - math.log10(1.0+1.0/(x+1.0)))

	ForgeryCoefficient = sum(benfordOffset)
	strForgeryCoefficient = '%.2f' % ForgeryCoefficient

	#\ PRIMARY OUTPUT \--------------------------------------------------------

	# open the output file
	if os.path.isfile('detailed_results.txt') and\
		os.path.exists('detailed_results.txt'):
		outHandle = open('detailed_results.txt', 'a')
	else:
		outHandle = open('detailed_results.txt', 'w')
		outHandle.write(('*'*80)+'\n')
		outHandle.write('** BENFORDS LAW\n')
		outHandle.write('** DETAILED SUMMARY\n')
		outHandle.write('** '+now+'\n')
		outHandle.write(('*'*80)+'\n')


	# display frequency totals and write them to a file
	heading = 'Detailed Summary: '+str(fileName)+'\n'+str(numsFound)+\
 		  ' integer elements were encountered analyzed.\n'+\
		  '-----------------------------------------------------------\n'+\
		  'DIGIT | FREQUENCY | RELATIVE FREQUENCY | BENFORD OFFSETS   \n'+\
		  '-----------------------------------------------------------\n'
	print heading
	outHandle.write(heading)

	for x in range(0, 9):
		stats =  ('%-7d|%-11d|%-20.3f|%-.3f\n') %\
			 ((x+1),\
			  digit[x],\
			  empiricalProb[x],\
			  benfordOffset[x]  )
		outHandle.write(stats)
		print stats

	# display the sum of the benford values (forgery coefficient)
	forgeryMessage = 'The Forgery coefficient for '\
			 +fileName+' is '+strForgeryCoefficient+'\n'

	print forgeryMessage
	# write the forgery messsage to outHandle
	outHandle.write(forgeryMessage)
	
	# close outHandle
	outHandle.close()

	#\ ERROR LOG OUTPUT \------------------------------------------------------
	
	# open the error_log file
	if os.path.isfile('error_log.txt') and\
		os.path.exists('error_log.txt'):
		oLogHandle = open('error_log.txt', 'a')
	else:
		oLogHandle = open('error_log.txt', 'w')
		# output a heading
		oLogHandle.write(('*'*80)+'\n')
		oLogHandle.write('** BENFORDS LAW\n')
		oLogHandle.write('** ERROR LOG\n')
		oLogHandle.write('** '+now+'\n')
		oLogHandle.write(('*'*80)+'\n')

	# output errorLog to file
	for messages in errorLog:
		oLogHandle.write(messages)
	
	# close oLogHandle
	oLogHandle.close()

	#\ RETURN \----------------------------------------------------------------

	return ForgeryCoefficient
	
	# end GetForgeryCo() \=====================================================

main()

