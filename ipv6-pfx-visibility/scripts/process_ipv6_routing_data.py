#!/usr/bin/env python2
from consecution import Node,Pipeline
from os import system
from os import path
import os
import time
import fire

def dateToEpoch(wdate):
	# hiredate= '1981-06-03'
	pattern = '%Y%m%d'
	try:
		epoch = int(time.mktime(time.strptime(wdate, pattern)))
		return epoch
	except:
		print "ERROR: invalid date {}".format(wdate)
		return 0
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

class initNode(Node):
	def process(self, item):
		self.push(item)

class fetchNode(Node):
	def process(self,item):
		# print item
		# last_item_digit = item[-1:]
		if self.name == "even" and (int(item) % 2 != 0):
			return
		fname = "/work/ipv6_lacnic_visible_%s.csv" % (item)
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
		ifname = "/work/ipv6_lacnic_visible_%s.csv" % (item)
		ofname = "/work/ipv6_lacnic_stage2_%s.csv" % (item)
		if shouldIProcessFile(ofname):
			cmd = """awk -F'|' '{{print $6,"\t",$8,"\t"101}}' {0} | sort -u > {1}""".format(ifname, ofname)
			print "Running %s" % (cmd)
			system(cmd)
		else:
			print "File %s already exists" % (ofname)
	
		pass
# end class extractfields

def main(targets):
	pipe = Pipeline( initNode('init') | [fetchNode('even'), fetchNode('odd')] | extractFields('extract fields'))
	print pipe
	# pipe.consume(['20130320', '20130327', '20130401'])
	print "Reading targets from file {}".format(targets)
	targetsfile = open(targets, "r")
	targets = []
	for l in targetsfile:
		targets = targets + [l.strip()]
	#
	# Launch pipeline
	print targets
	pipe.consume(targets)


if __name__ == "__main__":
	fire.Fire(main)
