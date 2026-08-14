# Parametric Curve Fitting and Parameter Estimation

## Overview

This project solves a parametric curve fitting problem using a dataset
containing 1500 `(x, y)` points.

The objective is to recover three unknown parameters from the supplied
data:

- `theta` — rotation angle
- `M` — exponential parameter
- `X` — horizontal offset

The given parametric curve is:

$$
x(t)=t\cos(\theta)-e^{M|t|}\sin(0.3t)\sin(\theta)+X
$$

$$
y(t)=42+t\sin(\theta)+e^{M|t|}\sin(0.3t)\cos(\theta)
$$

where

$$
6<t<60
$$


## Final Result

The numerical optimization recovered:

| Parameter | Estimated Value | Rounded Value |
|---|---:|---:|
| Theta | 29.99997293216684° | 30° |
| M | 0.029999996873069135 | 0.03 |
| X | 54.99999821281624 | 55 |

The final parameters are therefore:

$$
\boxed{\theta=30^\circ,\quad M=0.03,\quad X=55}
$$

The optimization produced a fitting error of:

$$
\boxed{1.8229979358776814\times10^{-8}}
$$


## Dataset

The input dataset is:

```text
xy_data.csv
