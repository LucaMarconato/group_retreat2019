# Data

The data must be place in the current folder, so you need to have the following directories:
```
./Annotation
./ExpressionMatrix
./MethylationData
```

All the compressed data in the subfolders of ./MethylationData must be decompressed; you can use the following command:

```
for f in $(find . -name '*.gz'); do gzip -d $f; done
```
