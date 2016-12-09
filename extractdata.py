import psycopg2
import json
import collections
import datetime

class extractdata:
    def getconnection(self):

        #Define our connection string to localhost
        #conn_string = "host='localhost' port='5432' dbname='postgres' user='postgres' password='satf..'"
        #Define our connection string to heroku basic database
        conn_string = "host='ec2-54-235-125-135.compute-1.amazonaws.com' port='5432' dbname='d4sjjjfm3g35dc' user='swobzoejynjhpk' password='aJS-yO6EBUg6DgzVQSFwp3Ac1v'"
        #Connection string to redshift
        #conn_string = "host='travelinsights-redshiftcluster-1vmmqnro7byz7.cbkwytfo7n8s.eu-west-1.redshift.amazonaws.com' port='5439' dbname='b2baggrarch' user='awsuser' password='asnou32mvdoQEsd!!24fgs6yhuU'"
     	#connect
        try:
            conn = psycopg2.connect(conn_string)
        except psycopg2.Error as e:
            print ("Unable to connect!")
            print (e.pgerror)
            print (e.diag.message_detail)
        else:
            print ("Connected!")

        return conn


    def getlasttimeupdate(self, table_name):

        connection = self.getconnection()
        cursor = connection.cursor()

        query = "SELECT to_char(max(dates),'YYYY-MM-DD') FROM log_updates WHERE tables = '"+table_name+"'"
        cursor.execute(query)
        results = cursor.fetchall()
        connection.close()
        return results[0][0]

    def getpopularitytable(self):

        connection = self.getconnection()
        cursor = connection.cursor()

        query = "SELECT origincitycode, destinationcitycode, concat(origincitycode, '-',destinationcitycode), seats FROM ptbexits_popular \
        WHERE origincitycode > 'AAA' and destinationcitycode > 'AAA' ORDER BY seats DESC LIMIT 10000"
        cursor.execute(query)

        rows = [('a','b','c', 1)]
        rowarray_list = []

        while len(rows) > 0:

            rows = cursor.fetchmany(500)
            # Convert query to row arrays
            for row in rows:
                rows_to_convert = (row[0], row[1], row[2], row[3])
                t = list(rows_to_convert)
                rowarray_list.append(t)

        j = json.dumps(rowarray_list)

        connection.close()
        return rowarray_list



    def getnewflightstable(self):

        connection = self.getconnection()
        cursor = connection.cursor()

        query = "SELECT concat(originairport, destinationairport,  carriercode, weekday_mon_1), originairport, destinationairport,  carriercode, weekday_mon_1, to_char(first_exit, 'YYYY-MM-DD'), to_char(first_flight, 'YYYY-MM-DD'), to_char(last_flight, 'YYYY-MM-DD')  FROM ptbexits_airservice \
        ORDER BY first_exit DESC LIMIT 10000"
        cursor.execute(query)

        rows = [('a','b','c', 'd', 'e', 'f', 'g', 'h')]
        rowarray_list = []

        while len(rows) > 0:

            rows = cursor.fetchmany(500)

            # Convert query to row arrays
            for row in rows:
                rows_to_convert = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                t = list(rows_to_convert)
                rowarray_list.append(t)

        j = json.dumps(rowarray_list)

        connection.close()
        return rowarray_list


def __init__(self):
        print ("in init")
