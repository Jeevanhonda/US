import streamlit as st
import pymongo
import pandas as pd
def app(name=None):
    namee=name
    # ---- MongoDB connection ----
    conn = pymongo.MongoClient("mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
    conn_obj = conn["jeevan"]
    cust = conn_obj["customer_detail"]

    # ---- Page Title ----
    st.title("🏍️ Customer Sale Update Portal")
    st.markdown("Use this tool to view customer details and update sale status.")

    # ---- Fetch and prepare data ----
    df_cust = pd.DataFrame(list(cust.find({}, {"_id": 0})))
    df_cust = df_cust.drop_duplicates()
    df_cust.index = range(1, len(df_cust) + 1)
    df_cust=df_cust[df_cust["Status"]=="Not Sale"]
    #st.write(df_cust)
    if namee==None:
        pass
    else:
         df_cust = df_cust[df_cust["Sales_person"].isin(namee)]

    # ---- Customer Selection ----
    st.subheader("🔍 Select a Customer")
    Name = st.selectbox("Customer Name", df_cust["Customer_name"])

    # ---- Display Customer Info ----
    selected_customer = df_cust[df_cust["Customer_name"] == Name].iloc[0]
    ph_no = selected_customer["Phone_no"]
    add = selected_customer["Address"]

    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📞 **Phone Number:** {ph_no}")
    with col2:
        st.info(f"🏠 **Address:** {add}")

    # ---- Update Button ----
    st.markdown("---")
    if st.button("✅ Mark as Sold"):
        cust.update_one({"Phone_no": ph_no}, {"$set": {"Status": "Sale"}})
        st.success("✅ Sale entry has been successfully entered!")
        st.rerun()



if __name__ == "__main__":
    app()      
