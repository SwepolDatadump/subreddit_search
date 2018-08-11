import mysql.connector


class DCon(object):
    def __init__(self, db):
        self.mydb = mysql.connector.connect(
            host="your_host",
            user="your_user",
            password="your_password",
            database=db  # swepoldb
        )

    def __delete__(self, instance):
        self.mydb.close()

    def convert_query_to_dict(self, table_name, query_payload):
        cursor = self.mydb.cursor()
        cursor.execute("desc %s" % (table_name,))
        raw_cols = cursor.fetchall()

        container_list = list()
        if len(query_payload) > 1:
            for individual_result in query_payload:
                query_dict = dict()
                keys = list()
                for column in raw_cols:
                    key = column[0]
                    keys.append(key)
                    query_dict[key] = list()
                assert len(query_payload[0]) == len(keys)
                for col_result in range(len(individual_result)):
                    query_dict[keys[col_result]] = individual_result[col_result]
                container_list.append(query_dict)

        elif len(query_payload) == 1:
            query_dict = dict()
            keys = list()
            for column in raw_cols:
                key = column[0]
                keys.append(key)
                query_dict[key] = list()
            assert len(query_payload[0]) == len(keys)
            for col_result in range(len(query_payload[0])):
                query_dict[keys[col_result]] = query_payload[0][col_result]
            container_list.append(query_dict)

        else:
            query_dict = dict()
            for column in raw_cols:
                query_dict[column[0]] = False
            container_list.append(query_dict)

        return container_list

    # example: "CREATE TABLE table_name (name VARCHAR(60) NOT NULL DEFAULT 15, ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    def create_table(self, table_name, query_list):
        column_def_str = str()
        for definition in range(len(query_list)):
            if definition != len(query_list) - 1:
                column_def_str += query_list[definition] + ", "
            else:
                column_def_str += query_list[definition]

        sql = "CREATE TABLE %s (%s)" % (table_name, column_def_str)
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        return True

    def insert_values(self, table_name, column_string, value_list):
        # example: "INSERT INTO 'customers' ('name, address') VALUES ('john, this_street_11')"
        assert column_string.count(",")+1 == len(value_list)
        formatted_values = str()
        for entry in value_list:
            formatted_values += "'%s', " % entry
        formatted_values = formatted_values[:len(formatted_values)-2]
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, column_string, formatted_values)
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        self.mydb.commit()

    def select_where(self, table_name, column_list, value_list, get_col=False):
        assert len(column_list) == len(value_list)
        statement = str()
        for pair in range(len(value_list)):
            statement += "%s = '%s' " % (column_list[pair], value_list[pair])
            if pair != len(value_list)-1:
                statement += "AND "

        sql = "SELECT * FROM %s WHERE %s" % (table_name, statement)
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        result = self.convert_query_to_dict(table_name, cursor.fetchall())
        if get_col is not False:
            result = result[get_col]
        return result

    def select_or(self, table_name, column_list, value_list, get_col=False):
        assert len(column_list) == len(value_list)
        statement = str()
        for pair in range(len(value_list)):
            statement += "%s = '%s' " % (column_list[pair], value_list[pair])
            if pair != len(value_list) - 1:
                statement += "OR "

        sql = "SELECT * FROM %s WHERE %s" % (table_name, statement)
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        result = self.convert_query_to_dict(table_name, cursor.fetchall())
        if get_col is not False:
            result = result[get_col]
        return result

    def select_all(self, table_name, get_col=False):
        sql = "SELECT * FROM %s" % (table_name,)
        cursor = self.mydb.cursor()
        cursor.execute(sql)
        result = self.convert_query_to_dict(table_name, cursor.fetchall())
        if get_col is not False and result is not False:
            result = result[get_col]
        return result
