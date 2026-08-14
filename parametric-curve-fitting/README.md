Parametric Curve Fitting and Parameter Estimation

Overview

This project solves a parametric curve fitting problem using 1500 (x, y) points supplied in a CSV file.

The goal is to recover three unknown parameters:

theta — rotation angle

M — exponential parameter

X — horizontal offset

The given parametric curve is:

$$
x(t)=t\cos(\theta)-e^{M|t|}\sin(0.3t)\sin(\theta)+X
$$

$$
y(t)=42+t\sin(\theta)+e^{M|t|}\sin(0.3t)\cos(\theta)
$$

with:

$$
6 < t < 60
$$

The final estimated parameters are:

$$
\boxed{\theta\approx30^\circ,\quad M\approx0.03,\quad X\approx55}
$$

Repository Structure

parametric-curve-fitting/
│
├── README.md
├── solve.py
├── xy_data.csv
├── requirements.txt
├── .gitignore
│
├── notes/
│   ├── mathematical_derivation.md
│   └── original_notes/
│       ├── page_1.jpeg
│       ├── page_2.jpeg
│       ├── page_3.jpeg
│       ├── page_4.jpeg
│       ├── page_5.jpeg
│       └── page_6.jpeg
│
└── results/
    ├── curve_comparison.png
    ├── python_curve.png
    ├── desmos_curve.png
    ├── terminal_output.png
    ├── fit_summary.txt
    └── run_output.txt

The notes/original_notes/ folder contains the original handwritten working used during the derivation. A cleaned mathematical explanation is available in notes/mathematical_derivation.md.

1. Dataset

The input file is:

xy_data.csv

It contains two columns:

x
y

The program reads the data using Pandas:

data = pd.read_csv("xy_data.csv")

x = data["x"].to_numpy()
y = data["y"].to_numpy()

The dataset contains:

1500 points

2. Simplifying the Given Equations

The common term

$$
e^{M|t|}\sin(0.3t)
$$

appears in both equations.

Define:

$$
A=e^{M|t|}\sin(0.3t)
$$

Then the original equations become:

$$
x-X=t\cos(\theta)-A\sin(\theta)
$$

and

$$
y-42=t\sin(\theta)+A\cos(\theta)
$$

This makes the rotational structure easier to work with.

3. Recovering (t)

Starting with:

$$
x-X=t\cos(\theta)-A\sin(\theta)
$$

multiply by $\cos(\theta)$.

Starting with:

$$
y-42=t\sin(\theta)+A\cos(\theta)
$$

multiply by $\sin(\theta)$.

Adding the equations cancels the $A$ terms:

t\left(\cos^2(\theta)+\sin^2(\theta)\right)
$$

Using:

$$
\cos^2(\theta)+\sin^2(\theta)=1
$$

we obtain:

$$
\boxed{
t=(x-X)\cos(\theta)+(y-42)\sin(\theta)
}
$$

The Python implementation is:

t = (
    (x - X) * np.cos(theta_rad)
    + (y - 42) * np.sin(theta_rad)
)

4. Recovering (A)

Combining the transformed equations in the opposite direction cancels the $t$ terms and gives:

$$
\boxed{
A=(y-42)\cos(\theta)-(x-X)\sin(\theta)
}
$$

The Python code calculates this as:

A_data = (
    -(x - X) * np.sin(theta_rad)
    + (y - 42) * np.cos(theta_rad)
)

The original model gives:

e^{M|t|}\sin(0.3t)
}
$$

which is implemented as:

A_expected = (
    np.exp(M * np.abs(t))
    * np.sin(0.3 * t)
)

5. Error Function

For a particular choice of theta, M, and X, the code compares:

$$
A_{\text{data}}
$$

with:

$$
A_{\text{expected}}
$$

The error for each point is:

$$
A_{\text{data}}-A_{\text{expected}}
$$

The objective minimized by the optimizer is the sum of squared errors:

\sum_i
\left(
A_{\text{data},i}-A_{\text{expected},i}
\right)^2
}
$$

In Python:

error = A_data - A_expected

return np.sum(error ** 2)

6. Parameter Ranges

The search is restricted to:

$$
0\leq\theta\leq50
$$

$$
-0.05\leq M\leq0.05
$$

$$
0\leq X\leq100
$$

These ranges are implemented as:

bounds = [
    (0, 50),
    (-0.05, 0.05),
    (0, 100)
]

7. Numerical Optimization

The parameters are not assumed in advance.

The program uses SciPy's differential_evolution optimizer:

result = differential_evolution(
    calculate_error,
    bounds,
    seed=42,
    tol=1e-10
)

The optimizer searches for the combination of theta, M, and X that produces the smallest objective error.

The overall workflow is:

CSV data
   ↓
