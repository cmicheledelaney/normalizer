import csv
import sys
import datetime
import pytz


#indices of the rows
Timestamp = 0
Address = 1
ZIP = 2
FullName = 3
FooDuration = 4
BarDuration = 5
TotalDuration = 6
Notes = 7
NbrColumns = 8


# changes the timestamp string to a datetime object and converts it to US/Eastern
def getDate(timestamp):
    # formats the string to a datetime object
    dateTimeObject = datetime.datetime.strptime(timestamp, '%m/%d/%y %I:%M:%S %p')
    #sets the original timezone to US/Pacific and the one
    #it needs to get converted to to US/Eastern
    oldTimezone = pytz.timezone("US/Pacific")
    newTimezone = pytz.timezone("US/Eastern")
    # sets its timezone to US/Pacific
    dateTimeObject = oldTimezone.localize(dateTimeObject)
    # converts it to US/Eastern
    dateTimeObject = dateTimeObject.astimezone(newTimezone)
    return (dateTimeObject.isoformat())


# pads the ZIP, if necessary, with zeroes until it contains 5 digits
# valid are only numeric ZIP codes, assuming they have to be from the US
def getZIP(ZIP):
    if not ZIP.isdigit():
        raise ValueError
    return (ZIP.zfill(5))


# converts the name to its uppercase form
# assumes there has to be a name, empty strings are not allowed
def getFullName(name):
    if not name:
        raise ValueError
    return(name.upper())


# splits the duration string into hours, minutes and seconds and converts it
# to seconds.
def getDuration(duration):
    h, m, s = duration.split(':')
    totalSeconds = (float(datetime.timedelta(hours=int(h), minutes=int(m), seconds=float(s)).total_seconds()))
    return (totalSeconds)


# adds FooDuration and BarDuration and sets the precision to
# the one with higher precision
def getTotalDuration(duration1, duration2):
    precision1 = len(str(duration1).split('.')[1])
    precision2 = len(str(duration2).split('.')[1])
    totalDuration = duration1 + duration2
    totalDuration = round(totalDuration, max(precision1, precision2))
    return totalDuration


def main():
    line = 0
    # sets the encoding of the stdin to utf-8 and replaces any invalid
    # characters with the replacement character
    sys.stdin.reconfigure(encoding='utf-8', errors='replace')
    # reads from stdin into f
    inputStream = sys.stdin
    # creates a list of the rows and columns of f
    inputCSV = csv.reader(inputStream)
    # iterates through the rows
    for row in inputCSV:
        if (line == 0):
            # formats the row back into csv format and prints it
            output = csv.writer(sys.stdout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            output.writerow(row)
        # if there are more or less than NbrColumns columns the input is invalid
        elif (len(row) != NbrColumns):
            sys.stderr.write("invalid number of columns\n")
        else:
            try:
                row[Timestamp] = getDate(row[Timestamp])
                row[ZIP] = getZIP(row[ZIP])
                row[FullName] = getFullName(row[FullName])
                row[FooDuration] = getDuration(row[FooDuration])
                row[BarDuration] = getDuration(row[BarDuration])
                row[TotalDuration] = getTotalDuration(row[BarDuration], row[FooDuration])
            # if any of the above raised a ValueError the input is considered
            # invalid and the row is not getting printed
            except ValueError:
                sys.stderr.write("invalid input\n")
                continue
            else:
                # no exception occured: row gets formatted into csv format
                output = csv.writer(sys.stdout, delimiter=',', quotechar='"')
                # prints the row
                output.writerow(row)
        line += 1

main()
