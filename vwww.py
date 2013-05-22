#!/usr/bin/env python2.7

import os, sys, shutil
from markdown import markdownFromFile

IN_DIR = "in"
OUT_DIR = "out"

def print_err(s):
    sys.stderr.write("error: {0}\n".format(s))
    sys.exit(1)

def get_file_list(dirn):
    if not os.path.exists(dirn):
        print_err("non-existent directory: {0}".format(dirn))

    return [ x for x in os.listdir(dirn) if x.endswith(".md") ]

def read_template(dirn):
    hpath = os.path.join(dirn, "header.html")
    fpath = os.path.join(dirn, "footer.html")

    with open(hpath, "r") as h_hndl: h_str = h_hndl.read()
    with open(fpath, "r") as f_hndl: f_str = f_hndl.read()

    return (h_str, f_str)

def process_md(md, h_str, f_str, indir, outdir):
    outfilename = os.path.join(outdir, md[0:-3] + ".html")
    infilename = os.path.join(indir, md)

    with open(outfilename, "w") as f:
        f.write(h_str)
        markdownFromFile(input=infilename, output=f)
        f.write(f_str)

def process_mds(mds, h_str, f_str, indir, outdir):
    if not os.path.exists(outdir): os.mkdir(outdir)

    for i in mds:
        print("processing {0}".format(i))
        process_md(i, h_str, f_str, indir, outdir)

def copy_resources(indir, outdir):
    resin = os.path.join(indir, "res")
    resout = os.path.join(outdir, "res")

    if os.path.exists(resin):
        shutil.copytree(resin, resout)

if __name__ == "__main__":
    mds = get_file_list(IN_DIR)

    if not mds: print_err("no markdown to process")
    if os.path.exists(OUT_DIR): print_err("output dir already exists")

    (h_str, f_str) = read_template(IN_DIR)
    process_mds(mds, h_str, f_str, IN_DIR, OUT_DIR)

    copy_resources(IN_DIR, OUT_DIR)
