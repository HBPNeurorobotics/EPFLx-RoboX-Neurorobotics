import numpy as np 
import pandas as pd
import os, fnmatch
import time
import importlib
import csv
import operator
import signal


class SOM_autograduation():
    

	def __init__(self):
    
		import warnings; warnings.filterwarnings('ignore')

		# parameters of graduation range 
		self.standard = [1.05, 1.5, 2.0, 3.0, 5.0, 10.0] # range of variation result and given note dependency

		# initialize the parameters of test (Map size and Number of trials)
		self.N = 1
		self.tau = 100.0
		self.limit = 65.0 # only integer value

		self.user = {}
		self.message = ""
		self.varis = np.zeros((3))
		self.vours = np.zeros((3))
		self.notes = np.zeros((3))





	#########################################################
	'''     Mode 1 - Evaluate ALL submitted solutions     '''
	#########################################################

	# make graduation of student implementations
	def all_functions_graduation(self):
		# search for all submitted student's functions
		files = self.find('SOM_*.py','./SOM_solutions')
		# graduation of each student's solution / each function
		for self.i,name in enumerate(files):
			print name
			self.one_function_graduation(name)



	#############################################
	###     Mode 1 - Additional functions     ###
	#############################################

	# search for all student functions
	def find(self, pattern, path):
		result = []
		for root, dirs, files in os.walk(path):
		    for name in files:
		        if fnmatch.fnmatch(name, pattern):
		            result.append(os.path.join(name))
		return result





	########################################################
	'''     Mode 2 - Evaluate ONE submitted solution     '''
	########################################################

	def one_function_graduation(self, funcname):
		func, self.user = self.user_function(funcname)
		SOM = self.upload_solution(func,True)
		self.message = ""
		for t in range(3):
			# define name of file with test-data
			#os.chdir('./SOM_tests')
			test = 'NRP_test'+str(t+1)+'_robot_position.csv'
			print test, ":"
			#os.chdir('..')


			variS = 0; variF = 0
			for e in range(self.N):
				print "Epoche", e

				# initialize crucial requirement from student's function
				# Function is compiling (work) and simulating within time limit (inlim)
				work = True; inlim = True

				# Evaluation of function based on one of tests
				# Function gives back a final variation achieved during a test  

				# import student's function and test data
				try: som = SOM(0,test) # som = SOM(Nn x Nn (lattice), tau, visualization, data file)
				except: work = False

				# set simulation time limit for the cases script doesn't work properly:
				# 1) script consists of endless loop
				# 2) script is simulating for a very long time
				signal.signal(signal.SIGALRM, self.handler)
				signal.alarm(int(self.limit))
				T = time.time()

				# run simulation of test
				try: som.run_som()
				except Exception, exc: inlim = False
				signal.alarm(0) # disable alarm

				# Challenge if script was simulating properly during all simulation time
				# if script was interrupted because of time limit, the current result had been saved for evaluation and graduation (work = True)
				# if script was interrupted before time limit it means there is another error of simulation (work = False)
				if(time.time()-T < self.limit and inlim==False): work = False; inlim = True

				# calculate variation of given test result
				if(work):     # Script was working properly or not (within time limit or not) 

					if(inlim): 	self.message += str(t+1) + ") Program worked properly and it has been estimated.  "
					else: 		self.message += str(t+1) + ") Program had been interrupted by time limit but a current result was estimated.  "

					# Estimate SOM by test
					from SOM_evaluation import SOM_evaluation
					somev = SOM_evaluation()
					vF, Nn = somev.run_evaluation()
					variF += vF/self.N

					# Estimate the reference solution
					from SOM_solution import SOM_solution
					soms = SOM_solution(Nn,0,test)
					soms.run_som()
					vS, Nn = somev.run_evaluation()
					variS += vS/self.N

				else:         # Script doesn't work / doesn't work properly
					# put punished value
					variF += 1000.0/self.N
					variS += 4.5/self.N
					self.message += str(t+1) + ") Program failed during simulation.  "

			# Notes
			self.note(t, variF, variS)
		
		# Save graduation
		self.save_graduation()



	#############################################
	###     Mode 2 - Additional functions     ###
	#############################################

	# extract function and student's names from file name
	def user_function(self, name):
		func = name.replace(".py", "")
		user = func.replace("SOM_", "")
		user = user.replace("_", " ")
		return func, user
		

	# upload function with student's solution
	def upload_solution(self, func, rank):
		if(rank): os.chdir('./SOM_solutions')
		module = importlib.import_module(func)
		SOM = getattr(module, 'SOM')
		if(rank): os.chdir('..')
		return SOM


	# define that test simulation time is over
	def handler(self, signum, frame):
		raise Exception("end of time")


	# find corresponding number of points
	def note(self, t, variF, variS):
		self.varis[t] = variF
		self.vours[t] = variS
		var = variF/variS
		
		if  (var < self.standard[0]): 	self.notes[t] = 6
		elif(var < self.standard[1]): 	self.notes[t] = 5
		elif(var < self.standard[2]): 	self.notes[t] = 4
		elif(var < self.standard[3]): 	self.notes[t] = 3
		elif(var < self.standard[4]): 	self.notes[t] = 2
		elif(var < self.standard[5]): 	self.notes[t] = 1
		else:                    		self.notes[t] = 0
		
		print "Result: ", variF,"/", variS,"=", var, self.notes[t]


	# save graduation results into file
	def save_graduation(self):
		# write evaluation of student results to file
		if os.path.isfile('SOM_graduation.csv'): mode = 'a'
		else: mode = 'w'

		# prepare data to write into file
		total = round((sum(self.notes)/3),1)
		export_data = [	self.user, 	str(round(self.varis[0],4)) + ' / ' + str(round(self.vours[0],4)),\
									str(round(self.varis[1],4)) + ' / ' + str(round(self.vours[1],4)),\
									str(round(self.varis[2],4)) + ' / ' + str(round(self.vours[2],4)),\
						self.notes[0], self.notes[1], self.notes[2], total, self.message]

		# write data into file
		with open('SOM_graduation.csv', mode) as myfile:
			wr = csv.writer(myfile)
			if(mode == 'w'): wr.writerow((	"Student name:", 	"Test 1 (you / us)",\
																"Test 2 (you / us)",\
																"Test 3 (you / us)",\
											"Note 1", "Note 2", "Note 3", "Final", "Comment"))
			wr.writerow(export_data)
		myfile.close()



	################################################
	###     HTML - Ranking table of students     ###
	################################################

	def sort_ranking(self):
		ifile =open('SOM_graduation.csv', 'rb')
		infile = csv.reader(ifile)
		# The first entry is the header line
		infields = infile.next()
		statindex = infields.index('Final')
		# create the sorted list
		sortedlist = sorted(infile, key=operator.itemgetter(statindex), reverse=True)
		ifile.close
		# open the output file - it can be the same as the input file
		ofile = open('SOM_graduation.csv', 'wb')
		# write the header
		outfile = csv.writer(ofile)
		outfile.writerow(infields)
		# write the sorted list
		for row in sortedlist:
			outfile.writerow(row)
		# processing finished, close the output file
		ofile.close()

	
	def create_html(self):
		with open('./HTML_Table/SOM_ranking_table.html', 'w') as the_file:
			the_file.write('<!DOCTYPE html>\n')
			the_file.write('<html lang="en">\n')

			#HTML start
			the_file.write('<!DOCTYPE html>\n')
			the_file.write('<html lang="en">\n')
			the_file.write('<head>\n')
			the_file.write('<title>Table V03</title>\n')
			the_file.write('<meta charset="UTF-8">\n')
			the_file.write('<meta name="viewport" content="width=device-width, initial-scale=1">\n')
			the_file.write('<link rel="icon" type="image/png" href="images/icons/favicon.ico"/>\n')
			the_file.write('<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">\n')
			the_file.write('<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">\n')
			the_file.write('<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">\n')
			the_file.write('<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">\n')
			the_file.write('<link rel="stylesheet" type="text/css" href="vendor/perfect-scrollbar/perfect-scrollbar.css">\n')
			the_file.write('<link rel="stylesheet" type="text/css" href="css/util.css">\n')
			the_file.write('<link rel="stylesheet" type="text/css" href="css/main.css">\n')
			the_file.write('</head>\n')

			the_file.write('<body>\n')
			the_file.write('<div class="limiter">\n')
			the_file.write('<div class="container-table100">\n')
			the_file.write('<div class="wrap-table100">\n')
			the_file.write('<div class="table100 ver2 m-b-110">\n')

			# begin the table
			infile = open("SOM_graduation.csv","r")

			the_file.write('<table data-vertable="ver2">\n')
			for i,line in enumerate(infile):
				row = line.split(",")
				student = row[0]
				test1 = row [1]
				test2 = row[2]
				test3 = row[3]
				note1 = row[4]
				note2 = row[5]
				note3 = row[6]
				final = row[7]
				comment = row[8]

				if(i==0):
				    the_file.write('<thead>\n')
				    the_file.write('<tr class="row100 head">\n')
				    the_file.write('<th class="column100 column1" data-column="column1">%s</th>\n' % student)
				    the_file.write('<th class="column100 column2" data-column="column2">%s</th>\n' % test1)
				    the_file.write('<th class="column100 column3" data-column="column3">%s</th>\n' % test2)
				    the_file.write('<th class="column100 column4" data-column="column4">%s</th>\n' % test3)
				    the_file.write('<th class="column100 column5" data-column="column5">%s</th>\n' % note1)
				    the_file.write('<th class="column100 column6" data-column="column6">%s</th>\n' % note2)
				    the_file.write('<th class="column100 column7" data-column="column7">%s</th>\n' % note3)
				    the_file.write('<th class="column100 column8" data-column="column8">%s</th>\n' % final)
				    the_file.write('<th class="column100 column9" data-column="column9">%s</th>\n' % comment)
				    the_file.write('</tr>\n')
				    the_file.write('</thead>\n')

				if(i>0):
				    if(i==1): the_file.write('<tbody>\n')
				    the_file.write('<tr class="row100">\n')
				    the_file.write('<td class="column100 column1" data-column="column1">%s</td>\n' % student)
				    the_file.write('<td class="column100 column2" data-column="column2">%s</td>\n' % test1)
				    the_file.write('<td class="column100 column3" data-column="column3">%s</td>\n' % test2)
				    the_file.write('<td class="column100 column4" data-column="column4">%s</td>\n' % test3)
				    the_file.write('<td class="column100 column5" data-column="column5">%s</td>\n' % note1)
				    the_file.write('<td class="column100 column6" data-column="column6">%s</td>\n' % note2)
				    the_file.write('<td class="column100 column7" data-column="column7">%s</td>\n' % note3)
				    the_file.write('<td class="column100 column8" data-column="column8">%s</td>\n' % final)
				    the_file.write('<td class="column100 column9" data-column="column9">%s</td>\n' % comment)
				    the_file.write("</tr>")

			the_file.write('</tbody>\n')
			the_file.write('</table>\n')
			# end the table

			the_file.write('</div>\n')
			the_file.write('</div>\n')
			the_file.write('</div>\n')
			the_file.write('</div>\n')

			the_file.write('<script src="vendor/jquery/jquery-3.2.1.min.js"></script>\n')
			the_file.write('<script src="vendor/bootstrap/js/popper.js"></script>\n')
			the_file.write('<script src="vendor/bootstrap/js/bootstrap.min.js"></script>\n')
			the_file.write('<script src="vendor/select2/select2.min.js"></script>\n')
			the_file.write('<script src="js/main.js"></script>\n')

			the_file.write('</body>\n')
			the_file.write('</html>\n')
			#HTML end

	
	def open_webpage(self):
		self.sort_ranking()
		self.create_html()
		
		import webbrowser, os
		webpage = webbrowser.open('./HTML_Table/SOM_ranking_table.html')
