import streamlit as st
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for Streamlit
import matplotlib.pyplot as plt    
import numpy as np

st.title("Centroid Calculator")

# Initialize session state for shapes and holes
if "shapes" not in st.session_state:
    st.session_state.shapes = []  # filled parts, positive area
if "holes" not in st.session_state:
    st.session_state.holes = []   # holes with negative area

shape_options = ["Rectangle", "Triangle", "Circle"]

def add_shape_or_hole(is_hole=False):
    st.subheader("Add " + ("Hole" if is_hole else "Shape"))
    shape_type = st.selectbox("Shape Type", shape_options, key="hole_shape" if is_hole else "shape_type")

    if shape_type == "Rectangle":
        length = st.number_input("Length (horizontal)", min_value=0.1, value=2.0, key=("hole_len" if is_hole else "shape_len"))
        width = st.number_input("Width (vertical)", min_value=0.1, value=2.0, key=("hole_w" if is_hole else "shape_w"))
        centroid_x = st.number_input("Centroid X", value=0.0, key=("hole_centroid_x" if is_hole else "shape_centroid_x"))
        centroid_y = st.number_input("Centroid Y", value=0.0, key=("hole_centroid_y" if is_hole else "shape_centroid_y"))

        area = length * width

        if st.button("Add " + ("Hole" if is_hole else "Shape"), key=("hole_add_btn" if is_hole else "shape_add_btn")):
            data = (shape_type, (length, width), (centroid_x, centroid_y), area)
            if is_hole:
                st.session_state.holes.append(data)
            else:
                st.session_state.shapes.append(data)
            st.success(f"{'Hole' if is_hole else 'Shape'} added!")

    elif shape_type == "Triangle":
        base = st.number_input("Base (horizontal)", min_value=0.1, value=2.0, key=("hole_base" if is_hole else "shape_base"))
        height = st.number_input("Height (vertical)", min_value=0.1, value=2.0, key=("hole_height" if is_hole else "shape_height"))
        centroid_x = st.number_input("Centroid X", value=0.0, key=("hole_centroid_x_tri" if is_hole else "shape_centroid_x_tri"))
        centroid_y = st.number_input("Centroid Y", value=0.0, key=("hole_centroid_y_tri" if is_hole else "shape_centroid_y_tri"))

        area = 0.5 * base * height

        if st.button("Add " + ("Hole" if is_hole else "Shape"), key=("hole_add_btn_tri" if is_hole else "shape_add_btn_tri")):
            data = (shape_type, (base, height), (centroid_x, centroid_y), area)
            if is_hole:
                st.session_state.holes.append(data)
            else:
                st.session_state.shapes.append(data)
            st.success(f"{'Hole' if is_hole else 'Shape'} added!")

    elif shape_type == "Circle":
        radius = st.number_input("Radius", min_value=0.1, value=1.0, key=("hole_radius" if is_hole else "shape_radius"))
        centroid_x = st.number_input("Centroid X", value=0.0, key=("hole_centroid_x_circ" if is_hole else "shape_centroid_x_circ"))
        centroid_y = st.number_input("Centroid Y", value=0.0, key=("hole_centroid_y_circ" if is_hole else "shape_centroid_y_circ"))

        area = np.pi * radius ** 2

        if st.button("Add " + ("Hole" if is_hole else "Shape"), key=("hole_add_btn_circ" if is_hole else "shape_add_btn_circ")):
            data = (shape_type, (radius,), (centroid_x, centroid_y), area)
            if is_hole:
                st.session_state.holes.append(data)
            else:
                st.session_state.shapes.append(data)
            st.success(f"{'Hole' if is_hole else 'Shape'} added!")

# Sidebar for adding shapes and holes
st.sidebar.title("Add Shapes & Holes")
add_shape_or_hole(is_hole=False)
st.sidebar.markdown("---")
add_shape_or_hole(is_hole=True)

# Display current shapes and holes
st.subheader("Composite Shape - Filled Parts")
if st.session_state.shapes:
    for i, shape in enumerate(st.session_state.shapes, 1):
        st.write(f"{i}. {shape[0]} centered at {shape[2]} with area {shape[3]:.2f}")
else:
    st.write("No filled shapes added.")

st.subheader("Holes (Cut-outs)")
if st.session_state.holes:
    for i, hole in enumerate(st.session_state.holes, 1):
        st.write(f"{i}. {hole[0]} hole centered at {hole[2]} with area {hole[3]:.2f}")
else:
    st.write("No holes added.")

# Calculate composite centroid considering holes as negative area
if st.button("Calculate Composite Centroid"):
    total_area = 0
    sum_x = 0
    sum_y = 0

    for _, _, (cx, cy), area in st.session_state.shapes:
        total_area += area
        sum_x += area * cx
        sum_y += area * cy

    for _, _, (cx, cy), area in st.session_state.holes:
        total_area -= area
        sum_x -= area * cx
        sum_y -= area * cy

    if total_area == 0:
        st.error("Total area is zero; check input shapes and holes.")
    else:
        centroid_x = sum_x / total_area
        centroid_y = sum_y / total_area
        st.success(f"Composite centroid is at (X: {centroid_x:.2f}, Y: {centroid_y:.2f}) with total area {total_area:.2f}.")

        # Plot composite shapes and holes centered at input centroids
        fig, ax = plt.subplots()

        for shape_type, params, (cx, cy), _ in st.session_state.shapes:
            if shape_type == "Rectangle":
                length, width = params
                # Draw rectangle centered at (cx, cy)
                lower_left_x = cx - length / 2
                lower_left_y = cy - width / 2
                rect = plt.Rectangle((lower_left_x, lower_left_y), length, width, color='lightblue', alpha=0.7)
                ax.add_patch(rect)

            elif shape_type == "Triangle":
                base, height = params
                # Triangle vertices with centroid at (cx, cy)
                # Centroid of triangle at (x0 + base/3, y0 + height/3)
                # Solve for vertex (x0,y0)
                x0 = cx - base / 3
                y0 = cy - height / 3
                points = [(x0, y0), (x0 + base, y0), (x0 + base / 3, y0 + height)]
                triangle = plt.Polygon(points, color='lightgreen', alpha=0.7)
                ax.add_patch(triangle)

            elif shape_type == "Circle":
                r = params[0]
                circle = plt.Circle((cx, cy), r, color='lightcoral', alpha=0.7)
                ax.add_patch(circle)

        for hole_type, params, (cx, cy), _ in st.session_state.holes:
            if hole_type == "Rectangle":
                length, width = params
                lower_left_x = cx - length / 2
                lower_left_y = cy - width / 2
                rect = plt.Rectangle((lower_left_x, lower_left_y), length, width, color='white')
                ax.add_patch(rect)

            elif hole_type == "Triangle":
                base, height = params
                x0 = cx - base / 3
                y0 = cy - height / 3
                points = [(x0, y0), (x0 + base, y0), (x0 + base / 3, y0 + height)]
                triangle = plt.Polygon(points, color='white')
                ax.add_patch(triangle)

            elif hole_type == "Circle":
                r = params[0]
                circle = plt.Circle((cx, cy), r, color='white')
                ax.add_patch(circle)

        # Draw composite centroid
        ax.scatter([centroid_x], [centroid_y], color='black', marker='X', s=150, label='Composite Centroid')

        ax.set_aspect('equal')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)


