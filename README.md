
# Image Automation Script

## Overview

This Bash script is designed to automate the process of resizing and archiving images within a specified directory. The script provides a menu-driven interface that allows users to:

1. **Create a virtual environment** for Python dependencies.
2. **Run the image automation process**, which includes selecting a directory, resizing images to a specified maximum size, and archiving them into a ZIP file.
3. **Exit** the program.

The script is useful for anyone who needs to batch process images, particularly when preparing images for web use or storage, where size constraints are critical.

## Features

- **Virtual Environment Setup**: Automatically creates a Python virtual environment and installs the necessary libraries (`Pillow` for image processing and `tqdm` for progress tracking).
  
- **Image Resizing**: Processes images in the chosen directory, resizing them to ensure that their file size does not exceed a user-defined maximum (in KB). Supports various image formats, including JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP, and HEIC.

- **Archiving**: After resizing, the images are archived into a user-specified ZIP file for easy storage or distribution.

- **Directory Selection**: Users can interactively choose the directory to process, ensuring that the correct folder is selected for automation.

- **Timeout Control**: The script allows setting a maximum time limit (in seconds) for the resizing operation, ensuring that the process does not run indefinitely.

- **Detailed Output**: After the process is complete, the script outputs lists of both modified and unmodified images, giving users insight into which files were processed.

## Prerequisites

- **Python 3.x** installed on the system.
- **Bash shell** (typically available by default on Linux and macOS systems).

## How to Use

1. **Run the Script**:
   - Execute the script from a terminal with Bash support. 
   - Example: `./image_automation.sh`

2. **Main Menu Options**:
   - **1. Create Virtual Environment**: This option will set up a Python virtual environment in the current directory and install the required Python packages.
   - **2. Start Automation**: This option initiates the image processing workflow:
     - **Directory Selection**: Choose the directory containing the images to be processed.
     - **Max Size**: Specify the maximum allowed size for each image (in KB).
     - **Timeout**: Set a time limit for the entire process (in seconds).
     - **Output ZIP File**: Define the name for the ZIP file that will contain the resized images.
     - **New Directory**: Specify a directory name where processed images will be stored.
   - **3. Exit**: This option exits the script.

3. **Process Flow**:
   - The script will display a list of directories, allowing you to choose one for processing.
   - After entering the required parameters (max size, timeout, ZIP file name, new directory), the script will process all images in the selected directory.
   - During processing, a progress bar will show the current status.
   - If the process exceeds the specified timeout, it will terminate automatically.
   - Once complete, the script will archive the processed images into the specified ZIP file and provide lists of modified and unmodified images.

4. **Post-Processing**:
   - Review the terminal output to see which images were modified.
   - The ZIP file containing the processed images will be available in the specified location.

## Error Handling

- **Invalid Directory**: The script checks if the selected directory is valid. If an invalid directory is selected, the user will be prompted to try again.
  
- **File Format Handling**: The script automatically skips non-image files (like PDFs) and processes only the supported image formats.

- **Quality Adjustment**: If an image's size exceeds the specified limit after the initial save, the script reduces the image quality in steps until it meets the size requirement or reaches the minimum acceptable quality.

- **Exception Handling**: The script catches exceptions during the image processing phase and outputs an error message for any images that could not be processed.

## Customization

Users can modify the script to:

- **Support additional image formats** by adding the appropriate file extensions in the processing loop.
- **Adjust the quality reduction steps** or the minimum quality threshold to better suit their needs.
- **Extend functionality** to include other image processing tasks like converting formats, changing resolutions, or applying watermarks.

## Conclusion

This script provides a convenient and automated way to resize and archive images in bulk, with user-friendly prompts and error handling. It is particularly useful for developers, photographers, and content managers who need to prepare large numbers of images for online use or storage.
