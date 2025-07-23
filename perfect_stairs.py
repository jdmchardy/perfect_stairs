import streamlit as st
import matplotlib.pyplot as plt

def draw_stair_diagram(total_rise, total_run, number_of_steps):
    fig, ax = plt.subplots(figsize=(8, 4))

    step_rise = total_rise / number_of_steps
    step_run = total_run / number_of_steps

    # Draw stair treads and risers
    for i in range(number_of_steps):
        x = i * step_run
        y = i * step_rise
        ax.plot([x, x + step_run], [y, y], color="brown", linewidth=2)  # tread
        ax.plot([x + step_run, x + step_run], [y, y + step_rise], color="brown", linewidth=2)  # riser

    # Draw stringer line
    ax.plot([0, total_run], [0, total_rise], linestyle="--", color="gray", label="Stringer")

    # Annotations
    ax.text(total_run / 2, total_rise + 20, "Total Rise (mm)", ha="center", fontsize=10)
    ax.text(total_run + 20, total_rise / 2, "Total Run (mm)", rotation=270, va="center", fontsize=10)

    ax.set_xlim(-10, total_run + 50)
    ax.set_ylim(-10, total_rise + 50)
    ax.set_aspect('equal')
    ax.axis("off")

    return fig

def main():
    st.set_page_config(page_title="Stair Joist Calculator", layout="centered")
    st.title("Stair Joist Dimension Input (mm)")

    st.markdown("### Enter Dimensions in Millimeters (mm)")

    # Input fields
    total_rise = st.number_input("Total Rise (mm)", min_value=10.0, step=10.0)
    total_run = st.number_input("Total Run (mm)", min_value=10.0, step=10.0)
    tread_thickness = st.number_input("Tread Thickness (mm)", min_value=0.0, step=1.0)
    number_of_steps = st.number_input("Number of Steps", min_value=1, step=1)
    stringer_thickness = st.number_input("Stringer Thickness (mm)", min_value=0.0, step=1.0)
    landing_height = st.number_input("Landing Height (mm)", min_value=0.0, step=10.0)
    joist_spacing = st.number_input("Joist Spacing (mm)", min_value=0.0, step=10.0)

    if st.button("Submit"):
        st.success("Parameters submitted. Drawing diagram...")

        input_data = {
            "total_rise": total_rise,
            "total_run": total_run,
            "tread_thickness": tread_thickness,
            "number_of_steps": number_of_steps,
            "stringer_thickness": stringer_thickness,
            "landing_height": landing_height,
            "joist_spacing": joist_spacing,
        }

        st.json(input_data)

        fig = draw_stair_diagram(total_rise, total_run, number_of_steps)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
