import streamlit as st
import pymongo
import pandas as pd

def app():
    # ---- MongoDB Connection ----
    conn = pymongo.MongoClient("mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
    conn_obj = conn["jeevan"]
    staff_name = conn_obj["staff_name"]
    branch = conn_obj["branch"]

    # ---- Page Title ----
    st.title("👨‍💼 Add Sales Staff")
    st.markdown("Register new sales staff and assign them to a branch.")

    # ---- Load Branches ----
    branches = list(branch.find({}, {"_id": 0}))
    df_branch = pd.DataFrame(branches)

    # ---- Staff Input Form ----
    st.subheader("📝 Staff Details")
    col1, col2 = st.columns(2)

    with col1:
        staff_namee = st.text_input("👤 Staff Name")
        phone = st.number_input("📱 Phone Number", step=1)

    with col2:
        Branch = st.selectbox("🏢 Select Branch", df_branch["Branch_Name"].unique())

    # ---- Fetch Existing Staff ----
    staff_list = list(staff_name.find({}, {"_id": 0}))
    df_staff = pd.DataFrame(staff_list)

    # ---- Save Button ----
    if st.button("💾 Save Staff"):
        staff_names = df_staff["Sales_Person"].tolist() if not df_staff.empty else []

        if not staff_namee:
            st.warning("⚠️ Please enter the staff name.")
        elif staff_namee in staff_names:
            st.warning("⚠️ Staff name already exists.")
        else:
            new_staff = {
                "Sales_Person": staff_namee,
                "Branch": Branch,
                "Phone_Number": phone
            }
            staff_name.insert_one(new_staff)
            st.success("✅ Staff member added successfully.")
            st.rerun()

    # ---- Show Existing Staff ----
    st.markdown("---")
    st.subheader("📋 Existing Staff Members")
    if not df_staff.empty:
        df_staff.index = range(1, len(df_staff) + 1)
        st.dataframe(df_staff)
    else:
        st.info("No staff records found.")


if __name__ == "__main__":
    app()      