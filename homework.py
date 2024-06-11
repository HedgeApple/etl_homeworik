"""
Name: Katie Golder
Date: 6-11-24
Description: Reads homework.csv and applies needed transformations to export as formatted.csv
"""

import csv #to read and write to the csv
from decimal import * #type for currency formatting

def main():
    #Reads homework.csv
    with open('homework.csv', newline='') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',')
        data = []
        rowCount = 0

        #Transformation lists
        changeDate = []
        changeCurrency = []
        changeDistance3 = []
        changeUPC = []

        #Goes through each row starting with headers
        for row in lineReader:
            newRow =[]
            colCount = 0 #Column count
            if rowCount == 0: #Header row
                for title in row:

                    if isDate(title) == True:
                        changeDate.append(colCount)

                    if isCurrency(title) == True:
                        changeCurrency.append(colCount)

                    unit = isDistance(title)
                    if unit != False:
                        title = title.replace(unit, "inches")
                        changeDistance3.append(colCount)

                    #No weights without pounds needing conversion

                    if isUPC(title) == True: #No Gtin or EAN
                        changeUPC.append(colCount)

                    newRow.append(title)
                    colCount += 1

            else:#Data rows
                colCount = 0
                for item in row:
                    
                    if item != "":
                        if colCount in changeDate:
                            item = makeISO(item)

                        if colCount in changeCurrency:
                            item = roundCurrency(item)

                        if colCount in changeDistance3:
                            item = convertInches3(item)

                        if colCount in changeUPC:
                            item = convertString(item)
                    
                    newRow.append(item)
                    colCount += 1
            
            data.append(newRow)
            rowCount += 1

    #Writes all information to formatted.csv
    with open('formatted.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def isDate(title):
    if "date" in title:
        return True
    else:
        return False
def makeISO(item):
    digits = item.split("/")

    year = "20" + digits[2]
    #month
    if len(str(digits[0])) == 1:#Acconts for single or double digits
        month = "0" + digits[0]
    else:
        month = digits[0]
    #day
    if len(str(digits[1])) == 1: #Acconts for single or double digits
        day = "0" + digits[1]
    else:
        day = digits[1]

    ISO = year + "-" + month + "-" + day
    return ISO

def isCurrency(title):
    if "$" in title:
        return True
    else:
        return False
def roundCurrency(item):
    numberOnly = (item.replace("$","")).replace(",","")
    roundNumber = Decimal(numberOnly).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return roundNumber

def isDistance(title):
    if ("feet" in title) and ("cubic" in title):
        return ("feet")
    else:
        return False
def convertInches3(item):
    return Decimal(float(item) * 1728).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def isUPC(title):
    if "upc" in title:
        return True
    else:
        return False
def convertString(item):
    return(str(item))


main()
