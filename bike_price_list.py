import streamlit as st
import pymongo
import pandas as pd

def app():
    # Streamlit page config
    

    # MongoDB connection
    conn = pymongo.MongoClient(
        "mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,"
        "ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,"
        "ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/"
        "?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"
    )

    conn_obj = conn["jeevan"]
    bike = conn_obj["bike_price"]

    # Title
    st.title("🏍️ Bike Quotation Manage")
    st.markdown("Enter and manage bike pricing details for **Jeevan Auto Moto Pvt Ltd**.")

    # --- Input Section ---
    st.subheader("📝 Add Bike Details")
    with st.form("bike_form"):
        bike_name = st.text_input("Bike Model Name", placeholder="e.g. Shine 125 Drum", key="bike_name")
        col1, col2 = st.columns(2)

        with col1:
            ex_show = st.number_input("Ex-Showroom Price (₹)", min_value=0.0, step=100.0, format="%.2f")
            rd_tax = st.number_input("Road Tax (₹)", min_value=0.0, step=100.0, format="%.2f")
            ins = st.number_input("Insurance (₹)", min_value=0.0, step=100.0, format="%.2f")

        with col2:
            war = st.number_input("Warranty (₹)", min_value=0.0, step=100.0, format="%.2f")
            fit = st.number_input("Fittings (₹)", min_value=0.0, step=100.0, format="%.2f")
            on_road = ex_show + rd_tax + ins + war + fit
            st.markdown(f"### 💰 On-Road Price: ₹ {on_road:,.2f}")

        submitted = st.form_submit_button("💾 Save Bike Details")

    # Prepare and fetch data
    bikes = list(bike.find({}, {"_id": 0}))
    df = pd.DataFrame(bikes)
    df.index = range(1, len(df) + 1)

    # --- Save Logic ---
    if submitted:
        existing_bikes = df["Bike_Model"].tolist() if not df.empty else []
        if bike_name:
            if bike_name not in existing_bikes:
                data = {
                    "Bike_Model": bike_name,
                    "Ex_showroom": ex_show,
                    "Road_tax": rd_tax,
                    "Insurance": ins,
                    "Warranty": war,
                    "Fitting": fit,
                    "On-Road-Price": on_road
                }
                bike.insert_one(data)
                st.success(f"✅ Bike '{bike_name}' saved successfully!")
                st.rerun()
            else:
                st.warning("⚠️ This bike model already exists.")
        else:
            st.error("❌ Please enter a valid bike model name.")

    # --- Display Section ---
    st.subheader("📋 Existing Bike Models")
    if df.empty:
        st.info("No bike records found.")
    else:
        st.dataframe(df, use_container_width=True, height=400)


if __name__ == "__main__":
    app()      