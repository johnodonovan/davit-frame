#!/usr/bin/env python3
"""
DXF Frame Visualizer
Creates a 3D visualization of the stainless steel metal frame and saves it as PNG
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import ezdxf
from ezdxf.math import Vec3
import math

def create_frame_visualization():
    """Create a 3D visualization of the metal frame."""
    
    # Frame specifications (matching the DXF file)
    VERTICAL_HEIGHT = 48.0
    HORIZONTAL_LENGTH = 24.0
    TUBE_DIAMETER = 2.0
    TUBE_RADIUS = TUBE_DIAMETER / 2.0
    BOTTOM_HORIZONTAL_HEIGHT = 12.0
    TOP_HORIZONTAL_HEIGHT = VERTICAL_HEIGHT
    VERTICAL_SPACING = HORIZONTAL_LENGTH
    BRACE_LENGTH = 12.0
    
    # Create figure and 3D axis
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Define tube positions
    left_vertical_center = np.array([0, 0, 0])
    right_vertical_center = np.array([VERTICAL_SPACING, 0, 0])
    
    # Vertical tubes
    left_vertical_end = left_vertical_center + np.array([0, 0, VERTICAL_HEIGHT])
    right_vertical_end = right_vertical_center + np.array([0, 0, VERTICAL_HEIGHT])
    
    # Horizontal tubes
    bottom_horizontal_start = np.array([0, 0, BOTTOM_HORIZONTAL_HEIGHT])
    bottom_horizontal_end = np.array([VERTICAL_SPACING, 0, BOTTOM_HORIZONTAL_HEIGHT])
    top_horizontal_start = np.array([0, 0, TOP_HORIZONTAL_HEIGHT])
    top_horizontal_end = np.array([VERTICAL_SPACING, 0, TOP_HORIZONTAL_HEIGHT])
    
    # Calculate corner brace positions
    brace_offset = BRACE_LENGTH / math.sqrt(2)
    
    # TOP CORNER BRACES
    # Left top corner brace - from vertical tube to horizontal tube
    left_top_brace_start = np.array([0, 0, TOP_HORIZONTAL_HEIGHT - brace_offset])
    left_top_brace_end = np.array([brace_offset, 0, TOP_HORIZONTAL_HEIGHT])
    
    # Right top corner brace - from vertical tube to horizontal tube
    right_top_brace_start = np.array([VERTICAL_SPACING, 0, TOP_HORIZONTAL_HEIGHT - brace_offset])
    right_top_brace_end = np.array([VERTICAL_SPACING - brace_offset, 0, TOP_HORIZONTAL_HEIGHT])
    
    # BOTTOM CORNER BRACES
    # Left bottom corner brace - from vertical tube to horizontal tube (above the horizontal bar)
    left_bottom_brace_start = np.array([0, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset])
    left_bottom_brace_end = np.array([brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT])
    
    # Right bottom corner brace - from vertical tube to horizontal tube (above the horizontal bar)
    right_bottom_brace_start = np.array([VERTICAL_SPACING, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset])
    right_bottom_brace_end = np.array([VERTICAL_SPACING - brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT])
    
    # Draw tubes as cylinders
    # Left vertical tube
    draw_cylinder(ax, left_vertical_center, left_vertical_end, TUBE_RADIUS, 'red', 'Vertical Tubes')
    
    # Right vertical tube
    draw_cylinder(ax, right_vertical_center, right_vertical_end, TUBE_RADIUS, 'red', '')
    
    # Bottom horizontal tube
    draw_cylinder(ax, bottom_horizontal_start, bottom_horizontal_end, TUBE_RADIUS, 'gold', 'Horizontal Tubes')
    
    # Top horizontal tube
    draw_cylinder(ax, top_horizontal_start, top_horizontal_end, TUBE_RADIUS, 'gold', '')
    
    # Corner braces - all four diagonal braces for corner reinforcement
    draw_cylinder(ax, left_top_brace_start, left_top_brace_end, TUBE_RADIUS, 'green', 'Corner Braces')
    draw_cylinder(ax, right_top_brace_start, right_top_brace_end, TUBE_RADIUS, 'green', '')
    draw_cylinder(ax, left_bottom_brace_start, left_bottom_brace_end, TUBE_RADIUS, 'green', '')
    draw_cylinder(ax, right_bottom_brace_start, right_bottom_brace_end, TUBE_RADIUS, 'green', '')
    
    # Add centerlines
    draw_centerlines(ax, left_vertical_center, right_vertical_center, 
                    VERTICAL_HEIGHT, BOTTOM_HORIZONTAL_HEIGHT, TOP_HORIZONTAL_HEIGHT)
    
    # Add dimensions and annotations
    add_dimension_annotations(ax, VERTICAL_HEIGHT, HORIZONTAL_LENGTH, BOTTOM_HORIZONTAL_HEIGHT, BRACE_LENGTH)
    
    # Set axis properties
    ax.set_xlabel('Length (inches)', fontsize=12)
    ax.set_ylabel('Width (inches)', fontsize=12)
    ax.set_zlabel('Height (inches)', fontsize=12)
    
    # Set equal aspect ratio
    max_range = max(VERTICAL_HEIGHT, HORIZONTAL_LENGTH) / 2.0
    mid_x = HORIZONTAL_LENGTH / 2.0
    mid_y = 0
    mid_z = VERTICAL_HEIGHT / 2.0
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(0, VERTICAL_HEIGHT + 5)
    
    # Set title and add specifications
    ax.set_title('Stainless Steel Metal Frame with Corner Reinforcement Braces\n48" x 24" x 2" OD Tubes + 12" Corner Diagonals (4 total)', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98))
    
    # Set viewing angle for best perspective
    ax.view_init(elev=20, azim=45)
    
    # Add grid
    ax.grid(True, alpha=0.3)
    
    return fig, ax

def draw_cylinder(ax, start_point, end_point, radius, color, label, segments=16):
    """Draw a 3D cylinder between two points."""
    
    # Calculate direction vector
    direction = end_point - start_point
    length = np.linalg.norm(direction)
    
    if length == 0:
        return
    
    direction = direction / length
    
    # Create perpendicular vectors
    if abs(direction[2]) < 0.99:
        perp1 = np.array([-direction[1], direction[0], 0])
        perp1 = perp1 / np.linalg.norm(perp1)
    else:
        perp1 = np.array([1, 0, 0])
    
    perp2 = np.cross(direction, perp1)
    perp2 = perp2 / np.linalg.norm(perp2)
    
    # Generate cylinder surface
    theta = np.linspace(0, 2*np.pi, segments)
    z_line = np.linspace(0, 1, 2)
    
    # Create meshgrid for cylinder surface
    theta_mesh, z_mesh = np.meshgrid(theta, z_line)
    
    # Calculate cylinder surface points
    x_cyl = np.zeros_like(theta_mesh)
    y_cyl = np.zeros_like(theta_mesh)
    z_cyl = np.zeros_like(theta_mesh)
    
    for i in range(len(z_line)):
        for j in range(len(theta)):
            # Point on circle
            circle_point = radius * (np.cos(theta[j]) * perp1 + np.sin(theta[j]) * perp2)
            # Position along tube
            tube_point = start_point + z_line[i] * direction * length + circle_point
            
            x_cyl[i, j] = tube_point[0]
            y_cyl[i, j] = tube_point[1]
            z_cyl[i, j] = tube_point[2]
    
    # Plot cylinder surface
    ax.plot_surface(x_cyl, y_cyl, z_cyl, color=color, alpha=0.8, label=label)
    
    # Draw end caps
    theta_cap = np.linspace(0, 2*np.pi, segments)
    
    # Start cap
    x_start = start_point[0] + radius * np.cos(theta_cap) * perp1[0] + radius * np.sin(theta_cap) * perp2[0]
    y_start = start_point[1] + radius * np.cos(theta_cap) * perp1[1] + radius * np.sin(theta_cap) * perp2[1]
    z_start = start_point[2] + radius * np.cos(theta_cap) * perp1[2] + radius * np.sin(theta_cap) * perp2[2]
    
    # End cap
    x_end = end_point[0] + radius * np.cos(theta_cap) * perp1[0] + radius * np.sin(theta_cap) * perp2[0]
    y_end = end_point[1] + radius * np.cos(theta_cap) * perp1[1] + radius * np.sin(theta_cap) * perp2[1]
    z_end = end_point[2] + radius * np.cos(theta_cap) * perp1[2] + radius * np.sin(theta_cap) * perp2[2]
    
    # Fill end caps
    ax.plot(x_start, y_start, z_start, color=color, linewidth=2)
    ax.plot(x_end, y_end, z_end, color=color, linewidth=2)

def draw_centerlines(ax, left_center, right_center, vertical_height, bottom_height, top_height):
    """Draw centerlines for fabrication reference."""
    
    # Vertical centerlines
    ax.plot([left_center[0], left_center[0]], 
            [left_center[1], left_center[1]], 
            [left_center[2], vertical_height], 
            'k--', alpha=0.5, linewidth=1, label='Centerlines')
    
    ax.plot([right_center[0], right_center[0]], 
            [right_center[1], right_center[1]], 
            [right_center[2], vertical_height], 
            'k--', alpha=0.5, linewidth=1)
    
    # Horizontal centerlines
    ax.plot([0, 24], [0, 0], [bottom_height, bottom_height], 
            'k--', alpha=0.5, linewidth=1)
    
    ax.plot([0, 24], [0, 0], [top_height, top_height], 
            'k--', alpha=0.5, linewidth=1)

def add_dimension_annotations(ax, vertical_height, horizontal_length, bottom_height, brace_length):
    """Add dimension annotations to the plot."""
    
    # Vertical dimension
    ax.text(-3, 0, vertical_height/2, f'{vertical_height}"', 
            fontsize=10, ha='center', va='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Horizontal dimension
    ax.text(horizontal_length/2, -3, 0, f'{horizontal_length}"', 
            fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Bottom rail height
    ax.text(26, 0, bottom_height/2, f'{bottom_height}"', 
            fontsize=10, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Add specifications text
    specs_text = f"""SPECIFICATIONS:
