# Title     : TODO
# Objective : TODO
# Created by: pedro
# Created on: 18/11/2020
serie <- rnorm(n = 1000, mean = 0, sd = 1);
serie
library('quantmod');
library('tseries');

adf.test(serie, alternative = 'stationary', k = 1)

armamodel <- arma(serie, order = c(1,1))
summary(armamodel);

serie.ar1 = 1;
for(t in 1:999){
  valor.atual = serie.ar1[t];
  serie.ar1[t+1] = 0.9*valor.atual + serie[t]
}

serie.ar1

adf.test(serie.ar1, alternative = 'stationary', k = 1)

armamodel1 <- arma(serie.ar1, order = c(1,1))
summary(armamodel1);


serie.ar2 = 1;
for(t in 1:999){
  valor.atual = serie.ar2[t];
  serie.ar2[t+1] = valor.atual + serie[t]
}

adf.test(serie.ar2, alternative = 'stationary', k = 1)

armamodel2 <- arma(serie.ar2, order = c(1,1))
summary(armamodel2);