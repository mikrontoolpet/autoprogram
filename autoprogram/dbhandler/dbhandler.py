import sqlite3 as sql


class DataBase:
    """
    Class to access sql3 databases
    """
    def __init__(self, _path):
        self.path = _path

    def __enter__(self):
        self.conn = sql.connect(self.path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

    def __getitem__(self, args):
        """
        This method get a value from a table column corresponding to a row value of another column

        Inputs:
            Iterable with the following elements
                1) Table
                2) Argument column
                3) Argument
                4) Result column
        Output:
            Result
        """
        try:
            table = args[0]
            arg_col = args[1]
            arg = args[2]
            res_col = args[3]
            qry = f"SELECT {res_col} FROM {table} WHERE {arg_col} = '{arg}'" # single quotes are needed to enclose the row name
            self.cursor.execute(qry)
            res = self.cursor.fetchall()[0][0]
            return res
        except sql.OperationalError:
            self.error_list(0, self.path)

    def __setitem__(self, args, val):
        """
        This method set a value into a table column corresponding to a row value of another column

        Inputs:
            Iterable with the following elements
                1) Table
                2) Argument column
                3) Argument
                4) Value column
            Value
        Output:
            None
        """
        table = args[0]
        arg_col = args[1]
        arg = args[2]
        val_col = args[3]
        qry = f"UPDATE {table} SET {val_col} = {val} WHERE {arg_col} = '{arg}'" # single quotes are needed to enclose the row name
        self.cursor.execute(qry)

    def error_list(self, err_id, *args, **kwargs):
        """
        In case of error
        """
        if err_id == 0:
            raise ValueError(f"No such a suitable database: {args[0]}.")