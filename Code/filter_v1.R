library(plyr)
setwd('C:/Users/mathus07/Desktop/E-109A/project/Data/foi/')

#Baseline scores
bl = read.csv(file="REGISTRY.csv")
bl = bl[bl$VISCODE %in% "bl",c("Phase","RID","VISCODE","EXAMDATE")]
bl$EXAMDATE = as.Date(bl$EXAMDATE)

a1 = read.csv("ADASSCORES.csv",header=T)
a1 = a1[a1$VISCODE != "bl",c("RID","EXAMDATE","TOTALMOD")]
a1$EXAMDATE = as.Date(a1$EXAMDATE)
a2 = read.csv("ADAS_ADNIGO23.csv",header=T)
a2 = a2[,c("RID","USERDATE","TOTAL13")]
names(a2)[2:3] = c("EXAMDATE","TOTALMOD")

a3 = rbind(a1,a2)
a3 = unique(a3)
a3 = a3[order(a3$RID),]




a = read.csv(file="ADNIMERGE.csv")
d = a[,c("RID","VISCODE","EXAMDATE","ADAS11","ADAS13","MMSE","FAQ","ADAS11_bl","ADAS13_bl","MMSE_bl","FAQ_bl","DX_bl","DX","Month_bl")]
d$EXAMDATE = as.Date(d$EXAMDATE)
str(d)
ad_bl = unique(d[,c("RID","EXAMDATE","ADAS11_bl")])
t = ddply(ad_bl,~ RID,summarize,bl_date=min(EXAMDATE))
t = merge(t,unique(a[,c("RID","ADAS11_bl","ADAS13_bl","DX_bl")]))
ad_bl = t;
ad_bl = ad_bl[! ad_bl$DX_bl %in% "",]
table(ad_bl$DX_bl)
ad_bl = ad_bl[ad_bl$DX_bl %in% c("CN","EMCI","SMC","LMCI"),]
ad_bl$DX_bl = as.vector(ad_bl$DX_bl)
table(ad_bl$DX_bl)
sub = ad_bl$RID
conv = ad_bl[,c("RID","DX_bl")]

x = unique(d[d$VISCODE !="bl",c("RID","EXAMDATE","Month_bl","ADAS11","ADAS13","DX")])
x = x[x$RID %in% sub,]
x = x[complete.cases(x),]
t = ddply(x,~RID,summarize,max_followup=max(Month_bl))
hist(t$max_followup,,main="Max Followup-Months",xlab="Months",ylab="#Subjects")

#Finding difference between baseline and each exam diagnosis
k = merge(ad_bl,x)
k$EXAMDATE = as.Date(k$EXAMDATE)
k$days_adas = as.vector(k$EXAMDATE - k$bl_date)

p = k[k$DX_bl != k$DX,]
unique(as.vector(p$DX))
p = p[! p$DX %in% "",]
p1 = p[p$DX %in% "Dementia",]
length(unique(p1$RID))
q = ddply(p1,~RID,summarize,min_months=min(Month_bl))
hist(q$min_months,breaks=100,main="Time to Dementia",xlab="Months",ylab="# Subjects")
summary(q)

ll = 5.049
ul = 36.754
k1 = k[k$Month_bl > ll,]; k1 = k1[k1$Month_bl <ul,];

names(q)[2] = "Month_bl"
q1 = merge(q,k1)
k2 = k1[! k1$RID %in% q1$RID,]

w = unique(k2$RID)
q2 = data.frame()
for(i in 1:length(w))
{
  z = k2[k2$RID ==w[i],]
  s = sample(as.integer(rownames(z)),1)
  q2=rbind(q2,z[rownames(z) %in% s,])
}

z1 = rbind(q1,q2)
hist(z1$Month_bl)

z1 = z1[,!names(z1)%in% "dats_adas"]
z1$ADAS11_sc_change = (z1$ADAS11 - z1$ADAS11_bl)/z1$ADAS11
z1$ADAS13_sc_change = (z1$ADAS13 - z1$ADAS13_bl)/z1$ADAS13
