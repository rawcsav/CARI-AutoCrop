# Auto Crop for CARI Scans

## Prerequisites

Before you begin, ensure you have the following installed on your computer:

1. **Python 3.10**
   - Download and install Python 3.10 from the official website: [Python Downloads](https://www.python.org/downloads/)
   - Make sure to check the box that says "Add Python to PATH" during installation.

2. **Git**
   - Download and install Git from the official website: [Git Downloads](https://git-scm.com/downloads)
   - Verify the installation by running:
     ```sh
     git --version
     ```

## Installation

1. **Clone the Repository**

   Open a terminal and run the following command to clone the repository:
   ```sh
   git clone https://github.com/rawcsav/CARI-AutoCrop.git
   ```

2. **Navigate to the Repository Directory**

   Change into the directory of the cloned repository:
   ```sh
   cd CARI-AutoCrop
   ```

3. **Install the Required Python Libraries**

   Run the following command to install the necessary Python libraries:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Basic Command Structure

The basic structure of the command to run the script is:
```sh
python autocrop.py [options]
```

### Options

- `-f` or `--folder`: Specify an input folder containing images to process. You can use this option multiple times to process multiple folders.
- `-i` or `--image`: Specify an individual image to process. You can use this option multiple times to process multiple individual images.
- `-o` or `--output`: Specify the base output directory (required).
- `-t` or `--threshold`: Set the threshold for determining black borders (0-255). Default is 40.
- `-w` or `--workers`: Set the number of worker threads. Default is the number of CPU cores.

### Understanding the Threshold Value

The threshold value (set with the `-t` option) determines how dark a pixel needs to be to be considered part of the border. The value ranges from 0 (black) to 255 (white):

- A lower threshold (e.g., 30) will be more aggressive in cropping and might remove dark (but not black) areas.
- A higher threshold (e.g., 100) will be more conservative and will only remove very dark or black areas.

Adjust this value if you find that the script is cropping too much (threshold too low) or not enough (threshold too high).

### Examples

1. **Process a Single Folder:**
   ```sh
   python autocrop.py -f /Users/YourName/Pictures/InputFolder -o /Users/YourName/Pictures/OutputFolder
   ```

2. **Process Multiple Folders:**
   ```sh
   python autocrop.py -f /Users/YourName/Folder1 -f /Users/YourName/Folder2 -o /Users/YourName/Output
   ```

3. **Process Individual Images:**
   ```sh
   python autocrop.py -i /Users/YourName/image1.jpg -i /Users/YourName/image2.png -o /Users/YourName/Output
   ```

4. **Mix Folders and Individual Images:**
   ```sh
   python autocrop.py -f /Users/YourName/Folder1 -i /Users/YourName/image1.jpg -o /Users/YourName/Output
   ```

5. **Set a Custom Threshold and Number of Workers:**
   ```sh
   python autocrop.py -f /Users/YourName/Folder1 -o /Users/YourName/Output -t 50 -w 4
   ```

## Notes

- The script will map your input directories to subdirectories within your output folder. Indvidually specified images will appear in the root of the output folder.
- The script supports PNG, JPG, JPEG, TIFF, and BMP file formats.