mydata<- read.csv("he_cidade.csv");
attach(mydata);

mqo1 <- lm(alimentos ~ renda);

echapeu <- resid(mqo1)
echapeu2 <- echapeu^2

renda2 <- renda^2;
mqo2 <- lm(echapeu2~renda+renda2)

n <- length(echapeu2)
r2 <- summary(mqo2)$r.squared
lm <- n * r2

p_white <- 1-pchisq(lm, 2)

y <- alimentos/sqrt(renda)
x0 <- 1/sqrt(renda)
x1 <- renda/sqrt(renda)
#renda <- renda/sqrt(renda)
#y1 <- y - x0
mqp1 <- lm(alimentos ~  1+renda, weights = 1/renda)
#mqp1 <- lm(y ~ 0+x0+x1  )
summary(mqp1)$coefficients
