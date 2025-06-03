#!/usr/bin/env python3
"""
3D DXF Generator for Stainless Steel Metal Frame
Specifications:
- Two 48" vertical tubes (2" outer diameter)
- Two 24" horizontal tubes (2" outer diameter)
- Top horizontal tube at the top of verticals
- Bottom horizontal tube 12" from bottom of verticals
- Four 45-degree corner braces (12" long) forming triangles at top
"""

import ezdxf
import math
from ezdxf.math import Vec3

def create_metal_frame_dxf():
    """Create a 3D DXF file for the metal frame fabrication."""
    
    # Create a new DXF document
    doc = ezdxf.new('R2010')  # Use AutoCAD 2010 format for better compatibility
    msp = doc.modelspace()
    
    # Frame specifications (all dimensions in inches)
    VERTICAL_HEIGHT = 48.0
    HORIZONTAL_LENGTH = 24.0
    TUBE_DIAMETER = 2.0
    TUBE_RADIUS = TUBE_DIAMETER / 2.0
    BOTTOM_HORIZONTAL_HEIGHT = 12.0  # Height from bottom
    TOP_HORIZONTAL_HEIGHT = VERTICAL_HEIGHT  # At the top
    BRACE_LENGTH = 12.0  # Length of diagonal braces
    
    # Spacing between vertical tubes (center to center)
    VERTICAL_SPACING = HORIZONTAL_LENGTH
    
    # Define colors for different components
    VERTICAL_COLOR = 1  # Red
    HORIZONTAL_COLOR = 2  # Yellow
    BRACE_COLOR = 3  # Green
    
    # Create layers for organization
    doc.layers.new('VERTICAL_TUBES', dxfattribs={'color': VERTICAL_COLOR})
    doc.layers.new('HORIZONTAL_TUBES', dxfattribs={'color': HORIZONTAL_COLOR})
    doc.layers.new('CORNER_BRACES', dxfattribs={'color': BRACE_COLOR})
    doc.layers.new('DIMENSIONS', dxfattribs={'color': 7})  # White
    doc.layers.new('CENTERLINES', dxfattribs={'color': 8, 'linetype': 'CENTER'})
    
    # Position coordinates for the frame
    # Left vertical tube center
    left_vertical_center = Vec3(0, 0, 0)
    # Right vertical tube center  
    right_vertical_center = Vec3(VERTICAL_SPACING, 0, 0)
    
    # Create vertical tubes as 3D solids
    # Left vertical tube
    create_tube_solid(msp, 
                     start_point=left_vertical_center,
                     end_point=left_vertical_center + Vec3(0, 0, VERTICAL_HEIGHT),
                     radius=TUBE_RADIUS,
                     layer='VERTICAL_TUBES')
    
    # Right vertical tube
    create_tube_solid(msp,
                     start_point=right_vertical_center,
                     end_point=right_vertical_center + Vec3(0, 0, VERTICAL_HEIGHT),
                     radius=TUBE_RADIUS,
                     layer='VERTICAL_TUBES')
    
    # Create horizontal tubes as 3D solids
    # Bottom horizontal tube (12" from bottom)
    bottom_horizontal_start = Vec3(0, 0, BOTTOM_HORIZONTAL_HEIGHT)
    bottom_horizontal_end = Vec3(VERTICAL_SPACING, 0, BOTTOM_HORIZONTAL_HEIGHT)
    
    create_tube_solid(msp,
                     start_point=bottom_horizontal_start,
                     end_point=bottom_horizontal_end,
                     radius=TUBE_RADIUS,
                     layer='HORIZONTAL_TUBES')
    
    # Top horizontal tube (at top of verticals)
    top_horizontal_start = Vec3(0, 0, TOP_HORIZONTAL_HEIGHT)
    top_horizontal_end = Vec3(VERTICAL_SPACING, 0, TOP_HORIZONTAL_HEIGHT)
    
    create_tube_solid(msp,
                     start_point=top_horizontal_start,
                     end_point=top_horizontal_end,
                     radius=TUBE_RADIUS,
                     layer='HORIZONTAL_TUBES')
    
    # Create diagonal corner braces at all four corners
    # Calculate brace positions to reinforce all frame corners
    # Each brace will be 12" long connecting vertical and horizontal tubes
    
    # For 12" braces at 45 degrees, the horizontal and vertical components are each 12/√2 ≈ 8.485"
    brace_offset = BRACE_LENGTH / math.sqrt(2)
    
    # TOP CORNER BRACES
    # Left top corner brace - from vertical tube to horizontal tube
    # Diagonal brace from left vertical down to a point on the top horizontal
    left_top_brace_start = Vec3(0, 0, TOP_HORIZONTAL_HEIGHT - brace_offset)  # Point on left vertical below top rail
    left_top_brace_end = Vec3(brace_offset, 0, TOP_HORIZONTAL_HEIGHT)  # Point on top horizontal
    
    create_tube_solid(msp,
                     start_point=left_top_brace_start,
                     end_point=left_top_brace_end,
                     radius=TUBE_RADIUS,
                     layer='CORNER_BRACES')
    
    # Right top corner brace - from vertical tube to horizontal tube
    # Diagonal brace from right vertical down to a point on the top horizontal
    right_top_brace_start = Vec3(VERTICAL_SPACING, 0, TOP_HORIZONTAL_HEIGHT - brace_offset)  # Point on right vertical below top rail
    right_top_brace_end = Vec3(VERTICAL_SPACING - brace_offset, 0, TOP_HORIZONTAL_HEIGHT)  # Point on top horizontal
    
    create_tube_solid(msp,
                     start_point=right_top_brace_start,
                     end_point=right_top_brace_end,
                     radius=TUBE_RADIUS,
                     layer='CORNER_BRACES')
    
    # BOTTOM CORNER BRACES
    # Left bottom corner brace - from vertical tube to horizontal tube (above the horizontal bar)
    # Diagonal brace from left vertical up to a point on the bottom horizontal
    left_bottom_brace_start = Vec3(0, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset)  # Point on left vertical above bottom rail
    left_bottom_brace_end = Vec3(brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT)  # Point on bottom horizontal
    
    create_tube_solid(msp,
                     start_point=left_bottom_brace_start,
                     end_point=left_bottom_brace_end,
                     radius=TUBE_RADIUS,
                     layer='CORNER_BRACES')
    
    # Right bottom corner brace - from vertical tube to horizontal tube (above the horizontal bar)
    # Diagonal brace from right vertical up to a point on the bottom horizontal
    right_bottom_brace_start = Vec3(VERTICAL_SPACING, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset)  # Point on right vertical above bottom rail
    right_bottom_brace_end = Vec3(VERTICAL_SPACING - brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT)  # Point on bottom horizontal
    
    create_tube_solid(msp,
                     start_point=right_bottom_brace_start,
                     end_point=right_bottom_brace_end,
                     radius=TUBE_RADIUS,
                     layer='CORNER_BRACES')
    
    # Add centerlines for fabrication reference
    add_centerlines(msp, left_vertical_center, right_vertical_center, 
                   VERTICAL_HEIGHT, BOTTOM_HORIZONTAL_HEIGHT, TOP_HORIZONTAL_HEIGHT)
    
    # Add dimensions
    add_dimensions(msp, VERTICAL_HEIGHT, HORIZONTAL_LENGTH, BOTTOM_HORIZONTAL_HEIGHT, BRACE_LENGTH)
    
    # Add text annotations
    add_annotations(msp)
    
    return doc

