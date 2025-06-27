# Flags Asset Catalog

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
- Total files processed: 251
- Successful conversions: 250
- Failed conversions: 1
- Filter: Only files ending with '_small.xml'
- Naming: UPPERCASE-s (e.g., us_small.xml → US-s.imageset)
- File type: SVG
- Sizes: 20x20 (1x), 40x40 (2x), 60x60 (3x)

## Usage
1. Copy the `Flags.assets` folder to your Xcode project
2. Add it to your project's asset catalog
3. Use in code: `Image("US-s")`
4. Xcode will automatically select the appropriate SVG size based on device scale
