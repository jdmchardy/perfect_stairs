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

def mk_init_params(min_steps, max_steps, min_overhang, max_overhang):
        steps_init = int((min_steps + max_steps)/2)
        overhang_init = int((min_overhang + max_overhang)/2)
        angle_init = 40 #The initial value for the inclination angle in degrees
        return steps_init, overhang_init, angle_init

def cost_function(params, ideal_values, total_rise):
    #ideal values is a list containing [opt_height, opt_depth, opt_overhang, opt_angle]

    number_steps = params[0]
    step_overhang = params[1]
    inclination_angle = params[2]

    h2_step_height = total_rise/number_steps
    w_step_cut_depth = h2_step_height/np.tan(np.radians(inclination_angle))
    t_step_tread_depth = w_step_cut_depth + step_overhang
    calc = [h2_step_height, t_step_tread_depth, step_overhang, inclination_angle]
    percentage = calc/ideal*100

    residuals = percentage-100
    cost = sum(residuals**2)
    return cost

def run_optimisation():
    a = 1

def get_cut_values(stair_solution):

    """
    number_steps = stair_solution[]
    total_rise = stair_solution[]
    actual_joist_width = stair_solution[]
    tread_thickness = stair_solution[]
    inclination_angle = stair_solution[]

    h2 = total_rise/number_steps
    h1 = h2 - tread_thickness

    a1 = actual_joist_width-h1*np.cos(np.radians(inclination_angle))
    a2 = actual_joist_width-(step_cut_depth*np.sin(np.radians(inclination_angle)))
    
    return a1, a2, b1, b2, b3, c1, c2, d1
    """

def main():
    st.set_page_config(page_title="Stair Joist Calculator", layout="centered")
    st.title("🪜 Stair Joist Calculator")

    st.markdown("### Enter Stair Parameters (mm)")

    st.markdown("#### Essential Parameters")
    col1, col2 = st.columns(2)
    with col1:
        joist_width = st.number_input("Actual Joist Width (mm)",value = 400, min_value=0, step=1, help="The actual width of the joist stringer.")
    with col2:
        total_rise = st.number_input("Total Rise (mm)", value = 2000, min_value=0, step=1)

    col1, col2 = st.columns(2)
    with col1:
        tread_thickness = st.number_input("Tread Thickness (mm)", value = 30, min_value=0, step=1, help="The thickness of the step material.")
    with col2:
        backboard_thickness = st.number_input("Backboard Thickness (mm)", value = 30, min_value=0, step=1, help="The thickness of the step backing material.")

    st.markdown("#### Optimum Values")

    col1, col2 = st.columns(2)
    with col1:
        opt_step_height = st.number_input("Optimal step height (mm)", value = 240, min_value=0, step=1, help="Desired step height.")
        opt_step_depth = st.number_input("Optimal step depth (mm)", value = 300, min_value=0, step=1, help="Desired step depth.")
    with col2:
        opt_overhang = st.number_input("Optimal overhang (deg)", value = 10, min_value=0, step=1, help="Ideal overhang.")
        opt_angle = st.number_input("Optimal inclination angle (deg)", value = 40.0, min_value=0.0, step=0.1, help="Desired inclination angle.")
    
    st.markdown("#### Constraints")
    col1, col2 = st.columns(2)
    with col1:
        max_run = st.number_input("Maximum run (mm)", value = 3000, min_value=0, step=1, help="Constraint on the maximum run allowed.")
    with col2:
        min_stringer_thickness = st.number_input("Minimum stringer Thickness (mm)", value=100, min_value=0, step=1, help="The allowable remaining joist thickness.")

    col1, col2 = st.columns(2)
    with col1:
        min_number_of_steps = st.number_input("Min number of steps", min_value=1, step=1)
    with col2:
        max_number_of_steps = st.number_input("Max number of steps", value=10, min_value=1, step=1)

    col1, col2 = st.columns(2)
    with col1:
        min_step_height = st.number_input("Min step height (mm)", value = 180, min_value=1, step=1)
    with col2:
        max_step_height = st.number_input("Max step height (mm)", value=260, min_value=1, step=1)

    col1, col2 = st.columns(2)
    with col1:
        min_step_depth = st.number_input("Min step depth (mm)", value= 220, min_value=1, step=1)
    with col2:
        max_step_depth = st.number_input("Max step depth (mm)", value=320, min_value=1, step=1)

    col1, col2 = st.columns(2)
    with col1:
        min_overhang = st.number_input("Min overhang (mm)", value=0, min_value=0, step=1, help="The minimum nosing overhang over each step.")
    with col2:
        max_overhang = st.number_input("Max overhang (mm)", value = 30, min_value=0, step=1, help="The maximum nosing overhang over each step.")

    if st.button("Compute stair geometry"):
        with st.spinner("Calculating stair geometry..."):

            #Run main calculations here.....
            st.success("Geometry Solved!")

            #Get initial parameter values
            steps_init, overhang_init, angle_init = mk_init_params(min_number_of_steps, max_number_of_steps, min_overhang, max_overhang)

            #Run the minimisation here
            initial_guess = [steps_init, overhang_init, angle_init]
            ideal_values = [opt_step_height, opt_step_depth, opt_overhang, opt_angle]
            cost = cost_function(initial_guess, ideal_values, total_rise)
            st.write(cost)
            

            #Calculate the cut values from the refined results

            #cut_values = get_cut_values()

            fig = draw_stair_diagram_realistic(total_rise, total_run, number_of_steps, tread_thickness, overhang)
            st.pyplot(fig)

if __name__ == "__main__":
    main()
