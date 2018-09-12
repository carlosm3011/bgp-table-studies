from consecution import Node,Pipeline
from os import system
from os import path
import os
import time

def dateToEpoch(wdate):
	# hiredate= '1981-06-03'
	pattern = '%Y%m%d'
	epoch = int(time.mktime(time.strptime(wdate, pattern)))
	return epoch
# end defToEpoch

def shouldIProcessFile(wfile):
	try:
		fstat = os.stat(wfile)
		if fstat.st_size > 10000 :
			return False
		else:		
			return True
	except:
		return True
# end checkFileStatus

class fetchNode(Node):
	def process(self,item):
		# print item
		fname = "ipv6_lacnic_visible_%s.csv" % (item)
		if shouldIProcessFile(fname):
			tstart = dateToEpoch(item)
			tend = tstart + 86400
			cmd =  "bgpreader -d broker -w {0},{1} -p ris -c rrc00 -t ribs -k 2001:1200::/23 -k 2800::/12 | pv -pt > {2}".format(tstart,tend,fname) 
			print "Running %s" % (cmd)
			system(cmd)
		else:
			print "File %s already exists" % (fname)
		self.push(item)
# end fetchnode


class extractFields(Node):
	def process(self,item):
		# head -50 ipv6_lacnic_visible_20170101.csv  | awk -F'|' '{print $6,"\t",$8,"\t"101}' | sort -u | wc -l
		ifname = "ipv6_lacnic_visible_%s.csv" % (item)
		ofname = "ipv6_lacnic_stage2_%s.csv" % (item)
		if shouldIProcessFile(ofname):
			cmd = ""
		pass
# end class extractfields

if __name__ == "__main__":
	pipe = Pipeline(fetchNode('ris'))
	print pipe
	# pipe.consume(['20130320', '20130327', '20130401'])
	print "Reading targets from file targets.txt"
	targetsfile = open("targets.txt", "r")
	targets = []
	for l in targetsfile:
		targets = targets + [l.strip()]
	#
	# Launch pipeline
	print targets
	pipe.consume(targets)
