from google.cloud import bigquery
import pandas as pd
import streamlit as st

client = bigquery.Client(project='bike-shop-408414')

def execute_query(sql_query):
    """
    Exécute une requête SQL sur BigQuery et retourne les résultats dans un DataFrame pandas.

    Args:
    sql_query (str): La requête SQL à exécuter.

    Returns:
    pandas.DataFrame: Les résultats de la requête.
    """
    try:
        query_job = client.query(sql_query)
        return query_job.to_dataframe()
    except Exception as e:
        print(f"Erreur lors de l'exécution de la requête: {e}")
        return None

def build_where_clause(filters):    
    conditions = []
    for column, values in filters.items():
        if values not in st.session_state: 
            st.session_state[values] = []
        if values:
            condition = " OR ".join([f"{column} = '{value}'" for value in values])
            conditions.append(f"({condition})")

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
        return where_clause
    else:
        return ""

def get_dimension_filter():
    company = execute_query("""
        select distinct
             company_name as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
    """)

    country = execute_query("""
        select distinct
             country as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
    """)

    city = execute_query("""
        select distinct
                city as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
    """)

    billing_status = execute_query("""
        select distinct
                billing_status as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
    """)

    delivery_status = execute_query("""
        select distinct
                delivery_status as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
    """)

    return company['dimension'], country['dimension'], city['dimension'], billing_status['dimension'], delivery_status['dimension']

def get_dimension_filter_product():
    product_name = execute_query("""
        select distinct
                product_name as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
    """)

    product_category = execute_query("""
        select distinct
                category_description as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
    """)

    company = execute_query("""
        select distinct
                company_name as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
    """)

    billing_status = execute_query("""
        select distinct
                billing_status as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
    """)

    delivery_status = execute_query("""
        select distinct
                delivery_status as dimension,
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
    """)

    return product_name['dimension'], product_category['dimension'], company['dimension'], billing_status['dimension'], delivery_status['dimension']
    
def get_sales_orders():

    filters = {
        'company_name': st.session_state.get('company_select_key_1', []),
        'country': st.session_state.get('country_select_key_1', []),
        'city': st.session_state.get('city_select_key_1', []),
        'billing_status': st.session_state.get('billing_status_select_key_1', []),
        'delivery_status': st.session_state.get('delivery_status_select_key_1', []),
    }
    where_clause = build_where_clause(filters)
    
    sales_by_month = execute_query(f"""                              
        SELECT 
            date_trunc(sales_order_date, MONTH) as month,
            sum(order_gross_amount) as amount,
            count(*) as nb_command,
            sum(case when delivery_status != 'Completed' then 1 else 0 end) as nb_non_delivery,
            sum(case when billing_status != 'Completed' then 1 else 0 end) as nb_non_billing,
            sum(billing_gross_amount) as billing_amount,
            sum(order_gross_amount) - sum(billing_gross_amount) as missing_amount
        FROM DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
        {where_clause}
            group by month
    """)

    order_by_country = execute_query(f"""
        select
            country,
            count(*) as nb_command
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
        {where_clause}
            group by country
            order by nb_command desc
            limit 10
    """)

    order_by_company = execute_query(f"""
        select 
            company_name,
            count(*) as nb_command
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_sales_orders
        {where_clause}
            group by company_name
            order by nb_command desc
            limit 10
    """)

    return sales_by_month, order_by_country, order_by_company


def get_product_dashboard():

    filters = {
        'product_name': st.session_state.get('product_select_key_2', []),
        'category_description': st.session_state.get('category_select_key_2', []),
        'company_name': st.session_state.get('company_select_key_2', []),
        'billing_status': st.session_state.get('billing_status_select_key_2', []),
        'delivery_status': st.session_state.get('delivery_status_select_key_2', []),
    }
    where_clause = build_where_clause(filters)

    product_total = execute_query(f"""
        select 
            product_name,
            any_value(product_description) as product_description,
            any_value(category_description) as category_description,
            sum(quantity) as quantity_sales,
            sum(total_gross_amount) as amount

        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
        {where_clause}
            group by product_name
            order by quantity_sales desc
        """)
    
    product_by_category = execute_query(f"""
        select 
            category_description,
            sum(quantity) as quantity_sales,
            sum(total_gross_amount) as amount

        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
        {where_clause}
            group by category_description
            order by quantity_sales desc
            limit 10
        """)
    
    product_by_company = execute_query(f"""
        select
            company_name,
            sum(quantity) as quantity_sales,
            sum(total_gross_amount) as amount
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
        {where_clause}
            group by company_name
            order by quantity_sales desc
            limit 10
        """)
    
    return product_total, product_by_category, product_by_company

def get_product_info():
    
    if 'product_name_select_key_3' not in st.session_state:
        st.session_state['product_name_select_key_3'] = 'CB-1161'

    product_info = execute_query(f"""
        select
            product_id as product_name,
            product_description,
            category_description,
            currency,
            weight_measure,
            weight_unit,
            price
        from DEV_DBT_CLIENT_BIKE_SHOP.dim_product
        where product_id = '{st.session_state['product_name_select_key_3']}'
    """)

    product_sales_by_month = execute_query(f"""
        select 
            any_value(product_name) as product_name,
            date_trunc(sales_order_date, MONTH) as month,
            sum(total_gross_amount) as amount,
            sum(quantity) as quantity_sales,
            sum(case when delivery_status != 'Completed' then 1 else 0 end) as nb_non_delivery,
            sum(case when billing_status != 'Completed' then 1 else 0 end) as nb_non_billing,
            sum(billing_gross_amount) as billing_amount,
            sum(total_gross_amount) - sum(billing_gross_amount) as missing_amount
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
        where product_name = '{st.session_state['product_name_select_key_3']}'
            group by month
    """)    
    
    product_sales = execute_query(f"""
        select 
            product_name,
            sum(total_gross_amount) as amount,
            sum(quantity) as quantity_sales,
            sum(case when delivery_status != 'Completed' then 1 else 0 end) as nb_non_delivery,
            sum(case when billing_status != 'Completed' then 1 else 0 end) as nb_non_billing,
            sum(billing_gross_amount) as billing_amount,
            sum(total_gross_amount) - sum(billing_gross_amount) as missing_amount
        from DEV_DBT_CLIENT_BIKE_SHOP.mart_product_sales
        where product_name = '{st.session_state['product_name_select_key_3']}'
            group by product_name
    """)                         

    return product_info, product_sales_by_month, product_sales