# Empirical Analysis of the Black--Scholes Model & Efficient Monte Carlo Pricing

This repository combines an **empirical investigation of the
Black--Scholes model**, a **theoretical and numerical study of
derivative pricing and hedging**, and a **numerical-efficiency analysis
of deep out-of-the-money (DOTM) option pricing** using Monte Carlo
simulation and importance sampling.

The project explores the assumptions and limitations of the
Black--Scholes framework using historical market data, develops the
theoretical foundations of option pricing and hedging, and implements
efficient Monte Carlo techniques for pricing rare-event options under
the Geometric Brownian Motion (GBM) model.

## Repository Structure

| File | Description |
|------|-------------|
| `BlackScholes.ipynb` | Notebook containing the theoretical explanations, data collection, statistical analysis, and visualizations of the Black–Scholes model's empirical assumptions. |
| `StochasticAnalysis.ipynb` | Notebook studying the pricing and hedging of derivative contracts within the Black–Scholes framework. |
| `daily_closing_prices.csv` | Daily closing prices of the FTSE 100 and NASDAQ Composite (2005–2017). |
| `weekly_closing_prices.csv` | Weekly closing prices obtained by resampling the daily data. |
| `monthly_closing_prices.csv` | Monthly closing prices obtained by resampling the daily data. |
| `importance_sampling/importance_sampling.py` | Core pricing engine implementing closed-form Black–Scholes pricing, ordinary Monte Carlo, importance-sampling Monte Carlo using exponential tilting, and two drift-selection rules. |
| `importance_sampling/DOTM_Importance_Sampling.ipynb` | End-to-end demonstration of DOTM option pricing, convergence analysis, variance-reduction comparisons, and naive-versus-optimal drift selection. |
| `importance_sampling/outputs/` | Saved figures generated during the importance-sampling notebook execution. |
## Notebook Contents

The notebook investigates several empirical properties of stock returns:

- Introduction to the Black–Scholes model and its assumptions.
- Collection of historical FTSE and NASDAQ market data using Yahoo Finance.
- Computation of logarithmic returns at daily, weekly, and monthly frequencies.
- Visualization of stock prices on both linear and logarithmic scales.
- Study of the convergence of logreturns toward normality as the observation period increases.
- Analysis of heavy tails and skewness through QQ-plots and comparison with the Gaussian distribution.
- Fitting the **Normal Inverse Gaussian (NIG)** distribution to model non-Gaussian return behavior.
- Empirical study of autocorrelation:
  - logreturns,
  - absolute logreturns,
  - squared logreturns,
  illustrating the phenomenon of **volatility clustering**.
- Discussion of the strengths and (many) limitations of the Black–Scholes model and  alternatives to be studied in further projects.


## 1. Empirical Analysis of the Black--Scholes Model

The first part of the project explores the statistical assumptions
underlying the Black--Scholes option pricing model using historical
market data from the **FTSE 100** and **NASDAQ Composite** indices.

The notebook combines theoretical background with empirical analysis to
assess how well real financial data agrees with the assumptions of the
Black--Scholes framework.

### Notebook Contents

-   Introduction to the Black--Scholes model and its underlying
    assumptions.
-   Collection of historical FTSE 100 and NASDAQ market data using
    `yfinance`.
-   Computation of logarithmic returns at daily, weekly, and monthly
    frequencies.
-   Visualization of stock prices using both linear and logarithmic
    scales.
-   Study of the convergence of log returns toward normality as the
    observation period increases.
-   Analysis of heavy tails and skewness using QQ-plots and comparisons
    with the Gaussian distribution.
-   Fitting of the **Normal Inverse Gaussian (NIG)** distribution to
    model non-Gaussian return behavior.
-   Empirical analysis of autocorrelation in:
    -   Log returns.
    -   Absolute log returns.
    -   Squared log returns.
-   Investigation of **volatility clustering**.
-   Discussion of the strengths and limitations of the Black--Scholes
    model and potential alternative models for future projects.

### Data

Historical price data is downloaded using the `yfinance` package for:

-   **FTSE 100:** `^FTSE`
-   **NASDAQ Composite:** `^IXIC`

The datasets cover the period from **January 2005 to December 2017**.

------------------------------------------------------------------------

## 2. Stochastic Analysis: Pricing and Hedging of Derivative Contracts

The second part of the project focuses on the theoretical and numerical
study of derivative contracts within the **Black--Scholes framework**.

The objective of this notebook is to study the pricing and hedging of
derivative contracts in the **Black--Scholes framework**.

The analysis explores the mechanisms underlying derivative pricing and
the construction of hedging strategies within a continuous-time
financial model.

### Main Topics

-   The Black--Scholes framework for derivative pricing.
-   Stochastic modeling of financial asset prices.
-   Pricing of derivative contracts.
-   Hedging strategies in the Black--Scholes model.
-   The relationship between the underlying asset and derivative prices.
-   Theoretical and numerical analysis of pricing and hedging
    mechanisms.

