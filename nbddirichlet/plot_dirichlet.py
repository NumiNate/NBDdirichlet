# plot_dirichlet
import matplotlib.pyplot as plt
import numpy as np

def plot_dirichlet(x, t=4, brand=None, incr=1, result=None):
    """
    Plot the Dirichlet model with penetration and shopping rate growth over time.

    Args:
        x: Dirichlet object representing the model.
        t: Number of quarters to simulate growth (default is 4).
        brand: List of brand indices to include in the plot (default is None for all brands).
        incr: Increment value for time sequence (default is 1).
        result: Dictionary containing precomputed penetration and shopping rate values (default is None).

    Returns:
        dict: A dictionary containing the simulated penetration and shopping rate values.
    """
    if brand is None:
        brand = range(x.nbrand)
    
    tseq = np.arange(0, t + incr, incr)
    nt = len(tseq)
    nb = len(brand)
    nc = plt.cm.rainbow(np.linspace(0, 1, nb))

    if result is None:
        r_pen = np.zeros((nb, nt))
        r_buy = np.ones((nb, nt))

        for j in range(1, nt):
            ct = tseq[j]
            x.period_set(ct)
            r_pen[:, j] = [x.brand_pen(b) for b in brand]
            r_buy[:, j] = [x.brand_buyrate(b) for b in brand]
    else:
        r_pen = result['pen']
        r_buy = result['buy']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    ax1.set_title(f"Theoretical Penetration Growth\nof Retailer Over {t} Quarters")
    ax1.set_xlabel("Quarters")
    ax1.set_ylabel("Penetration")
    ax1.set_ylim(0, 1)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax2.set_title(f"Theoretical Shopping Rate\nGrowth Over {t} Quarters")
    ax2.set_xlabel("Quarters")
    ax2.set_ylabel("Shopping Frequency")
    ax2.set_ylim(1, np.max(r_buy) + 0.1)
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

    for i in range(nb):
        ax1.plot(tseq, r_pen[i, :], linestyle='-', linewidth=2, color=nc[i], label=x.brand_name[brand[i]])
        ax2.plot(tseq, r_buy[i, :], linestyle='-', linewidth=2, color=nc[i], label=x.brand_name[brand[i]])

    ax1.legend()
    ax2.legend()

    plt.tight_layout()
    plt.show()

    return {'pen': r_pen, 'buy': r_buy}