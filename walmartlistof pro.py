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
