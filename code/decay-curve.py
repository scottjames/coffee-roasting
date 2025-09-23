
# pass in a set of data points (t,y)(t,y), and it will:
#  - Fit an exponential decay model (with or without baseline).
#  - Extract y0, k, C.
#  - Compute half-life, time constant, and AUC.


import numpy as np
from scipy.optimize import curve_fit

# ---- 1. Define exponential decay model ----
def exp_decay(t, y0, k, C):
    return y0 * np.exp(-k * t) + C

# ---- 2. Fit model to data ----
def fit_exp_decay(t_data, y_data):
    # initial guesses: y0 ~ max-min, k ~ 1/(span), C ~ min
    guess_y0 = np.max(y_data) - np.min(y_data)
    guess_k = 1.0 / (t_data[-1] - t_data[0] + 1e-6)
    guess_C = np.min(y_data)
    p0 = [guess_y0, guess_k, guess_C]

    popt, pcov = curve_fit(exp_decay, t_data, y_data, p0=p0, maxfev=10000)
    y0, k, C = popt

    # Derived metrics
    half_life = np.log(2) / k
    tau = 1.0 / k
    auc = y0 / k

    return {
        "y0": y0,
        "k": k,
        "C": C,
        "half_life": half_life,
        "tau": tau,
        "AUC": auc,
        "covariance": pcov
    }

# ---- 3. Example usage ----
if __name__ == "__main__":
    # synthetic noisy data
    t = np.linspace(0, 10, 50)
    y_true = exp_decay(t, y0=5, k=0.5, C=1)
    noise = np.random.normal(0, 0.2, size=len(t))
    y_measured = y_true + noise

    results = fit_exp_decay(t, y_measured)
    for k, v in results.items():
        print(f"{k:>10}: {v}")

