import streamlit as st
import pandas as pd


# Simulate a product database
@st.cache_data
def load_product_data():
    data = {
        'Product': ['Milk', 'Bread', 'Butter', 'Eggs', 'Salt'],
        'Price': [1.99, 2.49, 3.49, 1.89, 0.99],
        'In_Stock': [True, True, False, True, True],
        'On_Sale': [False, True, False, False, True]
    }
    return pd.DataFrame(data)


# Initialize session state
if 'alerts' not in st.session_state:
    st.session_state.alerts = []


# Function to register an alert
def register_alert(product, alert_type):
    st.session_state.alerts.append({
        'Product': product,
        'Alert_Type': alert_type
    })
    st.success(f"Alert set for {product} on {alert_type}")


# Function to check for alerts
def check_alerts(data):
    triggered_alerts = []
    for alert in st.session_state.alerts:
        product_info = data[data['Product'] == alert['Product']].iloc[0]
        if alert['Alert_Type'] == 'Sale' and product_info['On_Sale']:
            triggered_alerts.append(f"{alert['Product']} is now on sale!")
        elif alert['Alert_Type'] == 'Stock' and product_info['In_Stock']:
            triggered_alerts.append(f"{alert['Product']} is back in stock!")
        elif alert['Alert_Type'] == 'Price Drop' and product_info['Price'] < 2.00:
            triggered_alerts.append(f"{alert['Product']} has dropped in price!")
    return triggered_alerts


# Streamlit app
def main():
    st.title("Walmart Product Alerts")

    # Load product data
    product_data = load_product_data()

    # User input for alert setup
    st.subheader("Set Up Alerts")
    product = st.selectbox("Select Product", product_data['Product'])
    alert_type = st.radio("Alert Type", ('Sale', 'Stock', 'Price Drop'))

    if st.button("Set Alert"):
        register_alert(product, alert_type)

    # Display existing alerts
    if st.session_state.alerts:
        st.subheader("Your Alerts")
        st.write(st.session_state.alerts)

        # Check for triggered alerts
        triggered_alerts = check_alerts(product_data)
        if triggered_alerts:
            st.subheader("Triggered Alerts")
            for alert in triggered_alerts:
                st.warning(alert)
        else:
            st.info("No alerts triggered yet.")

    # Simulate email notifications
    st.subheader("Email Notifications")
    email = st.text_input("Enter your email to receive notifications (Simulation)")
    if st.button("Simulate Email Notification"):
        if email:
            st.success(f"Email notification sent to {email} (simulated).")
        else:
            st.error("Please enter a valid email address.")


if __name__ == "__main__":
    main()
