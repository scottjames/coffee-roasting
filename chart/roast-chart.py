
import matplotlib.pyplot as plt
import numpy as np

# Time axis in minutes
time = np.linspace(0, 12, 240)  # 12 minutes, 240 points

# Mock bean temperature curve (°C)
bean_temp = (
    25
    + 15 * np.log1p(time)         # initial rise
    + 5 * np.sqrt(time)           # mid roast
    + 2 * time                    # late roast climb
)

# Clip to realistic dark roast range
bean_temp = np.clip(bean_temp, 25, 230)

# Mock RoR curve (°C/min)
RoR = np.gradient(bean_temp, time)
RoR = np.clip(RoR, 0, 30)

# Plot
fig, ax1 = plt.subplots(figsize=(8, 5))

# Bean temp
ax1.plot(time, bean_temp, color="tab:red", linewidth=2, label="Bean Temp (°C)")
ax1.set_xlabel("Time (minutes)")
ax1.set_ylabel("Bean Temp (°C)", color="tab:red")
ax1.tick_params(axis="y", labelcolor="tab:red")
ax1.set_ylim(20, 240)

# Mark phases
ax1.axvline(3.3, color="gold", linestyle="--", label="Yellow (~3:15)")
ax1.axvline(7.8, color="green", linestyle="--", label="1st Crack (~7:45)")
ax1.axvline(10.2, color="blue", linestyle="--", label="2nd Crack (~10:15)")
ax1.axvline(10.8, color="black", linestyle="--", label="Drop (~10:45)")

# RoR on second axis
ax2 = ax1.twinx()
ax2.plot(time, RoR, color="tab:blue", linestyle=":", linewidth=2, label="RoR (°C/min)")
ax2.set_ylabel("RoR (°C/min)", color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")
ax2.set_ylim(0, 30)

# Legends
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc="lower right")

plt.title("Target Dark Roast Profile (150 g batch, 500 g drum roaster)")
plt.tight_layout()
plt.show()

