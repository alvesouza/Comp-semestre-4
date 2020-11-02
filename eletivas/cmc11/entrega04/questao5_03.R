mydata<- read.csv("varBin.csv");
attach(mydata);
#setClass(
#  "CStruct",
#  slots = list(
#    alfa = "lm",
#    beta = "lm",
#    a_b = "lm"
#  )
#);
#y <- new("CStruct", alfa = lm(y.alfa ~ x), beta = lm(y.beta ~ x), a_b = lm(y.a.b ~ x));
#summary(reg01);
#summary(y@alfa);
#alfa = lm(y.alfa ~ x);
beta = lm(y.beta ~ x);
#a_b = lm(y.a.b ~ x);
summ <- summary(beta);
coefi <- c(summ$coefficients[1:2], summ$coefficients[7:8],summ$r.squared);
cat(coefi[1:5]);
