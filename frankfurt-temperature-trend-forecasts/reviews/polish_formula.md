# Polish formula: monthly 2 m temperature, Frankfurt am Main

Scope: the body (`paper_draft.body.tex`) contains no displayed equations. Section 3 describes every estimator in words only. Below are (A) preamble additions, (B) ready-to-paste LaTeX for Section 3, (C) notation fixes in running text, and (D) mismatches between the code (`run_estimation.py`) and the draft's wording that the formulas make visible. No number is changed.

## A. Preamble additions (`paper_draft.tex`)

The draft loads `amsmath, amssymb, amsthm`. Add:

```latex
\usepackage{mathtools}
\usepackage{bm}
\DeclareMathOperator{\Var}{Var}
\DeclareMathOperator{\floor}{floor}
\newcommand{\degC}{^{\circ}\mathrm{C}}
\newcommand{\HAC}{\mathrm{HAC}}
```

Use `\bigl( ... \bigr)` rather than `\left ... \right`. Use `\eqref` for cross-references, or `\ref` with `Equation~`.

## B. Equations to insert in Section 3 (Empirical Strategy)

### B1. Notation paragraph, start of Section 3

```latex
Let $y_t$ denote the monthly mean temperature in $\degC$ for month $t=1,\ldots,540$
(January 1981 to December 2025), with calendar month $m(t)\in\{1,\ldots,12\}$ and
elapsed time $\tau_t=(t-1)/12$ in years. The training window is $\mathcal{T}=\{1,\ldots,504\}$
(forecast origin $T_0=504$, December 2022) and the hold-out is $\mathcal{H}=\{505,\ldots,540\}$,
so $H=36$. Annual means are $\bar y_s=\tfrac{1}{12}\sum_{t:\,\text{year}(t)=s} y_t$.
```

### B2. Trend description (replace the first sentences of 3.1)

```latex
The annual trend is the OLS slope in
\begin{equation}\label{eq:trend-annual}
  \bar y_s = \alpha + \beta\, (s - s_0) + u_s ,
  \qquad s = 1981,\ldots,S ,
\end{equation}
with $S=2022$ (training, $n=42$) or $S=2025$ (full sample, $n=45$), reported as $10\hat\beta$ in $\degC$ per decade.
Standard errors are Newey--West (HAC) with Bartlett kernel and bandwidth
\begin{equation}\label{eq:hac-lag}
  L = \Bigl\lfloor 4\,(T/100)^{2/9} \Bigr\rfloor ,
\end{equation}
where $T$ is the number of observations in the regression. The monthly analogue uses the deseasonalised series
\begin{equation}\label{eq:deseason}
  \tilde y_t = y_t - \hat\mu_{m(t)},
  \qquad
  \hat\mu_m = \frac{1}{|\{t: m(t)=m\}|}\sum_{t:\,m(t)=m} y_t ,
\end{equation}
with $\hat\mu_m$ estimated on the sample used, and $\tilde y_t=\alpha+\beta\,\tau_t+u_t$ estimated by OLS with $L$ from \eqref{eq:hac-lag} (and $L=24$ as a check).
Season-specific slopes apply \eqref{eq:trend-annual} to the seasonal means for DJF, MAM, JJA and SON.
```

Check: for T=42, L=floor(4*0.42^(2/9))=floor(3.30)=3. For T=504 L=floor(4*5.04^(2/9))=floor(5.7)=5. State these two values in the text, or in a table note, after confirming them in `estimation_results.json`.

### B3. Mann--Kendall and Sen's slope

```latex
With annual means $x_1,\ldots,x_n$, the Mann--Kendall statistic is
\begin{equation}\label{eq:mk}
  S_{\mathrm{MK}}=\sum_{i<j}\operatorname{sgn}(x_j-x_i),
  \qquad
  Z=\frac{S_{\mathrm{MK}}-\sgn(S_{\mathrm{MK}})}{\sqrt{\Var(S_{\mathrm{MK}})}} ,
\end{equation}
and Sen's slope is $\hat\beta_{\mathrm{Sen}}=\operatorname{median}_{i<j}\,(x_j-x_i)/(j-i)$.
The autocorrelation-corrected variant multiplies $\Var(S_{\mathrm{MK}})$ by an estimated variance inflation factor, which equals one here.
```

