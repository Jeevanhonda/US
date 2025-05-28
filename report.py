import streamlit as st
import pymongo
import pandas as pd
from datetime import datetime
def app(name=None):
    namee=name
    st.write(f"Wel {name}")
    # ---- MongoDB connection ----
    conn = pymongo.MongoClient(
        "mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"
    )
    conn_obj = conn["jeevan"]
    cust = conn_obj["customer_detail"]

    # ---- Page Title ----
    st.title("🏍️ Customer Report Portal")
    st.markdown("Use this tool to view customer details and update sale status.")

    # ---- Fetch and prepare data ----
    df_cust = pd.DataFrame(list(cust.find({}, {"_id": 0})))
    df_cust = df_cust.drop_duplicates()
    df_cust["Quotation_Date"] = pd.to_datetime(df_cust["Quotation_Date"], errors='coerce')  # Ensure datetime format

    # ---- User Filters ----
    st.sidebar.header("🔍 Filter Records")
    if name==None:
        staff_name = st.sidebar.selectbox("Select the Staff Name:", df_cust["Sales_person"].dropna().unique())
    else:
        staff_name = st.sidebar.selectbox("Select the Staff Name:", namee)
    status=st.sidebar.selectbox("Select Any One Of this Status",["Not Sale","Sale"])
    st_date = st.sidebar.date_input("Select Start Date")
    en_date = st.sidebar.date_input("Select End Date")

    # ---- Convert Streamlit date to datetime ----
    start_dt = datetime.combine(st_date, datetime.min.time())
    end_dt = datetime.combine(en_date, datetime.max.time())

    # ---- Filter Data ----
    filtered_df = df_cust[
        (df_cust["Sales_person"] == staff_name) &
        (df_cust["Quotation_Date"].between(start_dt, end_dt))&
        (df_cust["Status"]==status)
    ]

    # ---- Display Filtered Data ----
    if filtered_df.empty:
        st.warning("No records found for the selected staff and date range.")
    else:
        st.success(f"Showing records for {staff_name} from {st_date} to {en_date}")
        filtered_df.index=range(1,len(filtered_df)+1)
        st.dataframe(filtered_df)


if __name__ == "__main__":
    app()      
