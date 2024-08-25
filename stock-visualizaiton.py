import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import date, timedelta
import pandas as pd

def get_sp500_performance(start_date, end_date):
    sp500 = yf.Ticker("^GSPC")
    sp500_data = sp500.history(start=start_date, end=end_date)
    return sp500_data['Close']

def main():
    st.title('U.S. Stock Visualization App')
    
    # Display developer name in smaller font size
    st.markdown('<small>Developed by: <a href="https://www.linkedin.com/in/miyoko-shimura/" target="_blank">Miyoko Shimura</a></small>', unsafe_allow_html=True)

    # User input
    stock_symbol = st.text_input('Enter a ticker symbol (e.g., AAPL for Apple, NVDA for NVIDIA):', 'AAPL')
    
    # Date range selection
    start_date = st.date_input('Start date:', date.today() - timedelta(days=365))
    end_date = st.date_input('End date:', date.today())

    # S&P 500 comparison option
    compare_sp500 = st.checkbox('Compare with S&P 500')

    if st.button('Show Stock Price'):
        # Fetch data
        df = yf.download(stock_symbol, start=start_date, end=end_date)

        if df.empty:
            st.error('Unable to fetch data. Please check the ticker symbol.')
        else:
            # Create graph
            fig = go.Figure()
            fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name=stock_symbol))

            if compare_sp500:
                sp500_data = get_sp500_performance(start_date, end_date)
                fig.add_trace(go.Scatter(x=sp500_data.index, y=sp500_data, name='S&P 500', line=dict(color='red')))

            fig.update_layout(
                title=f'Stock Price Chart for {stock_symbol}',
                yaxis_title='Price (USD)',
                xaxis_title='Date'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Summary
            summary_data = {
                'Metric': ['Highest Price', 'Lowest Price', 'Average Closing Price'],
                'Value': [
                    f"${df['High'].max():.2f}",
                    f"${df['Low'].min():.2f}",
                    f"${df['Close'].mean():.2f}"
                ]
            }

            st.subheader('Summary')
            st.table(pd.DataFrame(summary_data).set_index('Metric'))

            # Performance and Comparison with S&P 500
            stock_return = (df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0] * 100
            
            st.subheader('Comparison with S&P 500')
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label=f"Total Return ({stock_symbol})", value=f"{stock_return:.2f}%")

            if compare_sp500:
                sp500_return = (sp500_data.iloc[-1] - sp500_data.iloc[0]) / sp500_data.iloc[0] * 100
                relative_performance = stock_return - sp500_return

                with col2:
                    st.metric(label="S&P 500 Return", value=f"{sp500_return:.2f}%")
                with col3:
                    delta_color = "normal"
                    if relative_performance < 0:
                        delta_color = "inverse"
                    elif relative_performance > 0:
                        delta_color = "normal"
                    st.metric(label="Relative Performance", value=f"{relative_performance:.2f}%", delta=f"{relative_performance:.2f}%", delta_color=delta_color)
            else:
                st.write("Enable 'Compare with S&P 500' to see more metrics")

if __name__ == "__main__":
    main()
