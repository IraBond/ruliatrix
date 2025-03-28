import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.special import comb
import random

def generate_fractal_recursion(max_rows, dimension, depth, fractal_type="Pascal-based"):
    """
    Generate fractal recursion data based on Pascal's triangle and Galois symmetries.
    
    Args:
        max_rows (int): Number of rows in the base Pascal triangle
        dimension (int): Target dimension for visualization
        depth (int): Recursion depth for the fractal
        fractal_type (str): Type of fractal to generate
        
    Returns:
        list: 3D coordinates representing the fractal pattern
    """
    # Base set of points from Pascal's triangle
    points = []
    
    # Generate the base Pascal structure
    if dimension == 2:
        # Standard Pascal's triangle
        for n in range(max_rows):
            for k in range(n + 1):
                val = int(comb(n, k))
                x = k - n/2
                y = 0
                z = -n
                points.append((x, y, z, val))
    else:
        # Higher dimensional Pascal structure
        for n in range(max_rows):
            for k in range(min(n+1, 50)):  # Limit number of points for large n
                val = int(comb(n, k))
                x = k - n/2
                y = n/4 - abs(k - n/2)/2  # Add some 3D structure
                z = -n
                points.append((x, y, z, val))
    
    # Apply fractal recursion based on the selected type
    all_points = []
    all_points.extend(points)
    
    if fractal_type == "Pascal-based":
        # Fractal based on Pascal's recurrence relation
        for d in range(1, depth + 1):
            scale = 0.5 ** d
            new_points = []
            
            for i, (x, y, z, val) in enumerate(points):
                # Create smaller copies of the structure at each point
                for j, (x2, y2, z2, val2) in enumerate(points):
                    if i % 3 == 0:  # To avoid too many points
                        new_x = x + x2 * scale
                        new_y = y + y2 * scale
                        new_z = z + z2 * scale
                        new_val = (val * val2) % 1000  # Modulo to avoid huge values
                        new_points.append((new_x, new_y, new_z, new_val))
            
            all_points.extend(new_points)
            # For the next iteration, use a subset of the newly created points
            points = random.sample(new_points, min(len(new_points), 50))
    
    elif fractal_type == "Galois-transformed":
        # Fractal based on Galois group transformations
        for d in range(1, depth + 1):
            scale = 0.5 ** d
            new_points = []
            
            # Define some transformation matrices inspired by G(2) group
            transforms = [
                # Rotation matrices in different planes
                lambda x, y, z: (x*np.cos(np.pi/6) - y*np.sin(np.pi/6), 
                                x*np.sin(np.pi/6) + y*np.cos(np.pi/6), z),
                lambda x, y, z: (x, y*np.cos(np.pi/4) - z*np.sin(np.pi/4),
                                y*np.sin(np.pi/4) + z*np.cos(np.pi/4)),
                lambda x, y, z: (x*np.cos(np.pi/3) - z*np.sin(np.pi/3),
                                y, x*np.sin(np.pi/3) + z*np.cos(np.pi/3)),
                # Reflection matrices
                lambda x, y, z: (-x, y, z),
                lambda x, y, z: (x, -y, z),
                lambda x, y, z: (x, y, -z)
            ]
            
            for i, (x, y, z, val) in enumerate(points):
                # Apply each transformation to create new points
                for transform in transforms:
                    new_x, new_y, new_z = transform(x, y, z)
                    new_points.append((
                        x + new_x * scale, 
                        y + new_y * scale, 
                        z + new_z * scale, 
                        val
                    ))
            
            all_points.extend(new_points)
            # For the next iteration, use a subset of the newly created points
            points = random.sample(new_points, min(len(new_points), 50))
    
    elif fractal_type == "Combined":
        # Combine both approaches
        # Iterate through recursion depth
        for d in range(1, depth + 1):
            scale = 0.5 ** d
            new_points = []
            
            # Define transformations
            transforms = [
                lambda x, y, z: (x*np.cos(np.pi/6) - y*np.sin(np.pi/6), 
                                x*np.sin(np.pi/6) + y*np.cos(np.pi/6), z),
                lambda x, y, z: (x, y*np.cos(np.pi/4) - z*np.sin(np.pi/4),
                                y*np.sin(np.pi/4) + z*np.cos(np.pi/4))
            ]
            
            # Apply transformations
            for i, (x, y, z, val) in enumerate(points):
                if i % (4-d) == 0:  # Selective application based on depth
                    # Apply Pascal-like recursive construction
                    for j, (x2, y2, z2, val2) in enumerate(points[:10]):  # Use just a few points
                        new_x = x + x2 * scale
                        new_y = y + y2 * scale
                        new_z = z + z2 * scale
                        new_points.append((new_x, new_y, new_z, val))
                    
                    # Apply Galois transformations
                    for transform in transforms:
                        new_x, new_y, new_z = transform(x, y, z)
                        new_points.append((
                            x + new_x * scale * 0.5, 
                            y + new_y * scale * 0.5, 
                            z + new_z * scale * 0.5, 
                            val
                        ))
            
            all_points.extend(new_points)
            # For the next iteration, use a subset of the newly created points
            points = random.sample(new_points, min(len(new_points), 30))
    
    # Format the output to include a logarithmic version of values for better visualization
    result = []
    for x, y, z, val in all_points:
        log_val = np.log1p(val) if val > 0 else 0
        result.append((x, y, z, log_val, val))
    
    return result

