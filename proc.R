
#parse the cache description and convert the cache number to per-core
proc.cachepercore <- function(df, cache, cachedesc, newcol=NA) {
  if (is.na(newcol)) {
    newcol <- cache;
  }
  
  tmp <- df[[cache]];
  cols <- grep("[0-9]+\\s*MB\\s*shared", df[[cachedesc]])
  desc <- df[[cachedesc]][cols];
  tmp[cols] <- as.numeric(gsub(".*([0-9]+)\\s*MB.*", "\\1", desc)) * 1024; 
  df[[newcol]] <- tmp;
  invisible(df);
}


#convert strange values to NA, coerce to number if desired
proc.nacol <- function(df, colnames,str,num=FALSE,fill=NA) {
  for (j in 1:length(colnames)) {
    colname <- colnames[[j]];
    for(i in 1:length(str)) {
      df[df[[colname]] == str[i] & !is.na(df[[colname]]),colname] <- fill;
    }
    
    if(num) {
      df[[colname]] <- as.numeric(as.character(df[[colname]]));
    }
  }
  invisible(df);
}

proc.groups <- function(proc,
                        cols=c("Family",
                          "Feature.Size",
                          "L2..available.per.core.",
                          "L3",
                          "Vdd_high",
                          "Clock..Mhz.")) {

  fam <- proc.family(proc, cols=cols);
  fam.n <- lapply(1:length(fam), function(idx) {invisible(dim(fam[[idx]])[1])});
  rrr <- fam[fam.n > 1];
  group <- do.call('rbind', lapply(1:length(rrr),
                                   function(idx) {df <- rrr[[idx]];
                                                  rrr[["Group"]] <- idx;
                                                  invisible(rrr);}))
  group <- group[,c("Group", colnames(group)[-length(colnames(group))])];
  
  invisible(group)
}


# return a list of data frames (1 for each unique family)
# this can be helpful for doing intra-family comparisons
proc.family <- function(proc,
                        cols=c("Family",
                               "Feature.Size",
                               "L2..available.per.core.",
                               "L3",
                               "Vdd_low",
                               "Vdd_high")) {

  #aggCols <- paste(proc[[cols[[1]]]], proc[[cols[[2]]]], sep="::")
  aggCols <- c()
  for (i in 1:length(cols)) {
    aggCols <- paste(aggCols, proc[[cols[[i]]]], sep="::")
  }
  
  proc[["agg"]] <- aggCols
  
  a <- tapply(1:dim(proc)[1], proc[["agg"]], function(idx) {
    df <- proc[idx,colnames(proc)[-dim(proc)[2]]]
    invisible(df)
  })

  invisible(a);
}


# give this the output of proc.family, produce a df of the best proc
# this ensures there is just one point for each design to avoid over-weighting
# particular famililes in the regression
proc.best <- function(procList, metric="Clock..Mhz.") {

  do.call('rbind', lapply(1:length(procList), function(idx) {
    df <- procList[[idx]];
    df2 <- data.frame(df[df[[metric]] == max(df[[metric]]),])
    invisible(df2)
  }))
}

proc.mean <- function(procList, metric="Clock..Mhz.") {

  do.call('rbind', lapply(1:length(procList), function(idx) {
    df <- procList[[idx]];
    df2 <- data.frame(df[df[[metric]] == max(df[[metric]]),])
    df2[[metric]] <- mean(df[[metric]], na.rm=TRUE)
    invisible(df2)
  }))
}

proc.worst <- function(procList, metric="Clock..Mhz.") {

  do.call('rbind', lapply(1:length(procList), function(idx) {
    df <- procList[[idx]];
    df2 <- data.frame(df[df[[metric]] == min(df[[metric]]),])
    invisible(df2)
  }))
}


# do regression
proc.lm <- function(df, lhs, rhs) {
  #filter out all NaNs, Infs
#  for (i in 1:length(lhs)) {
#    df <- df[is.finite(df[[lhs[[i]]]]),];
#  }
#  for (i in 1:length(rhs)) {
#    df <- df[is.finite(df[[rhs[[i]]]]),]
#  }
  regs <- lapply(1:length(lhs), function(idx) {
    regStr <- paste(lhs[[idx]], paste(rhs, collapse="+"), sep="~");
    invisible(lm(regStr, df));
  })
  invisible(regs);
}


