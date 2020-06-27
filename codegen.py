#!/usr/bin/env python3

import argparse
import glob
import os
import sys

import lxml.etree


parser = argparse.ArgumentParser(description='List all generated files')
parser.add_argument('input_dir', nargs='?', default='.')
parser.add_argument('output_dir', nargs='?', default='out')
parser.add_argument('separator', nargs='?', default='\n')


xslt_trees = [lxml.etree.parse('lower-%i.xslt' % i) for i in (1, 2)]
xslt_transforms = list(map(lxml.etree.XSLT, xslt_trees))


_ld_url = xslt_trees[0].getroot().nsmap['ld']
def ld_name(name):
    return lxml.etree.QName(_ld_url, name)


def load_and_transform(filename):
    tree = lxml.etree.parse(filename)
    for transform in xslt_transforms:
        tree = transform(tree)
    return tree


def write_codegen_out_xml(trees, output_dir):
    src_root = trees[0].getroot()
    new_root = src_root.makeelement(ld_name('data-definition'), nsmap=src_root.nsmap)
    new_root.text = '\n    '
    for tree in trees:
        for child in tree.getroot().iterchildren():
            new_root.append(child)
    with open(os.path.join(output_dir, 'codegen.out.xml'), 'wb') as f:
        f.write(lxml.etree.tostring(new_root))


def main():
    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    filenames = glob.glob(os.path.join(args.input_dir, 'df.*.xml'))
    filenames.sort()
    trees = list(map(load_and_transform, filenames))
    write_codegen_out_xml(trees, args.output_dir)


if __name__ == '__main__':
    main()
