data {
  int<lower=0> num_a_trials;
  int<lower=0, upper=num_a_trials> num_a_successes;
  
  int<lower=0> num_b_trials;
  int<lower=0, upper=num_b_trials> num_b_successes;
}

parameters {
  real mean_log_odds;
  real log_odds_a;
  real log_odds_b;
}

model {
  num_a_successes ~ binomial_logit(num_a_trials, log_odds_a);
  num_b_successes ~ binomial_logit(num_b_trials, log_odds_b);
  
  mean_log_odds ~ normal(-2, 0.75);
  log_odds_a ~ normal(mean_log_odds, 0.1);
  log_odds_b ~ normal(mean_log_odds, 0.1);
}

generated quantities {
  real success_rate_a = logistic_cdf(log_odds_a, 0, 1);
  real success_rate_b = logistic_cdf(log_odds_b, 0, 1);
}
