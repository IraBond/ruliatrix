import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.cm as cm

def generate_binomial_expansion(x, y, n):
    """
    Generate the binomial expansion for (x + y)^n.
    
    Args:
        x (sympy.Symbol): Variable x
        y (sympy.Symbol): Variable y
        n (int): Power for the expansion
        
    Returns:
        sympy.Expr: The expanded expression
    """
    expansion = sp.expand((x + y)**n)
    return expansion

def create_binomial_visualization(n):
    """
    Create a visualization of the binomial coefficients.
    
    Args:
        n (int): Power for the binomial expansion
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    # Calculate binomial coefficients
    coeffs = [int(sp.binomial(n, k)) for k in range(n+1)]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Calculate positions
    width = 0.8
    x_positions = np.arange(len(coeffs))
    
    # Find max coefficient for normalization
    max_coeff = max(coeffs)
    
    # Draw rectangles for each coefficient
    for i, coeff in enumerate(coeffs):
        # Normalize height
        height = coeff / max_coeff * 0.8
        
        # Normalize color based on coefficient
        normalized_val = coeff / max_coeff
        color = cm.viridis(normalized_val)
        
        # Draw rectangle
        rect = Rectangle((i - width/2, 0), width, height, 
                         color=color, alpha=0.8)
        ax.add_patch(rect)
        
        # Add coefficient as text
        ax.text(i, height + 0.05, str(coeff), 
                ha='center', va='bottom', fontsize=10)
        
        # Add term
        if n <= 10:  # Only show terms for smaller n values
            term = f"x^{n-i}y^{i}" if i > 0 and i < n else "x^{n}".format(n=n) if i == 0 else "y^{n}".format(n=n)
            ax.text(i, -0.1, term, ha='center', va='top', fontsize=8)
    
    # Set limits
    ax.set_xlim(-0.5, len(coeffs) - 0.5)
    ax.set_ylim(-0.2, 1.1)
    
    # Set labels and title
    ax.set_title(f"Binomial Coefficients for (x + y)^{n}")
    ax.set_xlabel("k")
    ax.set_ylabel("Normalized Coefficient Value")
    
    # Set x-ticks
    ax.set_xticks(x_positions)
    ax.set_xticklabels([f"{k}" for k in range(n+1)])
    
    # Add equation at the top
    equation = r"$(x + y)^{" + str(n) + r"} = \sum_{k=0}^{" + str(n) + r"} \binom{" + str(n) + r"}{k} x^{" + str(n) + r"-k} y^k$"
    ax.text(len(coeffs)/2, 1.05, equation, ha='center', va='bottom', fontsize=12)
    
    plt.tight_layout()
    return fig

def relate_pascal_to_binomial(pascal_triangle, n):
    """
    Create a visualization showing the relationship between Pascal's triangle
    and binomial expansion for a specific n.
    
    Args:
        pascal_triangle (list): Pascal's triangle as a list of lists
        n (int): The row of Pascal's triangle to highlight
        
    Returns:
        matplotlib.figure.Figure: The generated figure
    """
    if n >= len(pascal_triangle):
        n = len(pascal_triangle) - 1
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw the triangle
    rows = len(pascal_triangle)
    max_val = max(max(row) for row in pascal_triangle)
    
    for i, row in enumerate(pascal_triangle):
        for j, val in enumerate(row):
            # Calculate position - center the triangle
            x = j - i/2
            y = -i  # Negative to have the triangle point downward
            
            # Normalize value for color
            normalized_val = np.log1p(val) / np.log1p(max_val)
            
            # Determine if this cell is in the highlighted row
            is_highlighted = (i == n)
            
            # Set color based on whether it's highlighted
            if is_highlighted:
                color = 'red'
                alpha = 0.9
                edge_color = 'black'
                linewidth = 2
            else:
                color = cm.viridis(normalized_val)
                alpha = 0.7
                edge_color = None
                linewidth = 0
            
            # Draw the circle with the value
            circle = plt.Circle(
                (x, y), 0.4, 
                color=color, 
                alpha=alpha,
                edgecolor=edge_color,
                linewidth=linewidth
            )
            ax.add_patch(circle)
            
            # Add text (value) to the circle
            ax.text(x, y, str(val), ha='center', va='center', fontsize=8,
                    color='white' if normalized_val > 0.5 and not is_highlighted else 'black')
    
    # Set limits to make sure the entire triangle is visible
    ax.set_xlim(-rows/2 - 1, rows/2 + 1)
    ax.set_ylim(-rows - 1, 1)
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Draw the binomial expansion equation
    coeffs = pascal_triangle[n]
    equation = f"$(x + y)^{{{n}}} = "
    
    for k, coeff in enumerate(coeffs):
        term = f"{coeff}" if coeff > 1 else ""
        
        if k > 0:
            equation += " + "
        
        if n - k > 0:
            x_term = f"x^{{{n-k}}}" if n-k > 1 else "x"
        else:
            x_term = ""
            
        if k > 0:
            y_term = f"y^{{{k}}}" if k > 1 else "y"
        else:
            y_term = ""
            
        equation += f"{term}{x_term}{y_term}"
    
    equation += "$"
    
    # Add title and equation
    ax.set_title(f"Row {n} of Pascal's Triangle and its Binomial Expansion")
    ax.text(0, -n-1, equation, ha='center', va='center', fontsize=12)
    
    plt.tight_layout()
    return fig
