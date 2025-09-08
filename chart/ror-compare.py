

import matplotlib.pyplot as plt

# Time checkpoints (minutes)
time_points = [3, 8, 9.5, 10.5, 11]

# Good roast RoR values (°C/min)
good_ror = [15, 10, 7.5, 6, 5]

# Bad roast: Baked (crash after 1C)
baked_ror = [15, 6, 4, 3, 2]

# Bad roast: Tipped/Ashy (too high RoR)
tipped_ror = [18, 14, 12, 10, 9]

fig, ax = plt.subplots(figsize=(8, 5))

# Plot curves
#ax.plot(time_points, good_ror, "-o", color="green", label="✅ Good Balance")
#ax.plot(time_points, baked_ror, "--o", color="red", label="❌ Baked (crash after 1C)")
#ax.plot(time_points, tipped_ror, "--o", color="orange", label="❌ Tipped/Ashy (too high RoR)")
ax.plot(time_points, good_ror, "-o", color="green", label="Good Balance")
ax.plot(time_points, baked_ror, "--o", color="red", label="Baked (crash after 1C)")
ax.plot(time_points, tipped_ror, "--o", color="orange", label="Tipped/Ashy (too high RoR)")

# Labels and formatting
ax.set_title("RoR vs. Time — Balancing with Good DTR (150 g Dark Roast)")
ax.set_xlabel("Time (minutes)")
ax.set_ylabel("RoR (°C/min)")
ax.set_ylim(0, 20)
ax.grid(True, linestyle=":")
ax.legend()

plt.tight_layout()
plt.show()

