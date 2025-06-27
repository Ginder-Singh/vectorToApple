import os
import subprocess
import json
import shutil
from tqdm import tqdm

def convert_android_vector_to_svg(xml_file, output_file):
    """Converts an Android vector drawable XML file to an SVG file using npx."""
    try:
        subprocess.run(['npx', 'vector-drawable-svg', xml_file, output_file], check=True, timeout=15)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error converting {xml_file} to SVG: {e}")
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout: Conversion of {xml_file} took too long.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def optimize_svg(input_svg, output_svg):
    """Optimizes an SVG using scour for better scaling/rendering."""
    try:
        subprocess.run([
            'scour', '-i', input_svg, '-o', output_svg,
            '--enable-viewboxing', '--enable-id-stripping',
            '--shorten-ids', '--remove-metadata'
        ], check=True)
        return True
    except Exception as e:
        print(f"Error optimizing SVG {input_svg}: {e}")
        return False

def create_svg_with_size(input_svg, output_svg, width, height):
    """Creates an SVG with specific dimensions using rsvg-convert to properly scale content."""
    try:
        # Use rsvg-convert to resize the SVG while maintaining aspect ratio
        subprocess.run([
            'rsvg-convert',
            '-w', str(width),
            '-h', str(height),
            '-f', 'svg',
            '-o', output_svg,
            input_svg
        ], check=True)
        return True
    except Exception as e:
        print(f"Error creating sized SVG {output_svg}: {e}")
        return False

def create_imageset_contents_json(imageset_directory, asset_name, idiom="universal"):
    """Creates a Contents.json file for the imageset directory with SVG files."""
    images = [
        {"filename": f"{asset_name}.svg", "idiom": idiom, "scale": "1x"},
        {"filename": f"{asset_name}@2x.svg", "idiom": idiom, "scale": "2x"},
        {"filename": f"{asset_name}@3x.svg", "idiom": idiom, "scale": "3x"}
    ]
    
    contents = {
        "images": images,
        "info": {"author": "xcode", "version": 1}
    }
    
    with open(os.path.join(imageset_directory, "Contents.json"), 'w') as json_file:
        json.dump(contents, json_file, indent=2)

