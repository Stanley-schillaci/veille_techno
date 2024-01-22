import streamlit as st

from data.dataloader import get_sales_orders, get_dimension_filter
from utils.header import default_header
from utils.plot import plot_bar_chart, plot_scatter_chart, plot_line_chart, plot_pie_chart
from utils.stripped_dataframe import striped_dataframe

default_header('Sales Order', '📦')

company, country, city, billing_status, delivery_status = get_dimension_filter()

with st.sidebar:
    st.subheader('Filter')
    with st.expander('Dimensions', True):

        dimensions = [
            ('All Company', company, 'company_select_key_1'),
            ('All Country', country, 'country_select_key_1'),
            ('All City', city, 'city_select_key_1'),
            ('All Billing Status', billing_status, 'billing_status_select_key_1'),
            ('All Delivery Status', delivery_status, 'delivery_status_select_key_1'),
            
        ]
        
        for label, options, key in dimensions:
            st.multiselect(label, options, placeholder=label, label_visibility="collapsed", key=key)

sales_by_month, order_by_country, order_by_company = get_sales_orders()


st.markdown('## Order by Month')
tab1, tab2, tab3 = st.tabs(['Graph Amount', 'Graph Count', 'Table'])
with tab1:
    plot_bar_chart(sales_by_month, 'month', 'amount', 'Sales Order Amount', 'Date', 'Amount')
with tab2:
        plot_bar_chart(sales_by_month, 'month', 'nb_command', 'Sales Order Count', 'Date', 'Count')
with tab3:
    striped_dataframe(sales_by_month)

st.markdown('## Billing Information')
tab1, tab2 = st.tabs(['Graph Amount', 'Graph Status'])
with tab1:
    plot_line_chart(sales_by_month, 'month', ['billing_amount', 'missing_amount'], 'Billing Amount', 'Date', 'Amount')
with tab2:
    plot_line_chart(sales_by_month, 'month', ['nb_command', 'nb_non_billing', 'nb_non_delivery'], 'Order Status', 'Date', 'Count')


st.markdown('## Top Country & Company')
col1, col2 = st.columns(2)
with col1:
    plot_pie_chart(order_by_country, 'country', 'nb_command', 'Order by Country')
with col2:
    plot_pie_chart(order_by_company, 'company_name', 'nb_command', 'Order by Company')
    




