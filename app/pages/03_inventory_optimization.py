import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inventory Optimization", page_icon="📦", layout="wide")

st.title("📦 Inventory Optimization Recommendations")
st.markdown("Review automated safety stock and reorder quantities driven by the hybrid demand forecast.")

@st.cache_data
def load_inventory():
    try:
        # Load the latest inventory recommendations
        # Try v2 first (from our Day 10 hybrid notebook), otherwise fallback to the pipeline generated one
        try:
            return pd.read_csv('exports/week2_inventory_recommendations_v2.csv')
        except:
            return pd.read_csv('exports/week2_inventory_recommendations.csv')
    except Exception as e:
        st.error("Could not load inventory recommendations. Ensure the Week 2 pipeline is complete.")
        return None

df = load_inventory()

if df is not None:
    # Handle both schema types (from pipeline or notebook)
    if 'StockCode' in df.columns:
        item_col = 'StockCode'
    else:
        # Fallback if specific columns aren't there
        item_col = df.columns[0]
        
    st.sidebar.header("Filter Inventory")
    
    # If priority column exists, allow filtering
    if 'priority' in df.columns:
        priorities = st.sidebar.multiselect("Select Priority Level:", 
                                         options=df['priority'].dropna().unique().tolist(),
                                         default=df['priority'].dropna().unique().tolist())
        filtered_df = df[df['priority'].isin(priorities)]
    else:
        # Filter by reorder quantity
        min_reorder = st.sidebar.slider("Minimum Reorder Quantity", 0, int(df['reorder_qty'].max()), 10)
        filtered_df = df[df['reorder_qty'] >= min_reorder]

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Top Items to Reorder")
        # Ensure we have the right columns
        plot_df = filtered_df.head(20).copy()
        
        # Determine columns to plot
        if 'Description' in plot_df.columns:
            plot_df['ItemName'] = plot_df['Description'].astype(str) + " (" + plot_df['StockCode'].astype(str) + ")"
        else:
            plot_df['ItemName'] = plot_df[item_col].astype(str)
            
        reorder_col = 'reorder_qty' if 'reorder_qty' in plot_df.columns else 'recommended_reorder_qty'
        
        fig = px.bar(plot_df, x='ItemName', y=reorder_col, 
                     title="Top 20 Recommended Reorder Quantities",
                     labels={reorder_col: 'Reorder Quantity', 'ItemName': 'Product'})
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("Inventory Metrics")
        st.metric(label="Total SKUs Analyzed", value=f"{len(df):,}")
        total_reorder = filtered_df[reorder_col].sum()
        st.metric(label="Total Units to Reorder (Filtered)", value=f"{total_reorder:,.0f}")
        
    st.divider()
    
    st.subheader("Detailed Reorder Table")
    st.dataframe(filtered_df, use_container_width=True)
