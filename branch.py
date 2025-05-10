import streamlit as st
import pymongo
import pandas as pd

def app():
    # Streamlit page configuration
    

    # MongoDB connection
    conn = pymongo.MongoClient(
        "mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,"
        "ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/"
        "?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"
    )
    conn_obj = conn["jeevan"]
    branch = conn_obj["branch"]

    # Fetch existing branches
    branches = list(branch.find({}, {"_id": 0}))
    df = pd.DataFrame(branches)
    df.index = range(1, len(df) + 1)

    # Title
    st.title("🏢 Branch Manage")
    st.markdown("Use this tool to **add and view branches** of Jeevan Auto Moto Pvt Ltd.")

    # Input Section
    st.subheader("➕ Add a New Branch")
    with st.form("branch_form"):
        branch_name = st.text_input("Branch Name", placeholder="e.g. Madurai East, Chennai Main")
        submitted = st.form_submit_button("Save Branch")

        if submitted:
            existing_names = df["Branch_Name"].tolist()
            if branch_name:
                if branch_name not in existing_names:
                    branch.insert_one({"Branch_Name": branch_name})
                    st.success(f"✅ Branch '{branch_name}' saved successfully!")
                    st.rerun()
                else:
                    st.warning(f"⚠️ Branch '{branch_name}' already exists.")
            else:
                st.error("❌ Please enter a branch name.")

    # Display Section
    st.subheader("🏬 Existing Branches")
    if df.empty:
        st.info("No branches found. Add a new branch above.")
    else:
        st.dataframe(df, use_container_width=True, height=300)


if __name__ == "__main__":
    app()      