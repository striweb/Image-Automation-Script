#!/usr/bin/env bash

# Function to create a virtual environment
setup_virtualenv() {
    echo "Creating a virtual environment and installing necessary libraries..."
    python3 -m venv myenv
    source myenv/bin/activate
    pip install Pillow tqdm
    echo "The virtual environment has been created and libraries have been successfully installed."
}

# Function to start the automation
run_automation() {
    echo "Please choose the directory for automation:"
    while true; do
        ls -d */
        read -e -p "Directory: " directory
        if [ -d "$directory" ]; then
            break
        else
            echo "Invalid directory. Please try again."
        fi
    done

    read -p "Enter the maximum image size in KB (e.g., 100): " max_size_kb
    read -p "Enter the timeout in seconds (e.g., 3600): " timeout
    read -p "Enter the name of the output ZIP file (e.g., resized_images.zip): " output_zip
    read -p "Enter the name of the new directory for processed images: " new_directory

    echo "Starting the process of resizing and archiving images..."
    source myenv/bin/activate  # Activate the virtual environment
    python3 - <<EOF
import os
import zipfile
import sys
import time
from multiprocessing import Pool, Manager
from PIL import Image, ImageFile
from tqdm import tqdm

# Configuration to load truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

def resize_image_task(args):
    input_path, output_path, max_size_kb, modified_images, unmodified_images = args
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with Image.open(input_path) as img:
            if img.mode in ('P', 'RGBA', 'LA'):
                img = img.convert('RGBA')
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            quality = 95
            img.save(output_path, "JPEG", quality=quality)
            while os.path.getsize(output_path) / 1024 > max_size_kb and quality > 10:
                quality -= 5
                img.save(output_path, "JPEG", quality=quality)
        if os.path.getsize(output_path) / 1024 < os.path.getsize(input_path) / 1024:
            modified_images.append(input_path)
        else:
            unmodified_images.append(input_path)
    except Exception as e:
        print(f"Error processing {input_path}: {e}")

def process_directory(directory, new_directory, zip_file, max_size_kb=100, timeout=3600):
    start_time = time.time()
    manager = Manager()
    modified_images = manager.list()
    unmodified_images = manager.list()

    files_to_process = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('pdf')):
                print(f"Skipping PDF file: {file}")
                continue
            if file.lower().endswith(('jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'heic')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, directory)
                output_path = os.path.join(new_directory, relative_path)
                files_to_process.append((input_path, output_path, max_size_kb, modified_images, unmodified_images))

    total_files = len(files_to_process)

    with tqdm(total=total_files, desc="Processing Images") as pbar, Pool() as pool:
        for _ in pool.imap_unordered(resize_image_task, files_to_process):
            pbar.update(1)
            if time.time() - start_time > timeout:
                print(f"Timeout of {timeout} seconds exceeded. Stopping the process.")
                pool.terminate()
                break

    # Add resized images to zip file
    for _, output_path, _, _, _ in files_to_process:
        if os.path.exists(output_path):
            zip_file.write(output_path, os.path.relpath(output_path, new_directory))

    return list(modified_images), list(unmodified_images)

directory = "$directory"
max_size_kb = int("$max_size_kb")
timeout = int("$timeout")
output_zip = "$output_zip"
new_directory = "$new_directory"

os.makedirs(new_directory, exist_ok=True)

with zipfile.ZipFile(output_zip, 'w') as zipf:
    modified_images, unmodified_images = process_directory(directory, new_directory, zipf, max_size_kb, timeout)

print(f"The resized images have been saved in {output_zip}")
print("\nList of modified images:")
for image in modified_images:
    print(image)

print("\nList of unmodified images:")
for image in unmodified_images:
    print(image)
EOF
    echo "The resizing and archiving process is complete. Check the results in the terminal."
}

# Main menu
while true; do
    clear
    echo "Image Automation Menu"
    echo "1. Create virtual environment"
    echo "2. Start automation"
    echo "3. Exit"
    read -p "Choose an option: " choice

    case $choice in
        1)
            setup_virtualenv
            ;;
        2)
            run_automation
            ;;
        3)
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            ;;
    esac
    read -p "Press Enter to continue..."
done
