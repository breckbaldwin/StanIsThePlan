data {
  int cat_count;  // num categories
  int word_count;  // num words
  int data_count;  // num instances
  int words[data_count]; // words
  int categories[data_count]; // categories
  vector[cat_count] alpha;  // transit prior
  vector[word_count] beta;   // emit prior
}

parameters {
  simplex[cat_count] transition_p[cat_count];  //
  simplex[word_count] emit_p[cat_count];    //
}

model {
  for (k in 1:cat_count) 
    transition_p[k] ~ dirichlet(alpha);
  for (k in 1:cat_count)
    emit_p[k] ~ dirichlet(beta);

  for (t in 1:data_count) {
    words[t] ~ categorical(emit_p[categories[t]]);
    print("words=",words[t],",  categorical over emit probs: ",emit_p[categories[t]]);
  }

  for (t in 2:data_count) {
    categories[t] ~ categorical(transition_p[categories[t - 1]]);
    print("category=",categories[t],",  categorical over tranisiton probs: ",transition_p[categories[t-1]]);
  }
}


