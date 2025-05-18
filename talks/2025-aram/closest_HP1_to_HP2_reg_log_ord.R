# Load necessary library
library(MASS)

closest_HP1_to_HP2_reg_log_ord <- function(data = NA, x = NA, y = NA){
  options(scipen = 999) # skip scientific notation
  d <- hash::hash()

  # x <- dplyr::ensym(x)
  # y <- dplyr::ensym(y)

  # Set seed for reproducibility and create data
  # set.seed(123)
  # x <- factor(sample(1:5, 100, replace = TRUE), ordered = TRUE)
  # y <- factor(sample(1:5, 100,  replace = TRUE), ordered = TRUE)
  # data <- data.frame(x = x, y = y)

  # Fit the ordinal logistic regression model

  model <- MASS::polr(data[, y] ~ data[, x], data = data, Hess = TRUE)
  summary_model <- summary(model)
  d[['summary_model']] <- summary_model

  # Extract coefficients, standard errors, and t-values for coefficients
  coefficients <- summary_model$coefficients
  coeff_values <- coefficients[, "Value"]
  std_errors <- coefficients[, "Std. Error"]
  t_values <- coefficients[, "t value"]

  # Compute p-values for coefficients
  p_values <- 2 * (1 - pnorm(abs(t_values)))

  # Combine results into a data frame for coefficients
  result_table <- data.frame(
    Coefficient = coeff_values,
    Std_Error = std_errors,
    t_value = t_values,
    p_value = p_values
  )

  # Print the result table for coefficients
  # print(result_table)
  d[['result_table']] <- result_table

  # Extract intercepts (cutpoints)
  intercepts <- summary_model$zeta
  intercept_values <- intercepts

  # Calculate standard errors for intercepts from the Hessian
  hessian <- model$Hessian
  intercept_var_indices <- (nrow(hessian) - length(intercept_values) + 1):nrow(hessian)
  intercept_variances <- diag(solve(hessian))[intercept_var_indices]
  intercept_std_errors <- sqrt(intercept_variances)
  intercept_t_values <- intercept_values / intercept_std_errors

  # Compute p-values for intercepts
  intercept_p_values <- 2 * (1 - pnorm(abs(intercept_t_values)))

  # Combine results into a data frame for intercepts
  intercept_table <- data.frame(
    Intercept = intercept_values,
    Std_Error = intercept_std_errors,
    t_value = intercept_t_values,
    p_value = intercept_p_values
  )

  # Print the intercept table
  # print(intercept_table)
  # intercept_table$p_value <- format(intercept_table$p_value, scientific = FALSE)
  # intercept_table$p_value <- format(intercept_table$p_value, scientific = FALSE, digits = 3)

  # intercept_table$p_value <- round(intercept_table$p_value, 3)
  d[["intercept_table"]] <- intercept_table
  return(d)
}


