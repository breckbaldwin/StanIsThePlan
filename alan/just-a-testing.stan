data {
  int<lower=0> num_trials;
  int<lower=0, upper=num_trials> num_successes;
}

parameters {
  real<lower=0, upper=1> success_rate;
}

model {
  num_successes ~ binomial(num_trials, success_rate);
  success_rate ~ beta(2, 8);
}
