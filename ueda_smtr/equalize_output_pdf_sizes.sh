#!/bin/bash
pdfconstcrop() {
    pdfcrop --bbox "$(
        pdfcrop --verbose "$@" |
        grep '^%%HiResBoundingBox: ' |
        cut -d' ' -f2- |
        LC_ALL=C datamash -t' ' min 1 min 2 max 3 max 4
    )" "$@"
}
for i in $(ls):
do
    pdfconstcrop $i $i;
done
