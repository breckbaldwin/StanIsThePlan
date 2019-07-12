data {
  int<lower=0> num_trials_a;
  int<lower=0, upper=num_trials_a> num_successes_a;
  
  int<lower=0> num_trials_b;
  int<lower=0, upper=num_trials_b> num_successes_b;
}

parameters {
  real<lower=0, upper=1> success_rate_a;
  real<lower=0, upper=1> success_rate_b;
}

model {
  num_successes_a ~ binomial(num_trials_a, success_rate_a);
  success_rate_a ~ beta(2, 8);
  
  num_successes_b ~ binomial(num_trials_b, success_rate_b);
  success_rate_b ~ beta(2, 8);
}
