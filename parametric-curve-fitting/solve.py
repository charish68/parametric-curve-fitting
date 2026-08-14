import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution


# Read the data
data = pd.read_csv("xy_data.csv")

x = data["x"].to_numpy()
y = data["y"].to_numpy()

print("Number of points:", len(data))


# This function measures how well a particular
# theta, M and X fit the given data.
def calculate_error(params):
    theta, M, X = params

    # NumPy trigonometric functions use radians.
    theta_rad = np.radians(theta)

    # Recover t from the x and y coordinates.
    t = (
        (x - X) * np.cos(theta_rad)
        + (y - 42) * np.sin(theta_rad)
    )

    # Recover A directly from the data.
    A_data = (
        -(x - X) * np.sin(theta_rad)
        + (y - 42) * np.cos(theta_rad)
    )

    # A according to the mathematical model.
    A_expected = (
        np.exp(M * np.abs(t))
        * np.sin(0.3 * t)
    )

    # Difference between the data-derived and model values.
    error = A_data - A_expected

    # Sum of squared errors.
    return np.sum(error ** 2)


# Parameter ranges used in the assignment.
bounds = [
    (0, 50),          # theta in degrees
    (-0.05, 0.05),    # M
    (0, 100)          # X
]


# Search for the parameters giving the smallest error.
result = differential_evolution(
    calculate_error,
    bounds,
    seed=42,
    tol=1e-10
)

theta, M, X = result.x

print("\nEstimated parameters")
print("--------------------")
print("Theta =", theta, "degrees")
print("M     =", M)
print("X     =", X)

print("\nFitting error =", result.fun)


# Convert the final angle to radians.
theta_rad = np.radians(theta)


# Generate a smooth curve over the requested t interval.
t = np.linspace(6, 60, 1000)

x_curve = (
    t * np.cos(theta_rad)
    - np.exp(M * np.abs(t))
    * np.sin(0.3 * t)
    * np.sin(theta_rad)
    + X
)

y_curve = (
    42
    + t * np.sin(theta_rad)
    + np.exp(M * np.abs(t))
    * np.sin(0.3 * t)
    * np.cos(theta_rad)
    + 0
)


# Plot the original data and fitted curve.
plt.figure(figsize=(9, 6))

plt.scatter(
    x,
    y,
    s=10,
    label="Given data"
)

plt.plot(
    x_curve,
    y_curve,
    linewidth=2,
    label="Fitted curve"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Given Points and Fitted Curve")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Save instead of opening an interactive window.
plt.savefig("results/curve_comparison.png", dpi=200)
plt.close()


# Check the range of t obtained from the data.
t_from_data = (
    (x - X) * np.cos(theta_rad)
    + (y - 42) * np.sin(theta_rad)
)

print("\nT range")
print("-------")
print("Minimum t =", t_from_data.min())
print("Maximum t =", t_from_data.max())


# Reconstruct the original x and y coordinates.
x_fitted = (
    t_from_data * np.cos(theta_rad)
    - np.exp(M * np.abs(t_from_data))
    * np.sin(0.3 * t_from_data)
    * np.sin(theta_rad)
    + X
)

y_fitted = (
    42
    + t_from_data * np.sin(theta_rad)
    + np.exp(M * np.abs(t_from_data))
    * np.sin(0.3 * t_from_data)
    * np.cos(theta_rad)
)


# Point reconstruction L1 distance.
l1_error = (
    np.abs(x - x_fitted)
    + np.abs(y - y_fitted)
)

print("\nPoint reconstruction error")
print("--------------------------")
print("Total L1 error =", np.sum(l1_error))
print("Mean L1 error  =", np.mean(l1_error))
print("Maximum L1 error =", np.max(l1_error))


# Save a short machine-readable summary.
with open("results/fit_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"Number of points: {len(data)}\n")
    f.write(f"Theta degrees: {theta:.14f}\n")
    f.write(f"M: {M:.14f}\n")
    f.write(f"X: {X:.14f}\n")
    f.write(f"Fitting error: {result.fun:.16e}\n")
    f.write(f"Minimum t: {t_from_data.min():.14f}\n")
    f.write(f"Maximum t: {t_from_data.max():.14f}\n")
    f.write(f"Total point reconstruction L1: {np.sum(l1_error):.16e}\n")
    f.write(f"Mean point reconstruction L1: {np.mean(l1_error):.16e}\n")
    f.write(f"Maximum point reconstruction L1: {np.max(l1_error):.16e}\n")
