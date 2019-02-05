def main():
	'''tokeniser sample'''
	with open('snippet.huc') as file:
		stream = file.read()

	# tokens = stream.split(" ")
	tokens = stream.splitlines()
	new = [t.split(" ") for t in tokens]
	# print(stream)
	# print(tokens)
	print(new)

main()