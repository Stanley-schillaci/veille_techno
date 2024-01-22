import streamlit as st

from utils.header import default_header
from data.dataloader import get_product_dashboard, get_dimension_filter_product
from utils.plot import plot_bar_chart, plot_pie_chart
from utils.stripped_dataframe import striped_dataframe

default_header('Products Dashboard', '📊')

product_name, product_category, company, billing_status, delivery_status = get_dimension_filter_product()

with st.sidebar:
    st.subheader('Filter')
    with st.expander('Dimensions', True):

        dimensions = [
            ('All Product Name', product_name, 'product_name_select_key_2'),
            ('All Product Category', product_category, 'product_category_select_key_2'),
            ('All Company', company, 'company_select_key_2'),
            ('All Billing Status', billing_status, 'billing_status_select_key_2'),
            ('All Delivery Status', delivery_status, 'delivery_status_select_key_2'),
        ]
        
        for label, options, key in dimensions:
            st.multiselect(label, options, placeholder=label, label_visibility="collapsed", key=key)


product_total, product_by_category, product_by_company = get_product_dashboard()

st.markdown('## Product Sales')
tab1, tab2 = st.tabs(['Graph', 'Table'])
with tab1:
    plot_bar_chart(product_total, 'product_name', 'quantity_sales', 'Total Product', 'Product', 'Total')
with tab2:
    striped_dataframe(product_total)

st.markdown('## Product Sales by Category & Company')
col1, col2 = st.columns(2)
with col1:
    plot_pie_chart(product_by_category, 'category_description', 'quantity_sales', 'Product by Category')
with col2:
    plot_pie_chart(product_by_company, 'company_name', 'quantity_sales', 'Product by Company')




