from .connection import Connection

class MeterList:

    # Constructor
    def __init__(self):
        self.meter_list = []
        self.meter_count = 0
        self.Connection = Connection()
        self.connection = Connection.connection
        self.get_meter_list()

    # Add a meter to the list
    def add_meter(self, meter):
        self.meter_list.append(meter)
        self.meter_count += 1

    # Get the meter list
    def get_meter_list(self):
        cursor = self.Connection.connection.cursor()
        cmd = '''
                select
                cast('Water' as varchar(10)) as "Product_Type",
                cast(t.Turnout_ID as varchar(100)) as "Socket_ID",
                cast('0' as varchar(100)) as AccountID,
                cast(isnull(t.SerialNo, '') as varchar(50)) as "Meter_Serial_Number",
                cast(t.Description as varchar(100)) as "Meter_Address_1",
                cast('Fresno' as varchar(50)) as "Meter_City",
                cast('CA' as varchar(2)) as "Meter_State/Province"
                from turnout t
                join
                TurnoutCodes
                tc
                on
                t.Turnout_ID = tc.Turnout_ID and tc.Code_ID = 'TC0041'
                -- where
                -- t.Subsystem_ID in ('SGMA', 'GWMP') and
                -- isnull(t.IsActive, 0) = 1
                order
                by
                t.Turnout_ID;
              '''

        try:
            for row in cursor.execute(cmd):
                data = self.Connection.extract_row(row)
                self.add_meter(data)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

        return self.meter_list

