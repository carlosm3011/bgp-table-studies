#!/usr/bin/env python
# ----------------------------------------------------------------
# SIMPLEWHOIS: (c) carlos@lacnic.net 20180313,20180905
#
# v0.2: Simple queries via command line
# ----------------------------------------------------------------

import unittest
import sqlite3
import click
import sys

from SimpleWhois.SimpleWhois import SimpleWhois

_VERSION = "0.2"
_AUTHOR = "carlos@lacnic.net"

@click.group()
def cli():
    pass

@cli.command()
@click.option('--query', help='query string (asn, ip block)')
@click.option('--db', type=click.Path(exists=True), default="/data/netdata/netdata-20180308.db", help="DB file to use")
def autnum(query):
    # global sw
    sw = SimpleWhois(db)
    click.echo("AUTNUM query: %s" % (query) )
    r = sw.autnum(query)
    if r != None:
        click.echo(" R: %s" % ( dict(r) ) )
    else:
        click.echo("No results")
## end autnum

@cli.command()
@click.option('--query', help='query string (asn, ip block)')
@click.option('--db', type=click.Path(exists=True), default="/data/netdata/netdata-20180308.db", help="DB file to use")
def ip(query, dbname):
    sw = SimpleWhois(db)
    click.echo("IP query: %s" % (query) )
    r = sw.ip(query)
    if r != None:
        click.echo(" R: %s" % ( dict(r) ) )
    else:
        click.echo("No results")
## end ip

@cli.command()
@click.option('--fields', default='cc', help="List of fields to include, separated by commas")
@click.option('--outfile', default='-', help="Output file name, use - for stdout")
@click.option('--type', default='autnum', help="Content of the file, can be autnum or ip")
@click.option('--filter', default=None, help="%experimental% filter lines by rir")
@click.option('--db', type=click.Path(exists=True), default="/data/netdata/netdata-20180308.db", help="DB file to use")
def bulk(fields, outfile, type, filter, db):
    """
    Read a list of ASNs or IP resources from STDIN and return SW info on STDOUT.
    """
    # global sw
    sw = SimpleWhois(db)

    f = None
    if outfile == "-":
        f = sys.stdout
    else:
        f = open(outfile, "w")

    for line in sys.stdin:
        line = line.strip()
        if line.find("#") != 0: #if comment, skip
            parts = line.split("|")
            if line == "": # break on empty line
                break
            if type == "autnum":
                r = sw.autnum(parts[0].strip())
            elif type == "ip":
                r = sw.ip(parts[0].strip())
            else:
                break
            if r != None:
                # f.write("%s | %s\n" % (line, r[fields]))
                # f.write("%s | %s\n" % (line, {k: r[k] for k in fields.split(",")} ))
                if filter == None or (r['rir']==filter):
                    q = [line] + [str(r[k]) for k in fields.split(",")] 
                    f.write("|".join(q))
                    f.write("\n")
                #f.write(str(q))
            else:
                f.write("%s | %s\n" % (line, None) )

    if outfile != "-":
        f.close()
    return True
## end bulk query

if __name__ == "__main__":
    # sw = SimpleWhois("/data/netdata/netdata-20180308.db")
    click.echo( "SimpleWhois: %s, (c) %s\n" % (_VERSION, _AUTHOR) )
    cli()
    sys.exit()

## end simple whois
