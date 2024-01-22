import streamlit as st
import pandas as pd

def striped_rows(s):
    return ['background-color: #E6F2FC']*len(s) if s.name % 2 == 1 else ['']*len(s)

USD_COLUMNS_STYLE = {
    'amount': '${:,.0f}',
    'billing_amount': '${:,.0f}',
    'missing_amount': '${:,.0f}',
}

def striped_dataframe(data, height=None):
    if not isinstance(data, pd.DataFrame):
        st.text('Please provide a dataframe')
        return
    
    df = data.copy()
    df.index = df.index + 1

    for col in USD_COLUMNS_STYLE:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    st.dataframe(df.style.format(USD_COLUMNS_STYLE).apply(striped_rows, axis=1), use_container_width=True, height=height)