Declare `\sgn` (`\DeclareMathOperator{\sgn}{sgn}`) in the preamble, and use `\sgn` in `Z` instead of the mixed `\operatorname{sgn}`. Confirm in the code that the continuity correction in $Z$ is the one used. The draft's statistic of 4.48 should be this $Z$.

### B4. Amplitude and phase drift (matches `run_estimation.py` lines 316--325)

```latex
\begin{equation}\label{eq:drift}
  y_t = a + b\,\tau_t
      + (c_1 + d_1\tau_t)\cos(2\pi\tau_t)
      + (c_2 + d_2\tau_t)\sin(2\pi\tau_t) + u_t ,
  \qquad t\in\mathcal{T},
\end{equation}
so that amplitude and phase at time $\tau$ are
\begin{equation}\label{eq:amp-phase}
  A(\tau)=\sqrt{(c_1+d_1\tau)^2+(c_2+d_2\tau)^2},
  \qquad
  \phi(\tau)=\operatorname{atan2}\bigl(c_2+d_2\tau,\; c_1+d_1\tau\bigr).
\end{equation}
We report $A(\tau_{504})-A(0)$ and $\phi(\tau_{504})-\phi(0)$, and test $H_0: d_1=d_2=0$ with a joint Wald test based on HAC errors with the lag from \eqref{eq:hac-lag}.
```

Because the phase is the angle of $(\cos,\sin)$ coefficients, say that $\phi$ is in degrees and that $-1.6^\circ$ corresponds to roughly $-4.4$ days of timing ($1.6/360\times365.25$). This is an optional addition; do not state it unless the author wants it.

### B5. Forecasting models (new paragraph after "Forecasting models and evaluation" first paragraph)

```latex
Write $\hat y_{T_0+h\mid T_0}$ for the $h$-step forecast, $h=1,\ldots,36$. The baselines are
\begin{equation}\label{eq:baselines}
  \hat y^{\mathrm{SN}}_{T_0+h\mid T_0}=y_{T_0+h-12\lceil h/12\rceil},
  \qquad
  \hat y^{\mathrm{N}}_{T_0+h\mid T_0}=y_{T_0}.
\end{equation}
The first repeats the most recent observation of the same calendar month, which for $h>12$ is the value one, two or three years before the target.
The harmonic regression is
\begin{equation}\label{eq:harmonic}
  y_t=\alpha+\beta\,\tau_t+\sum_{k=1}^{K}\Bigl[\gamma_k\cos(2\pi k\tau_t)+\delta_k\sin(2\pi k\tau_t)\Bigr]+u_t ,
\end{equation}
estimated by OLS on $\mathcal{T}$ with $K\in\{1,\ldots,4\}$ chosen by AICc. ETS(A,Ad,A) is
\begin{equation}\label{eq:ets}
  \begin{aligned}
    y_t &= \ell_{t-1}+\phi\, b_{t-1}+s_{t-12}+\varepsilon_t ,\\
    \ell_t &= \ell_{t-1}+\phi\, b_{t-1}+\alpha\,\varepsilon_t ,\\
    b_t &= \phi\, b_{t-1}+\beta\,\varepsilon_t ,\\
    s_t &= s_{t-12}+\gamma\,\varepsilon_t ,
  \end{aligned}
\end{equation}
and ETS(A,N,A) sets $b_t\equiv 0$. The seasonal ARIMA model is $\Phi(B^{12})\,\varphi(B)\,(1-B)^d(1-B^{12})^D y_t=c+\Theta(B^{12})\,\theta(B)\,\varepsilon_t$ with orders $(p,d,q)(P,D,Q)_{12}$ chosen by AICc over $p,q\le 3$, $P,Q\le 2$, $d,D\in\{0,1\}$.
```

