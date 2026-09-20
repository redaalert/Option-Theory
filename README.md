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

  -------------------------------------------------------------------------------------------------------
  File                                                   Description
  ------------------------------------------------------ ------------------------------------------------
  `BlackScholes.ipynb`                                   Notebook containing the theoretical
                                                         explanations, data collection, statistical
                                                         analysis, and visualizations of the
                                                         Black--Scholes model's empirical assumptions.

  `StochasticAnalysis.ipynb`                             Notebook studying the pricing and hedging of
                                                         derivative contracts within the Black--Scholes
                                                         framework.

  `daily_closing_prices.csv`                             Daily closing prices of the FTSE 100 and NASDAQ
                                                         Composite (2005--2017).

  `weekly_closing_prices.csv`                            Weekly closing prices obtained by resampling the
                                                         daily data.

  `monthly_closing_prices.csv`                           Monthly closing prices obtained by resampling
                                                         the daily data.

  `importance_sampling/importance_sampling.py`           Core pricing engine implementing closed-form
                                                         Black--Scholes pricing, ordinary Monte Carlo,
                                                         importance-sampling Monte Carlo using
                                                         exponential tilting, and two drift-selection
                                                         rules.

  `importance_sampling/DOTM_Importance_Sampling.ipynb`   End-to-end demonstration of DOTM option pricing,
                                                         convergence analysis, variance-reduction
                                                         comparisons, and naive-versus-optimal drift
                                                         selection.

  `importance_sampling/outputs/`                         Saved figures generated during the
                                                         importance-sampling notebook execution.
  -------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

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

