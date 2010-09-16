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

