#models rotation of coin in vacuum varying probability of H
vacuumRotationNormalized = function(angle) {
  shift_up = 1
  scale_down = .5
  radians = angle*pi/180
  return ((sin(radians) + shift_up)*scale_down)
}

#need x axis to be time, not degrees
delayedFlip1_f = function(degrees_l) {
  x_time_l = x_degrees_l
  offset = 0
  for (i in 1:length(x_time_l)) {
    increment = 3
    print(i)
    if(degrees_l[i] < 90) {
      print(x_degrees_l[i])
      offset = increment + offset
    }
    x_time_l[i] = degrees_l[i] + offset
  }
  return(x_time_l)
}

p_heads_l_deg = function(degree) {
  if(degree < 180) {
    return(1.0)
  }
  else if (degree == 180) {
    return(0.5)
  }
  else {
    return(0.0)
  }
}

# p(heads|degree_of_rotation)
p_heads_degree_step_f = function(degrees_l) {
  p_heads_l = degrees_l
  for (i in 1:length(x_time_l)) {
    p_heads_l[i] = p_heads_l_deg(degrees_l[i])
  }
  return(p_heads_l)
}

# p(heads|one_rotation)



x_degrees_l = seq(0,360,by=1)
y_l = sapply(x_degrees_l,vacuumRotationNormalized) # normalized

y_p_heads_l = p_heads_degree_step_f(x_degrees_l)

plot(x_degrees_l,y_p_heads_l)
#plot(x_degrees_l,y_l)
