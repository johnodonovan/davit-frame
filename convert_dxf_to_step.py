#!/usr/bin/env python3
"""
DXF to STEP Converter
Converts the existing DXF file to STEP format using available conversion methods
"""

import os
import sys
import subprocess

def check_freecad_availability():
    """Check if FreeCAD is available for conversion."""
    try:
        import FreeCAD
        return True
    except ImportError:
        return False

def check_opencascade_availability():
    """Check if OpenCASCADE Python bindings are available."""
    try:
        import OCC
        return True
    except ImportError:
        try:
            import occwl
            return True
        except ImportError:
            return False

def convert_with_freecad(dxf_file, step_file):
    """Convert DXF to STEP using FreeCAD."""
    try:
        import FreeCAD
        import Import
        
        print("Using FreeCAD for conversion...")
        
        # Create new document
        doc = FreeCAD.newDocument("Conversion")
        
        # Import DXF file
        Import.insert(dxf_file, doc.Name)
        
        # Get all objects
        objects = doc.Objects
        
        if not objects:
            print("No objects found in DXF file")
            return False
        
        # Try to create a compound from all objects
        shapes = []
        for obj in objects:
            if hasattr(obj, 'Shape') and obj.Shape:
                shapes.append(obj.Shape)
        
        if shapes:
            import Part
            compound = Part.makeCompound(shapes)
            
            # Export to STEP
            compound.exportStep(step_file)
            print(f"✓ Converted to STEP: {step_file}")
            
            # Clean up
            FreeCAD.closeDocument(doc.Name)
            return True
        else:
            print("No valid shapes found for conversion")
            FreeCAD.closeDocument(doc.Name)
            return False
            
    except Exception as e:
        print(f"FreeCAD conversion failed: {e}")
        return False

def convert_with_external_tools():
    """Try to convert using external command-line tools."""
    
    # Check for common CAD conversion tools
    tools_to_try = [
        "meshconv",  # MeshLab command line
        "assimp",    # Open Asset Import Library
        "cadquery",  # CadQuery if available
    ]
    
    for tool in tools_to_try:
        if subprocess.run(["which", tool], capture_output=True).returncode == 0:
            print(f"Found external tool: {tool}")
            # Tool-specific conversion logic would go here
            return False  # Not implemented yet
    
    return False

def create_step_using_native_generator():
    """Use our native STEP generator instead of conversion."""
    
    print("Attempting to use native STEP generator...")
    
    # Check if our STEP generator script exists
    if os.path.exists("metal_frame_step_generator.py"):
        try:
            result = subprocess.run([sys.executable, "metal_frame_step_generator.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Successfully generated STEP file using native generator")
                print(result.stdout)
                return True
            else:
                print("Native STEP generator failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"Error running native STEP generator: {e}")
            return False
    else:
        print("Native STEP generator not found")
        return False

def main():
    """Main conversion function."""
    
    print("DXF to STEP Converter")
    print("=" * 30)
    
    # Check if DXF file exists
    dxf_file = "stainless_steel_frame_3d.dxf"
    step_file = "stainless_steel_frame.step"
    
    if not os.path.exists(dxf_file):
        print(f"DXF file not found: {dxf_file}")
        print("Please run metal_frame_generator.py first to create the DXF file")
        return False
    
    print(f"Input file: {dxf_file}")
    print(f"Output file: {step_file}")
    print()
    
    # Try different conversion methods in order of preference
    
    # Method 1: Use FreeCAD if available
    if check_freecad_availability():
        print("Method 1: Trying FreeCAD conversion...")
        if convert_with_freecad(dxf_file, step_file):
            return True
        print("FreeCAD conversion failed, trying next method...")
        print()
    
    # Method 2: Use native STEP generator
    print("Method 2: Trying native STEP generator...")
    if create_step_using_native_generator():
        return True
    print("Native STEP generator failed, trying next method...")
    print()
    
    # Method 3: Try external tools
    print("Method 3: Trying external conversion tools...")
    if convert_with_external_tools():
        return True
    print("External tools not available or failed...")
    print()
    
    # Method 4: Provide instructions for manual conversion
    print("Method 4: Manual conversion instructions")
    print("-" * 40)
    print("Automatic conversion failed. You can manually convert the DXF file using:")
    print()
    print("Option A - FreeCAD (Recommended):")
    print("1. Install FreeCAD: https://www.freecad.org/")
    print("2. Open FreeCAD")
    print("3. File → Open → Select stainless_steel_frame_3d.dxf")
    print("4. File → Export → Select STEP format")
    print("5. Save as stainless_steel_frame.step")
    print()
    print("Option B - Online Converters:")
    print("1. Visit: https://www.convertio.co/dxf-step/")
    print("2. Upload: stainless_steel_frame_3d.dxf")
    print("3. Convert to STEP format")
    print("4. Download the converted file")
    print()
    print("Option C - CAD Software:")
    print("1. Open the DXF file in AutoCAD, SolidWorks, or similar")
    print("2. Export/Save As STEP format")
    print()
    print("The DXF file contains proper 3D solid geometry and should")
    print("convert cleanly to STEP format using any of these methods.")
    
    return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Conversion completed successfully!")
        
        # Check if STEP file was created
        if os.path.exists("stainless_steel_frame.step"):
            file_size = os.path.getsize("stainless_steel_frame.step")
            print(f"📁 STEP file created: stainless_steel_frame.step ({file_size:,} bytes)")
            print("\nThe STEP file is ready for:")
            print("• CAD software import")
            print("• CNC machining")
            print("• 3D printing")
            print("• Manufacturing analysis")
        
    else:
        print("\n⚠️  Automatic conversion was not successful.")
        print("Please follow the manual conversion instructions above.")
    
    sys.exit(0 if success else 1) 