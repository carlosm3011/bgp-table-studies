#!/usr/bin/env python

"""
Analysis pipeline
"""
from __future__ import print_function
import csv
import os
import urlparse
from consecution import Node, Pipeline

class risFetcher(Node):
    def process(self, item):
        print('{: >15} processing {}'.format(self.name, item))  
        #
        #
        self.push(item)


class tableAnalysisNode(Node):
    #
    def process(self, item):
        print('{: >15} processing {}'.format(self.name, item))  
        #
        scr_tpl = """
        bgpreader -w $(date +%s --date='Mar 16, 2010 0:00utc'),$(date +%s --date='Mar 16, 2018 0:00utc') \
            -d singlefile -p ris -o rib-file,data/ris/{ifile} {filters} | \
            ./ixpAnalysis.py --outfile=data/{ofile} --criterion=3 --threshold=25
        """
        #
        # filters = "-k 200.0.0.0/13"
        filters = ""
        a = urlparse.urlparse(item[2])
        ifile = os.path.basename(a.path)
        ofile = "asn.gru.{date}.csv".format(date=item[0])
        scr = scr_tpl.format(ifile=ifile, ofile=ofile, filters=filters)
        # print(scr)
        os.system(scr)
        #
        self.push([item[0], ofile])

class simpleWhoisNode(Node):
    #
    def process(self, item):
        print('{: >15} processing {}'.format(self.name, item))
        #
        scr_tpl = """
        ./simplewhois.py bulk_query --outfile=data/{ofile} < data/{ifile} 
        """
        ifile = item[1]
        ofile = "asn.gru.cc.{date}.csv".format(date=item[0])
        scr = scr_tpl.format(ifile=ifile, ofile=ofile)
        # print(scr)
        os.system(scr)
        #
        self.push( [item[0], ofile] )

class concatenator(Node):
    #
    def begin(self):
        os.system("rm -f data/asn.gru.consolidated.csv && touch data/asn.gru.consolidated.csv")
        os.system("echo 'date | asn | count | cc' > data/asn.gru.consolidated.csv")
    #
    def process(self, item):
        print('{: >15} processing {}'.format(self.name, item))
        #
        scr_tpl = """
            # cat data/asn.gru.consolidated.csv data/{ifile} > /tmp/conso.csv
            awk '{{print {date}, "|", $0 }}' data/{ifile} > /tmp/withdate.csv
            cat data/asn.gru.consolidated.csv /tmp/withdate.csv > /tmp/conso.csv
            mv /tmp/conso.csv data/asn.gru.consolidated.csv
        """
        scr = scr_tpl.format(date=item[0], ifile=item[1])
        os.system(scr)
        # print(scr)
        #
        self.push(item)


# Define pipeline
pipe = Pipeline( 
    risFetcher('ris_file_fetcher') | 
    tableAnalysisNode('table_analysis') | 
    simpleWhoisNode('add_cc_data' ) |
    concatenator('concatenator')
)

pipe.plot()

# pipe.consume(range(5))

with open("source_files.csv", "r") as f:
    sfreader = csv.reader(f, delimiter="|")
    pipe.consume(sfreader)
