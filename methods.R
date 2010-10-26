source("proc.R")

proc <- read.csv("./allData.csv")

#use presence of date as a 'valid' filter
proc <- proc.nacol(proc, "Date", c("?",""));
proc <- proc[!is.na(proc[["Date"]]),];

#clean numeric columns (fill in NAs where needed)
cols.num <- c("Clock..Mhz.",
              "Feature.Size",
              "Bus.Width",
              "Num.Transistors",
              "Power..W.",
              "Die.size",
              "L1.I..per.core.",
              "L1.D..per.core.",
              "L2..available.per.core.",
              "L3",
              "basemean.int2006",
              "basemean.fp2006")
proc <- proc.nacol(proc, cols.num, c("?",""), num=TRUE)

proc[["L1"]] <- proc[["L1.I..per.core."]] + proc[["L1.D..per.core."]]

#replace 0 with 1 so log will work
proc <- proc.nacol(proc, c("L1.I..per.core.", "L1.D..per.core", "L1", "L2..available.per.core.", "L3"),
                   "0", num=TRUE, fill=1)

proc[["TotalC"]] <- proc[["L1"]] + proc[["L2..available.per.core."]] + proc[["L3"]]
proc[["FO4"]] <- proc[["Feature.Size"]] * 360 * 10^(-12)

proc[["Vdd"]] <- (proc[["Vdd_high"]] + proc[["Vdd_low"]])/2

proc[["energy.int"]] <- proc[["Power..W."]]/proc[["basemean.int2006"]]

proc[["logSpec"]]    <- log2(proc[["basemean.int2006"]])
proc[["logL1.I"]]    <- log2(proc[["L1.I..per.core."]])
proc[["logL1.D"]]    <- log2(proc[["L1.D..per.core."]])
proc[["logL1"]]      <- log2(proc[["L1"]])
proc[["logL2"]]      <- log2(proc[["L2..available.per.core."]])
proc[["logTotalC"]]  <- log2(proc[["TotalC"]])
proc[["logFeature"]] <- log2(proc[["Feature.Size"]])
proc[["logClk"]]     <- log2(proc[["Clock..Mhz."]])
proc[["logVdd"]]     <- log2(proc[["Vdd"]])
proc[["logEff"]]     <- log2(proc[["energy.int"]])

proc[["threading"]]  <- 0
proc[proc[["hw_nthreadspercore"]] > 1,"threading"] <- 1

proc[["logCores"]]   <- log2(proc[["hw_ncoresperchip"]])

proc[["pipelining"]] <- 1/proc[["FO4"]] * 1/(proc[["Clock..Mhz."]]*10^6)
proc[["intel"]] <- 0
proc[proc[["Name"]] == "Intel", "intel"] <- 1

proc[["logPipelining"]] <- log2(proc[["pipelining"]])

proc2 <- proc.best(proc.family(proc))
proc.new <- proc[as.POSIXct(proc[["Date"]]) > as.POSIXct("2003-01-01"),]
proc.old <- proc[as.POSIXct(proc[["Date"]]) <= as.POSIXct("2003-01-01") &
                 as.POSIXct(proc[["Date"]]) >  as.POSIXct("1990-01-01"),]

proc.new2 <- proc2[as.POSIXct(proc2[["Date"]]) > as.POSIXct("2003-01-01"),]
proc.old2 <- proc2[as.POSIXct(proc2[["Date"]]) <= as.POSIXct("2003-01-01") &
                 as.POSIXct(proc2[["Date"]]) >  as.POSIXct("1990-01-01"),]

lhs <- c("logSpec");
#rhs <- c("logFeature", "logTotalC", "pipelining")
candids <- c("logClk", "logFeature", "logPipelining", "logCores", "logL1", "logL2", "logTotalC", "logVdd")
rhs.old <- c("logFeature", "logPipelining")
rhs.new <- c("logFeature", "logPipelining", "threading", "logCores", "logTotalC")


