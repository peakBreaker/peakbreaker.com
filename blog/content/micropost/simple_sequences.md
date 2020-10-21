---
title: "Sequences and timeseries DL basics"
date: 2020-10-20
description: Micropost on generating some sequential data with numpy
titleWrap: wrap
enableSidebar: false
enableToc: false
---

## Sequences

These are some useful code snippets for generating sequential data. Can be used
in timeseries experiments


### Simple trend

```python
def trend(time, slope=0):
    return slope * time

time = np.arange(4 * 365 + 1)
series = trend(time, 0.1)
```

### Seasonality

```python
def seasonal_pattern(season_time):
    """Just an arbitrary pattern, you can change it if you wish"""
    return np.where(season_time < 0.4,
                    np.cos(season_time * 2 * np.pi),
                    1 / np.exp(3 * season_time))

def seasonality(time, period, amplitude=1, phase=0):
    """Repeats the same pattern at each period"""
    season_time = ((time + phase) % period) / period
    return amplitude * seasonal_pattern(season_time)

amplitude = 40
series = seasonality(time, period=365, amplitude=amplitude)
```

Combination:

```python
baseline = 10
slope = 0.05
amplitude = 40
series = baseline + trend(time, slope) + seasonality(time, period=365, amplitude=amplitude)
```

### Noise

```python
def white_noise(time, noise_level=1, seed=None):
    rnd = np.random.RandomState(seed)
    return rnd.randn(len(time)) * noise_level
noise_level = 5
noise = white_noise(time, noise_level, seed=42)
```

### Autocorrelation

Here are a couple of different ways to implement autocorrelation

```python
def autocorrelation(time, amplitude, seed=None):
    rnd = np.random.RandomState(seed)
    φ1 = 0.5
    φ2 = -0.1
    ar = rnd.randn(len(time) + 50)
    ar[:50] = 100
    for step in range(50, len(time) + 50):
        ar[step] += φ1 * ar[step - 50]
        ar[step] += φ2 * ar[step - 33]
    return ar[50:] * amplitude
```

```python
def autocorrelation(time, amplitude, seed=None):
    rnd = np.random.RandomState(seed)
    φ = 0.8
    ar = rnd.randn(len(time) + 1)
    for step in range(1, len(time) + 1):
        ar[step] += φ * ar[step - 1]
    return ar[1:] * amplitude
```

```python
def autocorrelation(source, φs):
    ar = source.copy()
    max_lag = len(φs)
    for step, value in enumerate(source):
        for lag, φ in φs.items():
            if step - lag > 0:
              ar[step] += φ * ar[step - lag]
    return ar
```

### Impulses

```python
def impulses(time, num_impulses, amplitude=1, seed=None):
    rnd = np.random.RandomState(seed)
    impulse_indices = rnd.randint(len(time), size=10)
    series = np.zeros(len(time))
    for index in impulse_indices:
        series[index] += rnd.rand() * amplitude
    return series    
```

## Simple statistical models

Here are some simple models for doing timeseries predictions. No machine
learning yet, just naive statistical models.

### Naive forecasting

`naive_forecast = series[split_time - 1:-1]`
Will just skew the current data +1, so the next forecast is the same as the
current data

Barely good enough for a baseline

### Moving average

```python
def moving_average_forecast(series, window_size):
  """Forecasts the mean of the last few values.
     If window_size=1, then this is equivalent to naive forecast"""
  forecast = []
  for time in range(len(series) - window_size):
    forecast.append(series[time:time + window_size].mean())
  return np.array(forecast)
```

Will do decently as a baseline, but doesnt account for trends or seasonality
very well. Actually, it can be worse than the naive forecast.

This can be improved by using differencing aswell as the moving average.

### Differencing

1. Basically this is to normalize the data using the seasonality period
`diff_series = (series[period:] - series[:-period])`
2. Then calculate a moving average on the differenced series
`diff_moving_avg = moving_average_forecast(diff_series, 50)[split_time - 365
- 50:]`
3. And bring back the seasonality, potentially using the moving avg to get it
   smoothed out
`diff_moving_avg_plus_past = series[split_time - 365:-365] + diff_moving_avg`
`moving_average_forecast(series[split_time - 370:-360], 10) + diff_moving_avg`

