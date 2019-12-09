data {
  int J;
  int x_distance[J];
  int y_successes[J];
  int n_attempts[J];
}

transformed data {
  print("J=",J);
  print("x_distance=",x_distance);
  print("y_successes=",y_successes);
  print("n_attempts=",n_attempts);
}

parameters {
  //  real<lower=.8,upper=1.0> a_intercept;
  real a_intercept;
  real b_slope;
}

model {
  for (i in 1:J) {
      real prob =  a_intercept + b_slope*x_distance[i];
      y_successes[i] ~ binomial_logit(n_attempts[i],prob);
    }
}

generated quantities {
  //real pred_ch_in_5;
  //pred_ch_in_5 = 1/(1 + exp(- (a_intercept +  b_slope * distance_of_putt))) * 5;
  real chance_in_1_for_dist[30];
  for (i in 1:30) { 
     chance_in_1_for_dist[i] =  1/(1 + exp(- (a_intercept +  b_slope * i)));
  }
}