def create_tube_solid(msp, start_point, end_point, radius, layer):
    """Create a proper closed 3D solid tube."""
    
    # Calculate tube direction and length
    direction = end_point - start_point
    length = direction.magnitude
    
    if length == 0:
        return
    
    direction = direction.normalize()
    
    # Create perpendicular vectors for the circular cross-section
    if abs(direction.z) < 0.99:
        perp1 = Vec3(-direction.y, direction.x, 0).normalize()
    else:
        perp1 = Vec3(1, 0, 0)
    
    perp2 = direction.cross(perp1).normalize()
    
    # Create a proper closed polyface mesh with end caps
    create_closed_tube_mesh(msp, start_point, end_point, radius, layer, direction, perp1, perp2)

def create_closed_tube_mesh(msp, start_point, end_point, radius, layer, direction, perp1, perp2, segments=16):
    """Create a closed tube using 3DFACE entities for maximum compatibility."""
    
    try:
        # Generate points for start and end circles
        start_points = []
        end_points = []
        
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            offset = radius * (math.cos(angle) * perp1 + math.sin(angle) * perp2)
            start_points.append(start_point + offset)
            end_points.append(end_point + offset)
        
        # Create side faces using 3DFACE
        for i in range(segments):
            next_i = (i + 1) % segments
            
            # Create rectangular face as a 4-point 3DFACE
            p1 = start_points[i]
            p2 = start_points[next_i]
            p3 = end_points[next_i]
            p4 = end_points[i]
            
            # Create 4-point face (quad)
            msp.add_3dface([p1, p2, p3, p4], dxfattribs={'layer': layer})
        
        # Create end caps using triangular faces
        # Start cap (bottom)
        for i in range(segments):
            next_i = (i + 1) % segments
            msp.add_3dface([start_point, start_points[i], start_points[next_i], start_points[next_i]], 
                           dxfattribs={'layer': layer})
        
        # End cap (top)
        for i in range(segments):
            next_i = (i + 1) % segments
            msp.add_3dface([end_point, end_points[next_i], end_points[i], end_points[i]], 
                           dxfattribs={'layer': layer})
        
    except Exception as e:
        print(f"Warning: Could not create 3DFACE tube: {e}")
        # Final fallback to basic cylinder representation
        create_basic_cylinder(msp, start_point, end_point, radius, layer, direction, perp1, perp2)

