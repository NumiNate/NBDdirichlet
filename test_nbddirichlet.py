import numpy as np
from nbddirichlet import Dirichlet, plot_dirichlet, summary_dirichlet, print_dirichlet

# Input data from the R example
cat_pen = 0.56  # Category Penetration
cat_buyrate = 2.6  # Category Buyer's Average Purchase Rate in a given period
brand_share = [0.25, 0.19, 0.1, 0.1, 0.09, 0.08, 0.03, 0.02]  # Brands' Market Share
brand_pen_obs = [0.2, 0.17, 0.09, 0.08, 0.08, 0.07, 0.03, 0.02]  # Brand Penetration
brand_name = ["Colgate DC", "Macleans", "Close Up", "Signal", "ultrabrite",
              "Gibbs SR", "Boots Priv. Label", "Sainsbury Priv. Lab."]

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

# Plot results
plot_dirichlet(dobj)

# You can add more specific tests here to compare individual values
# with the expected results from the R implementation