import os
import shutil
import time
import psutil
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to console
        logging.FileHandler("cleanup.log")  # Log to file
    ]
)

def get_storage_usage():
    usage = psutil.disk_usage('/')
    return usage.free / (1024 ** 3)  # Convert to GB

def find_and_delete_node_modules(start_dir):
    node_modules_folders = []
    total_dirs_checked = 0  # Initialize a counter for directories checked
    for root, dirs, _ in os.walk(start_dir):
        # Log the current directory being processed
        logging.info(f"Processing directory: {root}")
        
        # Increment the directory counter
        total_dirs_checked += 1
        
        # Filter out hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        if 'node_modules' in dirs:
            folder_path = os.path.join(root, 'node_modules')
            node_modules_folders.append(folder_path)
            logging.info(f"Deleting: {folder_path}")
            shutil.rmtree(folder_path, ignore_errors=True)
    
    return node_modules_folders, total_dirs_checked

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: python script.py <src-dir>")
        return
    
    start_dir = sys.argv[1]
    
    if not os.path.exists(start_dir):
        logging.error("Error: Directory does not exist.")
        return
    
    logging.info("Starting cleanup process...")
    start_time = time.time()
    start_storage = get_storage_usage()
    
    node_modules_folders, total_dirs_checked = find_and_delete_node_modules(start_dir)
    
    end_storage = get_storage_usage()
    end_time = time.time()
    
    report = [
        "\n\nCleanup Report:",
        f"Initial Free Space: {start_storage:.2f} GB",
        f"Total 'node_modules' folders deleted: {len(node_modules_folders)}",
        f"Total directories checked: {total_dirs_checked}",
        f"Final Free Space: {end_storage:.2f} GB",
        f"Storage Reclaimed: {end_storage - start_storage:.2f} GB",
        f"Time Taken: {end_time - start_time:.2f} seconds",
        "\nDeleted Folders:" if node_modules_folders else ""
    ]
    
    report.extend(node_modules_folders)
    
    logging.info("\n".join(report))
    logging.info("Cleanup process completed.")

if __name__ == "__main__":
    main()