import re
import glob

def removeTabs(stream):
	new = ""
	isString = False
	for i in range(len(stream)):
		char = stream[i]

		if char == '"' :
			if not isString:
				isString = True
			else:
				isString = False

		# ignore tab characters, keep rest
		if char != '\t':
			new = new + char
		elif isString:
			new = new + char
	return new

def removeCommentLines(stream):
	new = ""
	ignore = False
	isString = False
	for i in range(len(stream)):
		char = stream[i]

		if char == '"' :
			if not isString:
				isString = True
			else:
				isString = False

		# detect when comment starts
		if char == '#' and not isString:
			ignore = True # start ignoring input stream

		# detect when comment block ends
		if char == '\n' and ignore == True and not isString:
			ignore = False # stop ignoring input stream
		
		# ignore input stram or not
		if ignore == False:
			new = new + char
	return new

def removeBlockComments(stream):
	new = ""
	ignore = False
	isString = False
	line = 1 # line counter
	start_line = 0 # to record which line our comment block started from

	for i in range(len(stream)):
		if stream[i] == '\n':
			line += 1 # count lines

		if stream[i] == '"' :
			if not isString:
				isString = True
			else:
				isString = False

		# detect when comment block starts
		if stream[i:i+2] == '/*' and not isString:
			ignore = True # start ignoring input stream
			start_line = line # record line number

		# detect when comment block ends
		if stream[i-2:i] == '*/' and ignore == True and not isString:
			ignore = False # stop ignoring input stream

		# ignore input stram or not
		if ignore == False:
			new = new + stream[i]
		elif stream[i] == '\n':
			# if newline character is encountered in a comment block, then dont ignore it
			new = new + stream[i]

	if ignore == True:
		# if last detected comment block was not ended then error
		writeError(start_line,"End of comment block (*/) is missing for the comment started in line %d" %start_line,filename)

	return new

def writeError(line,message,myfile):
	with open(myfile + ".err",'a') as log:
			log.write("Line: "+str(line) + " - " + message + "\n")

def main(filename):
	'''tokeniser sample'''

	# initialise error file
	error_file = open(filename + ".err",'w')
	error_file.close()

	with open(filename+'.huc') as file:
		stream = file.read()

	# tokens = stream.splitlines()
	# new = [t.split(" ") for t in tokens]

	stream = removeTabs(stream)
	stream = removeCommentLines(stream)
	stream = removeBlockComments(stream)

	symbol_table = dict()
	str_count = 0
	no_strings = ""
	isString = False
	line = 1
	start_line = 0
	for i in range(len(stream)):
		char = stream[i]
		if char == '\n':
			line += 1
		if char == '"':
			if not isString:
				isString = True
				current = ""
				start_line = line
			else:
				isString = False
				current += char
				str_count += 1
				symbol_table[current] = "STR,"+str(str_count)
				continue
		if not isString:
			no_strings += char
		else:
			current += char
	if isString:
		writeError(start_line,'End of string literal (") is missing for the string started in line %d' %start_line,filename)

		#######################################################
		######    ERROR RECOVERY STRATEGY NUMBER TWO     ######
		#######################################################
		current += '"' # inserting missing character

		symbol_table[current] = "STR,"+str(str_count)

	token_list = ['}', 'void', '!=', '>=', 'public', '[', '{', 'var', ',', 'let', 'private', '-', '++', '<', 'elseif', ']', '>', '!', '<=', '+', 'while', 'bool', ')', 'for', 'float', 'str', 'this', '&', 'else', 'constructor', 'call', 'return', '//', '==', 'class', 'method', '**', '%', ';', '(', '=', '.', '|', 'if', 'int', '/', 'function', '*', 'true', 'false']

	tokens = no_strings.split()
	# print(tokens)

	unrecognised = list()
	for t in tokens:
		if t not in token_list:
			unrecognised.append(t)
	# print(unrecognised)
	# print(set(unrecognised)) # interpret these

	######      HERE     #######
	symbols = list(set(unrecognised))

	int_count = 0
	float_count = 0
	id_count = 0

	for s in symbols:
		if isInt(s):
			int_count += 1
			symbol_table[s] = "INT,"+str(int_count)
		elif isFloat(s):
			float_count += 1
			symbol_table[s] = "FLOAT,"+str(float_count)
		elif isIdentifier(s):
			id_count += 1
			symbol_table[s] = "ID,"+str(id_count)
		# else:
		# 	print("Error",s)
	
	# for key, value in symbol_table.items():
		# print(key+":",value)
		# print(value,key)
	# print(symbol_table)
	# print(stream)
	# input("\n?")

	current = ""
	out = ""
	isString = False
	ignore = False
	line = 1
	for i in range(len(stream)):
		char = stream[i]

		if char == '"' :
			if not isString:
				isString = True
			else:
				isString = False

		if char.isspace() and not isString:
			if current in token_list:
				out += "<"+current+">\n"
			elif current in symbol_table.keys():
				out += "<"+symbol_table[current]+">\n"
			elif current == "":
				pass 
			else:
				writeError(line,"Illegal literal: '"+current+"'",filename)

				#######################################################
				######    ERROR RECOVERY STRATEGY NUMBER ONE     ######
				#######################################################
				
				# not inserting a token for current into out
				# panic mode recovery: deleting characters till next recognisable token (basically till next separator character is found)

			# print(current,line)
			current = ""
		else:
			current += char

		if char == '\n':
			line += 1

	with open(filename+'.out','w') as token_file:
		token_file.write(out)
	with open(filename+'.sym','w') as symbol_file:
		for key,value in symbol_table.items():
			symbol_file.write(value + "\t-\t" + key + '\n')

def isIdentifier(arg):
	pattern = re.compile('^[A-Za-z][A-Za-z0-9_]*$')
	result = pattern.match(arg)
	return bool(result)

def isFloat(arg):
	pattern = re.compile('^([+-]?\d+\.\d+)([\e][+-]?[\d]+)?$')
	result = pattern.match(arg)
	return bool(result)

def isInt(arg):
	if len(arg) == 0:
		return False
	char = arg[0]
	if char not in ["-","+",'0','1','2','3','4','5','6','7','8','9']:
		return False
	for char in arg[1:]:
		if char not in ['0','1','2','3','4','5','6','7','8','9']:
			return False
	return True

# filename = "snippet"
# filename = "MergeSort"
# main(filename)

def getFiles():
	'''get list of all ".huc" files fron current directory'''
	return glob.glob("*.huc")

files = getFiles()
for filename in files:
	# print(filename[:-4])
	main(filename[:-4])

