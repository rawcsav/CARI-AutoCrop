import os
import sys
import argparse
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_image(filename, input_folder, output_folder, threshold=60):
    try:
        img_path = os.path.join(input_folder, filename)
        img = cv2.imread(img_path)

        if img is None:
            raise IOError(f"Could not read image {filename}")

        # Convert image to RGB (OpenCV loads in BGR format)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Calculate the mean value for each row and column
        row_means = np.mean(img_rgb, axis=(1, 2))
        col_means = np.mean(img_rgb, axis=(0, 2))

        # Find the first and last non-black row and column
        nonzero_rows = np.where(row_means > threshold)[0]
        nonzero_cols = np.where(col_means > threshold)[0]

        if len(nonzero_rows) > 0:
            top, bottom = nonzero_rows[0], nonzero_rows[-1]
        else:
            top, bottom = 0, img_rgb.shape[0] - 1
        if len(nonzero_cols) > 0:
            left, right = nonzero_cols[0], nonzero_cols[-1]
        else:
            left, right = 0, img_rgb.shape[1] - 1

        # Crop the image
        cropped_img = img_rgb[top:bottom + 1, left:right + 1]

        # Save the cropped image
        output_path = os.path.join(output_folder, filename)
        cropped_img_bgr = cv2.cvtColor(cropped_img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, cropped_img_bgr)

        print(f"Processed: {filename} ({cropped_img.shape[1]}x{cropped_img.shape[0]})")
        return True
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}", file=sys.stderr)
        return False

def process_images(input_folder, output_folder, threshold, max_workers):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filenames = [f for f in os.listdir(input_folder) if
                 f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))]

    print(f"Processing {len(filenames)} images from {input_folder}")

    success_count = 0
    failure_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_image, filename, input_folder, output_folder, threshold): filename for filename in filenames}
        for future in as_completed(futures):
            if future.result():
                success_count += 1
            else:
                failure_count += 1

    print(f"Finished processing images from {input_folder}")
    print(f"Successful: {success_count}, Failed: {failure_count}")

def main():
    parser = argparse.ArgumentParser(
        description="Process images by cropping out black borders.")
    parser.add_argument("-f", "--folder", action='append',
                        help="Input folder containing images to process")
    parser.add_argument("-i", "--image", action='append',
                        help="Individual image to process")
    parser.add_argument("-o", "--output", required=True, help="Base output directory")
    parser.add_argument("-t", "--threshold", type=int, default=60,
                        help="Threshold for determining black borders (0-255)")
    parser.add_argument("-w", "--workers", type=int, default=os.cpu_count(),
                        help="Number of worker threads (default: number of CPU cores)")
    args = parser.parse_args()

    if not args.folder and not args.image:
        parser.error("At least one input folder (-f) or image (-i) must be specified")

    try:
        if not os.path.exists(args.output):
            os.makedirs(args.output)

        # Process folders
        if args.folder:
            for input_folder in args.folder:
                if not os.path.exists(input_folder):
                    print(f"Error: Input folder {input_folder} does not exist", file=sys.stderr)
                    continue
                output_folder = os.path.join(args.output, os.path.basename(input_folder))
                process_images(input_folder, output_folder, args.threshold, args.workers)

        # Process individual images
        if args.image:
            for input_image in args.image:
                if not os.path.exists(input_image):
                    print(f"Error: Input image {input_image} does not exist", file=sys.stderr)
                    continue
                process_image(os.path.basename(input_image), os.path.dirname(input_image),
                              args.output, args.threshold)

        print("\nAll processing completed")
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()