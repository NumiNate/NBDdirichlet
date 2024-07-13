# print_dirichlet

def print_dirichlet(x):
    """
    Print various information related to Dirichlet model including error handling, brand details, market shares, penetrations, and model parameters.
    """
    if hasattr(x, 'error') and x.error == 1:
        print(f"ERROR! nstar is too small! (nstar={x.nstar}), Sum of Pn is (should be 1) {sum(x.Pn(i) for i in range(x.nstar + 1))}")
    
    print(f"Number of Brands in the Category = {x.nbrand}")
    print("Brand List :", ", ".join(x.brand_name))
    print(f"Brands' Market Shares: {', '.join([f'{s:.3f}' for s in x.brand_share])}")
    print(f"Brands' Penetration:   {', '.join([f'{p:.3f}' for p in x.brand_pen_obs])}")
    x.period_print()
    print(f"\nCategory Penetration = {x.cat_pen:.2f}, with Buying Rate = {x.cat_buyrate:.2f}")
    print("Estimated Dirichlet Model Parameters:")
    print(f"NBD: M = {x.M:.2f}, K = {x.K:.2f}; Dirichlet: S = {x.S:.2f}\n")