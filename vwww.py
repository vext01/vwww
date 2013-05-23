#!/usr/bin/env python2.7

import os, sys, shutil
from markdown import markdownFromFile

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
        markdownFromFile(output_format="xhtml1",input=infilename, output=f)
        f.write(f_str)

def process_mds(mds, h_str, f_str, indir, outdir):
    if not os.path.exists(outdir): os.mkdir(outdir)

    for i in mds:
        print("processing {0}".format(i))
        process_md(i, h_str, f_str, indir, outdir)

def copy_resources(indir, outdir):
    print("copying resources...")
    resin = os.path.join(indir, "res")
    resout = os.path.join(outdir, "res")
    if os.path.exists(resin): shutil.copytree(resin, resout)

if __name__ == "__main__":

    if len(sys.argv) != 3: print_err("usage: vwww indir outdir")

    indir = sys.argv[1]
    outdir = sys.argv[2]

    mds = get_file_list(indir)

    if not mds: print_err("no markdown to process")
    if os.path.exists(outdir): print_err("output dir already exists")

    (h_str, f_str) = read_template(indir)
    process_mds(mds, h_str, f_str, indir, outdir)

    copy_resources(indir, outdir)
