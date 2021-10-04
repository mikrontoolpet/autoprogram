import asyncio
import pandas as pd
from scipy import interpolate

class WorkBook:
    def __init__(self, path):
        """
        Create a dictionary, whose element are pd.DataFrames
        corresponding to different worksheets
        """
        self.wb = pd.read_excel(path, sheet_name=None)
     
    def lookup(self, sheet_name, arg_col, arg_val, res_col):
        """
        lookup method
        """
        try:
            sh = self.wb[sheet_name]
            sh[arg_col] = sh[arg_col].astype("float64") # format argument as float
            sh[res_col] = sh[res_col].astype("string") # format result as string
            filt = (sh[arg_col] <= arg_val) # Select all row idx whose argument is less or equal to the input
            if (~filt).all(): # If there isn't any match raise error
                self.error_list(0)
            rev_filt = filt[::-1] # in order to find the index of the last occurence of True value with idxmax() method
            idx = rev_filt.idxmax() # idmax() returns the idx of the max value in the series (the first idx, if there are multiple max values)
            res = sh.loc[idx, res_col] # return the correspondent element
            return res
        except KeyError:
            self.error_list(1)
        except ValueError:
            self.error_list(2)

    def trend(self, sheet_name, arg_col, arg_val, res_col):
        """
        trend method
        """
        try:
            sh = self.wb[sheet_name]
            arg_ser = sh[arg_col].astype("float64")
            res_ser = sh[res_col].astype("float64")
            f = interpolate.interp1d(arg_ser, res_ser)
            res = f(arg_val)
            return res
        except KeyError:
            self.error_list(1)
        except ValueError:
            self.error_list(2)

    def error_list(self, err_id):
        """
        In case of error
        """
        if err_id == 0:
            print("No argument in the sheet.")
        elif err_id == 1:
            print("No sheet or column in the workbook.")
        elif err_id == 2:
            print("Could not convert column to float or no argument in the worksheet.")