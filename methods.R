proc.nacol <- function(df, colname,str,num=FALSE) {
#  browser();
  for(i in 1:length(str)) {
    df[df[[colname]] == str[i] & !is.na(df[[colname]]),colname] <- NA;
  }

  if(num) {
    df[[colname]] <- as.numeric(as.character(df[[colname]]));
  }
  invisible(df);
}

proc <- read.csv("/home/kkelley/chipgen/papers/procPerf/procPerf.csv")
proc <- proc[2:dim(proc)[1],]

