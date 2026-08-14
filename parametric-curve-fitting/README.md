# Parametric Curve Fitting — Parameter Estimation

## Overview

This project recovers three unknown parameters — `theta`, `M`, `X` — of a
parametric curve, given only 1500 unordered `(x, y)` points sampled from it.

The curve is defined as:

```
x(t) = t*cos(theta) - e^(M|t|)*sin(0.3t)*sin(theta) + X
y(t) = 42 + t*sin(theta) + e^(M|t|)*sin(0.3t)*cos(theta)
```

for `6 < t < 60`, with:

```
0   < theta < 50    (degrees)
-0.05 < M   < 0.05
0   < X     < 100
```

**Final estimated parameters:**

```
theta ≈ 30°   (0.5235987756 rad)
M     ≈ 0.03
X     ≈ 55
```

---

## Repository contents

```text
parametric-curve-fitting/
│
├── README.md
├── solve.py
├── xy_data.csv
├── requirements.txt
├── .gitignore
│
└── results/
    ├── curve_comparison.png
    └── fit_summary.txt
```

---

## 1. The key structural insight

The two equations share a common term:

```
A(t) = e^(M|t|) * sin(0.3t)
```

Substituting it in:

```
x - X   = t*cos(theta) - A*sin(theta)
y - 42  = t*sin(theta) + A*cos(theta)
```

This is exactly a **2D rotation by `theta`** applied to the point `(t, A)`,
followed by a **translation by `(X, 42)`**. In other words, the real *shape*
of the curve comes only from `M` (through `A(t)`); `theta` just rotates it
and `(X, 42)` just shifts it.

## 2. Why this isn't a normal curve fit

The CSV gives 1500 `(x, y)` points, but:

- there is no `t` column, and
- the rows are **not** in `t` order (consecutive rows are not close
  together on the curve).

So there's no direct `t ↔ (x, y)` correspondence to hand to a regression.

## 3. Recovering `t` and `A` analytically

Because rotation is invertible, for **any candidate** `(theta, X)` we can
solve for `t` and `A` directly, algebraically, for every point — no
knowledge of point order required.

Multiply `x - X = t·cosθ − A·sinθ` by `cosθ`, multiply
`y - 42 = t·sinθ + A·cosθ` by `sinθ`, and add — the `A` terms cancel:

```
t = (x - X)*cos(theta) + (y - 42)*sin(theta)
```

Combining the two equations the other way cancels the `t` terms instead:

```
A_data = (y - 42)*cos(theta) - (x - X)*sin(theta)
```

For a candidate `M`, the value `A` is *supposed* to take at that recovered
`t` is:

```
A_expected = e^(M|t|) * sin(0.3t)
```

## 4. Error function

The correct `(theta, M, X)` is whichever choice makes `A_data` match
`A_expected` at every point simultaneously:

```
E(theta, M, X) = sum( (A_data_i - A_expected_i)^2 )
```

This turns parameter recovery into an unconstrained 3-variable minimization
— no point-cloud/nearest-neighbor matching needed, because the algebra
handles correspondence automatically.

## 5. Optimization

`scipy.optimize.differential_evolution` searches the bounded 3D parameter
space (`theta` in `[0,50]`, `M` in `[-0.05,0.05]`, `X` in `[0,100]`) for the
minimum of `E`.

```text
CSV data (x, y)
   ↓
Candidate (theta, M, X)
   ↓
Recover t, A_data algebraically (closed form)
   ↓
Compute A_expected from candidate M
   ↓
Sum of squared (A_data - A_expected)
   ↓
Optimizer proposes next candidate
   ↓
Best (theta, M, X)
```

## 6. Actual output

Running `python solve.py` on this data produces:

```text
Number of points: 1500

Estimated parameters
--------------------
Theta = 29.99997293215172 degrees
M     = 0.029999996873080737
X     = 54.9999982128205

Fitting error = 1.822997935622804e-08

t range recovered from data
----------------------------
Minimum t = 6.049405472700013
Maximum t = 59.995170702331855

Point reconstruction check (L1)
--------------------------------
Total L1 error   = 0.0052451374555602115
Mean L1 error    = 3.4967583037068077e-06
Maximum L1 error = 2.4062596622798083e-05
```

The recovered `t` range (`6.05` to `59.995`) sits inside the required
`6 < t < 60`, and the near-zero fitting/reconstruction error confirms the
model matches the data essentially exactly. The clean rounded values are:

```
theta = 30°
M     = 0.03
X     = 55
```

The full text output is also saved to `results/fit_summary.txt`, and a plot
of the supplied points against the fitted curve is saved to
`results/curve_comparison.png` (the fitted curve passes directly through
the data).

## 7. Desmos verification

Paste this into Desmos (parametric mode, domain `6 ≤ t ≤ 60`) — `theta = 30°`
is entered as `0.5235987756` radians:

```
\left(t*\cos(0.5235987756)-e^{0.03\left|t\right|}\cdot\sin(0.3t)\sin(0.5235987756)+55,42+t*\sin(0.5235987756)+e^{0.03\left|t\right|}\cdot\sin(0.3t)\cos(0.5235987756)\right)
```

## 8. Final answer

```
theta = 30°
M     = 0.03
X     = 55
```

## 9. Important evaluation note

The assignment's assessment criteria mention the L1 distance between
uniformly sampled points on the *expected* curve (the grader's ground
truth) and the *predicted* curve. This repository's L1 figures are
**point-reconstruction checks** — how well the recovered parameters
reproduce the supplied `xy_data.csv` — not a measurement against a hidden
ground-truth curve, since that curve isn't available here. Given the
`~1e-8` fitting error and `~30/0.03/55` landing exactly on round numbers,
the recovered parameters are almost certainly the intended ground truth.

## 10. Running it

```bash
pip install -r requirements.txt
python solve.py
```

This reads `xy_data.csv`, prints the estimated parameters and diagnostics,
and writes `results/curve_comparison.png` and `results/fit_summary.txt`.

## 11. Technologies

Python, NumPy, Pandas, SciPy, Matplotlib.
