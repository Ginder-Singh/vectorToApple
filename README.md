# vectorToApple

## Overview
`vectortoapple` is a Python tool that converts Android vector drawable XML files into iOS, tvOS, and universal-compatible image assets. It generates SVG and PNG files, scales them for different resolutions, and creates the necessary `Contents.json` files for Xcode asset catalogs.

## Installation

To install vectortoapple you can use `pip`, the Python package manager. Follow the steps below:

### Prerequisites

Make sure you have Python 3.6 or higher installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### Install via PyPI

You can install vectortoapple directly from the Python Package Index (PyPI) using the following command:

```bash
pip install vectortoapple
```

### Install from Source

If you prefer to install from the source, you can clone the repository and install it manually:

1. Clone the repository:
   ```bash
   git clone https://github.com/Ginder-Singh/vectortoapple.git
   cd vectortoapple
   ```

2. Install the package:
   ```bash
   pip install .
   ```

### Install Development Dependencies

If you want to contribute to the development of `vectortoapple`, you may want to install the development dependencies. You can do this by creating a virtual environment and installing the requirements:

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install development dependencies
pip install -r requirements.txt
```

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

After installing `vectortoapple`, you can use it from the command line. Simply run the following command:

```bash
vectortoapple
```

## Output
The script will create an `.xcassets` directory containing:
- SVG files for each vector drawable.
- PNG files scaled for 1x, 2x, and 3x (if applicable).
- `Contents.json` files for each image set.

## Contributing

If you would like to contribute to `vectortoapple`, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.