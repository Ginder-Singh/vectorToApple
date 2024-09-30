# vectorToApple

## Overview
`vectorToApple` is a Python script that converts Android vector drawable XML files into iOS and tvOS-compatible image assets. It generates SVG and PNG files, scales them for different resolutions, and creates the necessary `Contents.json` files for Xcode asset catalogs.

## Features
- Converts Android vector drawables to SVG format.
- Converts SVG files to PNG format with specified dimensions.
- Scales PNG images for 1x, 2x, and 3x resolutions.
- Generates `Contents.json` files for asset organization.

## Requirements
- Python 3.x
- `cairosvg` library
- `PIL` (Pillow) library
- `tqdm` library
- Node.js with `npx` installed
- `vector-drawable-svg` package

## Setup
1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```
2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. **Install required packages**:
   ```bash
   pip install cairosvg Pillow tqdm
   ```

## Usage
1. Place your Android vector drawable XML files in a directory. **Note:** Ensure that the Android vector assets are in the same aspect ratio as required for the target tvOS or iOS output.
2. Run the script:
   ```bash
   python convert.py
   ```
3. Follow the prompts to specify:
   - The folder name for the assets (default: `Flags.xcassets`)
   - A suffix for the file names (optional)
   - Desired width and height for the output images
   - The idiom (tv/ios)
   - The directory containing the `.xml` files

## Output
The script will create an `.xcassets` directory containing:
- SVG files for each vector drawable.
- PNG files scaled for 1x, 2x, and 3x (if applicable).
- `Contents.json` files for each image set.

## License
This project is licensed under the MIT License.