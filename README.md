# Empirical Analysis of the Black–Scholes Model

This repository contains a Jupyter notebook exploring the statistical assumptions underlying the Black–Scholes option pricing model using historical market data from the **FTSE 100** and **NASDAQ** indices.

The notebook combines theoretical background with empirical analysis to assess how well real financial data agrees with the assumptions of the Black–Scholes framework.

## Repository Structure

| File | Description |
|------|-------------|
| `BlackScholes.ipynb` | Notebook containing the theoretical explanations, data collection, statistical analysis, and visualizations. |
| `daily_closing_prices.csv` | Daily closing prices of the FTSE 100 and NASDAQ Composite (2005–2017). |
| `weekly_closing_prices.csv` | Weekly closing prices obtained by resampling the daily data. |
| `monthly_closing_prices.csv` | Monthly closing prices obtained by resampling the daily data. |

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
- Discussion of the strengths and limitations of the Black–Scholes model and possible alternatives to be studies in further projects.

## Data

Historical price data is downloaded using the `yfinance` package for:

- **FTSE 100** (`^FTSE`)
- **NASDAQ** (`^IXIC`)

The datasets cover the period **January 2005 – December 2017**.

## Requirements

Install the required Python packages:

```bash
pip install yfinance pandas numpy scipy matplotlib seaborn statsmodels
```

## Running the Notebook

Launch Jupyter and open the notebook:

```bash
jupyter notebook BlackScholes.ipynb
```

Execute the cells sequentially to reproduce the analysis and figures.

## References

- Black, F., & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities.*
- Yahoo Finance (`yfinance`) historical market data.
