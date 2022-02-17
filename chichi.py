#! /usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os
import re
import sys
import datetime
import shutil

__version = "1.0"


def options_parser():
    usage = "chichi -i input_file -o output_folder -e extension -p pattern -n name"
    version = __version
    example = """
Example: 
    chichi -i a/b/c/d -o a/b/c/d -e txt -p abc -n chichi

    """
    OptionParser.format_epilog = lambda self, formatter: self.epilog
    parser = OptionParser(usage=usage, version=version, epilog=example)
    parser.add_option(
        "-i", "--input", dest="InputFile",
        help="Path to Input File")
    parser.add_option(
        "-o", "--output", dest="OutputFolder",
        help="Path to Output Folder", default=None)
    parser.add_option(
        "-e", "--extension", dest="Extension",
        help="Extension of file need to be filtered", default=None)
    parser.add_option(
        "-p", "--pattern", dest="Pattern",
        help="Pattern of file need to be filtered", default=None)
    parser.add_option(
        "-n", "--name", dest="FolderName",
        help="Folder name to create", default=None)
    return parser


def get_options():
    parser = options_parser()
    (options, args) = parser.parse_args()
    if not options.InputFile or not options.OutputFolder:
        parser.print_help()
        sys.exit(1)

    if options.InputFile:
        if not os.path.exists(options.InputFile):
            print ("Invalid Path to Input File")
            sys.exit(1)
        if not os.path.isfile(options.InputFile):
            print ("Invalid file")
            sys.exit(1)

    if options.OutputFolder:
        if not os.path.exists(options.OutputFolder):
            print ("Invalid Path to Output Folder")
            sys.exit(1)

    if not options.Extension:
        options.Extension = "all"

    if not options.Pattern:
        options.Pattern = ""

    if not options.FolderName:
        options.FolderName = ""

    return options.InputFile, options.OutputFolder, options.Extension, options.Pattern, options.FolderName


def execute(input_file, output_folder, required_extension, pattern, folder_name):
    # Create output folder
    today_date = datetime.datetime.now().strftime("%Y%m%d")
    out_dir = os.listdir(output_folder)
    versions = []
    for i in out_dir:
        fullpath_i = os.path.join(output_folder, i)
        if os.path.isdir(fullpath_i):
            _re = re.search(today_date + "_(.*)", i)
            if _re:
                _version = _re.group(1)
                versions.append(_version)
    versions.sort()
    if versions:
        cur_ver = int(versions[-1])
    else:
        cur_ver = 0
    _new_version = cur_ver + 1
    _folder = today_date + "_" + str(_new_version)
    create_folder = os.path.join(output_folder, _folder)
    os.mkdir(create_folder)
    # Load input file
    f = open(input_file)
    for line in f:
        line = line.strip()
        if os.path.exists(line):
            path, extension = os.path.splitext(line)
            ext = extension.replace(".", "")
            if pattern not in line:
                continue
            if required_extension != "all" and ext != required_extension:
                continue
            if not folder_name:
                folder_name = ext
            create_subfolder = os.path.join(create_folder, folder_name)
            if not os.path.exists(create_subfolder):
                os.mkdir(create_subfolder)
        if not line:
            continue
        shutil.copy2(line, create_subfolder)


if __name__ == '__main__':
    input_file, output_folder, required_extension, pattern, folder_name = get_options()
    execute(input_file, output_folder, required_extension, pattern, folder_name)
