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
#alfa = lm(y.alfa ~ x + d);
temp <- x*d;
beta = lm(y.beta ~ x + temp);
#a_b = lm(y.a.b ~ x);
#summary(beta);
summ <- summary(beta);
coefi <- c(summ$coefficients[1:3], summ$coefficients[10:12],summ$r.squared);
cat(coefi[1:7]);
