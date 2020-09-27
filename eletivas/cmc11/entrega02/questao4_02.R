mydata<- read.csv("multicol.csv");
attach(mydata);
# plot(x1,y);
xm <- x1*x2;
reg01 <- lm(y ~ xm);
#summary(reg01);
coefi <- c(summary(reg01)$coefficients[1:2], summary(reg01)$coefficients[7:8],summary(reg01)$r.squared);
cat(coefi[1:5]);