Choose theta, M, X
   ↓
Calculate t
   ↓
Calculate A_data
   ↓
Calculate A_expected
   ↓
Calculate squared error
   ↓
Sum the errors
   ↓
Optimizer searches for smaller error
   ↓
Best theta, M, X

8. Optimization Result

The actual output from the program was:

Number of points: 1500

Estimated parameters
--------------------
Theta = 29.99997293216684 degrees
M     = 0.029999996873069135
X     = 54.99999821281624

Fitting error = 1.8229979358776814e-08

Therefore, the clean final values are:

$$
\boxed{\theta\approx30^\circ}
$$

$$
\boxed{M\approx0.03}
$$

$$
\boxed{X\approx55}
$$

The small difference between the optimizer output and these rounded values is due to numerical precision.

9. Checking the (t) Range

Using the recovered parameters, the program recalculates t for all CSV points.

The result was:

Minimum t = 6.049405472704011
Maximum t = 59.99517070233434

Therefore:

$$
\boxed{
6.0494\leq t\leq59.9952
}
$$

which is consistent with the required interval $6<t<60$.

10. Point Reconstruction

After finding the parameters, the original (x, y) coordinates are reconstructed.

The fitted x-coordinate is:

x_fitted = (
    t_from_data * np.cos(theta_rad)
    - np.exp(M * np.abs(t_from_data))
    * np.sin(0.3 * t_from_data)
    * np.sin(theta_rad)
    + X
)

The fitted y-coordinate is:

y_fitted = (
    42
    + t_from_data * np.sin(theta_rad)
    + np.exp(M * np.abs(t_from_data))
    * np.sin(0.3 * t_from_data)
    * np.cos(theta_rad)
)

11. L1 Reconstruction Check

The code calculates the point-wise L1 reconstruction error:

$$
L1_i=
|x_i-x_{\text{fitted},i}|
+
|y_i-y_{\text{fitted},i}|
$$

The implementation is:

l1_error = (
    np.abs(x - x_fitted)
    + np.abs(y - y_fitted)
)

The observed results were:

Total L1 error  = 0.0052451377573632385
Mean L1 error   = 3.4967585049088256e-06
Maximum L1 error = 2.406258323617294e-05

These values are very small, showing that the recovered parameters reproduce the supplied data closely.

12. Fitted Curve

The code generates 1000 evenly spaced values of t:

t = np.linspace(6, 60, 1000)

The fitted curve is then generated using the recovered parameters.

The graph is saved as:

results/curve_comparison.png

The plot contains:

the supplied CSV points

the fitted parametric curve

Curve comparison



13. Desmos Verification

The final parameters were also entered into Desmos.

Using:

$$
\theta=30^\circ,\quad M=0.03,\quad X=55
$$

the final curve is:

$$
\boxed{
x(t)=t\cos(30^\circ)
-e^{0.03|t|}\sin(0.3t)\sin(30^\circ)+55
}
$$

$$
\boxed{
y(t)=42+t\sin(30^\circ)
+e^{0.03|t|}\sin(0.3t)\cos(30^\circ)
}
$$

with:

$$
6\leq t\leq60
$$

For the Desmos input, $30^\circ$ was represented numerically as:

$$
0.5235987756
$$

radians.

The Desmos screenshot is stored in:

results/desmos_curve.png

14. Final Answer

The recovered unknown variables are:

Parameter

Estimated value

Rounded value

$\theta$

29.99997293216684°

30°

$M$

0.029999996873069135

0.03

$X$

54.99999821281624

55

The numerical optimizer produced an objective error of approximately:

$$
\boxed{1.823\times10^{-8}}
$$

15. Running the Project

Install dependencies

pip install -r requirements.txt

or:

pip install numpy pandas matplotlib scipy

Run

Make sure xy_data.csv and solve.py are in the project root, then run:

python solve.py

The program prints:

number of data points

estimated parameters

fitting error

t range

point reconstruction errors

It also saves the generated graph to:

results/curve_comparison.png

16. Technologies

Python

NumPy

Pandas

SciPy

Matplotlib

Desmos

Git

GitHub

17. Notes

The notes/original_notes/ folder contains the original handwritten working used during the mathematical derivation.

The cleaned derivation is available at:

notes/mathematical_derivation.md

The notes show the progression from the original parametric equations, through the trigonometric transformation, to the error calculation and numerical optimization.

Important Evaluation Note

The assignment's assessment mentions the L1 distance between uniformly sampled points on the expected and predicted curves.

The repository includes the point-reconstruction L1 validation from the Python implementation. However, the hidden expected curve used by an evaluator is not separately available in the supplied CSV.

Therefore, the reported L1 values in this repository are explicitly described as point reconstruction checks, not as the hidden evaluator's exact score.
