import streamlit as st
import pymongo
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import base64
from datetime import date, datetime

def app(name=None, add=None):
    namee = name

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

    # Title and Date
    st.title("🏍️ Bike Quotation Generator")
    st.markdown(f"**Date:** {current_date.strftime('%B %d, %Y')}")

    # Form for input
    with st.form("quotation_form"):
        st.subheader("🔹 Customer Details")
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name:", placeholder="Enter full name")
            phone_number = st.text_input("Phone Number:", placeholder="10-digit mobile number")
        with col2:
            address = st.text_area("Address:", placeholder="Enter complete address")

        st.subheader("🔹 Bike and Sales Info")
        col3, col4 = st.columns(2)
        with col3:
            
           
            # Selectbox that triggers rerun
            
            selected_bike = st.selectbox("Select Bike Model:", df_bike["Bike_Model"].unique())
            selected_pay_mod = st.selectbox("Select Payment Method:", ["Cash", "Finance"])
           

           

        

            
                
        
            
        with col4:
            if namee is None:
                selected_staff = st.selectbox("Salesperson:", df_staff["Sales_Person"].unique())
                
            else:
                selected_staff = st.selectbox("Salesperson:", namee)
            Fin_name=st.text_input("Enter the Finance Name:")
            
            
                

            


        submitted = st.form_submit_button("Generate Quotation")

    if submitted:
        if not phone_number or len(phone_number) != 10 or not phone_number.isdigit():
            st.error("Please enter a valid 10-digit phone number.")
            return
        else:
            st.success("Valid phone number entered.")

        selected_staff_phone = df_staff[df_staff["Sales_Person"] == selected_staff]["Phone_Number"].iloc[0]
        df_cust = pd.DataFrame(list(cust.find({}, {"_id": 0})))
        bike_row = df_bike[df_bike["Bike_Model"] == selected_bike].iloc[0]

        # Price breakdown
        ex_showroom = float(bike_row.get("Ex_showroom", 0))
        insurance = float(bike_row.get("Insurance", 0))
        registration = float(bike_row.get("Road_tax", 0))
        warranty = float(bike_row.get("Warranty", 0))
        sub=insurance+registration
        sub_tot=ex_showroom+sub+warranty
        accessories = float(bike_row.get("Fitting", 0))
       
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
                "Sales_person": selected_staff,
                "Payment_method":selected_pay_mod,
                "Finance_Name":Fin_name
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
                cust.update_one({"Phone_no": phone_number}, {"$set": {
                    "Customer_name": customer_name,
                    "Bike_Model": selected_bike,
                    "Address": address,
                    "Status": "Not Sale",
                    "Quotation_Date": datetime.combine(current_date, datetime.min.time()),
                    "Sales_person": selected_staff,
                    "Payment_method":selected_pay_mod,
                    "Finance_Name":Fin_name
                }})
                st.success("📅 New quotation inserted (more than 30 days old).")
            else:
                existing_bike_model = customer_record["Bike_Model"].iloc[0]
                bike_models = [model.strip() for model in existing_bike_model.split(",")]
                if selected_bike not in bike_models:
                    updated_bikes = ", ".join(bike_models + [selected_bike])
                else:
                    updated_bikes = existing_bike_model

                cust.update_one({"Phone_no": phone_number}, {"$set": {
                    "Customer_name": customer_name,
                    "Bike_Model": updated_bikes,
                    "Address": address,
                    "Status": "Not Sale",
                    "Quotation_Date": datetime.combine(current_date, datetime.min.time()),
                    "Payment_method":selected_pay_mod,
                    "Finance_Name":Fin_name
                }})
                st.info("ℹ️ Customer detail has been updated successfully.")

        class PDF(FPDF):
            def header(self):
                self.image("images.png", 10, 8, 33)
                self.set_font('Arial', 'B', 18)
                self.cell(0, 9, '', ln=True, align='C')
                self.cell(0, 10, 'Jeevan Auto Motor Pvt Ltd', ln=True, align='C')
                self.set_font('Arial', 'B', 12)
                if add == "kmr":
                    self.cell(0, 5, '109, Kamarajar Salai,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625009.', ln=True, align='C')
                elif add == "tnr":
                    self.cell(0, 5, '74, GST Road, Tiruparankundram,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625006.', ln=True, align='C')
                elif add == "nmp":
                    self.cell(0, 5, '74, Theni Main Road, Nagamalai Pudukottai,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625019.', ln=True, align='C')
                elif add == "tmg":
                    self.cell(0, 5, '304, Virudhunagar Road, Thirumangalam,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625706.', ln=True, align='C')
                elif add == "klk":
                    self.cell(0, 5, '6/544G, T.Kallupatti Road, Kalligudi,', ln=True, align='C')
                    self.cell(0, 5, 'Madurai - 625706.', ln=True, align='C')
                else:
                    self.cell(0, 5, '144/1, Tirupparankunram Rd,', ln=True, align='C')
                    self.cell(0, 5, 'Palangantham, Madurai - 625003.', ln=True, align='C')
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
                self.multi_cell(0, 5,
                    "   For NEFT/RTGS/BANK TRANSFERS       | Name: Jeevan Auto Motor Pvt Ltd,\n"
                    "   Bank: HDFC BANK LTD                             | Branch: ANDALPURAM\n"
                    "   A/C No: 50200083068012                          | IFSC Code: HDFC0003734"
                )
                self.set_xy(x + 2, y + h - 6)
                self.set_font("Arial", 'I', 15)
                self.cell(0, 5, "Note: Please bring this copy next time you visit our showroom", ln=True, align="C")

        pdf = PDF()
        pdf.add_page()

        # Set font for the initial part of the document
        pdf.set_font("Arial", size=12)
        pdf.cell(100, 10, f"Customer Name: {customer_name}", ln=False)
        pdf.cell(0, 10, f"Phone Number: {phone_number}", ln=True, align="R")
        pdf.multi_cell(0, 10, f"Address: {address}")
        pdf.cell(100, 10, f"Sales Person: {selected_staff}", ln=False)
        pdf.cell(0, 10, f"Phone: {selected_staff_phone}", ln=True, align="R")

        pdf.ln(10)

        # Set the font for the heading
        pdf.set_font("Arial", 'B', 20)
        pdf.cell(0, 10, "Proforma Invoice", ln=True, align="C")
        pdf.cell(0, 10, f"Bike Model: {selected_bike}", ln=True, align="C")

        # Set the font for the price details section
        pdf.set_font("Arial", '', 12)

        # Ex-Showroom Price
        pdf.set_x(13)
        pdf.cell(90, 10, "Ex-Showroom Price", border=1)
        pdf.cell(90, 10, f"Rs {ex_showroom:.2f}", border=1, ln=True, align="R")

        # Insurance + Registration
        pdf.set_x(13)
        pdf.set_font("Arial", '', 10)
        pdf.cell(90, 10, "Insurance(1year od +4year Third Party) + Registration", border=1)
        pdf.set_font("Arial", '', 12)
        pdf.set_x(103)  # Position the right side for the amount
        pdf.cell(90, 10, f"Rs {sub:.2f}", border=1, ln=True, align="R")
        
         # Warranty
        pdf.set_x(13)
        pdf.cell(90, 10, "Warranty", border=1)
        pdf.cell(90, 10, f"Rs {warranty:.2f}", border=1, ln=True, align="R")

        # Sub Total
        pdf.set_x(13)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(90, 10, "Sub Total", border=1)
        pdf.cell(90, 10, f"Rs {sub_tot:.2f}", border=1, ln=True, align="R")

        # Accessories
        pdf.set_x(13)
        pdf.set_font("Arial", '', 12)
        pdf.cell(90, 10, "Accessories", border=1)
        pdf.cell(90, 10, f"Rs {accessories:.2f}", border=1, ln=True, align="R")

       

        # Total Price
        pdf.set_x(13)
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(90, 10, "Total Price", border=1)
        pdf.cell(90, 10, f"Rs {total_price:.2f}", border=1, ln=True, align="R")

        pdf.ln(10)

        # Terms and Conditions Section
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, 'Terms and Conditions:', ln=True)

        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 8,
            '1. Above rates are inclusive of Applicable Taxes. Prices prevailing at the time of delivery will be APPLICABLE.\n'
            '2. DD/Cheque/Payorder should be drawn in favour of M/s Jeevan Auto Motor Pvt Ltd., payable at Madurai.\n'
            '3. Kindly bring proof of Aadhar, PAN, DL, Ration card, and 3 passport size photos.\n'
            '4. Delivery only after realization of Cheque/DD.')

        pdf_output = pdf.output(dest='S').encode('latin-1')
        pdf_buffer = BytesIO(pdf_output)

        st.download_button("📄 Download Quotation", data=pdf_buffer, file_name=f"{customer_name}_quotation.pdf", mime="application/pdf")
        st.subheader("📑 Preview Quotation")
        st.markdown(f'<iframe src="data:application/pdf;base64,{base64.b64encode(pdf_buffer.getvalue()).decode()}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)


if __name__ == "__main__":
    app()      
