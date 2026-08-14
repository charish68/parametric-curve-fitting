# Mathematical Derivation

## 1. Given curve

The assignment gives

\[
x(t)=t\cos(\theta)-e^{M|t|}\sin(0.3t)\sin(\theta)+X
\]

\[
y(t)=42+t\sin(\theta)+e^{M|t|}\sin(0.3t)\cos(\theta)
\]

with unknowns \(\theta, M, X\).

For convenience, define

\[
A=e^{M|t|}\sin(0.3t).
\]

Then

\[
x-X=t\cos(\theta)-A\sin(\theta)
\]

and

\[
y-42=t\sin(\theta)+A\cos(\theta).
\]

## 2. Recovering \(t\)

Multiply the first equation by \(\cos(\theta)\) and the second by \(\sin(\theta)\), then add them:

\[
(x-X)\cos(\theta)+(y-42)\sin(\theta)
=t(\cos^2(\theta)+\sin^2(\theta)).
\]

Using

\[
\cos^2(\theta)+\sin^2(\theta)=1,
\]

we get

\[
\boxed{t=(x-X)\cos(\theta)+(y-42)\sin(\theta)}.
\]

## 3. Recovering \(A\)

Using the same two transformed equations and cancelling the \(t\) terms gives

\[
\boxed{
A=(y-42)\cos(\theta)-(x-X)\sin(\theta)
}.
\]

The model also says

\[
\boxed{
A=e^{M|t|}\sin(0.3t)
}.
\]

Therefore, for a correct set of parameters, the data-derived value of \(A\) should be very close to the model value.

## 4. Error function

For every CSV point,

\[
A_{\text{data}}
=(y-42)\cos(\theta)-(x-X)\sin(\theta)
\]

and

\[
A_{\text{expected}}
=e^{M|t|}\sin(0.3t).
\]

The objective minimized in the Python code is

\[
\boxed{
E(\theta,M,X)
=
\sum_i
(A_{\text{data},i}-A_{\text{expected},i})^2
}.
\]

The optimizer searches the allowed parameter ranges and returns the parameter combination with the smallest objective error.
