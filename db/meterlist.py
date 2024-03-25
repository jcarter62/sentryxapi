from .connection import Connection
from decouple import config

class MeterList:

    # Constructor
    def __init__(self):
        self.tc_active = config("TC_ACTIVE")
        self.tc_inactive = config("TC_INACTIVE")
        self.meter_list = []
        self.meter_count = 0
        self.Connection = Connection()
        self.connection = Connection.connection
#        self.get_meter_list()

    # Add a meter to the list
    def add_meter(self, meter):
        self.meter_list.append(meter)
        self.meter_count += 1

    # Get the meter list
    def get_meter_list(self, tc_code=None):
        if tc_code is None:
            tc_where = f"(tc.Code_ID in ('{self.tc_active}', '{self.tc_inactive}'))"
        else:
            tc_where = f"(tc.Code_ID = '{tc_code}')"

        cursor = self.Connection.connection.cursor()
        cmd = f'''
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
                (t.Turnout_ID = tc.Turnout_ID) and {tc_where}
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


    def get_active_meters(self):
        return self.get_meter_list(self.tc_active)

    def get_inactive_meters(self):
        return self.get_meter_list(self.tc_inactive)