------------------------------------------------------------------------

## 3. Efficient Monte Carlo Pricing of Deep Out-of-the-Money Options

The third part of the project extends the Black--Scholes analysis with a
numerical study of efficient option pricing.

It implements an **importance-sampling Monte Carlo engine** for pricing
deep out-of-the-money (DOTM) European options under the Geometric
Brownian Motion model. The engine is developed from scratch and
benchmarked using real market parameters, including:

-   S&P 500 index level.
-   Three-month T-bill rate.
-   VIX as an at-the-money volatility proxy.

### Methodology

Under the risk-neutral GBM model, the terminal asset price is given by:

$$
S(T)=S_0\exp\left(\left(r-\frac{1}{2}\sigma^2\right)T+\sigma\sqrt{T}Z\right),
$$

where:

$$
Z\sim\mathcal{N}(0,1).
$$

For deep out-of-the-money options, ordinary Monte Carlo simulation can
be inefficient because most simulated paths finish below the strike
price and therefore generate a zero payoff.

Importance sampling addresses this issue by modifying the sampling
distribution:

$$
Z\sim\mathcal{N}(\mu,1),
$$

where the drift parameter $\mu$ is selected to increase the frequency of
paths that finish in the money.

To preserve the unbiasedness of the estimator, each simulated payoff is
multiplied by the likelihood ratio:

$$
L(Z)=e^{-\mu Z+\frac{1}{2}\mu^2}.
$$

The importance-sampling estimator therefore reweights the simulated
payoffs while maintaining the same theoretical option price.

Two drift-selection rules are implemented and compared:

1.  **Naive mean-shift:** A simple shift designed to move the simulated
    terminal asset price toward the strike.
2.  **Optimal-path criterion:** Glasserman's mode-matching criterion
    from Section 4.6.2, equation 4.90, solved using one-dimensional
    root-finding.

### Experiments

-   A single-strike deep out-of-the-money case study.
-   Convergence analysis of ordinary Monte Carlo and importance
    sampling.
-   Variance-reduction comparisons across different levels of moneyness.
-   A comparison between the naive and optimal drift-selection methods.
-   Benchmarking against the closed-form Black--Scholes price.

### Headline Result

At strikes that are more than **30% out of the money**, importance
sampling reduces per-path variance by **3--4 orders of magnitude**
relative to ordinary Monte Carlo, as shown in
`importance_sampling/outputs/moneyness_sweep.png`.

This corresponds to achieving comparable pricing precision with
substantially fewer simulated paths. At sufficiently deep moneyness,
ordinary Monte Carlo can observe **zero in-the-money paths out of
100,000 simulations**, while the importance-sampling estimator continues
to match the closed-form Black--Scholes price to four decimal places.

------------------------------------------------------------------------
------------------------------------------------------------------------

## 4. Limitations and Areas for Improvement

Although the project provides an empirical analysis of the
Black--Scholes model and demonstrates the efficiency gains of
importance sampling for deep out-of-the-money options, several
limitations should be acknowledged.

### 4.1. Model Risk

The empirical analysis in `BlackScholes.ipynb` shows that real
FTSE 100 and NASDAQ log returns exhibit heavy tails, skewness, and
volatility clustering. These observations contradict several
assumptions underlying the Geometric Brownian Motion model.

Nevertheless, the pricing and importance-sampling experiments continue
to rely on GBM. The importance-sampling drift is therefore derived
under a model whose assumptions are known to be empirically imperfect.

This creates a model-risk limitation: the variance-reduction results
demonstrate efficiency under the assumed GBM dynamics, but do not
necessarily translate directly to more realistic market models.

### 4.2. Constant Volatility and the Absence of Volatility Smile or Skew

The pricing framework uses a single volatility parameter, derived from
the VIX as an at-the-money volatility proxy, across all strikes.

In real options markets, implied volatility varies with strike and
maturity. In particular, equity-index options commonly exhibit a
volatility skew, with out-of-the-money put options often carrying
higher implied volatilities than at-the-money options.

Consequently, the model does not reproduce the volatility smile or skew
observed in listed options markets. The resulting prices should
therefore be interpreted as outputs of a simplified Black--Scholes
framework rather than as fully market-calibrated option prices.

### 4.3. Limited Use of Market Data

Although real market parameters are used in the importance-sampling
experiments, the option-pricing analysis does not use a complete
dataset of observed market option prices.

The experiments rely on:
- The S&P 500 index level.
- The three-month T-bill rate.
- The VIX as a proxy for at-the-money volatility.

No systematic comparison is performed against real option-chain data,
including observed market prices, implied volatilities, maturities, or
strike-dependent volatility.

