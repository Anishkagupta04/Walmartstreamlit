import streamlit as st
import pandas as pd


# Load the product data from a CSV file
@st.cache_data
def load_data():
    # Example CSV with 'Product', 'Brand', 'Category', 'Recommendations', 'Past Purchases' columns
    data = pd.read_csv('Untitled spreadsheet - Sheet1.csv')
    return data


# Function to filter products based on user input
def filter_products(product_list, data):
    filtered_data = data[data['Category'].str.lower().isin([p.lower() for p in product_list])]
    return filtered_data


# Function to get the most recommended and past purchased items
def get_top_recommended(data):
    top_recommended = data.sort_values(by='Recommendations', ascending=False).iloc[0]
    past_purchases = data[data['Past Purchases'] > 0]
    return top_recommended, past_purchases


# Streamlit app
def main():
    st.title("Walmart Grocery Product Recommendation System")

    # Load data
    data = load_data()

    # User input for list of products
    product_input = st.text_input("Enter the list of products separated by commas (e.g., salt, milk, butter, bread):")
    product_list = [item.strip() for item in product_input.split(',')]
#
    if st.button("Get Recommendations"):
        if product_list:
            filtered_data = filter_products(product_list, data)

            if not filtered_data.empty:
                st.header("Filtered Products:")

                for product in product_list:
                    st.subheader(f"{product.capitalize()} Brands:")
                    product_data = filtered_data[filtered_data['Category'].str.lower() == product.lower()]
                    st.table(product_data[['Brand', 'Recommendations']])

                # Get top recommended and past purchased items
                top_recommended, past_purchases = get_top_recommended(filtered_data)

                st.header("Top Recommended Product:")
                st.success(
                    f"{top_recommended['Brand']} ({top_recommended['Category']}) - {top_recommended['Recommendations']} Recommendations")

                if not past_purchases.empty:
                    st.header("Past Purchased Items:")
                    st.table(past_purchases[['Brand', 'Category', 'Past Purchases']])
                else:
                    st.info("No past purchases found for these products.")
            else:
                st.error("No matching products found.")
        else:
            st.warning("Please enter at least one product.")


if __name__ == "__main__":
    main()
# import streamlit as st
# import pandas as pd
#
#
# # Simulate a product database
# @st.cache_data
# def load_product_data():
#     data = {
#         'Product': ['Milk', 'Bread', 'Butter', 'Eggs', 'Salt'],
#         'Price': [1.99, 2.49, 3.49, 1.89, 0.99],
#         'In_Stock': [True, True, False, True, True],
#         'On_Sale': [False, True, False, False, True]
#     }
#     return pd.DataFrame(data)
#
#
# # Initialize session state
# if 'alerts' not in st.session_state:
#     st.session_state.alerts = []
#
#
# # Function to register an alert
# def register_alert(product, alert_type):
#     st.session_state.alerts.append({
#         'Product': product,
#         'Alert_Type': alert_type
#     })
#     st.success(f"Alert set for {product} on {alert_type}")
#
#
# # Function to check for alerts
# def check_alerts(data):
#     triggered_alerts = []
#     for alert in st.session_state.alerts:
#         product_info = data[data['Product'] == alert['Product']].iloc[0]
#         if alert['Alert_Type'] == 'Sale' and product_info['On_Sale']:
#             triggered_alerts.append(f"{alert['Product']} is now on sale!")
#         elif alert['Alert_Type'] == 'Stock' and product_info['In_Stock']:
#             triggered_alerts.append(f"{alert['Product']} is back in stock!")
#         elif alert['Alert_Type'] == 'Price Drop' and product_info['Price'] < 2.00:
#             triggered_alerts.append(f"{alert['Product']} has dropped in price!")
#     return triggered_alerts
#
#
# # Streamlit app
# def main():
#     st.title("Walmart Product Alerts")
#
#     # Load product data
#     product_data = load_product_data()
#
#     # User input for alert setup
#     st.subheader("Set Up Alerts")
#     product = st.selectbox("Select Product", product_data['Product'])
#     alert_type = st.radio("Alert Type", ('Sale', 'Stock', 'Price Drop'))
#
#     if st.button("Set Alert"):
#         register_alert(product, alert_type)
#
#     # Display existing alerts
#     if st.session_state.alerts:
#         st.subheader("Your Alerts")
#         st.write(st.session_state.alerts)
#
#         # Check for triggered alerts
#         triggered_alerts = check_alerts(product_data)
#         if triggered_alerts:
#             st.subheader("Triggered Alerts")
#             for alert in triggered_alerts:
#                 st.warning(alert)
#         else:
#             st.info("No alerts triggered yet.")
#
#     # Simulate email notifications
#     st.subheader("Email Notifications")
#     email = st.text_input("Enter your email to receive notifications (Simulation)")
#     if st.button("Simulate Email Notification"):
#         if email:
#             st.success(f"Email notification sent to {email} (simulated).")
#         else:
#             st.error("Please enter a valid email address.")
#
#
# if __name__ == "__main__":
#     main()
