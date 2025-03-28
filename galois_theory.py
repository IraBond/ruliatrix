import numpy as np
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp

def create_g2_symmetry_graph(symmetry_type="Root System", detail_level=3):
    """
    Creates a graph representing G(2) symmetry group based on the specified type.
    
    Args:
        symmetry_type (str): Type of symmetry to generate ("Root System", "Weyl Group", or "Dynkin Diagram")
        detail_level (int): Level of detail to include (1-5)
        
    Returns:
        networkx.Graph: A graph representing the G(2) symmetry
    """
    G = nx.Graph()
    
    if symmetry_type == "Root System":
        # Create the G(2) root system
        # G(2) has 12 roots in a 2D plane, arranged in a 12-pointed star
        # We'll embed this in 3D space for visualization
        
        # Define the fundamental roots
        alpha1 = np.array([1, -1, 0]) / np.sqrt(2)
        alpha2 = np.array([0, 1, -1]) / np.sqrt(2)
        
        roots = []
        
        # Generate the positive roots
        roots.append(alpha1)
        roots.append(alpha2)
        roots.append(alpha1 + alpha2)
        roots.append(2*alpha1 + alpha2)
        roots.append(3*alpha1 + alpha2)
        roots.append(3*alpha1 + 2*alpha2)
        
        # Add negative roots
        negative_roots = [-r for r in roots]
        roots.extend(negative_roots)
        
        # Add nodes for each root
        for i, root in enumerate(roots):
            G.add_node(i, pos=root, type='root')
        
        # Add edges between related roots based on detail level
        for i in range(len(roots)):
            for j in range(i+1, len(roots)):
                # Connect roots that differ by a simple root
                diff = roots[i] - roots[j]
                dist = np.linalg.norm(diff)
                if dist < 2 + (detail_level * 0.5):
                    G.add_edge(i, j, weight=1/dist)
    
    elif symmetry_type == "Weyl Group":
        # The Weyl group of G(2) is the dihedral group of order 12
        # It consists of 12 reflections and rotations in the plane
        
        # Create vertices for the 12 elements of the Weyl group
        for i in range(12):
            angle = 2 * np.pi * i / 12
            x = np.cos(angle)
            y = np.sin(angle)
            z = 0
            G.add_node(i, pos=np.array([x, y, z]), type='group_element')
        
        # Connect elements based on multiplication in the group
        for i in range(12):
            # Connect to immediate neighbors (generators)
            G.add_edge(i, (i+1) % 12, type='generator')
            
            # Add more connections based on detail level
            for j in range(2, 2 + detail_level):
                G.add_edge(i, (i+j) % 12, type='relation')
    
    elif symmetry_type == "Dynkin Diagram":
        # The Dynkin diagram for G(2) is simple - just 2 nodes with a triple edge
        # We'll represent this in 3D space
        
        # Create the two nodes for the simple roots
        G.add_node(0, pos=np.array([0, 0, 0]), type='simple_root')
        G.add_node(1, pos=np.array([1, 0, 0]), type='simple_root')
        
        # Add the triple edge between them
        G.add_edge(0, 1, weight=3, type='triple_edge')
        
        # If detail level is high, add more structure
        if detail_level > 2:
            # Add the derived roots
            G.add_node(2, pos=np.array([1.5, 0.5, 0]), type='derived_root')
            G.add_node(3, pos=np.array([2, 0, 0]), type='derived_root')
            G.add_node(4, pos=np.array([2.5, 0.5, 0]), type='derived_root')
            G.add_node(5, pos=np.array([3, 0, 0]), type='derived_root')
            
            # Connect to show relationships
            G.add_edge(1, 2, weight=1, type='derivation')
            G.add_edge(2, 3, weight=1, type='derivation')
            G.add_edge(3, 4, weight=1, type='derivation')
            G.add_edge(4, 5, weight=1, type='derivation')
        
        # If detail level is very high, add 3D structure
        if detail_level > 4:
            # Add projections to 3D
            for i in range(6):
                pos = G.nodes[i]['pos']
                new_pos = np.array([pos[0], pos[1], 0.5])
                G.add_node(i+6, pos=new_pos, type='projection')
                G.add_edge(i, i+6, weight=0.5, type='projection')
    
    return G

