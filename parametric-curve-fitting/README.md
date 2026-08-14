# Parametric Curve Fitting and Parameter Estimation

## About This Project

This project solves a parametric curve fitting problem using a dataset
containing 1500 `(x, y)` points.

The objective is to recover three unknown parameters from the supplied
data:

- `theta` — rotation angle
- `M` — exponential parameter
- `X` — horizontal offset

The given parametric curve is:

$$
x(t)
=
t\cos(\theta)
-
e^{M|t|}
\sin(0.3t)\sin(\theta)
+
X
$$

$$
y(t)
=
42+t\sin(\theta)
+
e^{M|t|}
\sin(0.3t)\cos(\theta)
$$

where:

$$
6<t<60
$$

The final parameters obtained from the numerical optimization are:

$$
\boxed{\theta\approx30^\circ,\quad M\approx0.03,\quad X\approx55}
$$


---

# 1. Problem Statement

The task is to determine the three unknown parameters:

$$
\theta,\ M,\ X
$$

from the supplied `(x, y)` data.

## The Given Parametric Curve

The given parametric curve is defined by the following two equations:

$$
x(t)=t\cos(\theta)-e^{M|t|}\sin(0.3t)\sin(\theta)+X
$$

$$
y(t)=42+t\sin(\theta)+e^{M|t|}\sin(0.3t)\cos(\theta)
$$

where:

$$
6<t<60
$$

The three unknown parameters are:

- $\theta$ — rotation angle
- $M$ — exponential parameter
- $X$ — horizontal offset

---

# 2. Dataset

The input dataset is:

```text
xy_data.csv
