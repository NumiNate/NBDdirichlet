# summary_dirichlet

import numpy as np
import pandas as pd

def summary_dirichlet(obj, type=('buy', 'freq', 'heavy', 'dup'), digits=3, freq_cutoff=5, heavy_limit=range(1, 5), dup_brand=0):
    """
    Generates a summary of the Dirichlet model for a given object and period.

    Args:
        obj (Dirichlet): The Dirichlet object representing the model.
        type (tuple, optional): The types of summaries to generate. Defaults to ('buy', 'freq', 'heavy', 'dup').
        digits (int, optional): The number of decimal places to round the results to. Defaults to 3.
        freq_cutoff (int, optional): The cutoff for the frequency summary. Defaults to 5.
        heavy_limit (range, optional): The range of values for the heavy limit. Defaults to range(1, 5).
        dup_brand (int, optional): The brand for the duplicate summary. Defaults to 0.

    Returns:
        dict: A dictionary containing the generated summaries. The keys are the types of summaries and the values are the corresponding results.

    """
    result = {}
    for tt in type:
        if tt == "buy":
            r = np.zeros((obj.nbrand, 3))
            for j in range(obj.nbrand):
                r[j, 0] = obj.brand_pen(j)  # This should now use current M and K
                r[j, 1] = obj.brand_buyrate(j)  # This should now use current M and K
                r[j, 2] = obj.wp(j)  # This should now use current M and K

            result[tt] = pd.DataFrame(r, index=obj.brand_name, 
                                      columns=["pen_brand", "pur_brand", "pur_cat"]).round(digits)

        elif tt == "freq":
            def prob_r(r, j):
                return sum(obj.Pn(n) * obj.p_rj_n(r, n, j) for n in range(r, obj.nstar + 1))

            r = np.zeros((obj.nbrand, freq_cutoff + 2))
            for j in range(obj.nbrand):
                r[j, :] = [prob_r(r, j) for r in range(freq_cutoff + 1)] + [sum(prob_r(r, j) for r in range(freq_cutoff + 1, obj.nstar + 1))]

            result[tt] = pd.DataFrame(r, index=obj.brand_name, 
                                      columns=[str(i) for i in range(freq_cutoff + 1)] + [f"{freq_cutoff+1}+"]).round(digits)

        elif tt == "heavy":
            Pn_sum = sum(obj.Pn(n) for n in heavy_limit)
            r = np.zeros((obj.nbrand, 2))
            for j in range(obj.nbrand):
                p0 = 1 - obj.brand_pen(j, limit=heavy_limit)
                r[j, 0] = 1 - p0 / Pn_sum
                r[j, 1] = obj.brand_buyrate(j, limit=heavy_limit) * obj.brand_pen(j) / (Pn_sum - p0)

            result[tt] = pd.DataFrame(r, index=obj.brand_name, columns=["Penetration", "Avg Purchase Freq"]).round(digits)

        elif tt == "dup":
            k = dup_brand
            r = np.zeros(obj.nbrand)
            r[k] = 1
            b_k = obj.brand_pen(k)
            others = [j for j in range(obj.nbrand) if j != k]

            for j in others:
                p0 = sum(obj.Pn(i) * obj.p_rj_n(0, i, [k, j]) for i in range(obj.nstar + 1))
                b_j_k = 1 - p0
                b_j = obj.brand_pen(j)
                b_jk = b_j + b_k - b_j_k
                b_j_given_k = b_jk / b_k
                r[j] = b_j_given_k

            result[tt] = pd.Series(r, index=obj.brand_name).round(digits)

    return result