def create_assets_catalog(input_directory, output_directory, suffix=""):
    """Creates a proper Xcode asset catalog structure with SVG files."""
    # Create the main assets directory
    assets_directory = os.path.join(output_directory, "Flags.assets")
    os.makedirs(assets_directory, exist_ok=True)
    
    # Create root Contents.json for the assets catalog
    root_contents = {"info": {"author": "xcode", "version": 1}}
    with open(os.path.join(assets_directory, "Contents.json"), 'w') as f:
        json.dump(root_contents, f, indent=2)
    
    # Only process XML files that end with _small
    xml_files = [f for f in os.listdir(input_directory) if f.endswith('.xml') and f.endswith('_small.xml')]
    
    print(f"\n📂 Processing {len(xml_files)} XML files (only '_small' files)...")
    print(f"📁 Output directory: {assets_directory}")
    
    successful_conversions = 0
    
    for filename in tqdm(xml_files, desc="Creating asset catalog", unit="file"):
        xml_file = os.path.join(input_directory, filename)
        
        # Transform filename: us_small.xml -> US-s
        base_name = os.path.splitext(filename)[0]  # us_small
        if base_name.endswith('_small'):
            base_name = base_name[:-6]  # Remove '_small' -> us
        base_name = base_name.upper()  # US
        asset_name = f"{base_name}-s"  # US-s
        
        # Add suffix if provided
        if suffix:
            asset_name = f"{base_name}-s-{suffix}"
        
        # Create imageset directory
        imageset_directory = os.path.join(assets_directory, f"{asset_name}.imageset")
        os.makedirs(imageset_directory, exist_ok=True)
        
        # Create temporary SVG files
        temp_svg = os.path.join(imageset_directory, f"{asset_name}.temp.svg")
        optimized_svg = os.path.join(imageset_directory, f"{asset_name}.opt.svg")
        
        # Step 1: Convert XML → SVG
        if convert_android_vector_to_svg(xml_file, temp_svg):
            # Step 2: Optimize SVG
            if optimize_svg(temp_svg, optimized_svg):
                # Use optimized version
                os.remove(temp_svg)
                shutil.move(optimized_svg, temp_svg)
            
            # Step 3: Create SVG files at different sizes (20, 40, 60)
            svg_1x = os.path.join(imageset_directory, f"{asset_name}.svg")      # 20x20
            svg_2x = os.path.join(imageset_directory, f"{asset_name}@2x.svg")  # 40x40
            svg_3x = os.path.join(imageset_directory, f"{asset_name}@3x.svg")  # 60x60
            
            # Create sized SVG files
            if create_svg_with_size(temp_svg, svg_1x, 20, 20):
                create_svg_with_size(temp_svg, svg_2x, 40, 40)
                create_svg_with_size(temp_svg, svg_3x, 60, 60)
                
                # Create Contents.json for this imageset
                create_imageset_contents_json(imageset_directory, asset_name)
                successful_conversions += 1
            else:
                print(f"Failed to create sized SVG for {filename}")
            
            # Clean up temporary SVG
            if os.path.exists(temp_svg):
                os.remove(temp_svg)
        else:
            print(f"Failed to convert {filename} to SVG")
    
    # Create catalog summary
    catalog_data = {
        "name": "Flags Asset Catalog",
        "version": "1.0",
        "total_files": len(xml_files),
        "successful_conversions": successful_conversions,
        "failed_conversions": len(xml_files) - successful_conversions,
        "filter": "Only files ending with '_small.xml'",
        "naming_convention": "UPPERCASE-s (e.g., us_small.xml -> US-s.imageset)",
        "file_type": "SVG",
        "sizes": "20x20 (1x), 40x40 (2x), 60x60 (3x)"
    }
    
    catalog_file = os.path.join(output_directory, "catalog.json")
    with open(catalog_file, 'w') as f:
        json.dump(catalog_data, f, indent=2)
    
    # Create README
    readme_content = f"""# Flags Asset Catalog

This directory contains a proper Xcode asset catalog structure for flag icons using SVG files.

## Structure
```
Flags.assets/
├── Contents.json
├── US-s.imageset/
│   ├── Contents.json
│   ├── US-s.svg          (20x20)
│   ├── US-s@2x.svg       (40x40)
│   └── US-s@3x.svg       (60x60)
└── [other flag imagesets...]
```

## Summary
- Total files processed: {len(xml_files)}
- Successful conversions: {successful_conversions}
- Failed conversions: {len(xml_files) - successful_conversions}
- Filter: Only files ending with '_small.xml'
- Naming: UPPERCASE-s (e.g., us_small.xml → US-s.imageset)
- File type: SVG
- Sizes: 20x20 (1x), 40x40 (2x), 60x60 (3x)

## Usage
1. Copy the `Flags.assets` folder to your Xcode project
2. Add it to your project's asset catalog
3. Use in code: `Image("US-s")`
4. Xcode will automatically select the appropriate SVG size based on device scale
"""
    
    readme_file = os.path.join(output_directory, "README.md")
    with open(readme_file, 'w') as f:
        f.write(readme_content)
    
    return successful_conversions, len(xml_files)

def main():
    print("🔄 Flags Asset Catalog Creator (SVG)")
    print("=" * 40)
    
    input_directory = input("Enter directory containing .xml files: ").strip()
    output_directory = input("Enter output directory: ").strip()
    suffix = input("Enter a suffix for file names (leave blank for none): ").strip()
    
    input_directory = os.path.abspath(os.path.expanduser(input_directory))
    output_directory = os.path.abspath(os.path.expanduser(output_directory))
    
    if not os.path.exists(input_directory):
        print(f"❌ Input directory does not exist: {input_directory}")
        return
    
    successful, total = create_assets_catalog(input_directory, output_directory, suffix)
    
    print(f"\n✅ Asset catalog created successfully!")
    print(f"📊 Successfully converted: {successful}/{total} files")
    print(f"📁 Asset catalog location: {os.path.join(output_directory, 'Flags.assets')}")
    print(f"📋 Catalog file: {os.path.join(output_directory, 'catalog.json')}")
    print(f"📖 README file: {os.path.join(output_directory, 'README.md')}")

if __name__ == "__main__":
    main()