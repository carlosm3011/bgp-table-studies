#!/usr/bin/env python
# ----------------------------------------------------------------
# SIMPLEWHOIS: (c) carlos@lacnic.net 20180313
#
# v0.1: Simple queries via command line
# ----------------------------------------------------------------

import ipaddr
import sqlite3
import click
import sys

## A VERY SIMPLE WHOIS
class SimpleWhois(object):

    dbcon = None
    dbcur = None

    def __init__(self, w_dbname):
        """Default constructor. Takes DB filename as single parameter"""
        try:
            self.dbcon = sqlite3.connect(w_dbname)
            self.dbcon.row_factory = sqlite3.Row
            self.dbcon.execute("PRAGMA cache_size=200000")
            self.dbcur = self.dbcon.cursor()
        except:
            raise

    def autnum(self, q):
        """
        Query autnums. Returns a single row.
        :todo: check the case where ASN could be within a range
        """
        r = self.dbcur.execute("SELECT * FROM numres WHERE type='asn' AND block=?", (q,) )
        p = r.fetchone()
        if p == None:
            return None
        else:
            return dict(p)
    ## end autnum

    def ip(self, q):
        try:
            n1 = ipaddr.IPv4Network(q)
            # query ipv4
            (s,e) = (int(n1.network), int(n1.broadcast))
            r = self.dbcur.execute("SELECT * FROM numres WHERE type='ipv4' and (istart<=? and ?<=iend)", (s,e))
            p = r.fetchone()
            if p != None:
                return dict(p)
            else:
                return None
        except ValueError:
            pass
        #
        try:
            n1 = ipaddr.IPv6Network(q)
            # query ipv6
            (s,e) = (int(n1.network)/pow(2,64), int(n1.broadcast)/pow(2,64))
            r = self.dbcur.execute("SELECT * FROM numres WHERE type='ipv6' and (istart<=? and ?<=iend)", (s,e))
            p = r.fetchone()
            if p != None:
                return dict(p)
            else:
                return None
        except ValueError:
            pass
        except:
            return None
        #
        return None
    ## end ip
## END SIMPLE WHOIS

if __name__ == "__main__":
    print "Not to be run directly!"
