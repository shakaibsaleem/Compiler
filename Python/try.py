def main(filename):
	'''tokeniser sample'''
	with open(filename+'.huc') as file:
		stream = file.read()

	# tokens = stream.splitlines()
	# new = [t.split(" ") for t in tokens]

	new = ""
	for i in range(len(stream)):
		char = stream[i]

		if char != '\t':
			new = new + char
	stream = new
	
	new = ""
	ignore = False
	for i in range(len(stream)):
		char = stream[i]

		if char == '#':
			ignore = True
		if char == '\n' and ignore == True:
			ignore = False
		if ignore == False:
			new = new + char
	stream = new
	
	# print(stream)

	new = ""
	ignore = False
	line = 1 # line counter
	start_line = 0 # to record which line our comment block started from

	for i in range(len(stream)):
		if stream[i] == '\n':
			line += 1 # count lines

		# detect when comment block starts
		if stream[i:i+2] == '/*':
			ignore = True # start ignoting input stream
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
		with open(filename + ".err",'w') as log:
			log.write("%d - End of comment block (*/) is missing for the comment started in line %d" %(start_line,start_line))
	stream = new
	
	# print(stream)
main("snippet")
