#!/usr/bin/env python3
"""
Create a rotating 3D GIF of the stainless steel marine davit support frame
For use in README and documentation
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
from PIL import Image
import io
import os

def create_frame_visualization_for_gif(azim_angle):
    """Create a 3D visualization of the frame at a specific rotation angle."""
    
    # Frame specifications (matching the updated design)
    VERTICAL_HEIGHT = 30.5
    HORIZONTAL_LENGTH = 24.125
    
    # Tube specifications
    MAIN_TUBE_DIAMETER = 1.375
    MAIN_TUBE_RADIUS = MAIN_TUBE_DIAMETER / 2.0
    
    BRACE_TUBE_DIAMETER = 1.125
    BRACE_TUBE_RADIUS = BRACE_TUBE_DIAMETER / 2.0
    
    # Position specifications - UPDATED TO 5"
    BOTTOM_HORIZONTAL_HEIGHT = 5.0
    TOP_HORIZONTAL_HEIGHT = VERTICAL_HEIGHT
    BRACE_LENGTH = 12.0
    
    # Create figure and 3D axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Set the viewing angle
    ax.view_init(elev=20, azim=azim_angle)
    
    # Define tube positions
    left_vertical_center = np.array([0, 0, 0])
    right_vertical_center = np.array([HORIZONTAL_LENGTH, 0, 0])
    
    # Create vertical tubes
    create_tube_3d(ax, left_vertical_center, 
                   left_vertical_center + np.array([0, 0, VERTICAL_HEIGHT]),
                   MAIN_TUBE_RADIUS, 'red', 'Vertical Tubes')
    
    create_tube_3d(ax, right_vertical_center,
                   right_vertical_center + np.array([0, 0, VERTICAL_HEIGHT]),
                   MAIN_TUBE_RADIUS, 'red', '')
    
    # Create horizontal tubes
    # Bottom horizontal
    create_tube_3d(ax, np.array([0, 0, BOTTOM_HORIZONTAL_HEIGHT]),
                   np.array([HORIZONTAL_LENGTH, 0, BOTTOM_HORIZONTAL_HEIGHT]),
                   MAIN_TUBE_RADIUS, 'gold', 'Horizontal Rails')
    
    # Top horizontal
    create_tube_3d(ax, np.array([0, 0, TOP_HORIZONTAL_HEIGHT]),
                   np.array([HORIZONTAL_LENGTH, 0, TOP_HORIZONTAL_HEIGHT]),
                   MAIN_TUBE_RADIUS, 'gold', '')
    
    # Create diagonal braces
    brace_offset = BRACE_LENGTH / math.sqrt(2)
    
    # Top corner braces
    create_tube_3d(ax, np.array([0, 0, TOP_HORIZONTAL_HEIGHT - brace_offset]),
                   np.array([brace_offset, 0, TOP_HORIZONTAL_HEIGHT]),
                   BRACE_TUBE_RADIUS, 'green', 'Diagonal Braces')
    
    create_tube_3d(ax, np.array([HORIZONTAL_LENGTH, 0, TOP_HORIZONTAL_HEIGHT - brace_offset]),
                   np.array([HORIZONTAL_LENGTH - brace_offset, 0, TOP_HORIZONTAL_HEIGHT]),
                   BRACE_TUBE_RADIUS, 'green', '')
    
    # Bottom corner braces
    create_tube_3d(ax, np.array([0, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset]),
                   np.array([brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT]),
                   BRACE_TUBE_RADIUS, 'green', '')
    
    create_tube_3d(ax, np.array([HORIZONTAL_LENGTH, 0, BOTTOM_HORIZONTAL_HEIGHT + brace_offset]),
                   np.array([HORIZONTAL_LENGTH - brace_offset, 0, BOTTOM_HORIZONTAL_HEIGHT]),
                   BRACE_TUBE_RADIUS, 'green', '')
    
    # Add boat cleat on top center
    cleat_center = np.array([HORIZONTAL_LENGTH/2, 0, TOP_HORIZONTAL_HEIGHT + 0.2])
    create_boat_cleat(ax, cleat_center, 'cyan', 'Boat Cleat')
    
    # Add semicircle rings on vertical tubes
    ring_height = 27.5
    create_semicircle_ring(ax, np.array([0, 0, ring_height]), 'purple', 'Semicircle Rings')
    create_semicircle_ring(ax, np.array([HORIZONTAL_LENGTH, 0, ring_height]), 'purple', '')
    
    # Set axis properties
    ax.set_xlabel('Length (inches)')
    ax.set_ylabel('Width (inches)')
    ax.set_zlabel('Height (inches)')
    
    # Set equal aspect ratio and limits
    max_range = max(HORIZONTAL_LENGTH, VERTICAL_HEIGHT) * 0.6
    ax.set_xlim([-5, HORIZONTAL_LENGTH + 5])
    ax.set_ylim([-10, 10])
    ax.set_zlim([0, VERTICAL_HEIGHT + 5])
    
    # Add title
    ax.set_title('316 Stainless Steel Marine Davit Support Frame\n' +
                f'30.5"H × 24.125"W - Bottom Rail at 5" Height',
                fontsize=12, fontweight='bold')
    
    # Add legend
    ax.legend(loc='upper left', bbox_to_anchor=(0, 1))
    
    # Remove background and make it clean
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.grid(True, alpha=0.3)
    
    return fig

def create_tube_3d(ax, start_point, end_point, radius, color, label):
    """Create a 3D tube visualization."""
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
    
    # Create cylinder
    theta = np.linspace(0, 2*np.pi, 16)
    z_line = np.linspace(0, length, 20)
    
    # Create surface
    theta_mesh, z_mesh = np.meshgrid(theta, z_line)
    x_mesh = radius * np.cos(theta_mesh)
    y_mesh = radius * np.sin(theta_mesh)
    
    # Transform to world coordinates
    points = np.zeros((x_mesh.shape[0], x_mesh.shape[1], 3))
    for i in range(x_mesh.shape[0]):
        for j in range(x_mesh.shape[1]):
            local_point = np.array([x_mesh[i,j], y_mesh[i,j], z_mesh[i,j]])
            world_point = start_point + z_mesh[i,j] * direction + local_point[0] * perp1 + local_point[1] * perp2
            points[i,j] = world_point
    
    # Plot surface
    ax.plot_surface(points[:,:,0], points[:,:,1], points[:,:,2], 
                   color=color, alpha=0.8, label=label if label else None)

def create_boat_cleat(ax, center, color, label):
    """Create a simple boat cleat representation."""
    # Simple rectangular representation of the cleat
    cleat_length = 6.0
    cleat_width = 1.5
    cleat_height = 0.3
    
    # Create a simple box
    x = [center[0] - cleat_length/2, center[0] + cleat_length/2]
    y = [center[1] - cleat_width/2, center[1] + cleat_width/2]
    z = [center[2], center[2] + cleat_height]
    
    # Plot as a simple line representation
    ax.plot([x[0], x[1]], [center[1], center[1]], [center[2], center[2]], 
           color=color, linewidth=8, label=label)

def create_semicircle_ring(ax, center, color, label):
    """Create a semicircle ring representation."""
    ring_radius = 1.5
    theta = np.linspace(0, np.pi, 20)  # Semicircle
    
    # Create semicircle in XZ plane (horizontal)
    x = center[0] + ring_radius * np.cos(theta)
    y = np.full_like(theta, center[1])
    z = center[2] + ring_radius * np.sin(theta)
    
    ax.plot(x, y, z, color=color, linewidth=6, label=label if label else None)

def create_rotating_gif():
    """Create a rotating GIF of the 3D frame."""
    
    print("Creating rotating 3D GIF of the stainless steel frame...")
    
    # Create frames for the GIF
    frames = []
    num_frames = 24  # 24 frames = 15 degree increments for full rotation
    
    for i in range(num_frames):
        azim_angle = i * (360 / num_frames)  # Rotate 360 degrees
        print(f"Generating frame {i+1}/{num_frames} (angle: {azim_angle:.1f}°)")
        
        # Create the plot
        fig = create_frame_visualization_for_gif(azim_angle)
        
        # Save to memory buffer with reduced DPI for smaller file size
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=80, bbox_inches='tight',  # Reduced from 100 to 80 DPI
                   facecolor='white', edgecolor='none')
        
        # Convert to PIL Image
        buf.seek(0)
        img = Image.open(buf)
        # Make a copy to avoid issues with buffer closing
        img_copy = img.copy()
        frames.append(img_copy)
        
        # Close the figure and buffer
        plt.close(fig)
        img.close()
        buf.close()
    
    # Save as GIF with optimized settings
    gif_filename = "frame_3d_rotation.gif"
    frames[0].save(
        gif_filename,
        save_all=True,
        append_images=frames[1:],
        duration=200,  # 200ms per frame for smaller file
        loop=0,  # Loop forever
        optimize=True  # Enable optimization for smaller file size
    )
    
    print(f"✓ Rotating GIF saved as: {gif_filename}")
    print(f"✓ GIF contains {num_frames} frames with 360° rotation")
    
    # Check file size
    if os.path.exists(gif_filename):
        file_size = os.path.getsize(gif_filename)
        print(f"✓ File size: {file_size:,} bytes ({file_size/1024/1024:.1f} MB)")
    
    return gif_filename

if __name__ == "__main__":
    create_rotating_gif()
    
    print("\n🎉 Rotating GIF creation complete!")
    print("📁 File created: frame_3d_rotation.gif")
    print("\nThis GIF shows the updated frame design with:")
    print("- Bottom rail at 5\" height (reduced from 6\")")
    print("- All structural components and connections")
    print("- 360° rotation view for complete visualization")
    print("\nReady to add to README.md!") 