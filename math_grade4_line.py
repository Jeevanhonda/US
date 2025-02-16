import pandas as pd
import streamlit as st
import plotly.express as px
def show():
        
    # Initialize session state variables
    if "page" not in st.session_state:
        st.session_state.page = 0

    st.header("Math-Grade 4 Gender-wise Average Scale Score Visualization")

    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv("grade_4_prediction_result.csv")
            return df
        except FileNotFoundError:
            st.error("Error: Data file not found. Please upload 'grade_4_prediction_result.csv'.")
            st.stop()

    df = load_data()

    # Define valid columns
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

    valid_columns = [col for col in all_num_cols if col in df.columns]

    # Convert columns to numeric
    df[valid_columns] = df[valid_columns].apply(pd.to_numeric, errors="coerce")

    # Group data by Gender
    df_gr = df.groupby("Gender", as_index=False)[valid_columns].mean()

    @st.cache_data
    def process_gender_data(gender):
        df_filtered = df_gr[df_gr["Gender"] == gender]
        if df_filtered.empty:
            return None

        col_actual = ["2003Average scale score", "2005Average scale score", "2007Average scale score",
                    "2009Average scale score", "2011Average scale score", "2013Average scale score_x",
                    "2015Average scale score_x", "2017Average scale score_x", "2019Average scale score_x",
                    "2022Average scale score_x", "2024Average scale score_x"]
        
        col_predicted = ["2013Average scale score_y", "2015Average scale score_y", "2017Average scale score_y",
                        "2019Average scale score_y", "2022Average scale score_y", "2024Average scale score_y",
                        "2025Average scale score"]
        
        col_mean = ["2013 mean", "2015 mean", "2017 mean", "2019 mean", "2022 mean", "2024 mean", "2025 mean"]
        col_median = ["2013 median", "2015 median", "2017 median", "2019 median", "2022 median", "2024 median", "2025 median"]

        valid_actual = [col for col in col_actual if col in df_filtered.columns]
        valid_predicted = [col for col in col_predicted if col in df_filtered.columns]
        valid_mean = [col for col in col_mean if col in df_filtered.columns]
        valid_median = [col for col in col_median if col in df_filtered.columns]

        df_melted_actual = df_filtered.melt(id_vars=["Gender"], value_vars=valid_actual,
                                            var_name="Year", value_name="Average Scale Score")
        df_melted_predicted = df_filtered.melt(id_vars=["Gender"], value_vars=valid_predicted,
                                            var_name="Year", value_name="Average Scale Score")
        df_melted_mean = df_filtered.melt(id_vars=["Gender"], value_vars=valid_mean,
                                        var_name="Year", value_name="Average Scale Score")
        df_melted_median = df_filtered.melt(id_vars=["Gender"], value_vars=valid_median,
                                            var_name="Year", value_name="Average Scale Score")

        # Extract year values correctly
        for df_melted in [df_melted_actual, df_melted_predicted, df_melted_mean, df_melted_median]:
            df_melted["Year"] = df_melted["Year"].str.extract(r'(\d{4})')[0].astype(int)

        df_melted_actual["Type"] = "Actual"
        df_melted_predicted["Type"] = "Predicted"
        df_melted_mean["Type"] = "Mean"
        df_melted_median["Type"] = "Median"

        df_combined = pd.concat([df_melted_actual, df_melted_predicted, df_melted_mean, df_melted_median])

        return df_combined

    # User Input Controls
    gender_choice = "Male"
    chart_type = "Line"

    # Process Data for Selected Gender
    df_combined = process_gender_data(gender_choice)

    # Plot Function
    def plot_chart(df_combined, chart_type, gender):
        if df_combined is None or df_combined.empty:
            st.warning(f"No data available for {gender}.")
            return

        df_combined = df_combined[~((df_combined["Year"] == 2025) & (df_combined["Type"] == "Actual"))]

        color_map = {"Actual": "green", "Predicted": "red", "Mean": "orange", "Median": "purple"}

        if chart_type == "Line":
            fig = px.line(df_combined, x="Year", y="Average Scale Score", color="Type",
                        line_dash="Type", markers=True, color_discrete_map=color_map,
                        title=f"{gender} Average Scale Score - Line Chart")

        elif chart_type == "Bar":
            fig = px.bar(df_combined, x="Year", y="Average Scale Score", color="Type",
                        barmode="group", color_discrete_map=color_map,
                        title=f"{gender} Average Scale Score - Bar Chart")

        elif chart_type == "Area":
            fig = px.area(df_combined, x="Year", y="Average Scale Score", color="Type",
                        color_discrete_map=color_map,
                        title=f"{gender} Average Scale Score - Area Chart")

        st.plotly_chart(fig)

    # Display Chart
    plot_chart(df_combined, "Line", "Male")
