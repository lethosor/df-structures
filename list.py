#!/usr/bin/env python3

import argparse
import glob
import os
import sys

import lxml.etree


parser = argparse.ArgumentParser(description='List all generated files')
parser.add_argument('input_dir', nargs='?', default='.')
parser.add_argument('output_dir', nargs='?', default='codegen')
parser.add_argument('separator', nargs='?', default='\n')


def list_files(dir):
    yield 'global_objects.h'
    yield 'static.inc'
    for t in ('ctors', 'enums', 'fields'):
        yield 'static.%s.inc' % t
    for c in range(ord('a'), ord('z') + 1):
        yield 'static.fields-%s.inc' % chr(c)
    for file in glob.glob(os.path.join(dir, "*.xml")):
        tree = lxml.etree.parse(file)
        for etype in ('enum-type', 'bitfield-type', 'struct-type', 'class-type', 'df-linked-list-type', 'df-other-vectors-type'):
            for node in tree.xpath('/data-definition/' + etype):
                name = node.attrib.get('type-name')
                if not name:
                    raise ValueError('Unnamed %s in %s:%i' % (etype, file, node.sourceline))
                yield name + ".h"

def main():
    args = parser.parse_args()
    sep = ''
    for file in list_files(args.input_dir):
        sys.stdout.write(sep + args.output_dir + '/' + file)
        sep = args.separator
    if args.separator == '\n':
        sys.stdout.write(args.separator)
    sys.stdout.flush()


if __name__ == '__main__':
    main()
