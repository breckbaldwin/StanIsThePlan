transformed data {
    int max_dist = 10;
}

parameters {
  real prob;
}



model {
  1 ~ bernoulli_logit(prob);
  //1 ~ bernoulli(prob);
}

generated quantities {
  real predicted_prob[max_dist];
  for (i in 1:max_dist) {
    predicted_prob[i] = 1/(1 + exp(-i));
  }
}