Notation collision: $\alpha,\beta$ appear in the trend regression, the harmonic regression, and ETS smoothing parameters. Either rename the ETS smoothing parameters to $(a_\ell, a_b, a_s)$ or state "symbols are local to each equation". The simplest fix is to use $\vartheta_\ell,\vartheta_b,\vartheta_s$ for the three smoothing parameters and $\phi$ for damping. Also $\phi$ is used for phase in \eqref{eq:amp-phase}; rename the phase to $\psi(\tau)$.

### B6. Accuracy measures and the Diebold--Mariano test

```latex
With hold-out errors $e_{h}=y_{T_0+h}-\hat y_{T_0+h\mid T_0}$, $h=1,\ldots,H$:
\begin{equation}\label{eq:accuracy}
  \mathrm{RMSE}=\Bigl(\tfrac1H\sum_{h=1}^{H}e_h^2\Bigr)^{1/2},
  \quad
  \mathrm{MAE}=\tfrac1H\sum_{h=1}^{H}|e_h| ,
  \quad
  \mathrm{MASE}=\frac{\mathrm{MAE}}{\frac{1}{T_0-12}\sum_{t=13}^{T_0}|y_t-y_{t-12}|} .
\end{equation}
The denominator is the in-sample seasonal naive MAE on $\mathcal{T}$, equal to 2.04$\degC$.
For loss $g(e)=e^2$ or $|e|$, let $d_h=g(e^{\mathrm{SN}}_h)-g(e^{\mathrm{M}}_h)$, so $\bar d>0$ means model $\mathrm{M}$ is better. The statistic is
\begin{equation}\label{eq:dm}
  \mathrm{DM}^{*}=\sqrt{\frac{H+1-2q+q(q-1)/H}{H}}\;\frac{\bar d}{\sqrt{\hat V(\bar d)}} ,
  \qquad
  \hat V(\bar d)=\frac1H\Bigl[\hat\gamma_0+2\sum_{k=1}^{q-1}\Bigl(1-\frac{k}{q}\Bigr)\hat\gamma_k\Bigr] ,
\end{equation}
where $\hat\gamma_k$ is the sample autocovariance of $d_h$ at lag $k$, and $\mathrm{DM}^{*}$ is compared with a $t_{H-1}$ distribution (two-sided).
```

The ratio MAE/scale in \eqref{eq:accuracy} follows Hyndman and Koehler (`hyndman2006another`). The sum in the scale starts at $t=13$, so it has $T_0-12=492$ terms.

### B7. Prediction-interval coverage

```latex
\begin{equation}\label{eq:coverage}
  \mathrm{Cov}=\frac1H\sum_{h=1}^{H}\mathbbm{1}\bigl\{\hat\ell_h\le y_{T_0+h}\le\hat u_h\bigr\} ,
\end{equation}
```

This needs `\usepackage{bbm}`. If the author prefers not to add bbm, write `\mathbf{1}` instead.

## C. Notation fixes in running text

1. Negative numbers: `$-0.15$` and `$-1.6$` are already in math mode. Keep. Write the unit consistently, either "degrees Celsius" in prose or `$\degC$`. The draft mixes "degrees", "degrees Celsius", and "°C".
2. Slope units: use "$0.50\,\degC$ per decade (HAC s.e. $0.083$)". Give the interval as `[lower, upper]` from `estimation_results.json`.
3. Test statistics: write $p<0.001$, $p=0.76$, and always italic $p$. Line 109 says "$p$-value bounded at 0.01"; write "$p<0.01$ (the tabulated lower bound)". Check whether this is the lower bound (p ≥ 0.01 reported by statsmodels when the statistic is beyond the table); if so the correct wording is "$p\le 0.01$".
4. Hypotheses: `H1` to `H3` in running text should be `$H_1$`, `$H_2$`, `$H_3$`, consistent with the hypothesis paragraph (line 78).
5. Section reference: line 78 says `Section~4` as plain text. Replace with `Section~\ref{sec:results}` and add `\label{sec:results}` after `\section{Results}`.
6. Model names: `ETS(A,N,A)` and `ETS(A,Ad,A)` as `\mathrm{ETS}(A,N,A)` in math, or `\text{ETS}(A,A_d,A)`, but plain text in prose is fine. Use `SARIMA$(p,d,q)(P,D,Q)_{12}$`; the output label contains `[12]`, so write `_{12}` in text, not `[12]`.
7. Ratios: the RMSE ratio (0.68, 0.71) is written in prose; define it once as $\mathrm{RMSE}_{\mathrm{M}}/\mathrm{RMSE}_{\mathrm{SN}}$ after \eqref{eq:accuracy}.

