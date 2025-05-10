import streamlit as st

# Import all submodules
import bike_price_list
import bike_price_list_update
import branch
import quotation
import report
import sale_entry
import staff_name

def app(name=None):
    name=name
    st.write(f"Welcome {name}")
    # Optional: check if user is logged in
    if not st.session_state.get("logged_in"):
        st.warning("⛔ Please log in to access this page.")
        return

    # Sidebar navigation
    st.sidebar.title("🏍️ Jeevan Honda Menu")
    page = st.sidebar.selectbox("📄 Select Page", ["Generate Quotation","Report","Sale Entry"])

    # Page routing
    if page == "Add Bike Model":
        bike_price_list.app()
    elif page == "Price Change":
        bike_price_list_update.app()
    elif page == "Add Branch":
        branch.app()
    elif page == "Add Staff Name":
        staff_name.app()
    elif page == "Generate Quotation":
        quotation.app(name=name)
    elif page == "Report":
        report.app(name=name)
    elif page == "Sale Entry":
        sale_entry.app(name=name)
