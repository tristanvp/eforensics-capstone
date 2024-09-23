import pytsk3, pyewf
import sys
from datetime import datetime
from backend.image.ewf_image import EWFImgInfo


class FileSystem:
    _TSK_FS_TYPE_MAP = {
        pytsk3.TSK_FS_TYPE_EXFAT: 'exFAT',
        pytsk3.TSK_FS_TYPE_EXT2: 'EXT2',
        pytsk3.TSK_FS_TYPE_EXT3: 'EXT3',
        pytsk3.TSK_FS_TYPE_EXT4: 'EXT4',
        pytsk3.TSK_FS_TYPE_EXT_DETECT: 'EXT',
        pytsk3.TSK_FS_TYPE_FAT12: 'FAT12',
        pytsk3.TSK_FS_TYPE_FAT16: 'FAT16',
        pytsk3.TSK_FS_TYPE_FAT32: 'FAT32',
        pytsk3.TSK_FS_TYPE_FAT_DETECT: 'FAT',
        pytsk3.TSK_FS_TYPE_FFS1B: 'FFS1b',
        pytsk3.TSK_FS_TYPE_FFS1: 'FFS1',
        pytsk3.TSK_FS_TYPE_FFS2: 'FFS2',
        pytsk3.TSK_FS_TYPE_FFS_DETECT: 'FFS',
        pytsk3.TSK_FS_TYPE_HFS: 'HFS',
        pytsk3.TSK_FS_TYPE_HFS_DETECT: 'HFS',
        pytsk3.TSK_FS_TYPE_ISO9660: 'ISO9660',
        pytsk3.TSK_FS_TYPE_ISO9660_DETECT: 'ISO9660',
        pytsk3.TSK_FS_TYPE_NTFS: 'NTFS',
        pytsk3.TSK_FS_TYPE_NTFS_DETECT: 'NTFS',
        pytsk3.TSK_FS_TYPE_YAFFS2: 'YAFFS2',
        pytsk3.TSK_FS_TYPE_YAFFS2_DETECT: 'YAFFS2'
    }

    def __init__(self, image, img_type, part_type=None):
        self.image =  image
        self.img_type = img_type
        self.part_type = part_type
        self.img_handle = None
        self.volume = None
        self.fs = []
        self.run()
        
    def run(self):
        self.create_handle()
        self.create_volume()
        self.open_fs()
        
    def is_valid_partition(self, part: pytsk3.TSK_VS_PART_INFO) -> bool:
        part_desc = part.desc.decode("utf-8")
        return part.len > 2048 and "Unallocated"not in part_desc and \
                        "Extended" not in part_desc and \
                        "Primary Table" not in part_desc

    def create_handle(self):
        print("[+] Opening {}".format(self.image))
        if self.img_type == "ewf":
            try:
                filenames = pyewf.glob(self.image)
            except IOError:
                _, e, _ = sys.exc_info()
                print("[-] Invalid EWF format:\n {}".format(e))
                sys.exit(2)

            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)

            # Open PYTSK3 handle on EWF Image
            self.img_handle = EWFImgInfo(ewf_handle)
        else:
            self.img_handle = pytsk3.Img_Info(self.image)
            
    def create_volume(self):
        try:
            if self.part_type is not None:
                attr_id = getattr(pytsk3, "TSK_VS_TYPE_" + self.part_type)
                self.volume = pytsk3.Volume_Info(self.img_handle, attr_id)
            else:
                self.volume = pytsk3.Volume_Info(self.img_handle)
        except IOError:
            _, e, _ = sys.exc_info()
            print("[-] Unable to read partition table:\n {}".format(e))
        
    def list_partitions(self):
        partitions = []
        if self.volume:
            for part in self.volume:
                if self.is_valid_partition(part):
                    offset = part.start * self.volume.info.block_size
                    ending_offset = (part.start + part.len - 1) * self.volume.info.block_size
                    try:
                        fs = pytsk3.FS_Info(self.img_handle, offset=offset)
                    except IOError:
                        _, e, _ = sys.exc_info()
                        print(f"[-] Unable to open FS:\n {e}")
                    partitions.append({
                        'partition': part.addr,
                        'part_desc': part.desc.decode("utf-8"),
                        'offset': offset,
                        'ending_offset': ending_offset,
                        'type': self._TSK_FS_TYPE_MAP.get(fs.info.ftype, "Unknown").lower()
                    })
                    
        return partitions

    def open_fs(self):
        print("[+] Recursing through files..")
        if self.volume:
            for part in self.volume:
                if self.is_valid_partition(part):
                    try:
                        self.fs.append(pytsk3.FS_Info(self.img_handle, offset=part.start * self.volume.info.block_size))
                    except IOError:
                        _, e, _ = sys.exc_info()
                        print(f"[-] Unable to open FS:\n {e}")          
        else:
            try:
                self.fs.append(pytsk3.FS_Info(self.img_handle)) 
            except IOError:
                _, e, _ = sys.exc_info()
                print(f"[-] Unable to open FS:\n {e}") 
    
    def recurse_files(self, substring="", path="/", logic="contains", case=False) -> list:
        files = []
        for i, fs in enumerate(self.fs):
            try:
                root_dir = fs.open_dir(path)
            except IOError:
                continue
            files += self.recurse_dir(i, fs, root_dir, [], [], [""], substring, logic, case)

        if files == []:
            return None
        else:
            return files
        
    
    def recurse_dir(self, part: int, fs: pytsk3.FS_Info, root_dir: pytsk3.Directory, dirs: list, data: list, parent: list, substring=None, logic=None, case=False):
        parent = [p.decode("utf-8") if isinstance(p, bytes) else p for p in parent]
        dirs.append(root_dir.info.fs_file.meta.addr)
        for fs_object in root_dir:
            if not hasattr(fs_object, "info") or \
                    not hasattr(fs_object.info, "name") or \
                    not hasattr(fs_object.info.name, "name") or \
                    fs_object.info.name.name in [".", ".."]:
                continue
            try:
                file_name = fs_object.info.name.name.decode("utf-8")
                file_path = f"{'/'.join(parent)}/{file_name}"
                if fs_object.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
                    f_type = "DIR"
                    file_ext = ""
                else:
                    f_type = "FILE"
                    file_ext = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
                
                file_info = {
                    "Partition": part,
                    "File Name": file_name, 
                    "File Path": file_path,
                    "FS Object": fs_object, 
                    "File Extension": file_ext, 
                    "Modified Date": self.convert_time(fs_object.info.meta.mtime), 
                    "Accessed Date": self.convert_time(fs_object.info.meta.atime),
                    "Created Date": self.convert_time(fs_object.info.meta.crtime),
                    "Size": fs_object.info.meta.size
                    
                }
                
                if (substring):
                    if f_type == "FILE":
                        if logic.lower() == 'contains':
                            if case is False:
                                if substring.lower() in file_name.lower():
                                    data.append(file_info)
                                    continue
                            else:
                                if substring in file_name:
                                    data.append(file_info)
                                    continue
                        elif logic.lower() == 'startswith':
                            if case is False:
                                if file_name.lower().startswith(substring.lower()):
                                    data.append(file_info)
                                    continue
                            else:
                                if file_name.startswith(substring):
                                    data.append(file_info)
                                    continue
                        elif logic.lower() == 'endswith':
                            if case is False:
                                if file_name.lower().endswith(substring.lower()):
                                    data.append(file_info)
                                    continue
                            else:
                                if file_name.endswith(substring):
                                    data.append(file_info)
                                    continue
                        elif logic.lower() == 'equal':
                            if case is False:
                                if substring.lower() == file_name.lower():
                                    data.append(file_info)
                                    continue
                            else:
                                if substring == file_name:
                                    data.append(file_info)
                                    continue
                        else:
                            sys.stderr.write("[-] Warning invalid logic {} provided\n".format(logic))
                            sys.exit()
                else:
                    data.append(file_info)

                if f_type == "DIR":
                    parent.append(fs_object.info.name.name)
                    sub_directory = fs_object.as_directory()
                    inode = fs_object.info.meta.addr
                    if inode not in dirs:
                        self.recurse_files(part, fs, sub_directory, dirs, data, parent)
                    parent.pop(-1)

            except IOError:
                pass
        dirs.pop(-1)
        return data

    @staticmethod
    def convert_time(ts: int):
        if str(ts) == "0":
            return ""
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')