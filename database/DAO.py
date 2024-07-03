from database.DB_connect import DBConnect
from model.state import State


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getShapes(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape
                    from new_ufo_sightings.sighting s
                    where year(s.`datetime`)=%s and shape!=""
                    order by shape asc"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row["shape"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllStates():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from new_ufo_sightings.state 
                    order by id asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNeighbors():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select state1, state2
                    from new_ufo_sightings.neighbor """

        cursor.execute(query)

        for row in cursor:
            result.append((row["state1"], row["state2"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPeso(state_id, year, shape):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)
        query = """ select count(*) as tot
                    from new_ufo_sightings.sighting s 
                    where s.state=%s and year(s.`datetime`)=%s and s.shape=%s """

        cursor.execute(query, (state_id, year, shape))

        for row in cursor:
            result = row["tot"]

        cursor.close()
        conn.close()
        return result

