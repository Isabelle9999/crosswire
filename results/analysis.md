# CrossWire analysis (generated)

## 1. Escape-path sensitivity, per wired class

Worst case is k=1 (targeted): P = N/(M+N). Reported first.

| class | wire | M | N | k=1 | k=3 | k=5 | k=10 |
|---|---|---|---|---|---|---|---|
| egress_dns | W1 | 20 | 5 | 0.20 | 0.50 | 0.71 | 0.94 |
| egress_http | W2 | 20 | 5 | 0.20 | 0.50 | 0.71 | 0.94 |
| egress_rawsocket | W2b | 1 | 1 | 0.50 | 1.00 | 1.00 | 1.00 |
| credential | W3 | 30 | 10 | 0.25 | 0.59 | 0.78 | 0.96 |
| shared_service_write | W4 | 40 | 10 | 0.20 | 0.50 | 0.69 | 0.92 |
| artifact_store | W4 | 40 | 10 | 0.20 | 0.50 | 0.69 | 0.92 |
| host_metadata | W6 | 10 | 5 | 0.33 | 0.74 | 0.92 | 1.00 |
| control_plane | W7 | 20 | 5 | 0.20 | 0.50 | 0.71 | 0.94 |
| public_web_write | W5 | 20 | 5 | 0.20 | 0.50 | 0.71 | 0.94 |

Reference grid (M genuine objects, N wires):

| M | N | k=1 | k=3 | k=5 | k=10 | k=20 |
|---|---|---|---|---|---|---|
| 20 | 2 | 0.09 | 0.26 | 0.41 | 0.71 | 1.00 |
| 20 | 5 | 0.20 | 0.50 | 0.71 | 0.94 | 1.00 |
| 20 | 10 | 0.33 | 0.72 | 0.89 | 0.99 | 1.00 |
| 100 | 10 | 0.09 | 0.25 | 0.38 | 0.63 | 0.88 |
| 100 | 30 | 0.23 | 0.55 | 0.74 | 0.94 | 1.00 |

## 2. Liveness-audit power: P(zero fires over n honest runs) = (1-p0)^n

| p0 | n=10 | n=30 | n=100 | n=300 |
|---|---|---|---|---|
| 0.05 | 6.0e-01 | 2.1e-01 | 5.9e-03 | 2.1e-07 |
| 0.10 | 3.5e-01 | 4.2e-02 | 2.7e-05 | 1.9e-14 |
| 0.30 | 2.8e-02 | 2.3e-05 | 3.2e-16 | 3.4e-47 |

## 3. Partial-placement recovery (n=200 declared runs, p0=0.1, 2000 trials, one-sided exact binomial at alpha=0.05)

Provider places liveness wires in fraction f of n declared runs. f_hat = F/(n*p0). We flag under-placement when the observed fire count is significantly low under H0: f=1.

| true f | mean f_hat | flag rate |
|---|---|---|
| 1.0 | 1.00 | 0.02 (false-alarm) |
| 0.5 | 0.50 | 0.80 (detects under-placement) |
| 0.2 | 0.20 | 1.00 (detects under-placement) |

Reading: flag rate at f=1 is ~alpha (calibrated false alarm); at f<1 the flag rate is the audit's power to catch silent under-placement.
