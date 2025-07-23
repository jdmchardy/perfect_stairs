import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def draw_stair_diagram_realistic(total_rise, total_run, number_of_steps, tread_thickness, overhang):
    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

    # Basic step dimensions
    rise = total_rise / number_of_steps
    run = total_run / number_of_steps

    # Modern colors
    tread_color = "#5c4033"
    riser_color = "#d9a066"
    stringer_color = "#d1ccc0"
    background_color = "#fefefe"

    fig.patch.set_facecolor(background_color)
    ax.set_facecolor(background_color)

    # Draw stairs
    for i in range(number_of_steps):
        x = i * run
        y = i * rise

        # Riser
        ax.add_patch(patches.Polygon(
            [(x, y), (x, y + rise)],
            closed=False, color='black', linewidth=1.2))

        # Tread with overhang
        ax.add_patch(patches.Rectangle(
            (x - overhang, y + rise), run + overhang, -tread_thickness,
            linewidth=1.2, edgecolor='black', facecolor=tread_color))

    # Draw stringer cutouts (triangles)
    for i in range(number_of_steps):
        x = i * run
        y = i * rise

        ax.add_patch(patches.Polygon(
            [(x, y), (x + run, y), (x + run, y + rise)],
            closed=True, edgecolor='black', facecolor=stringer_color, linewidth=0.8))

    # Final line from base to top corner (overall stringer)
    ax.plot([0, total_run], [0, total_rise], color='black', linestyle='--', linewidth=1)

    # Add annotations similar to your diagram
    angle_rad = math.atan2(total_rise, total_run)
    angle_deg = math.degrees(angle_rad)

    ax.text(total_run * 0.05, -25, f"RUN = {total_run:.0f} mm", fontsize=9)
    ax.text(-80, total_rise * 0.5, f"RISE = {total_rise:.0f} mm", fontsize=9, rotation=90)
    ax.text(total_run * 0.6, total_rise * 0.1, f"Angle α = {angle_deg:.1f}°", fontsize=9, color='darkblue')

    ax.text(run * 0.3, rise + tread_thickness + 10, f"Overhang = {overhang:.0f} mm", fontsize=9)
    ax.text(run * 0.3, rise + 5, f"Tread = {run:.0f} mm", fontsize=9)
    ax.text(run + 10, rise / 2, f"Riser = {rise:.0f} mm", fontsize=9)

    # Bounds
    ax.set_xlim(-100, total_run + 100)
    ax.set_ylim(-50, total_rise + 100)
    ax.set_aspect('equal')
    ax.axis('off')

    return fig

def main():
    st.set_page_config(page_title="Precision Stair Joist Visualizer", layout="centered")
    st.title("🪜 Precision Stair Joist Visualizer")

    st.markdown("### Enter Stair Parameters (mm)")

    total_rise = st.number_input("Total Rise (mm)", min_value=100.0, step=10.0)
    total_run = st.number_input("Total Run (mm)", min_value=100.0, step=10.0)
    tread_thickness = st.number_input("Tread Thickness (mm)", min_value=0.0, step=1.0)
    overhang = st.number_input("Tread Overhang (mm)", min_value=0.0, step=1.0)
    number_of_steps = st.number_input("Number of Steps", min_value=1, step=1)
    stringer_thickness = st.number_input("Stringer Thickness (mm)", min_value=0.0, step=1.0)
    landing_height = st.number_input("Landing Height (mm)", min_value=0.0, step=10.0)

    if st.button("Render Stair Diagram"):
        st.success("Rendering diagram with construction geometry...")

        fig = draw_stair_diagram_realistic(total_rise, total_run, number_of_steps, tread_thickness, overhang)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
