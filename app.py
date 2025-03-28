import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sympy as sp
import matplotlib.pyplot as plt

from pascal_triangle import (
    generate_pascal_triangle, 
    create_pascal_3d,
    visualize_pascal_2d,
    visualize_pascal_3d
)
from galois_theory import (
    create_g2_symmetry_graph,
    visualize_g2_symmetry
)
from fractal_recursion import (
    generate_fractal_recursion,
    visualize_fractal_recursion
)
from binomial_expansion import (
    generate_binomial_expansion,
    create_binomial_visualization,
    relate_pascal_to_binomial
)
from utils import format_math_latex

# Page configuration
st.set_page_config(
    page_title="Pascal-Euler-Galois Fractal Visualization",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("Pascal-Euler-Galois Fractal Visualization")
st.markdown("""
This application visualizes the profound relationships between Pascal's triangle, 
binomial expansion, Galois theory (particularly the G(2) group), and fractal recursion 
in higher-dimensional vector spaces.

Explore the mathematical structures and their interconnections through interactive visualizations.
""")

# Main sections in the sidebar
sections = [
    "Introduction",
    "Pascal's Triangle & Binomial Expansion",
    "3D Extension of Pascal's Triangle",
    "Galois Theory & G(2) Group Symmetries",
    "Fractal Recursion in Higher Dimensions",
    "Combined Visualization"
]

selected_section = st.sidebar.radio("Navigation", sections)

# Sidebar controls
st.sidebar.markdown("## Global Parameters")

# Global parameters in the sidebar that affect visualizations
max_rows = st.sidebar.slider("Number of Rows", min_value=5, max_value=30, value=10)
dimension = st.sidebar.slider("Dimension", min_value=2, max_value=5, value=3)
detail_level = st.sidebar.slider("Detail Level", min_value=1, max_value=5, value=3)
fractal_depth = st.sidebar.slider("Fractal Recursion Depth", min_value=1, max_value=4, value=2)

# Introduction
if selected_section == "Introduction":
    st.markdown("""
    ## Mathematical Foundations
    
    This application explores several fundamental mathematical concepts and their deep interconnections:
    
    ### 1. Pascal's Triangle
    A triangular array of binomial coefficients where each number is the sum of the two directly above it.
    
    ### 2. Binomial Expansion
    The coefficients in the expansion of $(x + y)^n$ correspond to rows in Pascal's triangle.
    
    ### 3. Galois Theory
    A branch of abstract algebra dealing with symmetries in mathematical structures, 
    particularly field extensions. The G(2) group represents specific symmetry transformations.
    
    ### 4. Fractal Recursion
    Patterns that repeat at different scales, creating self-similar structures across dimensions.
    
    ## The Pascal-Euler-Galois Fractal Ruliard Algorithm (PEGFRA)
    
    This visualization demonstrates how these concepts combine to form a unified mathematical structure:
    
    1. Starting with Pascal's triangle as a foundation
    2. Extending into 3D space using binomial relationships
    3. Applying Galois theory symmetries, especially the G(2) group
    4. Creating fractal recursion patterns in higher-dimensional vector spaces
    
    Use the navigation panel to explore each concept individually or see their combined visualization.
    """)
    
    # Display the equation for binomial expansion
    st.markdown("### Key Mathematical Relationship")
    st.latex(r"(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^{n-k} y^k")
    
    st.markdown("Where the binomial coefficient $\\binom{n}{k}$ corresponds to the entry in row $n$, position $k$ of Pascal's triangle.")

# Pascal's Triangle & Binomial Expansion
elif selected_section == "Pascal's Triangle & Binomial Expansion":
    st.markdown("## Pascal's Triangle & Binomial Expansion")
    
    st.markdown("""
    Pascal's triangle is an arithmetic triangular array where each number is the sum of the two directly above it.
    The binomial expansion formula $(x + y)^n$ produces coefficients that correspond exactly to the rows of Pascal's triangle.
    """)
    
    # Generate and display Pascal's triangle
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Pascal's Triangle")
        pascal_triangle = generate_pascal_triangle(max_rows)
        fig_pascal = visualize_pascal_2d(pascal_triangle)
        st.pyplot(fig_pascal)
    
    with col2:
        st.markdown("### Binomial Expansion")
        x_symbol = sp.Symbol('x')
        y_symbol = sp.Symbol('y')
        
        n_value = st.slider("Power (n)", min_value=0, max_value=max_rows-1, value=min(5, max_rows-1))
        
        # Generate and display binomial expansion
        expansion = generate_binomial_expansion(x_symbol, y_symbol, n_value)
        st.latex(f"(x + y)^{{{n_value}}} = {sp.latex(expansion)}")
        
        # Visualize binomial coefficients
        fig_binomial = create_binomial_visualization(n_value)
        st.pyplot(fig_binomial)
    
    # Relationship visualization
    st.markdown("### Relationship Between Pascal's Triangle and Binomial Expansion")
    relationship_fig = relate_pascal_to_binomial(pascal_triangle, n_value)
    st.pyplot(relationship_fig)
    
    st.markdown("""
    ### Mathematical Properties
    
    1. Each entry in Pascal's triangle is a binomial coefficient $\\binom{n}{k}$.
    2. The sum of entries in row $n$ is $2^n$.
    3. Each entry is the sum of the two entries above it: $\\binom{n}{k} = \\binom{n-1}{k-1} + \\binom{n-1}{k}$.
    4. The pattern contains many fractal-like properties which we'll explore in later sections.
    """)

# 3D Extension of Pascal's Triangle
elif selected_section == "3D Extension of Pascal's Triangle":
    st.markdown("## 3D Extension of Pascal's Triangle")
    
    st.markdown("""
    Pascal's triangle can be extended into three and higher dimensions. 
    In 3D, it becomes "Pascal's tetrahedron" or "Pascal's pyramid".
    
    In this extension:
    - Each entry is the sum of the entries directly above it in the previous layer
    - The entries represent multinomial coefficients rather than binomial coefficients
    - The structure extends the combinatorial properties of Pascal's triangle into higher dimensions
    """)
    
    # Controls for 3D Pascal visualization
    rotation_speed = st.slider("Rotation Speed", min_value=0.0, max_value=2.0, value=0.5, step=0.1)
    view_dimension = st.slider("View Dimensions", min_value=2, max_value=min(4, dimension), value=min(3, dimension))
    
    # Generate 3D Pascal data
    pascal_3d = create_pascal_3d(max_rows, dimension)
    
    # Visualize 3D Pascal's triangle
    fig_3d = visualize_pascal_3d(pascal_3d, view_dimension, rotation_speed)
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("""
    ### Mathematical Interpretation
    
    In higher dimensions, Pascal's triangle generalizes to Pascal's simplex, where each vertex represents a multinomial coefficient:
    
    $$\\binom{n}{k_1, k_2, ..., k_d} = \\frac{n!}{k_1!k_2!...k_d!}$$
    
    Where $k_1 + k_2 + ... + k_d = n$ and $d$ is the dimension.
    
    This structure corresponds to the coefficients in the multinomial expansion:
    
    $$(x_1 + x_2 + ... + x_d)^n = \\sum_{k_1+k_2+...+k_d=n} \\binom{n}{k_1, k_2, ..., k_d} x_1^{k_1}x_2^{k_2}...x_d^{k_d}$$
    """)

# Galois Theory & G(2) Group Symmetries
elif selected_section == "Galois Theory & G(2) Group Symmetries":
    st.markdown("## Galois Theory & G(2) Group Symmetries")
    
    st.markdown("""
    Galois theory studies symmetries in mathematical structures, particularly focusing on field extensions. 
    The G(2) group is a specific symmetry group that describes transformations in high-dimensional spaces.
    
    In our visualization, we represent:
    1. The automorphisms that preserve the structure
    2. Symmetry operations corresponding to the G(2) group
    3. How these symmetries relate to the patterns in Pascal's structures
    """)
    
    # Parameters for G(2) visualization
    symmetry_type = st.selectbox(
        "Symmetry Type", 
        ["Root System", "Weyl Group", "Dynkin Diagram"], 
        index=0
    )
    
    # Generate and visualize G(2) symmetry
    g2_graph = create_g2_symmetry_graph(symmetry_type, detail_level)
    fig_g2 = visualize_g2_symmetry(g2_graph, symmetry_type)
    st.plotly_chart(fig_g2, use_container_width=True)
    
    st.markdown("""
    ### G(2) Group Properties
    
    The G(2) group is one of the exceptional Lie groups, with special properties:
    
    - It has a rank of 2 and dimension of 14
    - Its root system has 12 roots in a 2-dimensional space
    - The Weyl group of G(2) is the dihedral group of order 12
    - It contains both SU(2) and SU(3) as subgroups
    
    These symmetries manifest in the patterns of higher-dimensional versions of Pascal's triangle,
    creating connections between combinatorial structures and abstract algebra.
    """)
    
    st.latex(r"""
    \text{The G(2) Cartan matrix: } 
    \begin{pmatrix}
    2 & -3 \\
    -1 & 2
    \end{pmatrix}
    """)

# Fractal Recursion in Higher Dimensions
elif selected_section == "Fractal Recursion in Higher Dimensions":
    st.markdown("## Fractal Recursion in Higher Dimensions")
    
    st.markdown("""
    The patterns in Pascal's triangle exhibit fractal-like properties. When extended to higher dimensions
    and transformed through Galois theory symmetries, they create self-similar structures across scales.
    
    Fractal recursion in this context means:
    1. Patterns that repeat at different scales
    2. Self-similar structures appearing in higher dimensions
    3. Recursive relationships between different layers of the mathematical structure
    """)
    
    # Parameters for fractal recursion
    fractal_type = st.selectbox(
        "Fractal Type", 
        ["Pascal-based", "Galois-transformed", "Combined"], 
        index=0
    )
    
    zoom_level = st.slider("Zoom Level", min_value=1.0, max_value=10.0, value=1.0, step=0.5)
    
    # Generate and visualize fractal recursion
    fractal_data = generate_fractal_recursion(
        max_rows, 
        dimension, 
        fractal_depth, 
        fractal_type
    )
    
    fig_fractal = visualize_fractal_recursion(fractal_data, fractal_type, zoom_level)
    st.plotly_chart(fig_fractal, use_container_width=True)
    
    st.markdown("""
    ### Mathematical Interpretation
    
    The fractal patterns emerge from iterative applications of:
    
    1. **Pascal's recurrence relation**: $\\binom{n}{k} = \\binom{n-1}{k-1} + \\binom{n-1}{k}$
    2. **Galois transformations**: Symmetry operations from the G(2) group
    3. **Dimensional extensions**: Projections between different dimensional spaces
    
    These combined operations create self-similar structures that repeat across scales and dimensions,
    revealing deep connections between combinatorial mathematics and abstract algebra.
    """)

# Combined Visualization
elif selected_section == "Combined Visualization":
    st.markdown("## Pascal-Euler-Galois Fractal: Combined Visualization")
    
    st.markdown("""
    This comprehensive visualization integrates all the mathematical concepts:
    - Pascal's triangle structure and binomial relationships
    - Extension into higher dimensions
    - Galois theory symmetries, particularly the G(2) group
    - Fractal recursion patterns across dimensions
    
    The resulting structure demonstrates how these different mathematical domains
    interconnect to form a unified framework for understanding combinatorial,
    algebraic, and geometric patterns.
    """)
    
    # Parameters for combined visualization
    integration_level = st.slider("Integration Level", min_value=1, max_value=5, value=3)
    animation_speed = st.slider("Animation Speed", min_value=0.1, max_value=2.0, value=1.0, step=0.1)
    
    # Create combined visualization using subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'surface'}, {'type': 'scatter3d'}],
               [{'type': 'scatter3d'}, {'type': 'surface'}]],
        subplot_titles=(
            "Pascal's 3D Extension", 
            "G(2) Group Symmetries",
            "Fractal Recursion", 
            "Combined Structure"
        )
    )
    
    # Generate the data for all visualizations
    pascal_3d = create_pascal_3d(max_rows, dimension)
    g2_graph = create_g2_symmetry_graph("Root System", detail_level)
    fractal_data = generate_fractal_recursion(max_rows, dimension, fractal_depth, "Combined")
    
    # 1. Pascal's 3D Extension
    pascal_fig = visualize_pascal_3d(pascal_3d, min(3, dimension), animation_speed, as_figure=True)
    for trace in pascal_fig.data:
        fig.add_trace(trace, row=1, col=1)
    
    # 2. G(2) Group Symmetries
    g2_fig = visualize_g2_symmetry(g2_graph, "Root System", as_figure=True)
    for trace in g2_fig.data:
        fig.add_trace(trace, row=1, col=2)
    
    # 3. Fractal Recursion
    fractal_fig = visualize_fractal_recursion(fractal_data, "Combined", 1.0, as_figure=True)
    for trace in fractal_fig.data:
        fig.add_trace(trace, row=2, col=1)
    
    # 4. Combined Visualization - merge all three concepts
    # This is a custom visualization combining elements from all three
    # Create a unified data structure
    unified_x, unified_y, unified_z = [], [], []
    unified_colors = []
    
    # Add transformed Pascal data
    for i in range(min(len(pascal_3d), 100)):
        x, y, z, log_val, val = pascal_3d[i]  # Unpack all 5 values from the tuple
        # Apply a transformation based on G(2) symmetry to show interconnection
        unified_x.append(x * np.cos(z * 0.1) - y * np.sin(z * 0.1))
        unified_y.append(x * np.sin(z * 0.1) + y * np.cos(z * 0.1))
        unified_z.append(z * 1.5)
        unified_colors.append('blue')
    
    # Add G(2) data points
    for vertex in g2_graph.nodes():
        x, y, z = g2_graph.nodes[vertex]['pos']
        # Scale and shift to integrate with Pascal data
        unified_x.append(x * 2 + 3)
        unified_y.append(y * 2 + 3)
        unified_z.append(z * 2 + max_rows/2)
        unified_colors.append('red')
    
    # Add fractal recursion data
    for i in range(min(len(fractal_data), 100)):
        x, y, z, log_val, val = fractal_data[i]  # Unpack all 5 values from fractal_data
        # Transform to integrate
        unified_x.append(x * 1.5 - 2)
        unified_y.append(y * 1.5 - 2)
        unified_z.append(z * 1.2)
        unified_colors.append('green')
    
    # Create the combined 3D scatter plot
    fig.add_trace(
        go.Scatter3d(
            x=unified_x,
            y=unified_y,
            z=unified_z,
            mode='markers',
            marker=dict(
                size=5,
                color=unified_colors,
                opacity=0.8
            ),
            name="Unified Structure"
        ),
        row=2, col=2
    )
    
    # Update layout for the entire figure
    fig.update_layout(
        height=800,
        width=1200,
        scene=dict(
            aspectmode='cube',
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        scene2=dict(
            aspectmode='cube',
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        scene3=dict(
            aspectmode='cube',
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        scene4=dict(
            aspectmode='cube',
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        title="Pascal-Euler-Galois Fractal: Integrated Mathematical Structure"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    ### The PEGFRA Mathematical Synthesis
    
    The Pascal-Euler-Galois Fractal Ruliard Algorithm (PEGFRA) unifies these mathematical domains:
    
    1. **Combinatorial Structures**: Represented by Pascal's triangle and its higher-dimensional extensions
    2. **Algebraic Symmetries**: Captured by Galois theory and the G(2) group
    3. **Geometric Patterns**: Manifested in the fractal recursion across dimensions
    
    This synthesis reveals new insights into the underlying mathematical structures that connect 
    discrete mathematics (Pascal's triangle), abstract algebra (Galois theory),
    and geometric visualization (fractal recursion).
    
    As the dimension parameter increases, more complex patterns emerge, demonstrating how
    these mathematical concepts scale and interact in higher-dimensional spaces.
    """)

# Add an explanation footer
st.markdown("---")
st.markdown("""
### About This Application

This visualization tool demonstrates the relationships between different mathematical
domains through interactive exploration. The underlying algorithms combine concepts from
combinatorial mathematics, abstract algebra, and fractal geometry.

Use the sidebar controls to adjust parameters and see how the mathematical structures
transform across dimensions and scales.
""")

