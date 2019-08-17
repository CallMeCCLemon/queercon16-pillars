###############################################################################
#    Author: CallMeCCLemon
#      Date: 2019
# Copyright: 2019 Thomas Littlejohn (@CallMeCCLemon) - Modified BSD License
###############################################################################

import pandas as pd
import pymysql

from PythonApp.cloud.model.DatabaseUpdate import DatabaseUpdate


class RdsDao:
    def __init__(self):
        self.host = "qc16-test-db-1.cywp7i1l4mst.us-west-2.rds.amazonaws.com"
        self.port = 3306
        self.dbname = "qc16_db_test_1"
        self.table_name = "badge_messages"
        self.user = "admin"
        self.password = "qc_16_db"
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(
            self.host,
            user=self.user,
            port=self.port,
            passwd=self.password,
            db=self.dbname)

    def execute_query(self, query):
        self.connect()
        results = self.conn.cursor().execute(query)
        self.conn.commit()
        self.disconnect()
        return results

    def read(self, query) -> pd.DataFrame:
        self.connect()
        response = pd.read_sql(query, con=self.conn)
        self.disconnect()
        return response

    def write_update(self, update: DatabaseUpdate):
        query = "insert into {} " \
                "(badge_id, badge_type, creation_time, currency_type, quantity) " \
                "values ({}, '{}', '{}', {}, {})"\
            .format(
                self.table_name,
                update.badge_id,
                update.badge_type.value,
                update.creation_time,
                update.currency_type.value,
                update.quantity)
        print(query)
        response = self.execute_query(query)
        return response

    def disconnect(self):
        self.conn.close()