def create_basic_cylinder(msp, start_point, end_point, radius, layer, direction, perp1, perp2, segments=16):
    """Create a basic cylinder using 3DFACE entities for maximum compatibility."""
    
    # Generate points for start and end circles
    start_points = []
    end_points = []
    
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        offset = radius * (math.cos(angle) * perp1 + math.sin(angle) * perp2)
        start_points.append(start_point + offset)
        end_points.append(end_point + offset)
    
    # Create side faces using 3DFACE
    for i in range(segments):
        next_i = (i + 1) % segments
        
        # Create rectangular face as two triangles
        p1 = start_points[i]
        p2 = start_points[next_i]
        p3 = end_points[next_i]
        p4 = end_points[i]
        
        # First triangle
        msp.add_3dface([p1, p2, p3, p3], dxfattribs={'layer': layer})
        # Second triangle
        msp.add_3dface([p1, p3, p4, p4], dxfattribs={'layer': layer})
    
    # Create end caps using triangular faces
    # Start cap
    for i in range(segments):
        next_i = (i + 1) % segments
        msp.add_3dface([start_point, start_points[i], start_points[next_i], start_points[next_i]], 
                       dxfattribs={'layer': layer})
    
    # End cap
    for i in range(segments):
        next_i = (i + 1) % segments
        msp.add_3dface([end_point, end_points[next_i], end_points[i], end_points[i]], 
                       dxfattribs={'layer': layer})

def create_tube_wireframe(msp, start_point, end_point, radius, layer, segments=16):
    """Create a 3D tube representation using circles and lines as wireframe."""
    
    # Calculate tube direction vector
    direction = end_point - start_point
    length = direction.magnitude
    
    if length == 0:
        return
    
    # Normalize direction
    direction = direction.normalize()
    
    # Create circles at both ends
    # Start circle
    msp.add_circle(center=start_point, radius=radius, 
                   dxfattribs={'layer': layer})
    
    # End circle
    msp.add_circle(center=end_point, radius=radius,
                   dxfattribs={'layer': layer})
    
    # Create lines connecting the circles (representing the tube surface)
    for i in range(0, segments, 2):  # Reduce number of lines for cleaner view
        angle = 2 * math.pi * i / segments
        
        # Calculate points on the circles
        if abs(direction.z) < 0.99:  # Not vertical
            # Create perpendicular vectors
            perp1 = Vec3(-direction.y, direction.x, 0).normalize()
        else:  # Vertical tube
            perp1 = Vec3(1, 0, 0)
        
        perp2 = direction.cross(perp1).normalize()
        
        # Points on start circle
        start_circle_point = start_point + radius * (
            math.cos(angle) * perp1 + math.sin(angle) * perp2)
        
        # Points on end circle
        end_circle_point = end_point + radius * (
            math.cos(angle) * perp1 + math.sin(angle) * perp2)
        
        # Create line connecting the points
        msp.add_line(start_circle_point, end_circle_point,
                     dxfattribs={'layer': layer})

