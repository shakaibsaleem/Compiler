def removeTabs(stream):
	new = ""
	for i in range(len(stream)):
		char = stream[i]
		# ignore tab characters, keep rest
		if char != '\t':
			new = new + char
	return new

def removeCommentLines(stream):
	new = ""
	ignore = False
	for i in range(len(stream)):
		char = stream[i]

		# detect when comment starts
		if char == '#':
			ignore = True # start ignoring input stream

		# detect when comment block ends
		if char == '\n' and ignore == True:
			ignore = False # stop ignoring input stream
		
		# ignore input stram or not
		if ignore == False:
			new = new + char
	return new

def removeBlockComments(stream):
	new = ""
	ignore = False
	line = 1 # line counter
	start_line = 0 # to record which line our comment block started from

	for i in range(len(stream)):
		if stream[i] == '\n':
			line += 1 # count lines

		# detect when comment block starts
		if stream[i:i+2] == '/*':
			ignore = True # start ignoring input stream
			start_line = line # record line number

		# detect when comment block ends
		if stream[i-2:i] == '*/' and ignore == True:
			ignore = False # stop ignoring input stream

		# ignore input stram or not
		if ignore == False:
			new = new + stream[i]
		elif stream[i] == '\n':
			# if newline character is encountered in a comment block, then dont ignore it
			new = new + stream[i]

	if ignore == True:
		# if last detected comment block was not ended then error
		writeError(start_line,"End of comment block (*/) is missing for the comment started in line %d" %start_line)

	return new

def writeError(line,message):
	with open(filename + ".err",'a') as log:
			log.write(str(line) + " - " + message + "\n")

def main(filename):
	'''tokeniser sample'''
	with open(filename+'.huc') as file:
		stream = file.read()

	# tokens = stream.splitlines()
	# new = [t.split(" ") for t in tokens]

	stream = removeTabs(stream)
	stream = removeCommentLines(stream)
	stream = removeBlockComments(stream)

	token_list = ['}', 'void', '!=', '>=', 'public', '[', '{', 'var', ',', 'let', 'private', '-', '++', '<', 'elseif', ']', '>', '!', '<=', '+', 'while', 'bool', ')', 'for', 'float', 'str', 'this', '&', 'else', 'constructor', 'call', 'return', '//', '==', 'class', 'method', '**', '%', ';', '(', '=', '.', '|', 'if', 'int', '/', 'function', '*']

	tokens = stream.split()
	# print(tokens)

	unrecognised = list()
	for t in tokens:
		if t not in token_list:
			unrecognised.append(t)

	# print(unrecognised)
	print(set(unrecognised)) # interpret these

	symbol_table = dict()

filename = "snippet"

# initialise error file
error_file = open(filename + ".err",'w')
error_file.close()

main(filename)
