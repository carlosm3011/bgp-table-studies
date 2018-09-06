from consecution import Node,Pipeline
from os import system
import time

def dateToEpoch(wdate):
	# hiredate= '1981-06-03'
	pattern = '%Y%m%d'
	epoch = int(time.mktime(time.strptime(wdate, pattern)))
	return epoch
# end defToEpoch

class fetchNode(Node):
	def process(self,item):
		# print item
		tstart = dateToEpoch(item)
		tend = tstart + 86400
		cmd =  "bgpreader -d broker -w {0},{1} -p ris -c rrc00 -t ribs -k 2001:1200::/23 -k 2800::/12 | tee ipv6_lacnic_visible_{2}.csv".format(tstart,tend,item) 
		print "Running %s" % (cmd)
		system(cmd)
		self.push(item)
# end fetchnode

if __name__ == "__main__":
	pipe = Pipeline(fetchNode('ris'))
	print pipe
	pipe.consume(['20130320', '20130327', '20130401'])
