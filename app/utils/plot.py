import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px

def plot_bar_chart(data, x_col, y_col, title, x_label, y_label, color_col=None):
    if not isinstance(data, pd.DataFrame):
        st.text('Please provide a dataframe')
        return
    
    if color_col:
        fig = px.bar(data, x=x_col, y=y_col, color=color_col, text=y_col)
    else:
        fig = px.bar(data, x=x_col, y=y_col, text=y_col)

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        barmode='group'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_scatter_chart(data, x_col, y_col, title, x_label, y_label, color_col=None):
    if not isinstance(data, pd.DataFrame):
        st.text('Please provide a dataframe')
        return
    
    if color_col:
        fig = px.scatter(data, x=x_col, y=y_col, color=color_col)
    else:
        fig = px.scatter(data, x=x_col, y=y_col)

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_line_chart(data, x_col, y_cols, title, x_label, y_label, color_col=None):
    if not isinstance(data, pd.DataFrame):
        st.text('Please provide a dataframe')
        return
    
    if color_col:
        fig = px.line(data, x=x_col, y=y_cols, color=color_col)
    else:
        melted_data = data.melt(id_vars=[x_col], value_vars=y_cols, var_name='Category', value_name=y_label)
        fig = px.line(melted_data, x=x_col, y=y_label, color='Category')

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    
    st.plotly_chart(fig, use_container_width=True)

def plot_pie_chart(data, dimension_col, value_col, title):
    if not isinstance(data, pd.DataFrame):
        st.text('Please provide a dataframe')
        return

    fig = px.pie(data, names=dimension_col, values=value_col, title=title)

    st.plotly_chart(fig, use_container_width=True)



