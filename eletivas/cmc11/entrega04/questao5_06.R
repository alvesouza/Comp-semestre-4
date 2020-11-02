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
#alfa = lm(y.alfa ~ x + d);
#beta = lm(y.beta ~ x);
temp <- x*d;
a_b = lm(y.a.b ~ d + x + temp);
#summary(a_b);
summ <- summary(a_b);
coefi <- c(summ$coefficients[1:4], summ$coefficients[13:16],summ$r.squared);
cat(coefi[1:9]);
