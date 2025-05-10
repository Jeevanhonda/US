import streamlit as st
import pymongo
import pandas as pd
def app():
    # Page configuration
    

    # MongoDB connection
    conn = pymongo.MongoClient(
        "mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,"
        "ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,"
        "ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/"
        "?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"
    )
    conn_obj = conn["jeevan"]
    bike = conn_obj["bike_price"]

    # Fetch records
    bikes = list(bike.find({}, {"_id": 0}))
    df = pd.DataFrame(bikes)

    # Page Title
    st.title("🛠️ Update Bike Price Details")
    st.markdown("Edit pricing details for any saved bike model.")

    if not df.empty:
        # Bike selector
        bike_model = st.selectbox("🔽 Select a Bike Model", df["Bike_Model"].unique())
        selected_bike = df[df["Bike_Model"] == bike_model].iloc[0]

        # Form for editing
        with st.form("edit_form"):
            st.markdown("### ✏️ Edit Bike Prices")

            col1, col2 = st.columns(2)
            with col1:
                ex_show = st.number_input("Ex-Showroom Price (₹)", min_value=0.0, step=100.0, value=float(selected_bike["Ex_showroom"]))
                rd_tax = st.number_input("Road Tax (₹)", min_value=0.0, step=100.0, value=float(selected_bike["Road_tax"]))
                ins = st.number_input("Insurance (₹)", min_value=0.0, step=100.0, value=float(selected_bike["Insurance"]))

            with col2:
                war = st.number_input("Warranty (₹)", min_value=0.0, step=100.0, value=float(selected_bike["Warranty"]))
                fit = st.number_input("Fittings (₹)", min_value=0.0, step=100.0, value=float(selected_bike["Fitting"]))
                on_road = ex_show + rd_tax + ins + war + fit
                st.markdown(f"### 💰 On-Road Price: ₹ {on_road:,.2f}")

            submitted = st.form_submit_button("💾 Save Changes")

        if submitted:
            update_data = {
                "Ex_showroom": ex_show,
                "Road_tax": rd_tax,
                "Insurance": ins,
                "Warranty": war,
                "Fitting": fit,
                "On-Road-Price": on_road
            }
            bike.update_one({"Bike_Model": bike_model}, {"$set": update_data})
            st.success(f"✅ '{bike_model}' updated successfully.")
            st.rerun()

        # Display updated table
        st.subheader("📋 Updated Bike Records")
        refreshed = list(bike.find({}, {"_id": 0}))
        df_new = pd.DataFrame(refreshed)
        df_new.index = range(1, len(df_new) + 1)
        st.dataframe(df_new, use_container_width=True, height=400)
    else:
        st.warning("⚠️ No bike records found in the database.")



if __name__ == "__main__":
    app()      