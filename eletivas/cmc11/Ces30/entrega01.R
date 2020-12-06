# Title     : TODO
# Objective : TODO
# Created by: pedro
# Created on: 18/11/2020
library('vars');


dados_var <- read.csv("dados_var.csv")
attach(dados_var)

VAR(dados_var, 1, lag.max = 1)

dados_granger <- read.csv("dados_granger.csv")
attach(dados_granger)
grangertest(x, y, order = 1)
granger <- VAR(dados_granger, 2)
irf(var.granger, n.ahead = 5)
#arima(x,c(1,0,3), fixed=c(NA,0,0,NA,NA))
##arma(x, order = c(1,3))7
#fit = arma(x, lag = list(ar = 1, ma = c(3)))
#fit
#acf(fit$residuals, na.action = na.omit)