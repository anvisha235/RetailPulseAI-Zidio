import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Demand Forecasting", page_icon="📈", layout="wide")

st.title("📈 Demand Forecasting & What-If Analysis")
st.markdown("Review the demand forecasts (Hybrid, Prophet, LSTM, ARIMA, SARIMA) and simulate demand shifts.")

@st.cache_data
def load_forecast():
    try:
        # Load the week 2 hybrid forecast
        df = pd.read_csv('exports/week2_hybrid_forecast.csv')
        df['InvoiceDay'] = pd.to_datetime(df['InvoiceDay'])
        return df
    except Exception as e:
        st.error(f"Could not load forecast data. Error: {e}")
        return None

df = load_forecast()

if df is not None:
    st.sidebar.header("Model Selection")
    model_options = {
        "Hybrid Ensemble": "hybrid_forecast",
        "Prophet": "prophet_like_forecast",
        "LSTM": "lstm_like_forecast",
        "ARIMA": "arima_forecast",
        "SARIMA": "sarima_forecast"
    }
    # Ensure columns exist before displaying them, to prevent errors if the pipeline hasn't run yet
    available_options = {k: v for k, v in model_options.items() if v in df.columns}
    if not available_options:
        available_options = {"Hybrid Ensemble": "hybrid_forecast"} # Fallback
        
    selected_model = st.sidebar.selectbox("Choose Forecasting Model", options=list(available_options.keys()))
    forecast_col = available_options[selected_model]

    st.sidebar.header("What-If Analysis")
    st.sidebar.markdown("Use this slider to simulate an artificial shift in future demand (e.g. from marketing campaigns or market shocks).")
    demand_multiplier = st.sidebar.slider("Future Demand Adjustment (%)", min_value=-50, max_value=100, value=0, step=5)
    
    # Separate historical actuals vs future forecast
    # We'll assume rows where actual_revenue is NaN or 0 are future days
    historical = df[df['actual_revenue'] > 0].copy()
    future = df[df['actual_revenue'].isna() | (df['actual_revenue'] == 0)].copy()
    
    # If week2_pipeline.py just generated historical overlapping predictions, we will treat the last 30 days as 'future' for the simulation
    if future.empty:
        split_idx = int(len(df) * 0.9)
        historical = df.iloc[:split_idx].copy()
        future = df.iloc[split_idx:].copy()
        
    # Apply what-if multiplier to future forecast
    future['simulated_forecast'] = future[forecast_col] * (1 + (demand_multiplier / 100.0))
    
    st.subheader(f"{selected_model} Demand Forecast (Adjusted by {demand_multiplier}%)")
    
    # Plotly interactive chart
    fig = go.Figure()
    
    # Actuals
    fig.add_trace(go.Scatter(x=historical['InvoiceDay'], y=historical['actual_revenue'], 
                             mode='lines', name='Actual Revenue', line=dict(color='blue')))
                             
    # Original Forecast
    fig.add_trace(go.Scatter(x=future['InvoiceDay'], y=future[forecast_col], 
                             mode='lines', name='Baseline Forecast', line=dict(color='orange', dash='dash')))
                             
    # Simulated Forecast (Only if multiplier != 0)
    if demand_multiplier != 0:
        color = 'green' if demand_multiplier > 0 else 'red'
        fig.add_trace(go.Scatter(x=future['InvoiceDay'], y=future['simulated_forecast'], 
                                 mode='lines', name='Simulated Forecast', line=dict(color=color, dash='dot')))
                                 
    fig.update_layout(height=500, xaxis_title="Date", yaxis_title="Daily Revenue ($)",
                      hovermode="x unified", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Forecast Evaluation (MAPE)")
        st.metric(label="Mean Absolute Percentage Error", value=f"{df['mape'].iloc[-1]:.2%}")
        st.info("The model accuracy meets the Zidio business goal of MAPE <= 12% if well-tuned.")
        
    with col2:
        st.subheader("Data Export")
        export_df = pd.concat([historical, future])
        st.download_button(
            label="Download Adjusted Forecast CSV",
            data=export_df.to_csv(index=False).encode('utf-8'),
            file_name="adjusted_forecast.csv",
            mime="text/csv"
        )
