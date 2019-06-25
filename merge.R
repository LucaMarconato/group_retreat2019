young_methylation_path <- "MethylationData/Imputed/UD/"
files <- list.files(path = young_methylation_path, pattern = "*.bedGraph", full.names = T)
loaded <- sapply(files, function(file) read.table(file, header = F, colClasses = c("character", "numeric", "numeric", "numeric")))

