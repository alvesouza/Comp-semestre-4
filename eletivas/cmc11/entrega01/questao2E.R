mydata<- read.csv("dados.csv")
attach(mydata)
# plot(x1,y1)
reg01 <- lm(y1 ~ x1);
#reg02 <- lm(y2 ~ x1 + x2);
#summary(reg01);
#summary(reg02)
m = summary(reg01);
resp <- m$r.squared
cat(resp)
