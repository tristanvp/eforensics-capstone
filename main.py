from __future__ import print_function
import argparse
import os
import sys
from backend.utility.image_mount import *
from backend.utility.filesystem import *
from backend.file_analysis.sus_files_discovery import *
from backend.file_analysis.keyword import *

def main(image, img_type, part_type):
    # Main Setup
    fs_handler = FileSystem(image, img_type, part_type)

    # SusFile call
    sus_files_discovery = SusFilesDiscovery(fs_handler)
    discovered_files = sus_files_discovery.run()

    # Discovered Files call
    print("Discovered Files:")
    for file_info in discovered_files:
        print(file_info)
    
    # Partitions call (High level)
    partitions = fs_handler.list_partitions()
    print("Partitions:")
    for partition in partitions:
        print(partition)
    print("Length of partitions: " + str(len(partitions)))

    # Mounting logic for files w/o partitions 
    if len(partitions) == 1:
        MountManager(image).mount_single("/mnt")
    else:
        MountManager(image).mount_multi("/mnt", len(partitions), partitions)

    try:
        # Keyword search
        searcher = FileSearcher('/mnt')
        matches = searcher.search_keyword('/mnt', 'bin')
        print(f"Files containing 'bin': {matches}")
    except Exception as e:
        print(f"Error in keyword searching: {e}")

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
        print("[-] Supplied input file {} does not exist or is not a file".format(args.EVIDENCE_FILE))
        sys.exit(1)