proc.lm.plot <- function(regs, lhs, rhs, save=FALSE) {

  for (j in 1:length(rhs)) {
    df <- data.frame(1:length(regs));
    se <- data.frame(1:length(regs));
    for (i in 1:length(regs)) {
      df[i,1] <- summary(regs[[i]])$coefficients[j+1,1]
      se[i,1] <- summary(regs[[i]])$coefficients[j+1,2]
    }
    if (save) {
      pdf(paste("/tmp/", rhs[[j]], sep=""))
    }
    else {
    x11()
  }
    
    ci.l <- as.matrix(df)-as.matrix(se)
    ci.h <- as.matrix(df)+as.matrix(se)
    xvals <- barplot(as.matrix(df), beside=TRUE, ylab=rhs[[j]], names.arg=lhs, ylim=c(0, max(ci.h)), main=rhs[[j]])
    arrows(xvals, as.matrix(df), xvals, as.matrix(df)+as.matrix(se), angle=90)
    arrows(xvals, as.matrix(df), xvals, as.matrix(df)-as.matrix(se), angle=90)
    if (save) {
      dev.off()
    }
  }
}


# condense raw Python output
proc.processFull <- function(proc) {

  # only proceed with results for 1 chip/test
  proc <- proc[proc[["hw_nchips"]]==1,]

  proc <- proc.nacol(proc, c("basemean", "peakmean"), c("Not Run", "--"), TRUE)

  invisible(do.call('rbind',
                    tapply(1:dim(proc)[1],
                           proc[["processor"]],
                           function(idx) { df <- proc[idx,];
                                           df2 <- data.frame(df[1,]);
                                           df2[["basemean"]] <- max(df[["basemean"]], na.rm=TRUE);
                                           df2[["peakmean"]] <- max(df[["peakmean"]], na.rm=TRUE);
                                           invisible(df2);}
                           )
                    )
            )
}

proc.renameCol <- function(df, colName, newColName) {
  colnames(df)[colnames(df)==colName] <- newColName;
  invisible(df)
}


proc.tmp <- function() {

  spec.int.2k6 <- proc.processFull(read.csv("/mnt/raid/research/stanford/procPerf/test.CINT2006_(2206).csv"))
  spec.fp.2k6 <- proc.processFull(read.csv("/mnt/raid/research/stanford/procPerf/test.CFP2006_(2161).csv"))
  specr.int.2k6 <- proc.processFull(read.csv("/mnt/raid/research/stanford/procPerf/test.CINT2006_Rates_(4189).csv"))
  specr.fp.2k6 <- proc.processFull(read.csv("/mnt/raid/research/stanford/procPerf/test.CFP2006_Rates_(3682).csv"))


  #proc.renameCol(spec.int.2k6, "basemean", "SpecInt2006Base")
  #proc.renameCol(spec.int.2k6, "peakmean", "SpecInt2006Peak")
  #proc.renameCol(spec.fp.2k6, "basemean",  "SpecFP2006Base")
  #proc.renameCol(spec.fp.2k6, "peakmean",  "SpecFP2006Peak")
  #
  #proc.renameCol(specr.int.2k6, "basemean", "SpecInt2006RBase")
  #proc.renameCol(specr.int.2k6, "peakmean", "SpecInt2006RPeak")
  #proc.renameCol(specr.fp.2k6, "basemean",  "SpecFP2006RBase")
  #proc.renameCol(specr.fp.2k6, "peakmean",  "SpecFP2006RPeak")

  sameCols <- c("processor", "clock", "hw_nthreadspercore",
                "hw_ncoresperchip", "hw_nchips", "hw_ncores")
  
  tmp <- merge(spec.int.2k6, spec.fp.2k6,
               by=sameCols, all=TRUE, suffixes = c(".int2006", ".fp2006"))
  tmpr <- merge(specr.int.2k6, specr.fp.2k6,
               by=sameCols, all=TRUE, suffixes = c(".rate.int2006", ".rate.fp2006"))
  tmp <- merge(tmp, tmpr, by=sameCols, all=TRUE)

  invisible(tmp)
}
