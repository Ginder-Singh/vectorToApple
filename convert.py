import os
import subprocess
import json
import cairosvg
import shutil
from tqdm import tqdm
from PIL import Image

def convert_android_vector_to_svg(xml_file, output_file):
    """Converts an Android vector drawable XML file to an SVG file using npx."""
    try:
        subprocess.run(['npx', 'vector-drawable-svg', xml_file, output_file], check=True, timeout=15)
    except subprocess.CalledProcessError as e:
        print(f"Error converting {xml_file} to SVG: {e}")
    except subprocess.TimeoutExpired:
        print(f"Timeout: Conversion of {xml_file} took too long.")
    except Exception as e:
        print(f"Unexpected error: {e}")

def convert_svg_to_png(input_file, output_file, width, height):
    """Converts an SVG file to a PNG file using cairosvg with specified dimensions."""
    try:
        cairosvg.svg2png(url=input_file, write_to=output_file, output_width=width, output_height=height)
    except Exception as e:
        print(f"Error converting {input_file} to PNG: {e}")

def scale_png(input_file, output_file, new_width, new_height):
    """Scales the PNG file to the specified width and height using PIL."""
    try:
        with Image.open(input_file) as img:
            img = img.resize((new_width, new_height), Image.LANCZOS)
            img.save(output_file, format='PNG')
    except Exception as e:
        print(f"Error scaling PNG {input_file}: {e}")

def create_contents_json(imageset_directory, flag_name, idiom):
    """Creates a Contents.json file for the imageset directory."""
    images = [
        {"filename": f"{flag_name}.png", "idiom": idiom, "scale": "1x"},
        {"filename": f"{flag_name}@2x.png", "idiom": idiom, "scale": "2x"},
    ]
    if idiom in ["ios", "universal"]:
        images.append({"filename": f"{flag_name}@3x.png", "idiom": idiom, "scale": "3x"})
    
    contents = {
        "images": images,
        "info": {"author": "xcode", "version": 1}
    }
    with open(os.path.join(imageset_directory, "Contents.json"), 'w') as json_file:
        json.dump(contents, json_file, indent=2)

def create_root_contents_json(xcassets_directory):
    """Creates a Contents.json file for the main assets directory."""
    contents = {"info": {"author": "xcode", "version": 1}}
    with open(os.path.join(xcassets_directory, "Contents.json"), 'w') as json_file:
        json.dump(contents, json_file, indent=2)

def main():
    xcassets_name = input("Enter the folder name for the assets (default: Flags.xcassets): ") or "Flags.xcassets"
    suffix = input("Enter a suffix for the file names (leave blank for none): ").strip()
    desired_width = int(input("Enter the desired width for the output images: "))
    desired_height = int(input("Enter the desired height for the output images: "))
    idiom = input("Enter the idiom (tv/ios/universal): ").strip().lower()
    input_directory = input("Enter the directory containing the .xml files: ")

    # Expand user directory if using ~
    input_directory = os.path.expanduser(input_directory)

    # Ensure the input directory is absolute
    input_directory = os.path.abspath(input_directory)

    xcassets_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), xcassets_name)
    os.makedirs(xcassets_directory, exist_ok=True)
    create_root_contents_json(xcassets_directory)

    xml_files = [f for f in os.listdir(input_directory) if f.endswith('.xml')]
    
    for filename in tqdm(xml_files, desc="Processing files", unit="file"):
        xml_file = os.path.join(input_directory, filename)
        flag_name = os.path.splitext(filename)[0]
        if suffix:
            flag_name += f"-{suffix}"

        output_svg_file = os.path.join(xcassets_directory, f"{flag_name}.svg")
        output_png_file = os.path.join(xcassets_directory, f"{flag_name}.png")

        convert_android_vector_to_svg(xml_file, output_svg_file)
        convert_svg_to_png(output_svg_file, output_png_file, desired_width, desired_height)

        if not os.path.exists(output_png_file) or os.path.getsize(output_png_file) == 0:
            continue

        imageset_directory = os.path.join(xcassets_directory, f"{flag_name}.imageset")
        os.makedirs(imageset_directory, exist_ok=True)
        shutil.move(output_png_file, os.path.join(imageset_directory, f"{flag_name}.png"))

        # Scale the PNG image for 2x output
        scaled_png_file_2x = os.path.join(imageset_directory, f"{flag_name}@2x.png")
        scale_png(os.path.join(imageset_directory, f"{flag_name}.png"), scaled_png_file_2x, desired_width * 2, desired_height * 2)

        # Scale for 3x output if idiom is ios or universal
        if idiom in ["ios", "universal"]:
            scaled_png_file_3x = os.path.join(imageset_directory, f"{flag_name}@3x.png")
            scale_png(os.path.join(imageset_directory, f"{flag_name}.png"), scaled_png_file_3x, desired_width * 3, desired_height * 3)

        create_contents_json(imageset_directory, flag_name, idiom)

        required_files = [
            os.path.join(imageset_directory, f"{flag_name}.png"),
            os.path.join(imageset_directory, f"{flag_name}@2x.png"),
        ]
        if idiom in ["ios", "universal"]:
            required_files.append(os.path.join(imageset_directory, f"{flag_name}@3x.png"))

        required_files.append(os.path.join(imageset_directory, "Contents.json"))

        if not all(os.path.exists(file) for file in required_files):
            shutil.rmtree(imageset_directory)

    for file in os.listdir(xcassets_directory):
        if file.endswith('.svg'):
            os.remove(os.path.join(xcassets_directory, file))

    print(f"\nTotal files processed: {len(xml_files)}")

if __name__ == "__main__":
    main()