def main():
	'''tokeniser sample'''
	with open('snippet.huc') as file:
		stream = file.read()
	# print(stream)
	# tokens = stream.splitlines()
	# print(tokens)

	# tokens = stream.split(" ")
	# new = [t.split(" ") for t in tokens]
	# print(new)

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
	for i in range(len(stream)):
		if stream[i:i+2] == '/*':
			ignore = True

		if stream[i-2:i] == '*/' and ignore == True:
			ignore = False
			# i+=1
		if ignore == False:
			new = new + stream[i]
	if ignore == True:
		
	stream = new
	
	print(stream)
main()
