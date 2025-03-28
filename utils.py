import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import plotly.graph_objects as go

def format_math_latex(expr):
    """
    Format a sympy expression as a LaTeX string that can be displayed in Streamlit.
    
    Args:
        expr (sympy.Expr): Sympy expression to format
        
    Returns:
        str: LaTeX formatted string
    """
    return f"${sp.latex(expr)}$"

def create_custom_colormap(name, colors):
    """
    Create a custom colormap for visualizations.
    
    Args:
        name (str): Name for the colormap
        colors (list): List of colors
        
    Returns:
        matplotlib.colors.LinearSegmentedColormap: Custom colormap
    """
    return LinearSegmentedColormap.from_list(name, colors)

def compute_multinomial_coefficient(n, k_list):
    """
    Compute the multinomial coefficient n! / (k_1! * k_2! * ... * k_m!)
    
    Args:
        n (int): Total sum of k values
        k_list (list): List of k values
        
    Returns:
        int: Multinomial coefficient
    """
    if sum(k_list) != n:
        raise ValueError("Sum of k values must equal n")
    
    # Calculate n!
    import math
    numerator = math.factorial(n)
    
    # Calculate product of k_i!
    denominator = 1
    for k in k_list:
        if k > 0:  # Avoid computing 0!
            denominator *= math.factorial(k)
    
    return numerator // denominator

def convert_to_homogeneous_coordinates(points):
    """
    Convert 3D points to homogeneous coordinates for projective transformations.
    
    Args:
        points (list): List of 3D points [x, y, z]
        
    Returns:
        list: Points in homogeneous coordinates [x, y, z, 1]
    """
    return [[x, y, z, 1] for x, y, z in points]

def apply_projective_transformation(points, transformation_matrix):
    """
    Apply a projective transformation to a list of points in homogeneous coordinates.
    
    Args:
        points (list): List of points in homogeneous coordinates
        transformation_matrix (numpy.ndarray): 4x4 transformation matrix
        
    Returns:
        list: Transformed points in Cartesian coordinates
    """
    result = []
    for point in points:
        # Convert to numpy array for matrix multiplication
        p = np.array(point)
        
        # Apply transformation
        transformed = transformation_matrix.dot(p)
        
        # Convert back from homogeneous coordinates to Cartesian
        w = transformed[3]
        if abs(w) > 1e-10:  # Avoid division by zero or very small numbers
            result.append([transformed[0]/w, transformed[1]/w, transformed[2]/w])
        else:
            # Point at infinity, handle appropriately (may skip or use a very large value)
            result.append([float('inf'), float('inf'), float('inf')])
    
    return result

def create_rotation_matrix(angle, axis='z'):
    """
    Create a 3D rotation matrix around the specified axis.
    
    Args:
        angle (float): Rotation angle in radians
        axis (str): Axis of rotation ('x', 'y', or 'z')
        
    Returns:
        numpy.ndarray: 4x4 rotation matrix in homogeneous coordinates
    """
    c = np.cos(angle)
    s = np.sin(angle)
    
    if axis == 'x':
        rotation = np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])
    elif axis == 'y':
        rotation = np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])
    else:  # axis == 'z'
        rotation = np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
    
    return rotation
