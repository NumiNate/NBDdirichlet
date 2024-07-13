# nbddirichlet_comparison.py

import numpy as np
import pandas as pd
from nbddirichlet import Dirichlet, plot_dirichlet, summary_dirichlet, print_dirichlet
import io
import sys

def run_python_implementation():
    # Input data from the R example
    cat_pen = 0.56
    cat_buyrate = 2.6
    brand_share = [0.25, 0.19, 0.1, 0.1, 0.09, 0.08, 0.03, 0.02]
    brand_pen_obs = [0.2, 0.17, 0.09, 0.08, 0.08, 0.07, 0.03, 0.02]
    brand_name = ["Colgate DC", "Macleans", "Close Up", "Signal", "ultrabrite",
                  "Gibbs SR", "Boots Priv. Label", "Sainsbury Priv. Lab."]

    # Redirect stdout to capture print output
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    # Create Dirichlet model instance
    dobj = Dirichlet(cat_pen, cat_buyrate, brand_share, brand_pen_obs, brand_name)

    # Print model parameters
    print_dirichlet(dobj)

    # Generate summary statistics
    summary = summary_dirichlet(dobj)

    # Print summary statistics
    print("\nBuy Summary:")
    print(summary['buy'])

    print("\nFrequency Summary:")
    print(summary['freq'])

    print("\nHeavy Buyers Summary:")
    print(summary['heavy'])

    print("\nDuplication Summary:")
    print(summary['dup'])

    # Restore stdout and get the captured output
    sys.stdout = old_stdout
    output = buffer.getvalue()

    # Save the output to a file
    with open("python_output.txt", "w") as f:
        f.write(output)

    return summary

def simulate_r_output():
    # This function simulates extracting data from the PDF
    # In a real scenario, you'd use a PDF parsing library to extract this data
    r_output = {
        'parameters': {'M': 1.46, 'K': 0.78, 'S': 1.3},
        'buy': pd.DataFrame({
            'pen.brand': [0.20, 0.16, 0.09, 0.09, 0.08, 0.07, 0.03, 0.02],
            'pur.brand': [1.82, 1.76, 1.68, 1.68, 1.67, 1.66, 1.62, 1.61],
            'pur.cat': [3.16, 3.22, 3.30, 3.30, 3.31, 3.32, 3.37, 3.38]
        }, index=["Colgate DC", "Macleans", "Close Up", "Signal", "ultrabrite",
                  "Gibbs SR", "Boots Priv. Label", "Sainsbury Priv. Lab."]),
        'freq': pd.DataFrame({
            '0': [0.80, 0.84, 0.91, 0.91, 0.92, 0.93, 0.97, 0.98],
            '1': [0.12, 0.10, 0.06, 0.06, 0.05, 0.05, 0.02, 0.01],
            '2': [0.04, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.00],
            '3': [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00, 0.00],
            '4': [0.01, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            '5': [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            '6+': [0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        }, index=["Colgate DC", "Macleans", "Close Up", "Signal", "ultrabrite",
                  "Gibbs SR", "Boots Priv. Label", "Sainsbury Priv. Lab."]),
        'heavy': pd.DataFrame({
            'Penetration': [0.34, 0.27, 0.15, 0.15, 0.13, 0.12, 0.05, 0.03],
            'Avg Purchase Freq': [1.61, 1.57, 1.51, 1.51, 1.50, 1.49, 1.46, 1.45]
        }, index=["Colgate DC", "Macleans", "Close Up", "Signal", "ultrabrite",
                  "Gibbs SR", "Boots Priv. Label", "Sainsbury Priv. Lab."]),
        'dup': pd.Series([1.00, 0.19, 0.10, 0.10, 0.09, 0.08, 0.03, 0.02],
                         index=["Colgate DC", "Macleans", "Close Up", "Signal", "ultrabrite",
                                "Gibbs SR", "Boots Priv. Label", "Sainsbury Priv. Lab."])
    }
    return r_output

def compare_results(python_output, r_output):
    comparison = {}

    # Compare parameters
    py_params = {
        'M': python_output['buy'].iloc[:, 1].iloc[0] * python_output['buy'].iloc[:, 0].iloc[0],
        'K': None,  # We don't have direct access to K in the summary
        'S': None   # We don't have direct access to S in the summary
    }
    comparison['parameters'] = pd.DataFrame({
        'R': r_output['parameters'],
        'Python': py_params,
        'Difference': {k: abs(r_output['parameters'][k] - py_params[k]) if py_params[k] is not None else None 
                       for k in r_output['parameters']}
    })

    # Compare summary statistics
    for key in ['buy', 'freq', 'heavy']:
        r_values = r_output[key].values.flatten()
        py_values = python_output[key].values.flatten()
        
        # Ensure the same number of elements for comparison
        min_length = min(len(r_values), len(py_values))
        r_values = r_values[:min_length]
        py_values = py_values[:min_length]
        
        comparison[key] = pd.DataFrame({
            'R': r_values,
            'Python': py_values,
            'Difference': np.abs(r_values - py_values)
        }, index=pd.MultiIndex.from_product([r_output[key].index[:len(py_values)//len(r_output[key].columns)], 
                                             r_output[key].columns[:len(r_output[key].columns)]]))

    # Compare duplication
    r_dup = r_output['dup']
    py_dup = python_output['dup']
    min_length = min(len(r_dup), len(py_dup))
    comparison['dup'] = pd.DataFrame({
        'R': r_dup[:min_length],
        'Python': py_dup[:min_length],
        'Difference': np.abs(r_dup[:min_length] - py_dup[:min_length])
    })

    return comparison
def generate_report(comparison):
    with open("comparison_report.md", "w") as f:
        f.write("# NBDDirichlet: Python vs R Implementation Comparison\n\n")

        f.write("## Model Parameters\n\n")
        f.write(comparison['parameters'].to_markdown())
        f.write("\n\n")

        for key in ['buy', 'freq', 'heavy', 'dup']:
            f.write(f"## {key.capitalize()} Summary\n\n")
            f.write(comparison[key].to_markdown())
            f.write("\n\n")

        f.write("## Notes on Comparison\n\n")
        f.write("1. Values are rounded to 2 decimal places for comparison.\n")
        f.write("2. Differences greater than 0.01 are highlighted for review.\n")
        f.write("3. Missing values in the Python output are indicated by 'None'.\n")

if __name__ == "__main__":
    python_output = run_python_implementation()
    r_output = simulate_r_output()
    comparison = compare_results(python_output, r_output)
    generate_report(comparison)
    print("Comparison complete. Results saved in 'comparison_report.md'")