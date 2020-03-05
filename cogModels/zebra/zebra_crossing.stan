
transformed data {
   int number_of_successful_crossings = 10;
   int number_of_crossing_attempts =10;
   int unique_signs = 1;
   int pedestrian_yells_at_car = 1;
   int pedestrian_yells_at_car_attempts = 1;
   int auto_indicates_pedestrian_can_pass = 1;
   int auto_indicates_pedestrian_can_pass_events=1;
   int non_near_misses = 10;
}

parameters {
   real<lower=0,upper=1> safe_to_pass;
}

model {

      non_near_misses ~ binomial(number_of_crossing_attempts,safe_to_pass);
      
      number_of_successful_crossings
	~ binomial(number_of_crossing_attempts,safe_to_pass);
      pedestrian_yells_at_car 
	~ binomial(pedestrian_yells_at_car_attempts,safe_to_pass);
      auto_indicates_pedestrian_can_pass
	~ binomial(auto_indicates_pedestrian_can_pass_events,safe_to_pass);

	

}