## D. Code versus draft: points the formulas expose

1. **DM truncation lag vs forecast horizon.** `dm_test` (`run_estimation.py`, lines 351--366) uses one argument `h` as both the Bartlett truncation lag and the HLN horizon term. In the tests labelled `squared_h12` and `h12`, `h=12`. The Harvey--Leybourne--Newbold correction is defined with $h$ the forecast horizon; here the multi-step horizon runs to 36, and the errors span horizons 1--36 pooled. The draft's \eqref{eq:dm} above is written with $q$ (truncation lag, $q=12$) in both places so that it matches the code. The draft should say so explicitly: "we truncate the long-run variance at $q=12$ lags, the seasonal cycle". It should not describe the correction as the standard $h$-step HLN. Also, `hln` uses $n+1-2q+q(q-1)/n$ with $q=12$ and $n=36$, which is $36+1-24+3.67=16.67>0$, so it is valid; but it is a conservative adjustment, so report this as a design choice.
2. **Bartlett weights.** The loop in the code runs $k=1,\ldots,q-1$ with weights $1-k/q$. That is what \eqref{eq:dm} states; do not write the sum to $q$.
3. **Harmonic count.** The text says "number of harmonics chosen by AICc" and the spec says $K=1,\ldots,4$. Insert the selected $K$ (`K_sel` in the script, stored in the model label) at \eqref{eq:harmonic}, e.g. "AICc selects $K=\ldots$".
4. **Seasonal-naive horizon index.** \eqref{eq:baselines} gives $y_{T_0+h-12\lceil h/12\rceil}$. For $h=1$ this is $y_{T_0-11}$ (January 2022), correct for a January target; for $h=13$ it is $y_{T_0-23}$, also correct. Check against `f_snaive` in the script that the multi-year horizons repeat the last observed year (not an average).
5. **Seasonal-naive interval.** The spec says the interval uses the seasonal-lag difference sd scaled by $\sqrt{k}$ where $k$ is the number of cycles ahead. If the draft's interval paragraph mentions this, write $\hat\sigma\sqrt{\lceil h/12\rceil}$, with $\hat\sigma$ the standard deviation of $y_t-y_{t-12}$ on $\mathcal{T}$ (as in Hyndman and Athanasopoulos, `hyndman2021forecasting`). For the random walk: $\hat\sigma\sqrt h$.
6. **Wald test.** The test in \eqref{eq:drift} has 2 restrictions; the statistic is compared with $\chi^2_2$. Say so with the reported $p=0.76$.
7. **Rolling origins.** Describe them formally once: origins $T_j=T_0^{\mathrm{ro}}+12j$ for $j=0,\ldots,19$, from December 2000 ($t=240$) to December 2019 ($t=468$), each with $h=1,\ldots,36$, so the last target is December 2022, the last training month. Check that $468+36=504$; yes. This confirms the origins do not touch the hold-out.

## E. Checks done

- Origin and sample arithmetic: $540=504+36$; $42$ annual training observations; $T_0-12=492$ terms in the MASE scale.
- Amplitude/phase formulas in \eqref{eq:drift}--\eqref{eq:amp-phase} reproduce the code's design matrix (columns: 1, $\tau$, $\cos$, $\sin$, $\tau\cos$, $\tau\sin$) and the `atan2(sin, cos)` phase; the Wald restriction rows select the last two columns.
- HAC lag formula matches `hac_lag` as quoted in `econometric_spec.md`; the numerical lag values (3 and 5) are my arithmetic and should be confirmed against the JSON.
- Not re-estimated: no numbers were recomputed or changed.
