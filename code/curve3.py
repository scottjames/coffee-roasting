
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ---- 1. Exponential decay model ----
def exp_decay(t, y0, k, C):
    return y0 * np.exp(-k * t) + C

# ---- 2. Fit model to data ----
def fit_exp_decay(t_data, y_data, alpha=0.05):
    # Initial parameter guesses
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

    # Standard errors and 95% confidence intervals
    perr = np.sqrt(np.diag(pcov))  # standard errors
    z_val = 1.96  # for 95% CI
    ci = [(p - z_val*err, p + z_val*err) for p, err in zip(popt, perr)]

    return {
        "params": (y0, k, C),
        "stderr": perr,
        "conf_int": ci,
        "half_life": half_life,
        "tau": tau,
        "AUC": auc
    }

# ---- 3. Example usage ----
if __name__ == "__main__":
    # Synthetic noisy data
    t = np.linspace(0, 10, 50)
    y_true = exp_decay(t, y0=5, k=0.5, C=1)
    noise = np.random.normal(0, 0.2, size=len(t))
    y_measured = y_true + noise

    # Fit
    results = fit_exp_decay(t, y_measured)
    y0, k, C = results["params"]

    # Print results with confidence intervals
    print("Fit results with 95% confidence intervals:")
    param_names = ["y0", "k", "C"]
    for name, val, se, ci in zip(param_names, results["params"], results["stderr"], results["conf_int"]):
        print(f"{name:>3} = {val:.4f} ± {se:.4f}  (95% CI: {ci[0]:.4f}, {ci[1]:.4f})")

    print(f"Half-life = {results['half_life']:.4f}")
    print(f"Tau       = {results['tau']:.4f}")
    print(f"AUC       = {results['AUC']:.4f}")

    # Generate smooth fit curve
    t_fit = np.linspace(0, max(t), 200)
    y_fit = exp_decay(t_fit, y0, k, C)

    # Plot
    plt.figure(figsize=(8,5))
    plt.scatter(t, y_measured, label="Data", color="blue", alpha=0.6)
    plt.plot(t_fit, y_fit, label="Fitted curve", color="red", linewidth=2)

    # Half-life marker
    hl = results["half_life"]
    plt.axvline(hl, color="green", linestyle="--", label=f"Half-life ≈ {hl:.2f}")

    plt.xlabel("Time")
    plt.ylabel("y(t)")
    plt.title("Exponential Decay Fit with Confidence Intervals")
    plt.legend()
    plt.grid(True)
    plt.show()

