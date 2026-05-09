import streamlit as st
import pandas as pd
import os
from datetime import date
from streamlit_gsheets import GSheetsConnection
conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet="https://docs.google.com/spreadsheets/d/1-yvBDHwkA__r3lsY-yGEcxb1kWz608yzZkIVQuzch4o/edit?usp=drivesdk")
st.header("Record New Sale")

# --- FORM SECTION ---
st.header("📝 Manual Sales Entry")

# Use text_input instead of selectbox for manual typing
item = st.text_input("Product Sold (e.g., Watch, Laptop, Shoe)")
location = st.text_input("Branch/Location (e.g., Accra, Berekum, Sunyani)")

# Keep these as number inputs for math
price = st.number_input("Sale price (GHS)", min_value=0.0)
quantity = st.number_input("Quantity", min_value=1, step=1)
sale_date = st.date_input("Date of Sale", date.today())

  # Change line 31 to include a unique key just in case

if st.button("Submit sale", key="manual_entry"):
    if item and location:
        # 1. Create the new row
        new_row = pd.DataFrame([{ "Date": str(sale_date), "Item": item,  "Location": location, "Quantity": quantity,}])
           

        # 2. Get existing data, add new row, and save back to Sheets
        existing_data = conn.read(worksheet="Sheet1")
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)

        st.success("Sale synced to Google Sheets!")
        st.balloons()
        st.warning("Please enter both a Product and a Location!") 

    if os.path.exists("sales_history.csv"):
        history_df = pd.read_csv("sales_history.csv")
        
        # --- ANALYTICS SECTION ---
st.divider()
st.header("Sales Analytics")

# 1. Get the data
df_history = conn.read(worksheet="Sheet1")

# 2. Show metrics (Make sure these are NOT indented anymore)
col1, col2 = st.columns(2)
with col1:
    total_revenue = df_history['Total'].sum()
    st.metric("Total Revenue", f"GHS {total_revenue:,.2f}")
# ... and so on
    
    # 1. Show Key Metrics
    col1, col2 = st.columns(2)
    with col1:
        total_revenue = df_history['Total'].sum()
        st.metric("Total Revenue", f"GHS {total_revenue:,.2f}")
    with col2:
        total_qty = df_history['Quantity'].sum()
        st.metric("Total Items Sold", int(total_qty))

    # 2. Sales by Location Chart
    st.subheader("Sales by City")
    city_sales = df_history.groupby("Location")["Total"].sum()
    st.bar_chart(city_sales)
    
    # Check if we actually have data to show
if not df_history.empty:
    with st.expander("View Full Sales Log"):
        st.dataframe(df_history.sort_values(by="Date", ascending=False))
else:
    st.info("No sales history found yet. Submit a sale to see analytics!")
