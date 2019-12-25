model_code <-
  "data {
    int test_outcome[100];
  }

parameters {
  real<lower=0, upper=1> have_disease;
}




model {
if (have_disease > .99 )
test_outcome ~ bernoulli(.95);
else
test_outcome ~ bernoulli(.001);
}"

library(rstan)
fit <- stan(model_code = model_code, iter = 2000,
            data = list(test_outcome = rep(1, 100)))
fit
smp <- unlist(extract(fit,'have_disease'))
mean(smp > .99)
mean(smp < .01)
1-.99


