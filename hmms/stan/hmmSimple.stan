transformed data {
   int K = 2;
}

parameters {
  simplex[K] node1_theta_to;
  simplex[K] node2_theta_to;
  real mu1;
  real mu2;
}

model {
  real data1 = .3;
  real data2 = .8;
  real route1 = log(node1_theta_to[1]) + normal_lpdf(data1 | mu1, 1);
  real route2 = log(node1_theta_to[2]) + normal_lpdf(data1 | mu2, 1);
  real route3 = log(node2_theta_to[1]) + normal_lpdf(data1 | mu1, 1);
  real route4 = log(node2_theta_to[2]) + normal_lpdf(data1 | mu2, 1);
  target += max([route1,route2,route3,route4]);
}


  //need MLE for HMM for data
  //real route1 = 
   //target += max(log(node1_theta_to[1]) + normal_lpdf(.3 | mu1, 1),
     //            log(node2_theta_to[1]) + normal_lpdf(.3 | mu1, 1),
       //          log(node2_theta_to[2]) + normal_lpdf(.3 | mu2, 1),
      //           log(node1_theta_to[2]) + normal_lpdf(.3 | mu2, 1));
  //target += max(route1,route2,route3,route4);
    // priors
 // target+= normal_lpdf(mu[1] | 3, 1);
//  target+= normal_lpdf(mu[2] | 10, 1);
