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
        except KeyError:
            raise ValueError(f"No {sheet_name} sheet in the worbook {self.wb}")
        try:
            sh[arg_col] = sh[arg_col].astype("float64")
            sh[res_col] = sh[res_col].astype("string")
            filt = (sh[arg_col] <= arg_val)
            if (~filt).all():
                raise ValueError("No argument in the worksheet")
            rev_filt = filt[::-1] # in order to find the index of the LAST occurence of True value with idxmax() method
            idx = rev_filt.idxmax()
            res = sh.loc[idx, res_col]
            return res
        except KeyError:
            raise ValueError(f"No {arg_col} or {res_col} column in the worbook {self.wb}")
        except ValueError:
            raise ValueError(f"Could not convert column to float or no argument in the worksheet")

    def trend(self, sheet_name, arg_col, arg_val, res_col):
        """
        trend method
        """
        try:
            sh = self.wb[sheet_name]
        except KeyError:
            raise ValueError(f"No {sheet_name} sheet in the worbook {self.wb}")
        try:
            arg_ser = sh[arg_col].astype("float64")
            res_ser = sh[res_col].astype("float64")
            f = interpolate.interp1d(arg_ser, res_ser)
            res = f(arg_val)
            return res
        except KeyError:
            raise ValueError(f"No {arg_col} or {res_col} column in the worbook {self.wb}")
        except ValueError:
            raise ValueError(f"Could not convert {arg_col} or {res_col} column to float")