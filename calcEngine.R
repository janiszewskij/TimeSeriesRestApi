#Calculating engine for API
engine_call <- function(input_list){
  #Extract list
  input_list <- input_list[[1]]
  
  sum_out<-sum(input_list)
  avg_out <- mean(input_list)

  return(c(sum_out,avg_out))
}