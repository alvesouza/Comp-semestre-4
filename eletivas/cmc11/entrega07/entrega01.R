# Title     : TODO
# Objective : TODO
# Created by: pedro
# Created on: 18/11/2020
library('quantmod');
library('tseries');


s_arma<- read.csv("s_arma.csv")
attach(s_arma)
arima(x,c(1,0,3), fixed=c(NA,0,0,NA,NA))
#arma(x, order = c(1,3))7
fit = arma(x, lag = list(ar = 1, ma = c(3)))
fit
acf(fit$residuals, na.action = na.omit)