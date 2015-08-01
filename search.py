import re
import string

invertedIndex = dict()
exclude = set(string.punctuation)
result = []
business = {}

def buildInvertedIndex(businessName, index):
	businessName = businessName.split(" ")
	for x in businessName:
		x = x.lower()
		x = x.strip()
		x = ''.join(ch for ch in x if ch not in exclude)
		if len(x) >= 3:
			if x in invertedIndex:
				if index not in invertedIndex[x]:
					invertedIndex[x].append(index)
			else:
				invertedIndex[x] = []
				invertedIndex[x].append(index)
	
def intersect(a, b):
     return list(set(a) & set(b))

def generateResult(query):
	global result
	try:
		result = invertedIndex[str(query[0]).lower().strip()]
	except KeyError:
		return

	size = len(query)
	for i in range(1,size):
		try:
			sec_list = invertedIndex[str(query[i]).lower().strip()]
			result = intersect(result, sec_list)
		except KeyError:
			pass

	
def printResult(fo):
	global result
	global business
	if not result:
		print "No business found"
	else:
		result = sorted(result)
		#print result
		index = 0
		size = len(result)
		for i in result:
			print business[i]


def SearchBusiness():
	global business
	global result
	fo = open("Result.txt","r")
	for i in range (1,2001):
		head = [next(fo) for x in xrange(6)]
		business[i] = head
		buildInvertedIndex( head[1].split("->")[1][:-1], i )
	query = raw_input()
	query = query.split(" ")
	if( len(query) == 1 ):
		try:
			result = invertedIndex[query[0].lower().strip()]
			print result
		except KeyError:
			pass
	else:
		generateResult(query)
	printResult(fo)
	fo.close()


if __name__ == "__main__":
	SearchBusiness()
