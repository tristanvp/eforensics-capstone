from __future__ import print_function
import argparse
from datetime import datetime
import os
import sys
from backend.utility.image_mount import *
from backend.utility.filesystem import *
from backend.file_analysis.sus_files_discovery import *

def main(image, img_type, part_type):
    fs_handler = FileSystem(image, img_type, part_type)
    sus_files_discovery = SusFilesDiscovery(fs_handler)
    sus_files_discovery.run()
    
    partitions = fs_handler.list_partitions()
    print(partitions)
    print("Length of partitions: " + str(len(partitions)))
    if (len(partitions) == 1):
        MountManager(image).mount_single("/mnt")
    else:
        MountManager(image).mount_multi("/mnt", len(partitions), partitions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("EVIDENCE_FILE", help="Evidence file path")
    parser.add_argument("TYPE", help="Type of Evidence",
                        choices=("raw", "ewf"))
    parser.add_argument("-p", help="Partition Type",
                        choices=("DOS", "GPT", "MAC", "SUN"))
    args = parser.parse_args()

    if os.path.exists(args.EVIDENCE_FILE) and os.path.isfile(args.EVIDENCE_FILE):
        main(args.EVIDENCE_FILE, args.TYPE, args.p)
    else:
        print("[-] Supplied input file {} does not exist oris not a "
              "file".format(args.EVIDENCE_FILE))
        sys.exit(1)