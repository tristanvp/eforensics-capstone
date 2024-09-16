import os
import subprocess
import sys
import datetime


class LoopDeviceManager:
    @staticmethod
    def get_next_loop_device():
        try:
            max_loop_number_cmd = (
                "lsblk | awk '{{sub(/:/,\"\",$1); print $1}}' | grep loop | "
                "awk -F 'loop' '{{print $2}}' | sort -n | tail -1"
            )
            max_loop_number = subprocess.check_output(max_loop_number_cmd, shell=True, text=True).strip()
            return f"/dev/loop{int(max_loop_number) + 1}"
        except subprocess.CalledProcessError as e:
            print(f"[-] Error getting loop device number: {e}")
            return None

    @staticmethod
    def create_loop_device(loop_device, img_file):
        create_loop_device_cmd = f"sudo losetup {loop_device} {img_file}"
        try:
            subprocess.check_call(create_loop_device_cmd, shell=True)
        except subprocess.CalledProcessError as e:
            print(f"[-] Error creating loop device: {e}")
            return False
        return True

class MountManager:
    def __init__(self, img_file):
        self.img_file = img_file
        
    def mount_single(self, mnt_path):
        if not os.path.exists(mnt_path):
            os.makedirs(mnt_path)
        print(f"[+] Attempting to Mount {self.img_file} at {mnt_path}")

        loop_device = LoopDeviceManager.get_next_loop_device()
        if not loop_device:
            return

        if not LoopDeviceManager.create_loop_device(loop_device, self.img_file):
            return

        try:
            retcode = subprocess.call(f"sudo mount {loop_device} {mnt_path}", shell=True)
            if retcode != 0:
                print(f"[-] Failed to mount {loop_device} at {mnt_path}")
                return
            print(f"   [+] Mounted {self.img_file} at {mnt_path}")
            print(f"   [INFO] To unmount run 'sudo umount {mnt_path}'")
        except Exception as e:
            print(f"[-] Failed to Mount {mnt_path}: {e}")

    def mount_multi(self, mnt_path, part_count, part_data):
        for i in range(part_count):
            offset = part_data[i]["offset"]
            new_path = os.path.join(mnt_path, str(offset))
            
            loop_device = LoopDeviceManager.get_next_loop_device()
            if not loop_device:
                continue  # Skip to the next partition

            create_loop_device_cmd = f"sudo losetup -o {offset} {loop_device} {self.img_file}"
            print(f"[+] Creating Loop Device at {loop_device}")
            try:
                subprocess.check_call(create_loop_device_cmd, shell=True)
            except subprocess.CalledProcessError as e:
                print(f"[-] Error creating loop device: {e}")
                continue  # Skip to the next partition

            print(f"[+] Creating Temp Mount Point at {new_path}")
            if not os.path.exists(new_path):
                try:
                    os.makedirs(new_path)
                except OSError as e:
                    print(f"[-] Error creating mount point directory {new_path}: {e}")
                    continue  # Skip to the next partition

            try:
                print(f"[+] Attempting to Mount Partition {i} at {new_path}")
                mount_cmd = f'sudo mount {loop_device} {new_path}'
                subprocess.check_call(mount_cmd, shell=True)
                print(f"   [+] Mounted {self.img_file} at {new_path}")
                print(f"   [INFO] To unmount run 'sudo umount {new_path}'")
            except subprocess.CalledProcessError as e:
                print(f"[-] Failed to mount {loop_device} at {new_path}: {e}")
            except Exception as e:
                print(f"[-] Unexpected error: {e}")

class E01MountManager(MountManager):
    def mount_ewf(self):
        print("[+] Processing E01 File")
        if not self.img_file.endswith('.E01'):
            print("[-] Not an E01 file")
            return None

        ts = datetime.datetime.now().strftime('%Y_%m_%d-%H_%S')
        ewf_path = f'/mnt/ewf_{ts}'
        if not os.path.exists(ewf_path):
            try:
                os.makedirs(ewf_path)
            except Exception as e:
                print(f"Unable to create Temp Dir: {e}")
                sys.exit()

        try:
            retcode = subprocess.call(f'ewfmount {self.img_file} {ewf_path}', shell=True)
            if retcode != 0:
                sys.exit()
            print(f"[+] Mounted E01 File at {ewf_path}/ewf1")
            print(f"   [-] To unmount run 'sudo umount {ewf_path}'")
            return f'{ewf_path}/ewf1'
        except Exception as e:
            print(f"Failed to mount E01 File: {e}")
            sys.exit()

class ImageMount:
    def __init__(self, file_path, file_type, partition_index=None):
        self.file_path = file_path
        self.file_type = file_type
        self.partition_index = partition_index
        self.mount_manager = self._create_mount_manager(file_path, file_type)

    def _create_mount_manager(self, file_path, file_type):
        if file_type == 'DD':
            return MountManager(file_path)
        elif file_type == 'E01':
            return E01MountManager(file_path)
        # Add other file types as needed
        else:
            raise ValueError("Unsupported file type")

    def list_partitions(self):
        if self.partition_index is None:
            return self.mount_manager.get_partitions()
        else:
            partitions = self.mount_manager.get_partitions()
            if self.partition_index < len(partitions):
                return [partitions[self.partition_index]]
            else:
                raise IndexError("Partition index out of range")

    def mount_partition(self, partition, mount_path):
        self.mount_manager.mount_single(mount_path)

    def close(self):
        # Implement if necessary
        pass