• Material: Stainless Steel
• Tube OD: 2.000"
• Vertical Height: 48.000"
• Horizontal Length: 24.000"
• Bottom Rail Height: 12.000"
• Corner Braces: {brace_length}" at 45° (4 total)
• Diagonal braces at all four corners
• Welded Construction"""
    
    ax.text2D(0.02, 0.02, specs_text, transform=ax.transAxes, 
              fontsize=9, verticalalignment='bottom',
              bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))

def save_visualization():
    """Create and save the frame visualization."""
    
    print("Creating 3D visualization of the metal frame...")
    
    # Create the visualization
    fig, ax = create_frame_visualization()
    
    # Save as PNG with high resolution
    filename = "stainless_steel_frame_visualization.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"✓ Visualization saved as: {filename}")
    
    # Also save a version with transparent background
    filename_transparent = "stainless_steel_frame_visualization_transparent.png"
    plt.savefig(filename_transparent, dpi=300, bbox_inches='tight', 
                facecolor='none', edgecolor='none', transparent=True)
    
    print(f"✓ Transparent version saved as: {filename_transparent}")
    
    # Show the plot
    plt.show()
    
    return filename

def main():
    """Main function to create the visualization."""
    try:
        filename = save_visualization()
        print(f"\n🎉 Frame visualization complete!")
        print(f"📁 Files created:")
        print(f"   • {filename}")
        print(f"   • stainless_steel_frame_visualization_transparent.png")
        print(f"\nThe visualization shows your 48\" x 24\" stainless steel frame")
        print(f"with 2\" OD tubes in full 3D detail!")
        
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 