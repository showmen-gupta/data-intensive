#!/usr/bin/env python
import csv
import sys

def main(source, destination):
    file = open(source, "rb")
    file1 = open(destination, "w")
    csv.field_size_limit(sys.maxsize)
    reader = csv.reader(file)

    rownum = 0
    for row in reader:
        if rownum == 0:
            header = row
        else:
            fileName = row[0]
            msg = row[1]
            file1.write("Message-URI: " +fileName+"\n")
            file1.write(msg+"\n")

        rownum += 1

    file.close()
    file1.close()
    print(rownum)


if __name__ == "__main__":
    source = sys.argv[1]
    destination = sys.argv[2]
    main(source, destination)