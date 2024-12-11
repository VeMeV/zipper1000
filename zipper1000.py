import os
import zipfile
from pathlib import Path
from tqdm import tqdm
import math

def batch_zip_files(source_dir, output_dir, batch_size=1000):
    """
    Zips files from source_dir into batches of specified size.
    
    Args:
        source_dir (str): Directory containing the text files
        output_dir (str): Directory where zip files will be saved
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
        
        # Create zip file for this batch
        zip_filename = f"batch_{batch_num + 1:04d}.zip"
        zip_path = Path(output_dir) / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Add files to zip
            for file_path in batch_files:
                
                # Use relative path within zip file
                arcname = file_path.name
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    
    # Example usage
    source_directory = "input"
    output_directory = "output"
    
    batch_zip_files(source_directory, output_directory)
