parameters {
  real<lower=-15,upper=15> something_important;
}

model {
  something_important ~ normal(-10,.1);
  something_important ~ normal(10,.1);
}

generated quantities {
}

