import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math

def draw_stair_diagram(total_rise, total_run, number_of_steps, tread_thickness, overhang):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    step_rise = total_rise / number_of_steps
    step_run = total_run / number_of_steps

    # Modern colors
    tread_color = "#8B4513"       # Saddle brown
    riser_color = "#A0522D"       # Sienna
    background = "#F9F9F9"

    fig.patch.set_facecolor(background)
    ax.set_facecolor(background)

    for i in range(number_of_steps):
        x = i * step_run
        y = i * step_rise

        # Draw tread with overhang
        tread = patches.FancyBboxPatch((x - overhang, y + tread_thickness), 
                                       step_run + overhang, -tread_thickness,
                                       boxstyle="round,pad=0.02", 
                                       linewidth=0.5, facecolor=tread_color, edgecolor="black")
        ax.add_patch(tread)

        # Draw riser (vertical face)
        ax.add_patch(patches.Rectangle((x, y), 0.5, step_rise, facecolor=riser_color, edgecolor="black", linewidth=0.5))

    # Draw dashed stringer line
    ax.plot([0, total_run], [0, total_rise], linestyle="--", color="gray", linewidth=1.0)

    # Add annotations
    ax.annotate(f"Total Rise: {total_rise:.0f} mm", xy=(0, total_rise), xytext=(-80, total_rise / 2),
                textcoords='data', arrowprops=dict(arrowstyle="->"), fontsize=9, ha='right')
    
    ax.annotate(f"Total Run: {total_run:.0f} mm", xy=(total_run, 0), xytext=(total_run / 2, -60),
                textcoords='data', arrowprops=dict(arrowstyle="->"), fontsize=9, ha='center')

    # Step height and tread thickness on first step
    ax.annotate(f"Step Height: {step_rise:.0f} mm", xy=(0, step_rise / 2), xytext=(30, step_rise / 2),
                arrowprops=dict(arrowstyle="->"), fontsize=9, va='center')

    ax.annotate(f"Tread Thickness: {tread_thickness:.0f} mm", xy=(step_run / 2, tread_thickness),
                xytext=(step_run / 2, tread_thickness + 25),
                arrowprops=dict(arrowstyle="->"), fontsize=9, ha='center')

    # Overhang annotation
    ax.annotate(f"Overhang: {overhang:.0f} mm", xy=(0, 5),
                xytext=(-20, 30), arrowprops=dict(arrowstyle="->"),
                fontsize=9, ha='left')

    # Stair angle
    angle_rad = math.atan2(total_rise, total_run)
    angle_deg = math.degrees(angle_rad)
    ax.text(total_run * 0.65, total_rise * 0.05,
            f"Stair Angle: {angle_deg:.1f}°", fontsize=10, color='darkblue')

    # Final formatting
    ax.set_xlim(-100, total_run + 100)
    ax.set_ylim(-50, total_rise + 100)
    ax.set_aspect('equal')
    ax.axis('off')

    return fig

def main():
    st.set_page_config(page_title="Stair Joist Calculator", layout="centered")
    st.title("🪜 Stair Joist Visualizer")

    st.markdown("### Enter Dimensions in Millimeters (mm)")

    total_rise = st.number_input("Total Rise (mm)", min_value=100.0, step=10.0)
    total_run = st.number_input("Total Run (mm)", min_value=100.0, step=10.0)
    tread_thickness = st.number_input("Tread Thickness (mm)", min_value=0.0, step=1.0)
    overhang = st.number_input("Step Overhang (mm)", min_value=0.0, step=1.0)
    number_of_steps = st.number_input("Number of Steps", min_value=1, step=1)
    stringer_thickness = st.number_input("Stringer Thickness (mm)", min_value=0.0, step=1.0)
    landing_height = st.number_input("Landing Height (mm)", min_value=0.0, step=10.0)

    if st.button("Submit"):
        st.success("Rendering high-quality diagram...")

        input_data = {
            "total_rise": total_rise,
            "total_run": total_run,
            "tread_thickness": tread_thickness,
            "overhang": overhang,
            "number_of_steps": number_of_steps,
            "stringer_thickness": stringer_thickness,
            "landing_height": landing_height,
        }

        st.json(input_data)

        fig = draw_stair_diagram(total_rise, total_run, number_of_steps, tread_thickness, overhang)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
