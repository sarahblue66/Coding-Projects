## TEAM 1
# Name: Han Bao, Tianyi Lan, Sijia Liu, Jiayu Zhu
# Andrew ID: hbao, tlan1, sijial, jiayuz1

#################
###  SET UP #####
#################

if (!require("stats")) {
  install.packages("stats")
  library("stats")
}

if (!require("randomForest")) {
    install.packages("randomForest")
    library("randomForest")
}

if (!require("glmnet")) {
  install.packages("glmnet")
  library("glmnet")
}

if (!require("MASS")) {
  install.packages("MASS")
  library("MASS")
}

if (!require("cluster")) {
  install.packages("cluster")
  library("cluster")
}

if (!require("survival")) {
  install.packages("survival")
  library("survival")
}

if (!require("Hmisc")) {
  install.packages("Hmisc")
  library("Hmisc")
}

# source additional functions for function panNew
source(
  "https://labs.genetics.ucla.edu/horvath/RFclustering/RFclustering/FunctionsRFclustering.txt")


#################################
###  Unsupervised Learning  #####
#################################

# Input: rbind(trianX, testX)
# Output: labels(class 0, 1) before Hamming

# Model 1
# PCA (scaling, centering, no whitening) 1st component
# and K-means

unsupModel1 <- function(data){
  pc = prcomp(data, center=TRUE, scale.=TRUE)
  km = kmeans(pc$x[,1], 2, algorithm="Lloyd")
  # turn class 1, 2 into class 0, 1
  rst = km$cluster-1
  return(rst)
}

# Model 2
# Unsupervised RF and Partition Around Metroids (for clustering)

unsupModel2 <- function(data){
  g = randomForest(data, keep.forest=FALSE, proximity=TRUE)
  labelRF = pamNew(g$proximity, 2)
  # turn class 1, 2 into class 0, 1
  rst = labelRF-1
  return(rst)
}

#################################
###  Supervised Learning  #######
#################################

# Input:  testX
# Output: labels(class 0, 1)
# In each function, the model would be 
# automatically trained at first with trainX, trianY


# Model 1
# Lasso with leave-one-out CV selected 1se and usual rule lambda
# choose the one with lower error in train dataset to make prediction

supModel1 <- function(data){
  load("data/TrainData.Rdata")
  x = as.matrix(trainX)
  y = trainY
  lamdas = cv.glmnet(x, y, nfolds=length(trainY), grouped=FALSE, alpha=1)
  a.las1 = glmnet(x, y, family="binomial", alpha=1, lambda=lamdas$lambda.min)
  a.las2 = glmnet(x, y, family="binomial", alpha=1, lambda=lamdas$lambda.1se)
  las1 = predict(a.las1, type="class", newx=x)
  las2 = predict(a.las2, type="class", newx=x)
  las1.error = 1-sum(las1==trainY)/length(trainY)
  las2.error = 1-sum(las2==trainY)/length(trainY)
  if (las1.error<las2.error) {
    pred = predict(a.las1, type="class", newx=as.matrix(data))
  } else {
    pred = predict(a.las2, type="class", newx=as.matrix(data))
  }
  return(pred)
}


# Model 2
# random forest

supModel2 <- function(data){
  load("data/TrainData.Rdata")
  new = cbind(trainY, trainX)
  rf = randomForest(as.factor(trainY) ~ ., 
                    ntree = 500, mtry = 16, data = new)
  pred = predict(rf, data)
  return(pred)
}
