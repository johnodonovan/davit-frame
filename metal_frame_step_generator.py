#!/usr/bin/env python3
"""
STEP File Generator for Stainless Steel Metal Frame
Generates proper 3D solid geometry in STEP format for CAD/CAM applications
"""

import math
import sys
import os

try:
    import FreeCAD
    import Part
    import Draft
except ImportError:
    print("Error: FreeCAD Python libraries not found.")
    print("Please install FreeCAD or run this script within FreeCAD environment.")
    print("You can install FreeCAD using:")
    print("  - macOS: brew install freecad")
    print("  - Ubuntu: sudo apt install freecad")
    print("  - Windows: Download from https://www.freecad.org/")
    sys.exit(1)

def create_tube_solid(start_point, end_point, outer_diameter):
    """Create a solid tube (cylinder) between two points."""
    
    # Calculate direction vector and length
    direction = FreeCAD.Vector(end_point) - FreeCAD.Vector(start_point)
    length = direction.Length
    
    if length == 0:
        return None
    
    # Create cylinder
    radius = outer_diameter / 2.0
    cylinder = Part.makeCylinder(radius, length)
    
    # Calculate rotation to align with direction
    z_axis = FreeCAD.Vector(0, 0, 1)
    if not direction.isEqual(z_axis, 1e-6) and not direction.isEqual(-z_axis, 1e-6):
        # Calculate rotation axis and angle
        rotation_axis = z_axis.cross(direction.normalize())
        rotation_angle = math.acos(z_axis.dot(direction.normalize()))
        
        # Apply rotation
        cylinder.rotate(FreeCAD.Vector(0, 0, 0), rotation_axis, math.degrees(rotation_angle))
    elif direction.isEqual(-z_axis, 1e-6):
        # Special case: rotate 180 degrees around X axis
        cylinder.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 180)
    
    # Translate to start position
    cylinder.translate(FreeCAD.Vector(start_point))
    
    return cylinder

def create_metal_frame_step():
    """Create the complete metal frame as STEP file."""
    
    # Frame specifications (all dimensions in inches, converted to mm for FreeCAD)
    INCH_TO_MM = 25.4
    
    VERTICAL_HEIGHT = 48.0 * INCH_TO_MM
    HORIZONTAL_LENGTH = 24.0 * INCH_TO_MM
    TUBE_DIAMETER = 2.0 * INCH_TO_MM
    BOTTOM_HORIZONTAL_HEIGHT = 12.0 * INCH_TO_MM
    TOP_HORIZONTAL_HEIGHT = VERTICAL_HEIGHT
    BRACE_LENGTH = 12.0 * INCH_TO_MM
    
    # Spacing between vertical tubes (center to center)
    VERTICAL_SPACING = HORIZONTAL_LENGTH
    
    print(f"Creating metal frame with dimensions:")
    print(f"- Vertical height: {VERTICAL_HEIGHT/INCH_TO_MM:.1f}\" ({VERTICAL_HEIGHT:.1f}mm)")
    print(f"- Horizontal length: {HORIZONTAL_LENGTH/INCH_TO_MM:.1f}\" ({HORIZONTAL_LENGTH:.1f}mm)")
    print(f"- Tube diameter: {TUBE_DIAMETER/INCH_TO_MM:.1f}\" ({TUBE_DIAMETER:.1f}mm)")
    
    # Create new FreeCAD document
    doc = FreeCAD.newDocument("MetalFrame")
    
    # Create all tube solids
    tubes = []
    
    # Position coordinates for the frame
    left_vertical_center = (0, 0, 0)
    right_vertical_center = (VERTICAL_SPACING, 0, 0)
    
    # Create vertical tubes
    print("Creating vertical tubes...")
    
    # Left vertical tube
    left_vertical_start = left_vertical_center
    left_vertical_end = (left_vertical_center[0], left_vertical_center[1], VERTICAL_HEIGHT)
    left_vertical = create_tube_solid(left_vertical_start, left_vertical_end, TUBE_DIAMETER)
    if left_vertical:
        tubes.append(left_vertical)
    
    # Right vertical tube
    right_vertical_start = right_vertical_center
    right_vertical_end = (right_vertical_center[0], right_vertical_center[1], VERTICAL_HEIGHT)
    right_vertical = create_tube_solid(right_vertical_start, right_vertical_end, TUBE_DIAMETER)
    if right_vertical:
        tubes.append(right_vertical)
    
    # Create horizontal tubes
    print("Creating horizontal tubes...")
    
    # Bottom horizontal tube
    bottom_horizontal_start = (0, 0, BOTTOM_HORIZONTAL_HEIGHT)
    bottom_horizontal_end = (VERTICAL_SPACING, 0, BOTTOM_HORIZONTAL_HEIGHT)
    bottom_horizontal = create_tube_solid(bottom_horizontal_start, bottom_horizontal_end, TUBE_DIAMETER)
    if bottom_horizontal:
        tubes.append(bottom_horizontal)
    
    # Top horizontal tube
    top_horizontal_start = (0, 0, TOP_HORIZONTAL_HEIGHT)
    top_horizontal_end = (VERTICAL_SPACING, 0, TOP_HORIZONTAL_HEIGHT)
    top_horizontal = create_tube_solid(top_horizontal_start, top_horizontal_end, TUBE_DIAMETER)
    if top_horizontal:
        tubes.append(top_horizontal)
    
    # Create corner braces
    print("Creating corner braces...")
    
    # Calculate brace offset for 45-degree angles
    brace_offset = BRACE_LENGTH / math.sqrt(2)
    
    # TOP CORNER BRACES
    # Left top corner brace
    left_top_brace_start = (0, 0, TOP_HORIZONTAL_HEIGHT - brace_offset)
    left_top_brace_end = (brace_offset, 0, TOP_HORIZONTAL_HEIGHT)
    left_top_brace = create_tube_solid(left_top_brace_start, left_top_brace_end, TUBE_DIAMETER)
    if left_top_brace:
        tubes.append(left_top_brace)
    
    # Right top corner brace
    right_top_brace_start = (VERTICAL_SPACING, 0, TOP_HORIZONTAL_HEIGHT - brace_offset)
    right_top_brace_end = (VERTICAL_SPACING - brace_offset, 0, TOP_HORIZONTAL_HEIGHT)
    right_top_brace = create_tube_solid(right_top_brace_start, right_top_brace_end, TUBE_DIAMETER)
    if right_top_brace:
        tubes.append(right_top_brace)
    
    # BOTTOM CORNER BRACES
    # Left bottom corner brace
    left_bottom_brace_start = (0, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset)
    left_bottom_brace_end = (brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT)
    left_bottom_brace = create_tube_solid(left_bottom_brace_start, left_bottom_brace_end, TUBE_DIAMETER)
    if left_bottom_brace:
        tubes.append(left_bottom_brace)
    
    # Right bottom corner brace
    right_bottom_brace_start = (VERTICAL_SPACING, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset)
    right_bottom_brace_end = (VERTICAL_SPACING - brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT)
    right_bottom_brace = create_tube_solid(right_bottom_brace_start, right_bottom_brace_end, TUBE_DIAMETER)
    if right_bottom_brace:
        tubes.append(right_bottom_brace)
    
    print(f"Created {len(tubes)} tube components")
    
    # Create compound of all tubes
    if tubes:
        print("Combining all components...")
        compound = Part.makeCompound(tubes)
        
        # Create FreeCAD object
        frame_obj = doc.addObject("Part::Feature", "MetalFrame")
        frame_obj.Shape = compound
        frame_obj.Label = "Stainless Steel Metal Frame"
        
        # Set material properties (for display)
        frame_obj.ViewObject.ShapeColor = (0.8, 0.8, 0.9)  # Light steel color
        frame_obj.ViewObject.Transparency = 0
        
        # Recompute document
        doc.recompute()
        
        return doc, frame_obj
    else:
        print("Error: No tubes were created successfully")
        return None, None