def visualize_fractal_recursion(fractal_data, fractal_type, zoom=1.0, as_figure=False):
    """
    Create a visualization of the fractal recursion.
    
    Args:
        fractal_data (list): List of 3D coordinates with values
        fractal_type (str): Type of fractal
        zoom (float): Zoom level for visualization
        as_figure (bool): If True, return the figure without showing
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure with visualization
    """
    # Extract coordinates and values
    x = [point[0] for point in fractal_data]
    y = [point[1] for point in fractal_data]
    z = [point[2] for point in fractal_data]
    log_vals = [point[3] for point in fractal_data]
    
    # Apply zoom (scale coordinates inversely to zoom level)
    x = [coord / zoom for coord in x]
    y = [coord / zoom for coord in y]
    z = [coord / zoom for coord in z]
    
    # Normalize values for marker size
    max_log_value = max(log_vals) if log_vals else 1
    normalized_sizes = [max(2, min(8, (val / max_log_value) * 10)) for val in log_vals]
    
    # Create the 3D scatter plot
    fig = go.Figure(data=[
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(
                size=normalized_sizes,
                color=log_vals,
                colorscale='Viridis',
                opacity=0.7,
                colorbar=dict(
                    title="Log(Value)"
                )
            ),
            hovertemplate='Value: %{text}<br>x: %{x:.2f}<br>y: %{y:.2f}<br>z: %{z:.2f}',
            text=[f"{int(fractal_data[i][4])}" for i in range(len(fractal_data))],
        )
    ])
    
    # Update layout
    fig.update_layout(
        title=f"{fractal_type} Fractal Recursion (Zoom: {zoom:.1f}x)",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'
        ),
        height=700
    )
    
    # Add a description based on the fractal type
    if fractal_type == "Pascal-based":
        description = """
        This fractal is built by recursively applying Pascal's triangle pattern at different scales.
        Each point spawns smaller versions of the entire structure, creating self-similarity across scales.
        """
    elif fractal_type == "Galois-transformed":
        description = """
        This fractal applies transformations derived from Galois theory, particularly the G(2) group.
        The symmetry operations create rotating and reflecting patterns throughout the structure.
        """
    elif fractal_type == "Combined":
        description = """
        This fractal combines both Pascal's recurrence and Galois transformations.
        The resulting structure shows how these mathematical domains interconnect in higher dimensions.
        """
    
    # Add mathematical description as annotation
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.0, y=-0.1,
        text=description,
        showarrow=False,
        font=dict(size=10),
        align="left"
    )
    
    if as_figure:
        return fig
    else:
        return fig
