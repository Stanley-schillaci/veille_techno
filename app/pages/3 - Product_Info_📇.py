import streamlit as st

from utils.header import default_header
from data.dataloader import get_product_info, get_dimension_filter_product
from utils.plot import plot_bar_chart, plot_pie_chart
from utils.stripped_dataframe import striped_dataframe

default_header('Products Info', '📇')
product_name, _, _, _, _ = get_dimension_filter_product()

with st.sidebar:
    st.subheader('Filter')
    with st.expander('Dimensions', True):

        dimensions = [
            ('All Product Name', product_name, 'product_name_select_key_3')
        ]
        
        for label, options, key in dimensions:
            st.selectbox(label, options, placeholder=label, label_visibility="collapsed", key=key)

product_info, product_sales_by_month, product_sales = get_product_info()

st.title(product_info['product_name'][0])

col1, col2 = st.columns(2)
with col1:
    st.markdown('#### Product Description' + '\n' + product_info['product_description'][0])
with col2:
    st.markdown('#### Product Category' + '\n' + product_info['category_description'][0])

col1, col2 = st.columns(2)
with col1:
    st.markdown('#### Product Price' + '\n' + str(product_info['price'][0]) + ' ' + product_info['currency'][0])
with col2:
    st.markdown('#### Product Weight' + '\n' + str(product_info['weight_measure'][0]) + ' ' + product_info['weight_unit'][0])

tab1, tab2, tab3 = st.tabs(['Product Sales Quantity', 'Product Sales Amount', 'Details Table'])
with tab1:
    plot_bar_chart(product_sales_by_month, 'month', 'quantity_sales', 'Product Sales', 'Month', 'Quantity')
with tab2:
    plot_bar_chart(product_sales_by_month, 'month', 'amount', 'Product Sales', 'Month', 'Amount')
with tab3:
    striped_dataframe(product_sales_by_month)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'#### Product Sales Amount : ${product_sales["amount"][0]:,.0f}')
    st.markdown(f'#### Product Billing Amount : ${product_sales["billing_amount"][0]:,.0f}')
    st.markdown(f'#### Product Missing Amount : ${product_sales["missing_amount"][0]:,.0f}')

with col2:    
    st.markdown('#### Product Sales Quantity : ' + str(product_sales['quantity_sales'][0]))
    st.markdown('#### Delivery unfinished : ' + str(product_sales['nb_non_delivery'][0]))
    st.markdown('#### Missing Billing : ' + str(product_sales['nb_non_billing'][0]))