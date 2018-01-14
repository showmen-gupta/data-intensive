#!/usr/bin/env python
import csv
import sys

def decide(emp, folders, fileName):
    if emp is None and folders is None:
        return True
    else:
        parts = fileName.split("/")
        empName = parts[0]
        folderName = parts[1]

        if emp is None and folders is not None:
            if folders == folderName:
                return True
        elif emp is not None and folders is None:
            if emp == empName:
                return True
        elif emp is not None and folders is not None:
            if emp == empName and folders == folderName:
                return True


def main(source, destination, emp, folders):
    file = open(source, "rb")
    file1 = open(destination, "w")
    csv.field_size_limit(sys.maxsize)
    reader = csv.reader(file)
    write = False
    count = 0
    rownum = 0
    for row in reader:
        if rownum == 0:
            header = row
        else:
            fileName = row[0]
            msg = row[1]
            write = decide(emp, folders, fileName)
            if write:
                file1.write("Message-URI: " +fileName+"\n")
                file1.write(msg+"\n")
                count += 1
        rownum += 1

    file.close()
    file1.close()
    #print(rownum)
    print(count)


if __name__ == "__main__":
    source = sys.argv[1] #"D://Downloads//enron-email-dataset//emails.csv"
    destination = sys.argv[2]
    emp = sys.argv[3]
    folders = sys.argv[4]
    if emp == "all": emp = None
    if folders == "all": folders = None
    main(source, destination, emp, folders)