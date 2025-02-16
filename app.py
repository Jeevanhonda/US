import streamlit as st
import math_grade4_line
import math_grade4_bar
import math_grade4_area
import math_grade4_female_line
import math_grade4_female_bar
import math_grade4_female_area
import math_grade4_overall_line
import math_grade4_overall_bar
import math_grade4_statewise_line
import math_grade4_statewise_area
import math_grade4_statewise_bar
import math_grade4_statewise_male_vs_female
import math_grade8_area
import math_grade8_bar
import math_grade8_line
import math_grade8_female_area
import math_grade8_female_bar
import math_grade8_female_line
import math_grade8_statewise_area
import math_grade8_statewise_bar
import math_grade8_statewise_line
import math_grade8_overall_bar
import math_grade8_overall_line
import reading_grade4_line
import reading_grade4_bar
import reading_grade4_area
import reading_grade4_female_line
import reading_grade4_female_bar
import reading_grade4_female_area
import reading_grade4_overall_line
import reading_grade4_overall_bar
import reading_grade4_statewise_line
import reading_grade4_statewise_area
import reading_grade4_statewise_bar
import reading_grade8_area
import reading_grade8_bar
import reading_grade8_line
import reading_grade8_female_area
import reading_grade8_female_bar
import reading_grade8_female_line
import reading_grade8_statewise_area
import reading_grade8_statewise_bar
import reading_grade8_statewise_line
import reading_grade8_overall_bar
import reading_grade8_overall_line
import math_grade8_statewise_male_vs_female
import reading_grade4_statewise_male_vs_female
import reading_grade8_statewise_male_vs_female

# Set page layout to wide
st.set_page_config(layout="wide")

# Read query params
params = st.query_params
page = params.get("page", "")  # Default to home if no query param

# Page Navigation
if page == "math_grade4_line":
    math_grade4_line.show()
elif page == "math_grade4_bar":
    math_grade4_bar.show()
elif page == "math_grade4_area":
    math_grade4_area.show()
elif page == "math_grade4_female_line":
    math_grade4_female_line.show()
elif page == "math_grade4_female_bar":
    math_grade4_female_bar.show()
elif page == "math_grade4_female_area":
    math_grade4_female_area.show()
elif page == "math_grade4_overall_line":
    math_grade4_overall_line.show()
elif page == "math_grade4_overall_bar":
    math_grade4_overall_bar.show()
elif page == "math_grade4_statewise_line":
    math_grade4_statewise_line.show()
elif page == "math_grade4_statewise_area":
    math_grade4_statewise_area.show()
elif page == "math_grade4_statewise_bar":
    math_grade4_statewise_bar.show()
elif page == "math_grade8_area":
    math_grade8_area.show()
elif page == "math_grade8_bar":
    math_grade8_bar.show()
elif page == "math_grade8_line":
    math_grade8_line.show()
elif page == "math_grade8_female_area":
    math_grade8_female_area.show()
elif page == "math_grade8_female_bar":
    math_grade8_female_bar.show()
elif page == "math_grade8_female_line":
    math_grade8_female_line.show()
elif page == "math_grade8_statewise_area":
    math_grade8_statewise_area.show()
elif page == "math_grade8_statewise_bar":
    math_grade8_statewise_bar.show()
elif page == "math_grade8_statewise_line":
    math_grade8_statewise_line.show()
elif page == "math_grade8_overall_bar":
    math_grade8_overall_bar.show()
elif page == "math_grade8_overall_line":
    math_grade8_overall_line.show()
elif page == "reading_grade4_line":
    reading_grade4_line.show()
elif page == "reading_grade4_bar":
    reading_grade4_bar.show()
elif page == "reading_grade4_area":
    reading_grade4_area.show()
elif page == "reading_grade4_female_line":
    reading_grade4_female_line.show()
elif page == "reading_grade4_female_bar":
    reading_grade4_female_bar.show()
elif page == "reading_grade4_female_area":
    reading_grade4_female_area.show()
elif page == "reading_grade4_overall_line":
    reading_grade4_overall_line.show()
elif page == "reading_grade4_overall_bar":
    reading_grade4_overall_bar.show()
elif page == "reading_grade4_statewise_line":
    reading_grade4_statewise_line.show()
elif page == "reading_grade4_statewise_area":
    reading_grade4_statewise_area.show()
elif page == "reading_grade4_statewise_bar":
    reading_grade4_statewise_bar.show()
elif page == "reading_grade8_area":
    reading_grade8_area.show()
elif page == "reading_grade8_bar":
    reading_grade8_bar.show()
elif page == "reading_grade8_line":
    reading_grade8_line.show()
elif page == "reading_grade8_female_area":
    reading_grade8_female_area.show()
elif page == "reading_grade8_female_bar":
    reading_grade8_female_bar.show()
elif page == "reading_grade8_female_line":
    reading_grade8_female_line.show()
elif page == "reading_grade8_statewise_area":
    reading_grade8_statewise_area.show()
elif page == "reading_grade8_statewise_bar":
    reading_grade8_statewise_bar.show()
elif page == "reading_grade8_statewise_line":
    reading_grade8_statewise_line.show()
elif page == "reading_grade8_overall_bar":
    reading_grade8_overall_bar.show()
elif page == "reading_grade8_overall_line":
    reading_grade8_overall_line.show()
elif page == "math_grade4_statewise_male_vs_female":
    math_grade4_statewise_male_vs_female.show()
elif page == "math_grade8_statewise_male_vs_female":
    math_grade8_statewise_male_vs_female.show()
elif page == "reading_grade4_statewise_male_vs_female":
    reading_grade4_statewise_male_vs_female.show()
elif page == "reading_grade8_statewise_male_vs_female":
    reading_grade8_statewise_male_vs_female.show()
else:
    st.write("Welcome to the Math Grade 4 Dashboard! Select a page from the sidebar.")
