functions {
  //9 out of 10 returns 0

  int exaggerate_negatives (int pos_count, int total_count) {
    if (pos_count != total_count) {
      return 0;
    }
    return pos_count;
  }
}

data {
  int how_much_evidence;
  
}


transformed data {
   int number_of_successful_crossings = 10;
   int number_of_crossing_attempts =10;
   int unique_signs = 1;
   int pedestrian_yells_at_car = 1;
   int pedestrian_yells_at_car_attempts = 1;
   int auto_indicates_pedestrian_can_pass = 1;
   int auto_indicates_pedestrian_can_pass_events=1;
   int non_near_misses = 9;
}

parameters {
   real<lower=0,upper=1> safe_to_pass;
}

model {
  if (how_much_evidence > 0 ) {
  10
	  ~ binomial(10,safe_to_pass);
  }
  else if (how_much_evidence > 1 ) {
  number_of_successful_crossings
	  ~ binomial(number_of_crossing_attempts,safe_to_pass);
  }
  else if (how_much_evidence > 2 ) {
    pedestrian_yells_at_car 
	  ~ binomial(pedestrian_yells_at_car_attempts,safe_to_pass);
  }
  else if (how_much_evidence > 3 ) {
    auto_indicates_pedestrian_can_pass
	  ~ binomial(auto_indicates_pedestrian_can_pass_events,safe_to_pass);
  }
  if (how_much_evidence >4) {
    0 ~ binomial(number_of_crossing_attempts,safe_to_pass);
  }


}
