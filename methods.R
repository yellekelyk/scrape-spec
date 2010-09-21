source("proc.R")

proc <- read.csv("./allData.csv")

#use presence of date as a 'valid' filter
proc <- proc.nacol(proc, "Date", c("?",""));
proc <- proc[!is.na(proc[["Date"]]),];

#clean numeric columns (fill in NAs where needed)
cols.num <- c("Clock..Mhz.", "Feature.Size","Bus.Width", "L1.I..per.core.", "L1.D..per.core.",
              "L2..available.per.core.", "L3", "basemean.int2006", "basemean.fp2006")
proc <- proc.nacol(proc, cols.num, c("?",""), num=TRUE)

proc[["L1"]] <- proc[["L1.I..per.core."]] + proc[["L1.D..per.core."]]

#replace 0 with 0.001 so log will work
proc <- proc.nacol(proc, c("L1.I..per.core.", "L1.D..per.core", "L1", "L2..available.per.core.", "L3"),
                   "0", num=TRUE, fill=0.001)

proc[["TotalC"]] <- proc[["L1"]] + proc[["L2..available.per.core."]]
proc[["FO4"]] <- proc[["Feature.Size"]] * 360 * 10^(-12) /2

proc[["logSpec"]]    <- log(proc[["basemean.int2006"]])
proc[["logL1.I"]]    <- log(proc[["L1.I..per.core."]])
proc[["logL1.D"]]    <- log(proc[["L1.D..per.core."]])
proc[["logL1"]]      <- log(proc[["L1"]])
proc[["logL2"]]      <- log(proc[["L2..available.per.core."]])
proc[["logTotalC"]]  <- log(proc[["TotalC"]])
proc[["logFeature"]] <- log(proc[["Feature.Size"]])

proc[["pipelining"]] <- 1/proc[["FO4"]] * 1/(proc[["Clock..Mhz."]]*10^6)
proc[["intel"]] <- 0
proc[proc[["Name"]] == "Intel", "intel"] <- 1

lhs <- c("logSpec");
rhs <- c("logFeature", "logTotalC", "pipelining")

