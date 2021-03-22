import streamlit as st
import pandas as pd
import random
import base64
from plotly.subplots import make_subplots
import plotly.express as px
#import numpy as np
import plotly.graph_objects as go


#st.set_page_config(layout="wide")
#st.markdown('<style>h1{color: red;}</style>', unsafe_allow_html=True)
st.title('Data Plots / Stats')
st.subheader('Create plots and show main stats for each parameter')

uploaded_csv_file = st.file_uploader(label = "Choose a file/files in csv format",
                                    accept_multiple_files = True, type = ["csv"])



def file_download_stats(df):
    #stats = df.describe(percentiles = [.5]).T
    stats_raw = df.agg(["min", "max", "mean", "median", "std"])
    stats = stats_raw.T
    csv = stats.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="stats.csv">Download CSV File with Stats</a>'
    return href

@st.cache(suppress_st_warning=True)
def display_plots(df_csv, parameters):
    fig = go.Figure()
    for param in parameters:
        fig.add_trace(go.Scatter(y = df_csv[param], name=param))
    fig.update_layout(legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation="h"),
            plot_bgcolor='rgb(255, 255, 251)',                #title_text='Plot'
            xaxis=dict(
            linecolor="#BCCCDC",
            showspikes=True,
            spikethickness=2,
            spikedash="dot",
            spikecolor="#999999",
            spikemode="across"))
    fig.update_xaxes(title_text='Samples', showgrid=True, gridwidth=0.01, gridcolor='LightPink',
        zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.01, gridcolor='LightPink',
        zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    #st.plotly_chart(fig)
    return fig

@st.cache(suppress_st_warning=True)
def subplots(df_csv, parameters):
    rows = len(parameters)
    fig = make_subplots(rows = rows,  cols = 1, shared_xaxes = True, subplot_titles = parameters)
    for param in parameters:
        fig.add_trace(go.Scatter(y = df_csv[param], name=param), row=parameters.index(param) +1, col=1)
        fig.update_layout(showlegend= False, plot_bgcolor='rgb(255, 255, 255)')
        fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
    #st.plotly_chart(fig)
    return fig

#@st.cache(suppress_st_warning=True)
def single_plots(df_csv, parameters):
    for param in parameters:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y = df_csv[param], name= param, opacity=1,
        line=dict(color=random.choice(px.colors.qualitative.Plotly))))
        fig.update_layout(showlegend= True, plot_bgcolor='White',
                        legend=dict(yanchor="top", y=1.2, xanchor="center", x=0.5, orientation="h"))
        fig.update_xaxes(showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        fig.update_yaxes(title_text='Value counts', showgrid=True, gridwidth=0.05, gridcolor = "LightPink",
            zeroline=True, zerolinewidth=2, zerolinecolor='Black')
        st.plotly_chart(fig)


@st.cache
def load_multiple_csv_files(uploaded_csv_files):
    for file in uploaded_csv_files:
        file.seek(0)

        uploaded_data_read = (pd.read_csv(file) for file in uploaded_csv_files)
        combined_csv_files = pd.concat(uploaded_data_read, axis = 1)
        return combined_csv_files


if uploaded_csv_file:

    file = load_multiple_csv_files(uploaded_csv_file)
    st.write('Dataset size (rows, columns) = ', file.shape)
    st.markdown('👈 **Select parameters to start the analysis**')
    param_names = file.columns.tolist()

    st.sidebar.title("List of Parameters")
    list_of_parameters = st.sidebar.multiselect(label = "Parameters to plot", options = param_names)
    if list_of_parameters:

        check_box_raw_data = st.checkbox("Display raw data")
        if check_box_raw_data:
            st.subheader("Raw data")
            st.dataframe(file[list_of_parameters])

        check_box_stats = st.checkbox("Display Stats")
        if check_box_stats:
            st.subheader("Stats")
            #st.table(file[list_of_parameters].describe(percentiles = [.5]).T)
            stats = file[list_of_parameters].agg(["min", "max", "mean", "median", "std"])
            st.table(stats.T)
            st.markdown(file_download_stats(file[list_of_parameters]), unsafe_allow_html=True)

        check_box_plots = st.checkbox("Display Plots")

        if check_box_plots:
            st.subheader("Display Data based on the selected parameters")
            st.plotly_chart(display_plots(file, list_of_parameters))
            check_box_subplots = st.checkbox("Display Subplots")

            if check_box_subplots:
                st.subheader('Create subplots for the selected parameters')
                st.plotly_chart(subplots(file, list_of_parameters))

            check_box_single_plot = st.checkbox("Display plot for each parameter")
            if check_box_single_plot:
                st.subheader('Create a separate figure for each selected parameter')
                single_plots(file, list_of_parameters)


hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    """
st.markdown(hide_footer_style, unsafe_allow_html=True)