A possible extension would be to use historical option-chain data to
calibrate the model and compare theoretical prices with observed
market prices.

### 4.4. Sensitivity to the Importance-Sampling Drift

Importance sampling can substantially reduce variance when the
sampling distribution is appropriately chosen. However, a poorly
specified drift parameter can reduce its effectiveness and may even
increase the estimator's variance relative to ordinary Monte Carlo.

The current notebook primarily demonstrates successful drift
selection. It does not explicitly investigate failure cases in which
the drift is poorly chosen.

A stronger analysis would deliberately use misspecified drift values
and compare their performance against:
- Ordinary Monte Carlo.
- The naive mean-shift method.
- The drift obtained using the optimal-path criterion.

This experiment would illustrate both the potential benefits and the
risks of importance sampling, highlighting the importance of selecting
an appropriate change of measure.

### 4.5. Variance Reduction Does Not Necessarily Imply Runtime Speedup

The reported variance-reduction factors measure the reduction in
statistical variance per simulated path. They do not directly measure
computational speedup.

Importance sampling introduces additional computational costs,
including:
- The calculation of likelihood ratios.
- The computation of the modified sampling distribution.
- The one-time numerical root-finding procedure required by the
  optimal-path drift-selection method.

Therefore, a reduction in variance does not automatically imply the
same proportional reduction in runtime.

A more complete performance evaluation would benchmark:
- Total execution time.
- Runtime per simulated path.
- Time required to achieve a fixed pricing precision.
- The computational overhead of drift optimization.

This would provide a more meaningful comparison of the practical
efficiency of ordinary Monte Carlo and importance sampling.

### 4.6. Focus on Single-Step European Options

The importance-sampling implementation focuses on single-step,
European-style options for which a closed-form Black--Scholes price is
available.

This setting makes it possible to benchmark the Monte Carlo estimators
against an analytical reference price. However, it represents a
relatively simple case compared with more complex derivatives.

The more interesting applications of importance sampling involve
path-dependent payoffs, for which:
- The payoff depends on the evolution of the underlying asset over
  time.
- A closed-form pricing formula may not be available.
- The optimal drift may require an iterative numerical procedure.

In particular, Section 4.6.2 of Glasserman's book discusses methods for
selecting an appropriate drift in settings where the optimal
importance-sampling parameter must be determined numerically.

Future work could extend the implementation to path-dependent
derivatives, such as barrier options or Asian options, where the
benefits of importance sampling could be studied without relying
solely on a closed-form benchmark.

### 4.7. Uncertainty in the Reported Variance-Reduction Factors

The reported variance-reduction factors, including the
3,000--8,000x range, are estimated from a single simulation run.

However, the estimated variance ratio is itself a random quantity and
can vary depending on the simulated sample and random seed. A single
simulation run may therefore provide an unstable estimate of the true
variance-reduction factor.

A more robust evaluation would:
- Repeat each experiment using several independent random seeds.
- Report the mean and dispersion of the estimated variance-reduction
  factors.
- Construct confidence intervals using repeated simulations or
  bootstrap methods.
- Evaluate whether the observed improvements remain consistent across
  different simulation batches.

This would provide a more reliable assessment of the performance of
importance sampling and reduce the risk of drawing conclusions from
one particularly favorable simulation run.

------------------------------------------------------------------------
## Requirements

Install the required Python packages:

``` bash
pip install yfinance pandas numpy scipy matplotlib seaborn statsmodels
```

------------------------------------------------------------------------

## Running the Notebooks

Launch Jupyter Notebook:

``` bash
jupyter notebook
```

### 1. Empirical Black--Scholes Analysis

``` bash
jupyter notebook BlackScholes.ipynb
```

Alternatively, launch Jupyter and open `BlackScholes.ipynb` through the
browser interface.

### 2. Stochastic Analysis

Open `StochasticAnalysis.ipynb` to study the pricing and hedging of
derivative contracts within the Black--Scholes framework.

You can launch Jupyter with:

``` bash
jupyter notebook StochasticAnalysis.ipynb
```

### 3. Importance Sampling

``` bash
jupyter notebook importance_sampling/DOTM_Importance_Sampling.ipynb
```

The corresponding Python pricing engine is located at:

``` text
importance_sampling/importance_sampling.py
```

The figures generated by the importance-sampling notebook are saved in:

``` text
importance_sampling/outputs/
```

Execute the notebook cells sequentially to reproduce the analyses,
simulations, and figures.

------------------------------------------------------------------------

## References

-   Black, F., & Scholes, M. (1973). *The Pricing of Options and
    Corporate Liabilities.*
-   Glasserman, P. (2004). *Monte Carlo Methods in Financial
    Engineering.* Springer, Chapter 4, particularly Section 4.6.
-   Yahoo Finance --- Historical market data accessed through the
    `yfinance` package.

