# NBDDirichlet

NBDDirichlet is a Python implementation of the NBD-Dirichlet model, a powerful tool for analyzing and predicting consumer behavior in marketing contexts. This package provides functionality for estimating model parameters, generating predictions, and visualizing results.

## Features

- Estimate NBD-Dirichlet model parameters from observed data
- Generate predictions for brand penetration and purchase frequency
- Visualize model results with customizable plots
- Provide summary statistics for various aspects of consumer behavior

## Installation

You can install NBDDirichlet using pip:

```bash
pip install nbddirichlet
```

Or, to install from source:

```bash
git clone https://github.com/yourusername/nbddirichlet.git
cd nbddirichlet
pip install .
```

## Usage

Here's a basic example of how to use NBDDirichlet:

```python
from nbddirichlet import Dirichlet, plot_dirichlet, summary_dirichlet

# Create a Dirichlet model instance
model = Dirichlet(
    cat_pen=0.8,           # Category penetration
    cat_buyrate=5,         # Category buy rate
    brand_share=[0.3, 0.2, 0.5],  # Brand market shares
    brand_pen_obs=[0.4, 0.3, 0.6],  # Observed brand penetrations
    brand_name=['Brand A', 'Brand B', 'Brand C']  # Brand names
)

# Generate and print summary statistics
summary = summary_dirichlet(model, t=4, type=['buy', 'freq'])
print(summary['buy'])
print(summary['freq'])

# Plot results
plot_dirichlet(model, t=4)
```

## Documentation

For more detailed information about the package and its functions, please refer to the [full documentation](link-to-your-documentation).

## Contributing

Contributions to NBDDirichlet are welcome! Please refer to our [contribution guidelines](link-to-contributing.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](link-to-license) file for details.

## Contact

If you have any questions or feedback, please open an issue on GitHub or contact (mailto:your-email@example.com).

## Acknowledgments

This package is based on the work of [relevant authors or papers]. We thank them for their contributions to the field of marketing analytics.