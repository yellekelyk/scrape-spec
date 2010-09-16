source("proc.R")

proc <- read.csv("./procPerf.csv")
proc <- proc[3:dim(proc)[1],]

#use presence of date as a 'valid' filter
proc <- proc.nacol(proc, "Date", c("?",""));
proc <- proc[!is.na(proc[["Date"]]),];

#clean numeric columns (fill in NAs where needed)
cols.num <- c("Clock.Speed..MHz.", "Feature.Size..um.","Bus.Width", "I..", "D..", "I.D", "L2..", "L3.", "Spec2006", "Spec2006.1", "SpecAvg", "IPC", "FO4")
proc <- proc.nacol(proc, cols.num, c("?",""), num=TRUE)

#replace 0 with 0.001 so log will work
proc <- proc.nacol(proc, c("I..", "D..", "I.D", "L2..", "L3."),
                   "0", num=TRUE, fill=0.001)

proc[["TotalC"]] <- proc[["I.D"]] + proc[["L2.."]]


proc[["logSpec"]]    <- log(proc[["Spec2006"]])
proc[["logL1.I"]]    <- log(proc[["I.."]])
proc[["logL1.D"]]    <- log(proc[["D.."]])
proc[["logL1"]]      <- log(proc[["I.D"]])
proc[["logL2"]]      <- log(proc[["L2.."]])
proc[["logTotalC"]]  <- log(proc[["TotalC"]])
proc[["logFeature"]] <- log(proc[["Feature.Size..um."]])

proc[["pipelining"]] <- 1/proc[["FO4"]] * 1/(proc[["Clock.Speed..MHz."]]*10^6)

lhs <- c("logSpec");
rhs <- c("logFeature", "logTotalC", "pipelining")

