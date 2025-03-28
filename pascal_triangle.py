import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy.special import comb
import matplotlib.cm as cm
import math

def generate_pascal_triangle(rows):
    """
    Generate Pascal's triangle with the specified number of rows
    
    Args:
        rows (int): Number of rows to generate
        
    Returns:
        list: A list of lists representing Pascal's triangle
    """
    triangle = []
    for n in range(rows):
        row = []
        for k in range(n + 1):
            row.append(int(comb(n, k)))
        triangle.append(row)
    return triangle

def visualize_pascal_2d(triangle):
    """
    Create a 2D visualization of Pascal's triangle
    
    Args:
        triangle (list): Pascal's triangle as a list of lists
        
    Returns:
        matplotlib.figure.Figure: Matplotlib figure object
    """
    rows = len(triangle)
    
    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calculate the maximum value for color normalization
    max_val = max(max(row) for row in triangle)
    
    # Draw the triangle
    for n, row in enumerate(triangle):
        for k, val in enumerate(row):
            # Calculate position - center the triangle
            x = k - n/2
            y = -n  # Negative to have the triangle point downward
            
            # Normalize value for color
            # Use log scale for better visualization since values grow exponentially
            normalized_val = np.log1p(val) / np.log1p(max_val)
            color = cm.viridis(normalized_val)
            
            # Draw the circle with the value
            circle = plt.Circle((x, y), 0.4, color=color, alpha=0.8)
            ax.add_patch(circle)
            
            # Add text (value) to the circle
            if rows <= 15:  # Only show numbers for smaller triangles
                ax.text(x, y, str(val), ha='center', va='center', fontsize=8,
                        color='white' if normalized_val > 0.5 else 'black')
    
    # Set limits to make sure the entire triangle is visible
    ax.set_xlim(-rows/2 - 1, rows/2 + 1)
    ax.set_ylim(-rows - 1, 1)
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add a title
    ax.set_title(f"Pascal's Triangle ({rows} rows)")
    
    # Add a colorbar
    sm = plt.cm.ScalarMappable(cmap=cm.viridis, norm=plt.Normalize(0, max_val))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Value (linear scale)')
    
    plt.tight_layout()
    return fig

def create_pascal_3d(rows, dimension=3):
    """
    Generate 3D coordinates for Pascal's triangle extended to higher dimensions
    
    Args:
        rows (int): Number of rows
        dimension (int): Target dimension for the extension
        
    Returns:
        list: List of 3D coordinates with associated values
    """
    points = []
    
    if dimension == 2:
        # Standard Pascal's triangle in 3D space
        for n in range(rows):
            for k in range(n + 1):
                value = int(comb(n, k))
                x = k - n/2
                y = 0
                z = -n
                points.append((x, y, z, value))
    
    elif dimension == 3:
        # Pascal's tetrahedron
        for n in range(rows):
            for i in range(n + 1):
                for j in range(n - i + 1):
                    k = n - i - j
                    value = int(math.factorial(n) / (math.factorial(i) * math.factorial(j) * math.factorial(k)))
                    # Convert to Cartesian coordinates
                    x = i - n/3
                    y = j - n/3
                    z = -n + k/3
                    points.append((x, y, z, value))
    
    elif dimension >= 4:
        # Higher dimensional representations projected to 3D
        # We use a spherical projection for dimensions > 3
        theta_step = 2 * np.pi / rows
        phi_step = np.pi / rows
        
        for n in range(rows):
            row_points = min(n + 1, 50)  # Limit points for very large rows
            for point_idx in range(row_points):
                # Create a spherical distribution of points
                theta = point_idx * theta_step
                phi = n * phi_step
                
                # Convert to Cartesian coordinates using hyper-spherical projection
                x = (rows - n) * np.sin(phi) * np.cos(theta)
                y = (rows - n) * np.sin(phi) * np.sin(theta)
                z = (rows - n) * np.cos(phi)
                
                # Calculate multinomial coefficient for this position
                # For higher dimensions, we approximate using a representative value
                value = int(comb(n, min(point_idx, n)))
                
                points.append((x, y, z, value))
    
    # Convert to desired format
    result = []
    for x, y, z, value in points:
        # Scale value logarithmically to handle large numbers
        log_value = np.log1p(value)
        result.append((x, y, z, log_value, value))
    
    return result

def visualize_pascal_3d(pascal_3d, dimension=3, rotation_speed=0.5, as_figure=False):
    """
    Create a 3D visualization of Pascal's triangle extension
    
    Args:
        pascal_3d (list): 3D Pascal data
        dimension (int): The dimension being visualized
        rotation_speed (float): Speed of rotation animation
        as_figure (bool): If True, return the figure without showing
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure object
    """
    # Extract coordinates and values
    x = [point[0] for point in pascal_3d]
    y = [point[1] for point in pascal_3d]
    z = [point[2] for point in pascal_3d]
    log_values = [point[3] for point in pascal_3d]
    
    # Normalize log values for marker size
    max_log_value = max(log_values)
    normalized_sizes = [max(3, (val / max_log_value) * 15) for val in log_values]
    
    # Create a colorscale based on log values
    fig = go.Figure(data=[
        go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=dict(
                size=normalized_sizes,
                color=log_values,
                colorscale='Viridis',
                opacity=0.8,
                colorbar=dict(
                    title="Log(Value)"
                )
            ),
            hovertemplate='Value: %{text}<br>x: %{x:.2f}<br>y: %{y:.2f}<br>z: %{z:.2f}',
            text=[f"{int(pascal_3d[i][4])}" for i in range(len(pascal_3d))],
        )
    ])
    
    # Set figure title and labels
    fig.update_layout(
        title=f"{dimension}D Pascal's Triangle Projection",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'
        ),
        height=700
    )
    
    # Add animation if specified
    if rotation_speed > 0:
        # Create frames for rotation
        frames = []
        for angle in np.linspace(0, 2*np.pi, 100):
            frame = go.Frame(
                data=[
                    go.Scatter3d(
                        x=x,
                        y=y,
                        z=z,
                        mode='markers',
                        marker=dict(
                            size=normalized_sizes,
                            color=log_values,
                            colorscale='Viridis',
                            opacity=0.8
                        ),
                        hovertemplate='Value: %{text}<br>x: %{x:.2f}<br>y: %{y:.2f}<br>z: %{z:.2f}',
                        text=[f"{int(pascal_3d[i][4])}" for i in range(len(pascal_3d))],
                    )
                ],
                layout=go.Layout(
                    scene_camera=dict(
                        eye=dict(
                            x=1.25 * np.cos(angle),
                            y=1.25 * np.sin(angle),
                            z=0.5
                        )
                    )
                )
            )
            frames.append(frame)
        
        fig.frames = frames
        
        # Add animation controls
        fig.update_layout(
            updatemenus=[{
                'type': 'buttons',
                'showactive': False,
                'buttons': [{
                    'label': 'Play',
                    'method': 'animate',
                    'args': [None, {
                        'frame': {'duration': 50 / rotation_speed, 'redraw': True},
                        'fromcurrent': True,
                        'transition': {'duration': 0}
                    }]
                }, {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {
                        'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }]
                }],
                'x': 0.1,
                'y': 0,
                'xanchor': 'right',
                'yanchor': 'bottom'
            }]
        )
    
    if as_figure:
        return fig
    else:
        return fig
