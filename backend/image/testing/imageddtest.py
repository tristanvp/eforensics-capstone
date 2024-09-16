from image import ImageHandler
from drive_hash import DriveHash

def test_image(file_path, file_type):
    print(f"\nTesting file: {file_path} ({file_type} image)")

    try:
        # initialize the image handler
        handler = ImageHandler(file_path, file_type)
        print(f"Image handler initialized successfully for {file_path}")

        # get and print partition information
        try:
            partition_count = handler.get_partitions()
            if partition_count > 0:
                print(f"Partitions found: {partition_count}")
            else:
                print("No partitions found or partition information not available for this image type.")
        except Exception as e:
            print(f"Error accessing partition info for {file_path}: {e}")

        # compute and print md5 hash
        try:
            hash_calculator = DriveHash(file_path)
            md5_hash = hash_calculator.md5_hash()
            print(f"MD5 Hash for {file_path}: {md5_hash}")
        except Exception as e:
            print(f"Error computing MD5 hash for {file_path}: {e}")

    except Exception as e:
        print(f"Error initializing image for {file_path}: {e}")

# paths to the image files
image_files = [
    (r"C:\-a\11-carve-fat.dd", "DD"),
    (r"C:\-a\fat-img-kw.dd", "DD"),
    (r"C:\-a\ntfs-img-kw-1.dd", "DD"),
    (r"C:\-a\ext-part-test-2.dd", "DD")
]

# test each image file
for path, file_type in image_files:
    test_image(path, file_type)
