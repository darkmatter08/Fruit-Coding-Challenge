#!/usr/bin/env python

# Shantanu Jain
# 10/26/2014
# Fruit Coding Challenge

import sys, json

def handleQuestion(question):
	""" Question is a JSON-style dictionary, that must have
		a 'question' key that defines the question, and optionally
		a 'choices' key that represents the 'select one' options for the 
		question. It contains a list of dicts, each dict with a required 
		key of 'choice', and optionally a key of 'follow-ups' that 
		represents additional questions to query the user in case that 
		option is selected.
		Returns a list, representing the responses of the user.
		Interacts with the user using stdin/stdout (CLI).
	"""
	inputFunc = raw_input
	print '\n', question['question']
	if 'choices' in question:
		inputFunc = input # parse input as ints instead of strs.
		for i in range(len(question['choices'])):
			print str(i) + ')', question['choices'][i]['choice']
	response = inputFunc()

	if 'choices' in question and \
		'follow-ups' in question['choices'][response]:
		followUpQuestions = question['choices'][response]['follow-ups']
		followUpResponses = [handleQuestion(followUp) for followUp in followUpQuestions]
		
		# In JSON order matters, so the responses will be arranged 
		# according to the order they are listed in.
		response = [response, followUpResponses]

	return response

def fileToQuestions(questions_JSONFile):
	""" Takes a JSON file in the questions-options-followup format
		and returns a dictionary representation.
	"""
	commandFile = open(questions_JSONFile)
	rawJSON = commandFile.read()
	commandFile.close()
	return json.loads(rawJSON)

def askAndStoreResponses(inputFile, outputFile):
	# Get user's name
	nameQuestion = {'question': 'Please enter your full name (first and last):'}
	userName = handleQuestion(nameQuestion)

	# do questions from file
	questions = fileToQuestions(inputFile) 
	responses = [handleQuestion(item) for item in questions]

	addToResults(outputFile, userName, responses)

def addToResults(outputFile, userName, responses):
	# Grab and parse old JSON
	of = open(outputFile)
	oldRespondents = of.read()
	of.close()
	
	# Handle blank output file case
	allRespondents = {} if oldRespondents == '' else json.loads(oldRespondents)
	
	# Add new respondent and write to file
	allRespondents[userName] = responses
	allRespondentsJSON = json.dumps(allRespondents)
	of = open(outputFile, 'w')
	of.write(allRespondentsJSON)
	of.close()

if __name__ == '__main__':
	DEBUG = False
	if 0:
		addToResults('asdf', 'payal', ["aloo", 1, 2])
		addToResults('asdf', 'shawn', ['pizza', 'mac', 'linux'])
		addToResults('asdf', 'shivani', ['ice cream', 'windows', 'waubonsie'])
	else:
		if len(sys.argv) < 3 or sys.argv[1] == '--help' or sys.argv[1] == '-h':
			print "usage: cliExercise.py input.json results.json"
		else: 
			askAndStoreResponses(sys.argv[1], sys.argv[2])
	