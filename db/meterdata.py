from .connection import Connection

class MeterData:

    # Constructor
    def __init__(self,id):
        self.meter_list = []
        self.meter_count = 0
        self.Connection = Connection()
        self.connection = Connection.connection
        self.id = id
        # self.get_meter_data()

    # Add a meter to the list
    def add_meter(self, meter):
        self.meter_list.append(meter)
        self.meter_count += 1

    # Get the meter list
    def get_meter_data(self):
        cursor = self.Connection.connection.cursor()
        cmd = 'select * from turnout where turnout_id = ?'

        try:
            self.meter_list = []
            for row in cursor.execute(cmd, (self.id,)):
                data = self.Connection.extract_row(row)
                self.add_meter(data)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

        return self.meter_list


    def get_meter_lateral(self):
        cursor = self.Connection.connection.cursor()
        cmd = ''
        cmd += 'select lt.turnout_id, l.LatName as lateral '
        cmd += 'from latTurnout lt '
        cmd += 'left join lat l on lt.latid = l.id '
        cmd += 'where lt.turnout_id = ?;'
        try:
            self.meter_list = []
            for row in cursor.execute(cmd, (self.id,)):
                data = self.Connection.extract_row(row)
                self.add_meter(data)
        except Exception as e:
            print(e)
        finally:
            cursor.close()

        return self.meter_list
