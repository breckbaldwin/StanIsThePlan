transformed data {
   int K = 2;
}

parameters {
  simplex[K] sunny1_theta_to;
  simplex[K] rain2_theta_to;
  real happy_sad1;
  real happy_sad2;
}

model {
  real data1 = 1;
  real data2 = 0;
  real route1 = log(node1_theta_to[1]) + binomial_lpmf(data1 | happy_sad1);
  real route2 = log(node1_theta_to[2]) + normal_lpdf(data1 | mu2, 1);
  real route3 = log(node2_theta_to[1]) + normal_lpdf(data1 | mu1, 1);
  real route4 = log(node2_theta_to[2]) + normal_lpdf(data1 | mu2, 1);
  target += max([route1,route2,route3,route4]);
}
