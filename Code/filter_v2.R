library(plyr)
setwd('C:/Users/mathus07/Desktop/E-109A/project/Data/foi/')

a = read.csv(file="ADNIMERGE.csv")
d = a[,c("RID","VISCODE","EXAMDATE","DX_bl","DX","Month_bl")]
d = d[!d$VISCODE %in% "bl",]
d=d[,!names(d)%in% "VISCODE"]

q = read.csv(file="UWNPSYCHSUM_10_27_17.csv")
q = q[,c("RID","VISCODE","EXAMDATE","ADNI_MEM","ADNI_EF")]
q = q[! q$EXAMDATE %in% "",]
q$EXAMDATE = as.Date(as.character(q$EXAMDATE), "%m/%d/%Y")
q_bl = q[q$VISCODE %in% "bl",]
q_bl = q_bl[,!names(q_bl)%in% "VISCODE"]
names(q_bl)[2:4] = c("bl_date","mem_bl","ef_bl")
q = merge(q,q_bl)
q = q[!q$VISCODE %in% "bl",]
q = q[,!names(q)%in% "VISCODE"]
summary(q)
q = q[complete.cases(q),]

#Merging info of initial and test diagnosis
q1 = merge(q,d)

#Removing AD patients from the initial diagnosis
q1 = q1[!q1$DX_bl %in% "AD",]
unique(as.vector(q1$DX_bl))
q1$DX_bl = as.vector(q1$DX_bl)
q1$DX = as.vector(q1$DX)

p = q1[q1$DX_bl != q1$DX,]
unique(as.vector(p$DX))
p = p[! p$DX %in% "",]
##Subjects that convert to dementia
p1 = p[p$DX %in% "Dementia",]
length(unique(p1$RID))
q = ddply(p1,~RID,summarize,min_months=min(Month_bl))
hist(q$min_months,breaks=100,main="Time to Dementia",xlab="Months",ylab="# Subjects")
summary(q)

ll = 5.049
ul = 39.557
k1 = k[k$Month_bl > ll,]; k1 = k1[k1$Month_bl <ul,];

names(q)[2] = "Month_bl"
x1 = merge(q,q1)
k2 = q1[! q1$RID %in% x1$RID,]

w = unique(k2$RID)
x2 = data.frame()
for(i in 1:length(w))
{
  z = k2[k2$RID ==w[i],]
  s = sample(as.integer(rownames(z)),1)
  x2=rbind(x2,z[rownames(z) %in% s,])
}

z1 = rbind(x1,x2)

#z1 = z1[,!names(z1)%in% "dats_adas"]
z1$MEM_change = (z1$ADNI_MEM - z1$mem_bl)/z1$mem_bl
z1$EF_change = (z1$ADNI_EF - z1$ef_bl)/z1$ef_bl

