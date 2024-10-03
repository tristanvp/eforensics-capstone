from __future__ import print_function
import argparse
from datetime import datetime
import os
import sys
from definitions import *
from backend.utility.drive_hash import *
from backend.utility.image_mount import *
from backend.utility.filesystem import *
from backend.file_analysis.sus_files_discovery import *
from backend.file_analysis.file_carver.file_carver import FileCarver
from backend.file_analysis.file_headers import *
from backend.file_analysis.renamed_file import *
from backend.file_analysis.keywords import *
from backend.file_analysis.undeleted_file import *
from backend.utility.report_generator import ReportGenerator

def main(image, img_type, part_type, mnt_path, keywords, template, output):
    # all info of filesystem (ie: all files, partitions)
    fs_handler = FileSystem(image, img_type, part_type)
    partitions = fs_handler.list_partitions()
    '''recurse all files based on the filesystem
        (this recurses all the undeleted (allocated) files in filesystem)'''
    all_files = fs_handler.recurse_files() 
    partitions_index = [file["partition"] for file in all_files]
    fs_obj_list = [file["fs object"] for file in all_files]
    filenames = [file["name"] for file in all_files]
    filepaths = [file["path"] for file in all_files]
    
    # mounting imager
    ImageMount(image, img_type, len(partitions), partitions).mount_partition(mnt_path)

    # hash the image file
    DriveHash(file_path=image).save_hash_to_file()
    
    # hash the all files within the filesystem
    DriveHash(file_path=filepaths, fs_object=fs_obj_list, partitions_index=partitions_index).save_hash_to_file()
    
    # find all renamed file 
    renamed_files = RenamedFileFinder(fs_obj_list=fs_obj_list, filenames=filenames, filepaths=filepaths).find_renamed_files()
    
    # carves file from unallocated space or data stream
    carved_files = FileCarver(filenames=fs_handler.unallocated_parts, output_dir="carved_files").carve()
    
    # find the header of the files
    headers = FileHeaderDetector(fs_obj_list=fs_obj_list, filepaths=filepaths).scan_files_for_headers()
    
    # searching for keywords in the files
    keys_included_files = GrepKeyword(fs_obj_list=fs_obj_list, filepaths=filepaths, keywords=keywords).search()
    
    sus_files = SusFilesDiscovery(fs_handler).suspicious_files
    
    context = {
        'undeleted_files': all_files,
        'renamed_files': renamed_files,
        'carved_files': carved_files,
        'sus_files': sus_files,
        'keywords': keys_included_files,
        'headers': headers,
    }
    
    # generate report based on the above findings
    report_generator = ReportGenerator(template, output)
    report_generator.generate_report(context)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("EVIDENCE_FILE", help="Evidence file path")
    parser.add_argument("TYPE", help="Type of Evidence",
                        choices=("dd", "ewf", "l01", "zip"))
    parser.add_argument("-p", help="Partition Type",
                        choices=("DOS", "GPT", "MAC", "SUN"))
    parser.add_argument("-m", help="Mount path", default="/mnt")
    parser.add_argument("--keywords", help="List of keywords to be searched (eg: key1,key2,..)", default=None)
    parser.add_argument("--template", help="Predefined template of the report", default=f"{ROOT_DIR}/backend/utility/template/template_eforensics_analysis_report.docx")
    parser.add_argument("-o", help="Output of the report", default=f"{ROOT_DIR}/eforensic_report.docx")
    args = parser.parse_args()
    
    if args.keywords != None:
        keywords = [key.strip() for key in args.keywords.split(",")]
        
    if os.path.exists(args.EVIDENCE_FILE) and os.path.exists(args.EVIDENCE_FILE) and os.path.isfile(args.EVIDENCE_FILE):
        main(args.EVIDENCE_FILE, args.TYPE, args.p, args.m, keywords, args.template, args.o)
    else:
        print("[-] Supplied input file {} does not exist or is not a "
              "file".format(args.EVIDENCE_FILE))
        sys.exit(1)