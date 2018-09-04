#!/usr/bin/python3
import csv
import sys

reader = csv.reader(sys.stdin, delimiter='|')

asn_count = {}

for r in reader:
	try:
		asn = r[5]
		asn_count[asn] = asn_count.get(asn, 0) + 1
		if asn_count[asn] == 1:
			print("new asn: ", asn)
	except:
		continue
	# print('---')
	# c = 0
	# for x in r:
	# 	print(c, ' ', x)
	# 	c = c + 1

print("Results")
print(asn_count)
