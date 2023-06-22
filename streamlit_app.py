import streamlit as st
from pulp import *

# Set page configuration
st.set_page_config(layout="wide")

# Function to align input fields to the left
def left_align():
    st.markdown('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# Function to align output to the right
def right_align():
    st.markdown('<style>div.row-widget.stButton > button{margin-left:auto}</style>', unsafe_allow_html=True)

def solve_integer_programming(obj_coefficients, num_vars, restricted_vars, constraint_coeffs, constraint_signs, rhs_entries, optimization_mode):
    # Create the problem variable
    prob = LpProblem("Integer_Programming_Problem", LpMaximize if optimization_mode == "Maximize" else LpMinimize)

    # Define the decision variables
    decision_vars = []
    for i in range(num_vars):
        var_name = f"x{i+1}"
        var_type = 'Integer' if restricted_vars[i] else 'Continuous'
        var = LpVariable(var_name, lowBound=0, cat=var_type)
        decision_vars.append(var)

    # Define the objective function
    objective = lpSum(obj_coefficients[i] * decision_vars[i] for i in range(len(decision_vars)))
    if optimization_mode == "Maximize":
        prob += objective
    else:
        prob += -objective

    # Define the constraints
    for i in range(len(constraint_coeffs)):
        constraint_expr = lpSum(constraint_coeffs[i][j] * decision_vars[j] for j in range(len(decision_vars)))
        if constraint_signs[i] == "<=":
            prob += constraint_expr <= float(rhs_entries[i])
        elif constraint_signs[i] == "=":
            prob += constraint_expr == float(rhs_entries[i])
        else:
            prob += constraint_expr >= float(rhs_entries[i])

    # Solve the problem
    prob.solve()

    # Print the results
    result = "Optimal Solution:\n"
    for var in decision_vars:
        result += f"{var.name} = {var.varValue}\n"
    result += f"Objective Value: {int(prob.objective.value())}"
    return result


# Streamlit app
def main():
    st.title("Integer Programming Solver")

    # Add logo
    logo_path = "E:\\sanjay\\Bpo\\Project\\IP.png"
    logo_col, title_col = st.columns([1, 4])
    with logo_col:
        st.image(logo_path, use_column_width=True)
    with title_col:
        st.write("")
        st.write("")
        st.write("")
        st.header("Integer Programming Solver")


    # Get the number of variables and constraints
    num_vars = st.number_input("Enter the number of variables:", value=1, step=1)
    num_constraints = st.number_input("Enter the number of constraints:", value=1, step=1)

    if st.button("Reset"):
        st.experimental_rerun()

    if num_vars > 0 and num_constraints > 0:
        left_align()

        # Move objective function coefficients below the number of constraints
        st.write("---")
        st.header("Objective Function Coefficients")

        # Get the objective function coefficients
        obj_coefficients = []
        for i in range(num_vars):
            coeff = st.number_input(f"Enter the coefficient for x{i+1}:")
            obj_coefficients.append(coeff)

        # Get the restricted variables
        restricted_vars = []
        for i in range(num_vars):
            value2 = st.selectbox(f"Select the restriction for x{i+1}:", options=["Unrestricted", "Restricted"])
            restricted_vars.append(value2 == "Restricted")

        # Get the constraint coefficients and right-hand sides
        constraint_coeffs = []
        constraint_signs = []
        rhs_entries = []
        st.write("---")
        st.header("Constraints")
        for i in range(num_constraints):
            constraint_coefficients = []
            for j in range(num_vars):
                coeff = st.number_input(f"Enter the coefficient for x{j+1} in constraint {i+1}:")
                constraint_coefficients.append(coeff)
            constraint_coeffs.append(constraint_coefficients)

            sign = st.selectbox(f"Select the sign for constraint {i+1}:", options=["<=", ">=", "="])
            constraint_signs.append(sign)

            rhs = st.number_input(f"Enter the right-hand side for constraint {i+1}:")
            rhs_entries.append(rhs)

        # Get the optimization mode
        optimization_mode = st.selectbox("Select the optimization mode:", options=["Maximize", "Minimize"])

        if st.button("Solve"):
            result = solve_integer_programming(obj_coefficients, num_vars, restricted_vars, constraint_coeffs, constraint_signs, rhs_entries, optimization_mode)
            st.text(result)


if __name__ == "__main__":
    main()
    right_align()
