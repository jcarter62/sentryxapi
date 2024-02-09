import pyodbc
from decouple import config


class DBError(Exception):
    """
    Exception class for database errors.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Connection:
    """
    This class is used to connect to the WMIS database, and provide a connection object.
    """
    _server = ''
    _instance = ''
    _database = ''
    _username = ''
    _password = ''
    _trusted = ''
    connection = None

    def __init__(self) -> None:
        """
        Constructor for the Connection class.
        depends on the decouple library to read the connection details from the environment variables or .env file.
        :return: None
        """
        self._server = config('SERVER', default='localhost')
        self._instance = config('INSTANCE', default='')
        self._database = config('DATABASE', default='database')
        self._username = config('UID', default='username')
        self._password = config('PASSWORD', default='password')
        self._trusted = config('TRUSTED', default='no')
        self.connection = self._connection_()
        super().__init__()
        return

    def _conn_str_(self, ):
        con_str = 'Driver={ODBC Driver 17 for SQL Server};'

        con_str += 'SERVER=' + self._server
        if self._instance != '':
            con_str += '\\' + self._instance
        con_str += ';'

        con_str += 'DATABASE=' + self._database + ';'
        if self._trusted.lower() == 'yes':
            con_str += 'Trusted_Connection=yes;'
        else:
            con_str += 'UID=' + self._username + ';'
            con_str += 'PWD=' + self._password + ';'
        con_str += 'PORT=1433;ENCRYPT=NO;'
        return con_str

    def _connection_(self):
        if self.connection is None:
            self.connection = pyodbc.connect(self._conn_str_())
        return self.connection

    @staticmethod
    def extract_row(row: pyodbc.Cursor):
        """
        extract_row is a static method that takes a pyodbc cursor object and returns a dictionary of the row data.
        each field in the row is converted to a string and the dictionary keys are converted to lower case.
        """
        r = {}
        i = 0
        try:
            for item in row.cursor_description:
                name = item[0]
                val = str(row[i])
                name = name.lower()
                i += 1
                r[name] = val
        except DBError as err:
            print(f'Error in extract_row: {err}')
            r['error'] = f'Error in extract_row: {err}'

        return r
