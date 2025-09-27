
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ---- 1. Exponential decay model ----
def exp_decay(t, y0, k, C):
    return y0 * np.exp(-k * t) + C

# ---- 2. Fit model to data ----
def fit_exp_decay(t_data, y_data):
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

    return {
        "params": (y0, k, C),
        "half_life": half_life,
        "tau": tau,
        "AUC": auc,
        "covariance": pcov
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

    # Print results
    print("Fit results:")
    for kname, val in results.items():
        if kname != "params" and kname != "covariance":
            print(f"{kname:>10}: {val:.4f}")

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
    plt.title("Exponential Decay Fit")
    plt.legend()
    plt.grid(True)
    plt.show()

