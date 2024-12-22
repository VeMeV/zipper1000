import os
import zipfile
from pathlib import Path
from tqdm import tqdm
import math
import sys

def batch_zip_files(source_dir, output_dir, prefix="batch", batch_size=1000):
    """
    Zips files from source_dir into batches of specified size and removes original files.
    
    Args:
        source_dir (str): Directory containing the text files
        output_dir (str): Directory where zip files will be saved
        prefix (str): Prefix for zip filenames
        batch_size (int): Number of files per zip archive
    """
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get list of all text files
    files = [f for f in Path(source_dir).glob("*.txt")]
    total_files = len(files)
    total_batches = math.ceil(total_files / batch_size)
    
    print(f"Found {total_files} text files")
    print(f"Will create {total_batches} zip files")
    
    # Process files in batches
    for batch_num in tqdm(range(total_batches), desc="Creating zip files"):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, total_files)
        batch_files = files[start_idx:end_idx]
        
        # Create zip file for this batch with prefix from argv
        zip_filename = f"{prefix}_{batch_num + 1:04d}.zip"
        zip_path = Path(output_dir) / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add files to zip
            for file_path in batch_files:
                # Convert Path object to string and ensure proper path handling
                file_path_str = str(file_path)
                arcname = file_path.name
                zipf.write(file_path_str, arcname)
    
    # After all files have been zipped, remove the original text files
    print("Removing original text files...")
    for file_path in tqdm(files, desc="Removing files"):
        file_path.unlink()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python zipper1000.py <source_dir> <output_dir> <zip_prefix>")
        sys.exit(1)
    
    source_directory = sys.argv[1]
    output_directory = sys.argv[2]
    zip_prefix = sys.argv[3]
    
    batch_zip_files(source_directory, output_directory, zip_prefix)
