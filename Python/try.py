def main():
	'''tokeniser sample'''
	with open('snippet.huc') as file:
		stream = file.read()
	# print(stream)
	tokens = stream.splitlines()
	print(tokens)

	# tokens = stream.split(" ")
	# new = [t.split(" ") for t in tokens]
	# print(new)

main()