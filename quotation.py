import streamlit as st
import pymongo
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import base64
from datetime import date, datetime

def app(name=None,add=None):
    namee=name
    add=add
        
    # Streamlit Page Config
    

    # MongoDB connection
    conn = pymongo.MongoClient(
        "mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,"
        "ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/"
        "?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0"
    )
    conn_obj = conn["jeevan"]
    cust = conn_obj["customer_detail"]
    staff_name = conn_obj["staff_name"]
    bike = conn_obj["bike_price"]

    df_staff = pd.DataFrame(list(staff_name.find({}, {"_id": 0})))
    df_bike = pd.DataFrame(list(bike.find({}, {"_id": 0})))

    current_date = date.today()

    # UI Title
    st.title("🏍️ Bike Quotation Generator")
    st.markdown(f"**Date:** {current_date.strftime('%B %d, %Y')}")

    # Form layout
    with st.form("quotation_form"):
        st.subheader("🔹 Customer Details")
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name:", placeholder="Enter full name")
            phone_number = st.text_input("Phone Number:", placeholder="10-digit mobile number")
        with col2:
            address = st.text_area("Address:", placeholder="Enter complete address including area and pincode")
        
        st.subheader("🔹 Bike and Sales Info")
        col3, col4 = st.columns(2)
        with col3:
            selected_bike = st.selectbox("Select Bike Model:", df_bike["Bike_Model"].unique())
        with col4:
            if namee==None:
                selected_staff = st.selectbox("Salesperson:", df_staff["Sales_Person"].unique())
            else:
                selected_staff = st.selectbox("Salesperson:", namee)
        
        submitted = st.form_submit_button("Generate Quotation")

    if submitted:
        if phone_number:
            if len(phone_number) == 10 and phone_number.isdigit():
                st.success("Valid phone number entered.")
            else:
                st.error("Please enter a valid 10-digit phone number.")
        else:
            st.warning("Phone number cannot be empty.")
        selected_staff_phone = df_staff[df_staff["Sales_Person"] == selected_staff]["Phone_Number"].iloc[0]
        df_cust = pd.DataFrame(list(cust.find({}, {"_id": 0})))
        bike_row = df_bike[df_bike["Bike_Model"] == selected_bike].iloc[0]
        ex_showroom = float(bike_row.get("Ex_showroom", 0))
        insurance = float(bike_row.get("Insurance", 0))
        registration = float(bike_row.get("Road_tax", 0))
        accessories = float(bike_row.get("Fitting", 0))
        warranty = float(bike_row.get("Warranty", 0))
        total_price = ex_showroom + insurance + registration + accessories + warranty

        customer_record = df_cust[df_cust["Phone_no"] == phone_number]

        if customer_record.empty:
            out = {
                "Customer_name": customer_name,
                "Phone_no": phone_number,
                "Bike_Model": selected_bike,
                "Address": address,
                "Status": "Not Sale",
                "Quotation_Date": datetime.combine(current_date, datetime.min.time()),
                "Sales_person": selected_staff
            }
            cust.insert_one(out)
            st.success("✅ Customer detail has been inserted successfully.")
        else:
            last_quotation_date = customer_record["Quotation_Date"].iloc[0]
            if isinstance(last_quotation_date, datetime):
                days_difference = (current_date - last_quotation_date.date()).days
            else:
                days_difference = 0

            if days_difference > 30:
                out = {
                    "Customer_name": customer_name,
                    "Phone_no": phone_number,
                    "Bike_Model": selected_bike,
                    "Address": address,
                    "Status": "Not Sale",
                    "Quotation_Date": datetime.combine(current_date, datetime.min.time()),
                    "Sales_person": selected_staff
                }
                cust.update_one({"Phone_no": phone_number}, {"$set": out})
                st.success("📅 New quotation inserted (more than 30 days old).")
            else:
                existing_bike_model = customer_record["Bike_Model"].iloc[0]
                bike_models = [model.strip() for model in existing_bike_model.split(",")]
                if selected_bike not in bike_models:
                    updated_bikes = ", ".join(bike_models + [selected_bike])
                else:
                    updated_bikes = existing_bike_model

                update_fields = {
                    "Customer_name": customer_name,
                    "Bike_Model": updated_bikes,
                    "Address": address,
                    "Status": "Not Sale",
                    "Quotation_Date": datetime.combine(current_date, datetime.min.time()),
                }
                cust.update_one({"Phone_no": phone_number}, {"$set": update_fields})
                st.info("ℹ️ Customer detail has been updated successfully.")

        class PDF(FPDF):            
            def header(self):
                if add==None:
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '144/1, Tirupparankunram Rd,', ln=True, align='C')
                    self.cell(0, 5, 'Palangantham, Madurai - 625003.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')
                if add=="ho":
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '144/1, Tirupparankunram Rd,', ln=True, align='C')
                    self.cell(0, 5, 'Palangantham, Madurai - 625003.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')
                if add=="kmr":
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '109, Kamarajar Salai,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625009.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')
                if add=="tnr":
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '74, GST Road, Tiruparankundram,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625006.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')
                if add=="nmp":
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '74,Theni Main Road, Nagamalai Pudukottai,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625019.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')
                if add=="ckm":
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '74,Theni Main Road, Nagamalai Pudukottai,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625019.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')
                if add=="tmg":
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '304,Virudhunagar Road, Thirumangalam,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625706.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')
                if add=="klk":
                    self.image("images.png", 10, 8, 33)
                    self.set_font('Arial', 'B', 18)
                    self.cell(0, 9, '', ln=True, align='C')
                    self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 5, '6/544G,T.Kallupatti Road, Kalligudi', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625706.', ln=True, align='C')
                    self.cell(0, 5, '', ln=True, align='C')
                    self.set_font('Arial', 'B', 16)
                    self.cell(0, 5, f'Date : {current_date}', ln=True, align='R')


            def footer(self):
                self.set_y(-42)
                self.set_font("Arial", '', 10)
                x = 10
                y = self.get_y()
                w = 190
                h = 34
                self.rect(x, y, w, h)
                self.set_xy(x + 2, y + 1)
                self.set_font("Arial", 'B', 8)
                self.cell(15, 4, "Scan UPI QR", ln=False)
                self.image("upi.jpg", x + 2, y + 6, 15, 15)
                self.set_xy(x + 20, y + 3)
                self.set_font("Arial", '', 12)
                self.multi_cell(
                    0, 5,
                    "   For NEFT/RTGS/BANK TRANSFERS       |            Name: Jeevan Auto Motor Pvt Ltd,\n"
                    "   Bank: HDFC BANK LTD                             |            Branch: ANDALPURAM\n"
                    "   A/C No: 50200083068012                          |            IFSC Code: HDFC0003734"
                )
                self.set_xy(x + 2, y + h - 6)
                self.set_font("Arial", 'I', 15)
                self.cell(0, 5, "Note: Please bring this copy next time you visit our showroom", ln=True, align="C")

        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(100, 10, f"Customer Name: {customer_name}", ln=False)
        pdf.cell(0, 10, f"       Phone Number: {phone_number}", ln=True, align="R")
        pdf.multi_cell(0, 10, f"Address: {address}", align="L")
        pdf.cell(100, 10, f"Sales Person : {selected_staff}", ln=False)
        pdf.cell(0, 10, f"Sales Person Phone Number: {selected_staff_phone}", ln=True, align="R")

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, "Quotation Details", ln=True, align="C")
        pdf.cell(0, 10, f"Bike Model: {selected_bike}", ln=True, align="C")

        pdf.set_x(13)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(90, 10, "Ex-Showroom Price", border=1)
        pdf.cell(90, 10, f"Rs {ex_showroom:.2f}", border=1, ln=True, align="R")

        pdf.set_x(13)
        pdf.cell(90, 10, "Insurance", border=1)
        pdf.cell(90, 10, f"Rs {insurance:.2f}", border=1, ln=True, align="R")

        pdf.set_x(13)
        pdf.cell(90, 10, "Registration Charges", border=1)
        pdf.cell(90, 10, f"Rs {registration:.2f}", border=1, ln=True, align="R")

        pdf.set_x(13)
        pdf.cell(90, 10, "Accessories", border=1)
        pdf.cell(90, 10, f"Rs {accessories:.2f}", border=1, ln=True, align="R")

        pdf.set_x(13)
        pdf.cell(90, 10, "Warranty", border=1)
        pdf.cell(90, 10, f"Rs {warranty:.2f}", border=1, ln=True, align="R")

        pdf.set_x(13)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(90, 10, "Total Price", border=1)
        pdf.cell(90, 10, f"Rs {total_price:.2f}", border=1, ln=True, align="R")

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, '', ln=True)
        
        pdf.cell(0, 10, 'Terms and Conditions:', ln=True)
        pdf.cell(0, 10, '', ln=True)
        
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 8, 
            '1. Above rates are inclusive of Applicable Taxes. Prices prevailing at the time of delivery will be APPLICABLE.\n'
            '2. DD/Cheque/Payorder should be drawn in favour of m/s Jeevan Auto Motor Pvt Ltd., payable at Madurai.\n'
            '3. Kindly bring a proof of Aadhar, Pan, Driving License, Ration smart card, and 3 passport size photos.\n'
            '4. Delivery only after realization of cheque.')

        pdf_output = pdf.output(dest='S').encode('latin-1')
        pdf_buffer = BytesIO(pdf_output)

        pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
        pdf_data_uri = f"data:application/pdf;base64,{pdf_base64}"

        st.download_button("📄 Download Quotation", data=pdf_buffer, file_name=f"{customer_name}_quotation.pdf", mime="application/pdf")
        st.subheader("📑 Preview Quotation")
        st.markdown(f'<iframe src="{pdf_data_uri}" width="700" height="500"></iframe>', unsafe_allow_html=True)


if __name__ == "__main__":
    app()      
