import streamlit as st
import numpy as np
import pandas as pd
from nbddirichlet import Dirichlet, plot_dirichlet, summary_dirichlet, print_dirichlet
import io
import sys
import matplotlib
matplotlib.use('Agg')

def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    func(*args, **kwargs)
    output = new_stdout.getvalue()
    sys.stdout = old_stdout
    return output

def format_number(x):
    if x == 0:
        return '-'
    elif isinstance(x, (int, float)):
        return f'{x:.2f}'
    return x

st.title('Dirichlet Model Web Interface')

# Default values from test_nbddirichlet.py
default_cat_pen = 0.56
default_cat_buyrate = 2.6
default_brand_share = [0.25, 0.19, 0.1, 0.1, 0.09, 0.08, 0.03, 0.02]
default_brand_pen_obs = [0.2, 0.17, 0.09, 0.08, 0.08, 0.07, 0.03, 0.02]
default_brand_name = ["Colgate DC", "Macleans", "Close Up", "Signal", "ultrabrite",
                      "Gibbs SR", "Boots Priv. Label", "Sainsbury Priv. Lab."]

# Input fields
cat_pen = st.number_input('Category Penetration', value=default_cat_pen, format='%.2f')
cat_buyrate = st.number_input('Category Buyer\'s Average Purchase Rate', value=default_cat_buyrate, format='%.2f')

# Add input for time period multiple
t_value = st.number_input('Time Period Multiple', value=1, min_value=1, max_value=99, step=1)

st.subheader('Brand Information')
num_brands = st.number_input('Number of Brands', min_value=1, value=len(default_brand_name), step=1)

brand_share = []
brand_pen_obs = []
brand_name = []

for i in range(int(num_brands)):
    col1, col2, col3 = st.columns(3)
    with col1:
        default_name = default_brand_name[i] if i < len(default_brand_name) else f'Brand {i+1}'
        brand_name.append(st.text_input(f'Brand {i+1} Name', value=default_name))
    with col2:
        default_share = default_brand_share[i] if i < len(default_brand_share) else 0.1
        brand_share.append(st.number_input(f'Brand {i+1} Market Share', value=default_share, format='%.2f'))
    with col3:
        default_pen = default_brand_pen_obs[i] if i < len(default_brand_pen_obs) else 0.1
        brand_pen_obs.append(st.number_input(f'Brand {i+1} Penetration', value=default_pen, format='%.2f'))

if st.button('Run Dirichlet Model'):
    # Create Dirichlet model instance
    dobj = Dirichlet(cat_pen, cat_buyrate, brand_share, brand_pen_obs, brand_name)

    # Set the time period
    dobj.period_set(t_value)

    # Print model parameters
    st.subheader('Model Parameters')
    st.text(capture_output(print_dirichlet, dobj))
    st.text(capture_output(dobj.period_print))

    # Generate summary statistics
    summary = summary_dirichlet(dobj)

    # Format and display summary statistics
    for key in summary:
        if isinstance(summary[key], pd.DataFrame):
            summary[key] = summary[key].applymap(format_number)
        elif isinstance(summary[key], pd.Series):
            summary[key] = summary[key].map(format_number)

    st.subheader('Buy Summary')
    st.dataframe(summary['buy'])

    st.subheader('Frequency Summary')
    st.dataframe(summary['freq'])

    st.subheader('Heavy Buyers Summary')
    st.dataframe(summary['heavy'])

    st.subheader('Duplication Summary')
    st.dataframe(summary['dup'])

    # Plot results
    st.subheader('Dirichlet Plot')
    fig = dobj.plot_dirichlet()  # Call the method on the Dirichlet object
    st.pyplot(fig)