def add_centerlines(msp, left_center, right_center, vertical_height, 
                   bottom_height, top_height):
    """Add centerlines for fabrication reference."""
    
    # Vertical centerlines
    msp.add_line(left_center, left_center + Vec3(0, 0, vertical_height),
                 dxfattribs={'layer': 'CENTERLINES'})
    
    msp.add_line(right_center, right_center + Vec3(0, 0, vertical_height),
                 dxfattribs={'layer': 'CENTERLINES'})
    
    # Horizontal centerlines
    msp.add_line(Vec3(0, 0, bottom_height), Vec3(24, 0, bottom_height),
                 dxfattribs={'layer': 'CENTERLINES'})
    
    msp.add_line(Vec3(0, 0, top_height), Vec3(24, 0, top_height),
                 dxfattribs={'layer': 'CENTERLINES'})

def add_dimensions(msp, vertical_height, horizontal_length, bottom_height, brace_length):
    """Add dimension annotations."""
    
    # Vertical dimension
    msp.add_linear_dim(
        base=Vec3(-3, 0, 0),
        p1=Vec3(-2, 0, 0),
        p2=Vec3(-2, 0, vertical_height),
        text=f'{vertical_height}"',
        dxfattribs={'layer': 'DIMENSIONS'}
    )
    
    # Horizontal dimension
    msp.add_linear_dim(
        base=Vec3(0, -3, 0),
        p1=Vec3(0, -2, 0),
        p2=Vec3(horizontal_length, -2, 0),
        text=f'{horizontal_length}"',
        dxfattribs={'layer': 'DIMENSIONS'}
    )
    
    # Bottom horizontal height dimension
    msp.add_linear_dim(
        base=Vec3(26, 0, 0),
        p1=Vec3(25, 0, 0),
        p2=Vec3(25, 0, bottom_height),
        text=f'{bottom_height}"',
        dxfattribs={'layer': 'DIMENSIONS'}
    )
    
    # Add brace length annotation as text
    msp.add_text(
        f'Brace Length: {brace_length}"',
        height=1.0,
        dxfattribs={'layer': 'DIMENSIONS'}
    ).set_placement(Vec3(5, -20, 0))

def add_annotations(msp):
    """Add text annotations with specifications."""
    
    # Title
    msp.add_text(
        "STAINLESS STEEL METAL FRAME WITH CORNER REINFORCEMENT BRACES",
        height=2.0,
        dxfattribs={'layer': 'DIMENSIONS'}
    ).set_placement(Vec3(5, -8, 0))
    
    # Specifications
    specs = [
        "SPECIFICATIONS:",
        "- Material: Stainless Steel",
        "- Tube OD: 2.000\"",
        "- Vertical Height: 48.000\"",
        "- Horizontal Length: 24.000\"",
        "- Bottom Rail Height: 12.000\"",
        "- Corner Braces: 12.000\" at 45° (4 total)",
        "- Diagonal braces at all four corners",
        "- All dimensions in inches",
        "- Welded construction"
    ]
    
    for i, spec in enumerate(specs):
        msp.add_text(
            spec,
            height=1.0,
            dxfattribs={'layer': 'DIMENSIONS'}
        ).set_placement(Vec3(5, -12 - i * 1.5, 0))

def main():
    """Main function to generate the DXF file."""
    print("Generating 3D DXF file for stainless steel metal frame...")
    
    # Create the DXF document
    doc = create_metal_frame_dxf()
    
    # Save the file
    filename = "stainless_steel_frame_3d.dxf"
    doc.saveas(filename)
    
    print(f"✓ DXF file saved as: {filename}")
    print("\nFrame Specifications:")
    print("- Two 48\" vertical tubes (2\" OD)")
    print("- Two 24\" horizontal tubes (2\" OD)")
    print("- Top horizontal at 48\" height")
    print("- Bottom horizontal at 12\" height")
    print("- Material: Stainless Steel")
    print("\nThe DXF file is ready for CAD software and fabrication!")

if __name__ == "__main__":
    main() 