"""
Author: Sean Brady
Contact: seanbrady100@icloud.com
phone: 417-834-5651
"""

import pandas as pd #used for manipulating dataframes
import re #used to split input into tokens based off of regex expression
import sys #used to get command line args

class Processor:
    """ A class used to process into the format of example """


    def __init__(self, filename):
        try:
            self.df = pd.read_csv(filename) #open the csv file
        except:
            print("Error opening file. Exiting...")
            exit(-1)

    def driver(self):
        """
        A method called to drive dataframe transformations
        """
        
        #perform transformations on the data
        for column in self.df:
            #change dates to ISO 8601 format where applicable
            if "date" in column:
                self.df[column] = self.df[column].apply(self.__transform_date)
            elif "price" in column or "$" in column:
                self.df[column] = self.df[column].apply(self.__transform_price) #round currency to unit of accounting
            elif "inches" in column:
                self.df[column] = self.df[column].apply(self.__transform_inches)
            elif "feet" in column:
                self.df[column] = self.df[column].apply(self.__transform_feet)
            elif "upc" in column:
                self.df[column] = self.df[column].apply(lambda x: self.__float_to_str(x))#.apply(lambda x: try: str(int(x)) except: str(x))#astype('string')#str)
            elif "item number" in column:
                self.df[column] = self.df[column].astype('string')#str)
            
   
        #rename columns to fit naming standards where applicable
        for column in self.df:
            if (self.__fits_column_convention(column)): #check if column naming conventions are being followed
                continue
            else:
                self.df = self.df.rename(columns={column : self.__transform_columns(column)}) #rename columns

    def save_dataframe(self,name):
        """
        Method used to save dataframe to specified name
        i.e. formatted.csv
        """
        save_name = name + ".csv"
        self.df.to_csv(save_name, index=False)


    def __fits_column_convention(self,column):
        """
        Method to ensure column naming conventions are being followed
        Input: a column name
        Output: True or False
        """
        invalid = "/()- " #a set of characters found in homework file that are invalid
        #return false if invalid chars in column name, else true
        if any(elem in column for elem in invalid):
            return False
        else:
            return True

    def __transform_columns(self, original_col):
        """
        Function to transform column name to follow convention
        Input: original column name
        Output: column name following convention
        """
        strings_to_del = ["inches", "pounds", "cubic feet"] #a list of strings we will delete if found in column name

        tokens = re.split(r"[/()\- ]+",original_col) #split column name into tokens based off of regex expression
        tokens = [t for t in tokens if t] #remove potential trailing empty strings 
        
        tokens = [t for t in tokens if t not in strings_to_del] #delete tokens matching strings_to_del
        
        #replace $ with price
        tokens = ["price" if t in "$" and "price" not in tokens else t for t in tokens]
        #remove $ from case where tokens included both price and $ in previous list comprehension 
        tokens = [t for t in tokens if t not in "$"]
        
        #create new column name by joining tokens with _
        new_col = "_".join(tokens)
        return new_col

    def __float_to_str(self,x):
        try:
            x = str(int(x))
        except:
            x = str(x)
        return x
    
    def __transform_date(self,date):
        """
        A function used to transform a date
        in the format MM/DD/YY -> YYYY-MM-DD
        """
        tokens = re.split(r"[/]+",date) #split date based off of forward slash
        
        #if we have three tokens (month,day, year), then transform the date
        if len(tokens)==3: 
            month,day,year = tokens #get individual tokens
            year = "20" + year #prepend 20 to year
            return f"{year}-{month}-{day}"
        else:
            return date

    def __transform_price(self,price):
        """
        A method used to round prices to unit of accounting
        i.e. 14.5 -> 14.50
        """

        #if price is nan, return 
        if (str(price)=="nan"):
            #return "$00.00"
            return price
        else:
            #remove dollar sign to perform operations
            if '$' in str(price):
                price = str(price).replace("$","")
            #remove comma to perform operations
            if ',' in str(price):
                price = str(price).replace(",","")
            #return price formatted to two decimals with commas where applicable
            return "$" + "{:,.2f}".format(float(price))
                

    def __transform_inches(self,val):
        """
        method used to format columns already in inches
        Round to two decimals. Set nan values to 00.00
        remove non decimals
        If multiple values, separate them with x
        """
        if (str(val)=="nan"):
            return val
        else:
            tokens = self.__extract_tokens(str(val)) #get tokens
            tokens = ["{:,.2f}".format(float(t)) if self.__is_num(t) else t for t in tokens] #format tokens
            
            return "".join(tokens)

    def __transform_feet(self,val):
        """
        method used to transform feet to inches.
        functions like __transform_inches, but changes unit of measurement to inches
        """
        if (str(val)=="nan"):
            return val
        else:
            tokens = self.__extract_tokens(str(val)) #get tokens
            tokens = ["{:,.2f}".format(float(t)*12) if self.__is_num(t) else t for t in tokens] #format tokens
            
            return "".join(tokens)

    def __is_num(self,val):
        """
        returns true if a string is a number
        """
        try:
            float(val)
            return True
        except:
            return False

    def __extract_tokens(self,val):
        """
        helper method to extract tokens from a string
        returns a list of tokens (numbers and strings)
        """
        return re.findall(r"\d+\.\d+|\d+|[a-zA-Z]+",val)


    def __extract_nums(self,val):
        """
        helper method used to extract numbers from a string.
        Returns a list of individual numbers
        """
        return re.findall(r"\d+\.\d+|\d+",val)

    def print(self):
        """method to print column name values"""
        for column in self.df:
            values = self.df[column].values
            print(column)
            print(values)

    def print_col(self,col):
        """method to print values of an individual column"""
        values = self.df[col].values
        print(col)
        print(values)


def main():
    if (len(sys.argv) != 2):
        print("invalid number of arguments supplied. Exiting")
        exit(-1)
    entity = Processor(sys.argv[1])
    entity.driver()
    entity.save_dataframe("formatted")

if __name__=='__main__':
    main()
