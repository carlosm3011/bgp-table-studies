#!/usr/bin/python -W ignore
"""
ixpAnalysis: Simple tool to perform different analysis on IXP routing tables
(c) carlos@lacnic.net, 20180313
"""
from __future__ import print_function
import csv
import sys
import ipaddr
# from ipwhois import IPWhois, WhoisRateLimitError
import pickle
import fire

class ixpAnalysis:

	uniq_pfx = {}
	ixp_asn = {}
	line_count = 0

	def load(self, f_t):
		# try:
		# 	with open(f_t, "rb") as f:
		# 		self = pickle.load(f)
		# except FileNotFoundError:
		# 	self.uniq_pfx = {}
		pass
	## end load

	def save(self, f_t):
		try:
			with open(f_t, "wb") as f:
				pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
		except:
			raise
	## end save

	# count an ASN
	def add_asn(self, asn_t):
		self.ixp_asn[asn_t] = self.ixp_asn.get(asn_t, {'count': 0, 'country': None} )
		self.ixp_asn[asn_t]['count'] = self.ixp_asn[asn_t]['count'] + 1
		if self.ixp_asn[asn_t]['count'] == 1:
			# el as es nuevo
			pass
		# print("ASN: ", asn_t, " count ", self.ixp_asn[asn_t]['count'])
		self.line_count = self.line_count + 1
		return self.ixp_asn[asn_t]['count']
	## end add_asn

	## get ASNs
	def get_asns(self, threshold):
		r = []
		for y in self.ixp_asn.keys():
			if self.ixp_asn[y]['count'] >= threshold:
				r.append(y)
		return r
	## end get ASNs

	# count a prefix
	def add_pfx(self, pfx_t):
		# pfx_t = r[7]

		pfx_n = ipaddr.IPNetwork(pfx_t)

		if pfx_n.version == 4:
			self.uniq_pfx[pfx_n] = self.uniq_pfx.get(pfx_n, {'count': 0, 'country': None} )
			self.uniq_pfx[pfx_n]['count'] = self.uniq_pfx[pfx_n]['count'] + 1

			if self.uniq_pfx[pfx_n]['count'] == 1:
				print("Pfx: ", pfx_t," - country code: ", self.uniq_pfx[pfx_n]['country'], " log: ", msg)
		#
		self.line_count = self.line_count + 1

		return self.uniq_pfx[pfx_n]['count']
	## end add_pfx

## end ixpAnalysis

def main(outfile = "-", criterion="1", threshold="10"):
	ixpP = ixpAnalysis()

	reader = csv.reader(sys.stdin, delimiter='|')

	# counting engine
	for r in reader:
		try:
			# pfx_t = r[7]
			peer_asn_t = r[5].strip() # field 5: peer asn
			field_t = r[9].strip() #field 9: as path
			origin_asn_t = r[10].strip() # field 11: origin asn
			as_path = field_t.split(" ")
			# print("origin asn ", origin_asn_t," - aspath: ", as_path)
			try:
				# we count an asn as "local" to ptt.sp if the originating as y either first or
				# second in the AS_PATH.
				if criterion == 1:
					if (as_path.index(origin_asn_t) == 0 or as_path.index(origin_asn_t) == 1):
						c = ixpP.add_asn(origin_asn_t)
						print("origin asn ", origin_asn_t," - aspath: ", as_path, "- count: ", c)
				elif criterion == 2:
					c = ixpP.add_asn(as_path[0])
					if (c==1):
						print("new ixp_asn (crit=2) asn ", as_path[0]," - aspath: ", as_path, "- count: ", c)
				elif criterion == 3:
					if (as_path.index(origin_asn_t) == 0 or as_path.index(origin_asn_t) == 1) and len(as_path)<=2:
						c = ixpP.add_asn(origin_asn_t)
						if (c==1):
							print("new ixp_asn (crit=3) asn ", origin_asn_t," - aspath: ", as_path, "- count: ", c)
				else:
					print("Unknown classification criteria!")
					sys.exit(-1)
			except ValueError:
				print("not in list: ", origin_asn_t)
				continue
			except:
				raise
		except IndexError:
 			continue
	# end for

	# print results
	print(" ")
	print("Summary results:")
	print("  - Number of different ASes: ", len(ixpP.ixp_asn.keys()) )
	print("  - Numer of lines read: ", ixpP.line_count)

	# if not stdout, open file
	f = None
	if outfile == "-":
		f = sys.stdout
	else:
		f = open(outfile, "w")

	L = ixpP.get_asns(threshold)
	f.write("# ---- cut here ----\n")
	f.write("#  - Numer of lines read: %s\n" %  (ixpP.line_count) )
	f.write("#  - Number of different ASes: %s\n" % ( len(L) ) )
	for x in L:
		f.write("%s | %s\n" % (x, ixpP.ixp_asn[x]['count']) ) 
	f.write("# ---- cut here ----\n")
	if outfile != "-":
		f.close()
# end main

if __name__ == "__main__":
	fire.Fire(main)
	# main()

## END MAIN
