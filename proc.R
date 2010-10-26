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


# return a list of data frames (1 for each unique family) 
proc.family <- function(proc,
                        cols=c("Family",
                                "Feature.Size",
                                "hw_nthreadspercore",
                                "hw_ncoresperchip",
                                "L2..available.per.core.",
                                "L3",
                                "Die.size",
                                "Vdd_high")) {

  aggCols <- paste(proc[[cols[[1]]]], proc[[cols[[2]]]], sep="::")
  for (i in 3:length(cols)) {
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
proc.best <- function(procList, clk="Clock..Mhz.") {

  do.call('rbind', lapply(1:length(procList), function(idx) {
    df <- procList[[idx]];
    df2 <- data.frame(df[df[[clk]] == max(df[[clk]]),])
    invisible(df2)
  }))
}



# do regression
proc.lm <- function(df, lhs, rhs) {

  #filter out all NaNs, Infs
  df <- df[is.finite(df[[lhs]]),];

  for (i in 1:length(rhs)) {
    df <- df[is.finite(df[[rhs[[i]]]]),]
  }
  regStr <- paste(lhs, paste(rhs, collapse="+"), sep="~");
  invisible(lm(regStr, df));
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
