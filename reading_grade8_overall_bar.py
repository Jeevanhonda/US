import pandas as pd
import streamlit as st
import plotly.express as px
def show():
    # Initialize session state variables
    if "page" not in st.session_state:
        st.session_state.page = 0

    st.header("Reading-Grade 8 Gender-wise Average Scale Score Visualization")

    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv("readings_grade_8_prediction_result.csv")
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

    df = df.copy()  # Avoid modifying the original DataFrame

                    # Drop 'Unnamed: 0' if it exists
                    # Drop 'Unnamed: 0' if it exists
    if "Unnamed: 0" in df.columns:
            df.drop(columns="Unnamed: 0", inplace=True)
        
        # Select relevant columns
    col = df.columns[2:]

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Data Cleaning: Remove parentheses and replace non-numeric values with 0
    for i in col:
        df[i] = df[i].replace(r'[\(\)]', '', regex=True)  # Remove ()
        df[i] = df[i].replace(r'^[^0-9].*', '0', regex=True)  # Replace non-numeric starts
        df[i] = pd.to_numeric(df[i], errors="coerce")  # Convert to numeric

    # Replace 0 values with column mean (excluding 0s)
    for i in col:
        lis = df[i].tolist()  # Convert column to list
        non_zero_values = [x for x in lis if x != 0]  # Exclude 0s
        
        if non_zero_values:  # Check if there are non-zero values
            mean_value = sum(non_zero_values) / len(non_zero_values)  # Calculate mean excluding 0s
            df[i] = [mean_value if x == 0 else x for x in lis]  # Replace all 0s

    df=df.iloc[:,2:]
    col=df.columns
    dic = {i: df[i].mean() for i in df.columns}

    df2 = pd.DataFrame(dic, index=[0])  # Put means in a single row
    col1 = [
        "2003Average scale score", "2005Average scale score", "2007Average scale score",
        "2009Average scale score", "2011Average scale score","2013Average scale score_x", 
        "2015Average scale score_x","2017Average scale score_x","2019Average scale score_x",
        "2022Average scale score_x", "2024Average scale score_x"]
    col2=[
            "2013Average scale score_y",
        "2015Average scale score_y", "2017Average scale score_y", "2019Average scale score_y",
        "2022Average scale score_y", "2024Average scale score_y","2025Average scale score"]

    col3=["2013 mean","2015 mean","2017 mean","2019 mean","2022 mean","2024 mean","2025 mean"]
    col4=["2013 median","2015 median","2017 median","2019 median","2022 median","2024 median","2025 median"]

    df3=df2[col1]               
    df4=df2[col2]
    df5=df2[col3]
    df6=df2[col4]
    df3["Type"] = "Actual"
    df4["Type"] = "Predicted"
    df5["Type"]="Mean"
    df6["Type"]="Median"

    # Merge both DataFrames
    df_combined = pd.concat([df3, df4,df5,df6])

    # Ensure consistent column naming
    df_combined.columns = [col.replace("_x", "").replace("_y", "").strip() for col in df_combined.columns]

    # Melt the DataFrame for Plotly
    df_melted = df_combined.melt(id_vars=["Type"], var_name="Year", value_name="Average Scale Score")
    df_melted["Year"] = df_melted["Year"].str.extract(r'(\d{4})').astype(int)

    # Line Chart
    fig5 = px.line(
        df_melted, 
        x="Year", 
        y="Average Scale Score", 
        color="Type",
        line_dash="Type",
        color_discrete_map={"Actual": "blue", "Predicted": "red","Mean":"Green","Median":"Purple"},
        title="Actual vs Predicted Average Scale Score", 
        markers=True
        
    )

    # Bar Chart
    fig5_bar = px.bar(
        df_melted, 
        x="Year", 
        y="Average Scale Score", 
        color="Type",
        barmode="group",  # Actual & Predicted side by side
        color_discrete_map={"Actual": "blue", "Predicted": "red","Mean":"Green","Median":"Purple"},
        title="Actual vs Predicted Average Scale Score (Bar Chart)"
        
    )

    # Set Y-axis to start at 0 and adjust range
    fig5_bar.update_layout(
        yaxis=dict(
            title="Average Scale Score", 
            gridcolor="lightgrey", 
            zeroline=True, 
            zerolinecolor="black", 
            rangemode="tozero"
        ),
        xaxis=dict(title="Year", showgrid=True),
        plot_bgcolor="white",
        title_font=dict(size=18, family="Arial", color="black"),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.5)", bordercolor="black", borderwidth=1)
    )

    # Ensure Y-axis starts at 0 for the bar chart
    fig5_bar.update_layout(
        yaxis=dict(
            range=[df_melted["Average Scale Score"].min() - 5, df_melted["Average Scale Score"].max() + 5]
        )
    )

    # Area Chart
    fig2_area = px.area(
        df_melted,  # Use df_melted to maintain consistency
        x="Year", 
        y="Average Scale Score", 
        color="Type",
        color_discrete_map={"Actual": "blue", "Predicted": "red"},
        title="Overall Average Scale Score (Actual vs Predicted)"  # Fixed title
        
    )

    # Force Y-axis to start at 0
    fig2_area.update_layout(
        yaxis=dict(title="Average Scale Score", gridcolor="lightgrey", zeroline=True, zerolinecolor="black", rangemode="tozero"),
        xaxis=dict(title="Year", showgrid=True),
        plot_bgcolor="white",
        title_font=dict(size=18, family="Arial", color="black"),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.5)", bordercolor="black", borderwidth=1),
    )


    st.plotly_chart(fig5_bar)