import datetime
from mysql.connector import connect, Error


class basa:
    def __init__(self, host, user, password, database):
        self._connection = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conect_to_database(self):
        try:
            connection = connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            print("Успешное соедениенение с базой данных: " + self.database)
            self._connection = connection
        except Error as e:
            print(e)

    def create_new_table(self, name, create_table):
        create_table_query = """
        CREATE TABLE {}(
            {}
        )
        """.format(name, create_table)
        try:
            cursor = self._connection.cursor()
            cursor.execute(create_table_query)
            self._connection.commit()
            print("Успешное создание таблицы " + name)
        except Error as e:
            print(e)

    def delete_table(self, name):
        try:
            delete = """
            DROP TABLE {}
            """.format(name)
            cursor = self._connection.cursor()
            cursor.execute(delete)
            self._connection.commit()
            print("Успешное удаление таблицы " + name)
        except Error as e:
            print(e)

    def add_new_trunk(self, Model, ParamCharge, ParamQn,
                      ParamQg,
                      ParamQv,
                      P,
                      T,
                      ParamFlowRegime,
                      ParamFacticVelocity,
                      ParamCriticVelocity,
                      ParamCrash,
                      ParamLifetime,
                      ResidualResource):
        stmt = """INSERT
                    INTO trunks (Model, ParamCharge, ParamQn, ParamQg, ParamQv,
                           P,
                           T,
                           ParamFlowRegime,
                           ParamFacticVelocity,
                           ParamCriticVelocity,
                           ParamCrash,
                           ParamLifetime,
                           ResidualResource, created)
                    VALUES(%s, %s, %s, %s, %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s, UTC_TIMESTAMP());"""

        try:
            cursor = self._connection.cursor()
            cursor.execute(stmt, (Model, ParamCharge, ParamQn,
                                  ParamQg,
                                  ParamQv,
                                  P,
                                  T,
                                  ParamFlowRegime,
                                  ParamFacticVelocity,
                                  ParamCriticVelocity,
                                  ParamCrash,
                                  ParamLifetime,
                                  ResidualResource))
            self._connection.commit()
            print("Успешное добавление трубы в базу")
        except Error as e:
            print(e)

    def get_trunk(self, Model):
        try:
            cursor = self._connection.cursor()
            stmt = """SELECT id, Model, ParamCharge, ParamQn,
		ParamQg,
		ParamQv,
		P,
		T,
		ParamFlowRegime,
		ParamFacticVelocity,
		ParamCriticVelocity,
		ParamCrash,
		ParamLifetime,
		ResidualResource, created FROM trunks
    WHERE Model = %s """

            cursor.execute(stmt,(Model,))
            row = cursor.fetchone()
            print(row)

        except Error as e:
            print(e)

    def delete_all_rows(self, table_name):
        delete = """DELETE FROM {}""".format(table_name)
        try:
            cursor = self._connection.cursor()
            cursor.execute(delete)
            self._connection.commit()
            print("Успешное удаление всех строк из базы " + table_name)
        except Error as e:
            print(e)

    def print_all_rows(self, table_name):
        try:
            cur = self._connection.cursor()
            # Reading the Employee data
            cur.execute("select * from {}".format(table_name))
            # fetching the rows from the cursor object
            result = cur.fetchall()
            # printing the result
            for x in result:
                # if x!=None:
                print(x)
        except:
            self._connection.rollback()

    def custom_command(self, comand):
        r = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(comand)
            self._connection.commit()
            print("Успешное выполнение вашего запроса")
            r = cursor.fetchall()
        except Error as e:
            print(e)
        return r

    def check_conection(self):
        conect = self._connection
        print(conect.is_connected())
        if not conect.is_connected():
            conect = self.conect_to_database()
            self._connection = conect

    def disconect_database(self):
        try:
            self._connection.close()
            print("Сеанс с базой данных окончен успешно")
        except Error as e:
            print(e)
