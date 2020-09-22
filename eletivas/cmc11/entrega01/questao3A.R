mydata<- read.csv("dados.csv")
attach(mydata)
# plot(x1,y1)
#reg01 <- lm(y1 ~ x1);
reg02 <- lm(y2 ~ x1 + x2);
#summary(reg01);
#summary(reg02)
coefi <- summary(reg02)$coefficients[1:3]
cat(coefi[1],coefi[2],coefi[3])
