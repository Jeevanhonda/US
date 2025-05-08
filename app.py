import streamlit as st
import pymongo
import pandas as pd

# MongoDB connection
conn = pymongo.MongoClient("mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
conn_obj = conn["jeevan"]
branch = conn_obj["branch"]

# Fetch existing branches
branches = list(branch.find({}, {"_id": 0}))
df = pd.DataFrame(branches)
df.index = range(1, len(df) + 1)

# Input and save logic
branch_name = st.text_input("Enter the Branch Name :")
if st.button("Save Branch"):
    existing_names = df["Branch_Name"].tolist()  # Convert to list
    if branch_name:
        if branch_name not in existing_names:
            branch.insert_one({"Branch_Name": branch_name})
            st.success("Branch saved!")
            st.rerun()
        else:
            st.warning("The branch already exists.")
    else:
        st.error("Please enter a branch name.")

# Show saved branches
st.subheader("Saved Branches:")

st.write(df)