def export_to_step(doc, frame_obj, filename="stainless_steel_frame.step"):
    """Export the frame to STEP format."""
    
    if not doc or not frame_obj:
        print("Error: No valid frame object to export")
        return False
    
    try:
        # Export to STEP format
        print(f"Exporting to STEP format: {filename}")
        
        # Get the shape
        shape = frame_obj.Shape
        
        # Export using Part module
        shape.exportStep(filename)
        
        print(f"✓ STEP file saved as: {filename}")
        
        # Get file size for confirmation
        file_size = os.path.getsize(filename)
        print(f"✓ File size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"Error exporting to STEP: {e}")
        return False

def create_technical_drawing_info():
    """Print technical specifications for the frame."""
    
    print("\n" + "="*60)
    print("STAINLESS STEEL METAL FRAME - TECHNICAL SPECIFICATIONS")
    print("="*60)
    print("FRAME DIMENSIONS:")
    print("- Overall Height: 48.000\"")
    print("- Overall Width: 24.000\"")
    print("- Tube Outer Diameter: 2.000\"")
    print("- Material: Stainless Steel")
    print("")
    print("COMPONENT DETAILS:")
    print("- Vertical Tubes: 2 pieces @ 48.000\" length")
    print("- Horizontal Tubes: 2 pieces @ 24.000\" length")
    print("  * Top rail at 48.000\" height")
    print("  * Bottom rail at 12.000\" height")
    print("- Corner Braces: 4 pieces @ 12.000\" length")
    print("  * Positioned at 45° angles")
    print("  * 2 braces at top corners")
    print("  * 2 braces at bottom corners")
    print("")
    print("FABRICATION NOTES:")
    print("- All joints to be welded")
    print("- Corner braces provide structural reinforcement")
    print("- Bottom braces positioned above bottom rail")
    print("- Top braces positioned below top rail")
    print("- All dimensions in inches unless noted")
    print("="*60)

def main():
    """Main function to generate the STEP file."""
    
    print("STEP File Generator for Stainless Steel Metal Frame")
    print("=" * 55)
    
    try:
        # Create the frame
        doc, frame_obj = create_metal_frame_step()
        
        if doc and frame_obj:
            # Export to STEP
            step_filename = "stainless_steel_frame.step"
            success = export_to_step(doc, frame_obj, step_filename)
            
            if success:
                # Also export as IGES for additional compatibility
                try:
                    iges_filename = "stainless_steel_frame.iges"
                    frame_obj.Shape.exportIges(iges_filename)
                    print(f"✓ IGES file also saved as: {iges_filename}")
                except:
                    print("Note: IGES export not available")
                
                # Print technical specifications
                create_technical_drawing_info()
                
                print(f"\n🎉 Frame generation complete!")
                print(f"📁 Files created:")
                print(f"   • {step_filename} (STEP format)")
                if os.path.exists("stainless_steel_frame.iges"):
                    print(f"   • stainless_steel_frame.iges (IGES format)")
                
                print(f"\nThe STEP file is ready for:")
                print(f"   • CAD software import")
                print(f"   • CNC machining")
                print(f"   • 3D printing")
                print(f"   • Manufacturing analysis")
                
                return True
            else:
                print("❌ Failed to export STEP file")
                return False
        else:
            print("❌ Failed to create frame geometry")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    finally:
        # Clean up FreeCAD document
        try:
            if 'doc' in locals() and doc:
                FreeCAD.closeDocument(doc.Name)
        except:
            pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 