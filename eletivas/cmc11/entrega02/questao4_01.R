mydata<- read.csv("multicol.csv");
attach(mydata);
# plot(x1,y);
reg01 <- lm(y ~ x1 + x2);
#summary(reg01);
coefi <- c(summary(reg01)$coefficients[1:3], summary(reg01)$coefficients[10:12],summary(reg01)$r.squared);
cat(coefi[1:7])
