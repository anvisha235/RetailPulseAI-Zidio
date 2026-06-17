import streamlit as st
import pandas as pd
import os
import zipfile
import io

st.set_page_config(page_title="Alerts & Exports", page_icon="🚨", layout="wide")

st.title("🚨 Real-Time Alerts & Exports")
st.markdown("Monitor system drift, review automated alerts, and generate consolidated reports.")

# --- Alerts Section (Day 19) ---
st.header("Active System Alerts")

def check_drift():
    try:
        df = pd.read_csv('exports/week2_drift_checks.csv')
        drift_count = df['drift_flag'].sum()
        return df, drift_count
    except:
        return None, 0

drift_df, drift_count = check_drift()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Drift Status")
    if drift_count > 0:
        st.error(f"⚠️ {drift_count} Features are exhibiting statistical drift!")
        st.dataframe(drift_df[drift_df['drift_flag'] == True])
    else:
        st.success("✅ No significant data drift detected in the current data batch.")

with col2:
    st.subheader("Inventory Stockout Risk")
    try:
        inv = pd.read_csv('exports/week2_inventory_recommendations_v2.csv')
        # Simulate a check: if reorder qty is very high compared to safety stock, it's a risk
        critical = inv[inv['reorder_qty'] > (inv['safety_stock'] * 3)]
        if not critical.empty:
            st.warning(f"⚠️ {len(critical)} SKUs are facing potential stockouts due to recent demand spikes.")
            st.dataframe(critical.head(5)[['StockCode', 'Quantity', 'reorder_qty']])
        else:
            st.success("✅ All SKUs are within safe reorder margins.")
    except:
        st.info("Inventory data not fully loaded.")

st.divider()

# --- Export Section (Day 20) ---
st.header("Report Generation (Exports)")
st.markdown("Download consolidated CSV reports for external stakeholders.")

# Function to zip files
def create_zip():
    files_to_zip = [
        'exports/week2_hybrid_forecast.csv',
        'exports/week2_churn_predictions.csv',
        'exports/week2_inventory_recommendations_v2.csv'
    ]
    
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in files_to_zip:
            if os.path.exists(file_path):
                # Add file to zip with just the filename, not the full path
                zip_file.write(file_path, os.path.basename(file_path))
    
    return zip_buffer.getvalue()

col3, col4 = st.columns(2)

with col3:
    st.info("The Master Report includes Demand Forecasts, Churn Predictions, and Inventory Recommendations in a single ZIP file.")
    zip_data = create_zip()
    
    st.download_button(
        label="📥 Download Master Report (ZIP)",
        data=zip_data,
        file_name="RetailPulse_Executive_Report.zip",
        mime="application/zip",
        type="primary"
    )

with col4:
    st.write("Or download individual components:")
    try:
        churn_data = pd.read_csv('exports/week2_churn_predictions.csv').to_csv(index=False).encode('utf-8')
        st.download_button("Download Churn List (CSV)", data=churn_data, file_name="churn_list.csv", mime="text/csv")
        
        inv_data = pd.read_csv('exports/week2_inventory_recommendations_v2.csv').to_csv(index=False).encode('utf-8')
        st.download_button("Download Inventory List (CSV)", data=inv_data, file_name="inventory_list.csv", mime="text/csv")
    except Exception as e:
        st.write("Ensure all pipelines are run to enable individual downloads.")