def visualize_g2_symmetry(g2_graph, symmetry_type, as_figure=False):
    """
    Creates a visualization of the G(2) symmetry graph.
    
    Args:
        g2_graph (networkx.Graph): Graph representing G(2) symmetry
        symmetry_type (str): Type of symmetry being visualized
        as_figure (bool): If True, return the figure without displaying
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure with the visualization
    """
    # Extract node positions and types
    node_x = []
    node_y = []
    node_z = []
    node_colors = []
    node_sizes = []
    
    for node in g2_graph.nodes():
        pos = g2_graph.nodes[node]['pos']
        node_x.append(pos[0])
        node_y.append(pos[1])
        node_z.append(pos[2])
        
        node_type = g2_graph.nodes[node].get('type', 'default')
        
        # Assign colors based on node type
        if node_type == 'root':
            node_colors.append('red')
            node_sizes.append(8)
        elif node_type == 'simple_root':
            node_colors.append('gold')
            node_sizes.append(12)
        elif node_type == 'derived_root':
            node_colors.append('orange')
            node_sizes.append(10)
        elif node_type == 'group_element':
            node_colors.append('blue')
            node_sizes.append(8)
        elif node_type == 'projection':
            node_colors.append('purple')
            node_sizes.append(6)
        else:
            node_colors.append('gray')
            node_sizes.append(8)
    
    # Extract edge positions
    edge_x = []
    edge_y = []
    edge_z = []
    edge_colors = []
    edge_widths = []
    
    for u, v, data in g2_graph.edges(data=True):
        x0, y0, z0 = g2_graph.nodes[u]['pos']
        x1, y1, z1 = g2_graph.nodes[v]['pos']
        
        # Add line coordinates
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])
        
        # Assign colors and widths based on edge type
        edge_type = data.get('type', 'default')
        weight = data.get('weight', 1)
        
        if edge_type == 'triple_edge':
            edge_colors.extend(['darkred', 'darkred', 'darkred'])
            edge_widths.extend([4, 4, 4])
        elif edge_type == 'generator':
            edge_colors.extend(['navy', 'navy', 'navy'])
            edge_widths.extend([3, 3, 3])
        elif edge_type == 'derivation':
            edge_colors.extend(['orange', 'orange', 'orange'])
            edge_widths.extend([2, 2, 2])
        elif edge_type == 'projection':
            edge_colors.extend(['purple', 'purple', 'purple'])
            edge_widths.extend([1, 1, 1])
        else:
            edge_colors.extend(['rgba(150,150,150,0.5)', 'rgba(150,150,150,0.5)', 'rgba(150,150,150,0.5)'])
            edge_widths.extend([weight, weight, weight])
    
    # Create a figure with edge traces
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color=edge_colors, width=2),
        hoverinfo='none',
        showlegend=False
    ))
    
    # Add nodes
    fig.add_trace(go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        marker=dict(
            size=node_sizes,
            color=node_colors,
            opacity=0.8
        ),
        text=[f"Node {i}" for i in range(len(node_x))],
        hoverinfo='text'
    ))
    
    # Update layout
    fig.update_layout(
        title=f"G(2) Group - {symmetry_type}",
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        height=700,
        showlegend=False
    )
    
    # Add mathematical annotation
    if symmetry_type == "Root System":
        fig.add_annotation(
            text=r"G(2) Root System: 12 roots in a plane",
            xref="paper", yref="paper",
            x=0.5, y=0.97,
            showarrow=False
        )
    elif symmetry_type == "Weyl Group":
        fig.add_annotation(
            text=r"G(2) Weyl Group: Dihedral group of order 12",
            xref="paper", yref="paper",
            x=0.5, y=0.97,
            showarrow=False
        )
    elif symmetry_type == "Dynkin Diagram":
        fig.add_annotation(
            text=r"G(2) Dynkin Diagram: ○═══○",
            xref="paper", yref="paper",
            x=0.5, y=0.97,
            showarrow=False
        )
    
    if as_figure:
        return fig
    else:
        return fig
