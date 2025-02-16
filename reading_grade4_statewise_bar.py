import pandas as pd
import streamlit as st
import plotly.express as px




def show():
    st.header("Reading-Grade 4 Gender-wise Average Scale Score Visualization")
    

    # Load dataset
    df = pd.read_csv("readings_grade_4_prediction_result.csv")

    # Define numerical columns for scale scores
    all_num_cols = [
        "2003Average scale score", "2005Average scale score", "2007Average scale score",
        "2009Average scale score", "2011Average scale score", "2013Average scale score_y",
        "2013Average scale score_x", "2015Average scale score_y", "2015Average scale score_x",
        "2017Average scale score_y", "2017Average scale score_x", "2019Average scale score_y",
        "2019Average scale score_x", "2022Average scale score_y", "2022Average scale score_x",
        "2024Average scale score_y", "2024Average scale score_x", "2025Average scale score",
        "2013 mean","2015 mean","2017 mean","2019 mean","2022 mean","2024 mean","2025 mean",
        "2013 median","2015 median","2017 median","2019 median","2022 median","2024 median","2025 median"
    ]

    # Convert numerical columns to numeric type (handle errors gracefully)
    for col in all_num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ensure 'Jurisdiction' column exists
    if "Jurisdiction" not in df.columns:
        st.error("🚨 The dataset does not contain a 'Jurisdiction' column!")
        st.stop()

    # Get unique states (Jurisdiction)
    state_list = df["Jurisdiction"].dropna().unique().tolist()

    # Split states into two columns
    states_col1 = state_list[:27]  
    states_col2 = state_list[27:]  

    # Create layout columns
    col1, col2, col3 = st.columns([1, 1, 2])  

    # Store selected states
    selected_states = []

    # Checkboxes in col1
    with col1:
        st.subheader("Select One State")
        for state in states_col1:
            if st.checkbox(state, key=f"state_{state}"):  
                selected_states.append(state)

    # Checkboxes in col2
    with col2:
        st.subheader("")
        for state in states_col2:
            if st.checkbox(state, key=f"state_{state}"):  
                selected_states.append(state)

    # Check for valid selection
    with col3:
        if len(selected_states) == 0 or len(selected_states) >= 2:
            st.warning("⚠️ Please select exactly one state to display data.")
        else:
            selected_state = selected_states[0]  # Get the selected state

                # Filter DataFrame based on selected state
        df_filtered = df[df["Jurisdiction"] == selected_state]



        # Group by Jurisdiction (State) and calculate mean
        df_gr = df_filtered.groupby("Jurisdiction", as_index=False)[all_num_cols].mean()

        # Define actual and predicted score columns
        score_columns_x = [
            "2003Average scale score", "2005Average scale score", "2007Average scale score",
            "2009Average scale score", "2011Average scale score", "2013Average scale score_x",
            "2015Average scale score_x", "2017Average scale score_x", "2019Average scale score_x",
            "2022Average scale score_x", "2024Average scale score_x"
        ]

        score_columns_y = [
            "2013Average scale score_y", "2015Average scale score_y", "2017Average scale score_y",
            "2019Average scale score_y", "2022Average scale score_y", "2024Average scale score_y",
            "2025Average scale score"
        ]
        score_columns_z = ["2013 mean","2015 mean","2017 mean","2019 mean","2022 mean","2024 mean","2025 mean"]
        score_columns_a = ["2013 median","2015 median","2017 median","2019 median","2022 median","2024 median","2025 median"]

        # Convert wide format to long format for visualization
        df_melted1 = df_gr.melt(id_vars=["Jurisdiction"], value_vars=score_columns_x, var_name="Year", value_name="Average Scale Score")
        df_melted2 = df_gr.melt(id_vars=["Jurisdiction"], value_vars=score_columns_y, var_name="Year", value_name="Average Scale Score")
        df_melted3= df_gr.melt(id_vars=["Jurisdiction"], value_vars=score_columns_z, var_name="Year", value_name="Average Scale Score")
        df_melted4= df_gr.melt(id_vars=["Jurisdiction"], value_vars=score_columns_a, var_name="Year", value_name="Average Scale Score")
        # Extract numeric Year from column names
        df_melted1["Year"] = df_melted1["Year"].str.extract(r'(\d{4})').astype(int)
        df_melted2["Year"] = df_melted2["Year"].str.extract(r'(\d{4})').astype(int)
        df_melted3["Year"] = df_melted3["Year"].str.extract(r'(\d{4})').astype(int)
        df_melted4["Year"] = df_melted4["Year"].str.extract(r'(\d{4})').astype(int)

        # Assign labels
        df_melted1["Type"] = "Actual"
        df_melted2["Type"] = "Predicted"
        df_melted3["Type"] = "Mean"
        df_melted4["Type"] = "Median"

        # Merge both datasets
        df_combined = pd.concat([df_melted1, df_melted2,df_melted3,df_melted4])
        

        # Plot data using Plotly
        fig2 = px.bar(
            df_combined, 
            x="Year", 
            y="Average Scale Score", 
            color="Type",
            barmode="group",  # Ensures bars appear side by side
            color_discrete_map={"Actual": "green", "Predicted": "red", "Mean": "purple", "Median": "pink"},
            title=f"{selected_state} Average Scale Score (Actual vs Predicted)",
            height=500
        )
        fig2.update_layout(
                        yaxis=dict(
                            range=[df_combined["Average Scale Score"].min() - 5, df_combined["Average Scale Score"].max() + 5]
                        ),bargap=0.005,  # Reduce spacing between bars
        bargroupgap=0.015  # Reduce spacing between groups
                    )

        st.plotly_chart(fig2)
