import streamlit as st
import pymongo
import pandas as pd
from fpdf import FPDF
from io import BytesIO
import base64

# MongoDB connection
conn = pymongo.MongoClient("mongodb://jeevanhonda:Vignesh_3@ac-s8itqus-shard-00-00.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-01.ogrtcr1.mongodb.net:27017,ac-s8itqus-shard-00-02.ogrtcr1.mongodb.net:27017/?ssl=true&replicaSet=atlas-iwwj88-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
conn_obj = conn["jeevan"]

# Load data from MongoDB
staff_name = conn_obj["staff_name"]
bike = conn_obj["bike_price"]

df_staff = pd.DataFrame(list(staff_name.find({}, {"_id": 0})))
df_bike = pd.DataFrame(list(bike.find({}, {"_id": 0})))

# Streamlit form
st.title("Bike Quotation Generator")

customer_name = st.text_input("Customer Name:")
address=st.text_area("Enter The Address :")
phone_number = st.text_input("Phone Number:")
selected_bike = st.selectbox("Select Bike Model:", df_bike["Bike_Model"].unique())
selected_staff = st.selectbox("Salesperson:", df_staff["Sales_Person"].unique())
selected_staff_phone=df_staff[df_staff["Sales_Person"]==selected_staff]["Phone_Number"][0]
def pdf_to_base64(pdf_buffer):
    """
    Convert the PDF buffer to a base64 encoded string.
    """
    pdf_base64 = base64.b64encode(pdf_buffer.getvalue()).decode('utf-8')
    return pdf_base64

if st.button("Generate Quotation"):
    # Get bike price
    bike_row = df_bike[df_bike["Bike_Model"] == selected_bike].iloc[0]
    ex_showroom = float(bike_row.get("Ex_showroom", 0))
    insurance = float(bike_row.get("Insurance", 0))
    registration = float(bike_row.get("Road_tax", 0))
    accessories = float(bike_row.get("Fitting", 0))
    waranty=float(bike_row.get("Warranty",0))
    total_price = ex_showroom + insurance + registration + accessories+waranty

    # PDF generation
    class PDF(FPDF):
        def header(self):
            logo_path_left = r"G:\jeevan\images.png"  # Update the path to your logo file (Left)
            logo_path_right = r"G:\jeevan\images.png"  # Update the path to your logo file (Right)
            
            # Left logo
            self.image(logo_path_left, 10, 8, 33)  # Position and size of the left logo (x, y, width)
            
            # Right logo
            self.image(logo_path_right, 170, 8, 33)  # Position and size of the right logo (x, y, width)
            
            # Title and address
            self.set_font('Arial', 'B', 18)
            self.cell(0, 9, '', ln=True, align='C')
            self.cell(0, 10, 'Jeevan Auto Moto Pvt Ltd', ln=True, align='C')
            self.set_font('Arial', 'B', 12)
            self.cell(0, 5, '144/1, Tirupparankunram Rd,', ln=True, align='C')
            self.cell(0, 5, ' Palangantham,Madurai - 625003.', ln=True, align='C')
            self.cell(0, 5, '', ln=True, align='C')
            self.set_font('Arial', 'B', 16)

        def footer(self):
            self.set_y(-20)
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, 'This is a system-generated quotation.', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_font("Arial", size=12)

    # Customer Name and Phone Number (Left-aligned)
    pdf.cell(100, 10, f"Customer Name: {customer_name}", ln=False)  # 100 units for the left part
    pdf.cell(0, 10, f"       Phone Number: {phone_number}", ln=True)  # Right-aligned automatically

    # Salesperson and Salesperson Phone Number (Right-aligned)
    
    pdf.cell(0, 10, f"Address : {address}", ln=True,align="J")
    pdf.cell(100, 10, f"Sales Person : {selected_staff}", ln=False)  # 100 units for the left part
    pdf.cell(0, 10, f"Sales Person Phone Number: {selected_staff_phone}", ln=True, align="R")  # Right-aligned

        
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, "", ln=True, align="C")
    pdf.cell(0, 10, "", ln=True, align="C")
    pdf.cell(0, 10, "Quotation Details", ln=True, align="C")
    pdf.cell(0, 10, f"Bike Model: {selected_bike}", ln=True,align="C")
    
    pdf.set_x(35)  # Center the table horizontally
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(70, 10, "Ex-Showroom Price", border=1, align="L")
    pdf.cell(70, 10, f"Rs {ex_showroom:.2f}", border=1, ln=True, align="C")

    pdf.set_x(35)
    pdf.cell(70, 10, "Insurance", border=1, align="L")
    pdf.cell(70, 10, f"Rs   {insurance:.2f}", border=1, ln=True, align="C")

    pdf.set_x(35)
    pdf.cell(70, 10, "Registration Charges", border=1, align="L")
    pdf.cell(70, 10, f"Rs {registration:.2f}", border=1, ln=True, align="C")

    pdf.set_x(35)
    pdf.cell(70, 10, "Accessories", border=1, align="L")
    pdf.cell(70, 10, f"Rs  {accessories:.2f}", border=1, ln=True, align="C")

    pdf.set_x(35)
    pdf.cell(70, 10, "Warranty", border=1, align="L")
    pdf.cell(70, 10, f"Rs    {waranty:.2f}", border=1, ln=True, align="C")

    pdf.set_x(35)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(70, 10, "Total Price", border=1, align="L")
    pdf.cell(70, 10, f"Rs {total_price:.2f}", border=1, ln=True, align="C")


    # Output to BytesIO for preview and download
    pdf_output = pdf.output(dest='S').encode('latin-1')
    pdf_buffer = BytesIO(pdf_output)

    # Convert PDF to Base64
    pdf_base64 = pdf_to_base64(pdf_buffer)

    # Create data URI for the PDF (for embedding in iframe)
    pdf_data_uri = f"data:application/pdf;base64,{pdf_base64}"

    # Streamlit download button for the PDF
    st.download_button("Download Quotation", data=pdf_buffer, file_name=f"{customer_name}_quotation.pdf", mime="application/pdf")

    # Optional preview inside Streamlit (can show PDF inline using iframe)
    st.subheader("Preview Quotation")
    st.markdown(f'<iframe src="{pdf_data_uri}" width="700" height="500"></iframe>', unsafe_allow_html=True)
