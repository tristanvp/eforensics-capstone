from __future__ import print_function
import argparse
from datetime import datetime
import os
import sys
from backend.utility.drive_hash import *
from backend.utility.image_mount import *
from backend.utility.filesystem import *
from backend.file_analysis.sus_files_discovery import *
from backend.file_analysis.file_carver.file_carver import FileCarver
from backend.file_analysis.renamed_file import *
from backend.file_analysis.keywords import *

def main(image, img_type, part_type):
    fs_handler = FileSystem(image, img_type, part_type)
    # file carving
    FileCarver(filenames=fs_handler.unallocated_parts, output_dir="carved_files").carve()
    
    # recurse all files based on the filesystem
    all_files = fs_handler.recurse_files()
    fs_obj_list = [file["FS Object"] for file in all_files]
    filenames = [file["File Name"] for file in all_files]
    filepaths = [file["File Path"] for file in all_files]
    keywords = ["r-alloc", "r-unalloc", "r-fads", "r-dads", "n-alloc", "n-unalloc", "n-frag", "n-slack", "n-fads", "n-dads"]
    print(all_files)
    RenamedFileFinder(fs_obj_list=fs_obj_list, filenames=filenames, filepaths=filepaths).find_renamed_files()
    keywords_grepper = GrepKeyword(fs_obj_list=fs_obj_list, filepaths=filepaths, keywords=keywords).search()
    if all_files != None: 
        for file in all_files:
            DriveHash(file["File Path"], file["FS Object"]).save_hash_to_file(partition=file["Partition"])
    
    # sus_files_discovery = SusFilesDiscovery(fs_handler)
    # sus_files_discovery.run()
    
    # partitions = fs_handler.list_partitions()
    # print(partitions)
    # print("Length of partitions: " + str(len(partitions)))
    # mounter = ImageMount(image, img_type, len(partitions), partitions)
    # mounter.mount_partition("/mnt")
    # print(mounter.mount_manger.mnt_path)
    # for mnt_path in mounter.mount_manger.mnt_path:
    #     file_path = f"{mnt_path}/"
    #     DriveHash(mnt_p)
    # print(FileCarver(filename=image, output_dir="carved_files").carve())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("EVIDENCE_FILE", help="Evidence file path")
    parser.add_argument("TYPE", help="Type of Evidence",
                        choices=("dd", "ewf"))
    parser.add_argument("-p", help="Partition Type",
                        choices=("DOS", "GPT", "MAC", "SUN"))
    args = parser.parse_args()

    if os.path.exists(args.EVIDENCE_FILE) and os.path.isfile(args.EVIDENCE_FILE):
        main(args.EVIDENCE_FILE, args.TYPE, args.p)
    else:
        print("[-] Supplied input file {} does not exist or is not a "
              "file".format(args.EVIDENCE_FILE))
        sys.exit(1)