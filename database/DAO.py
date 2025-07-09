from database.DB_connect import DBConnect
from model.order import Order


class DAO():

    @staticmethod
    def getAllStores():
         conn = DBConnect.get_connection()

         results = []

         cursor = conn.cursor(dictionary = True)

         query = """select distinct o.store_id as store from orders o """

         cursor.execute(query)

         for row in cursor:
             results.append(row["store"])

         cursor.close()
         conn.close()
         return results

    @staticmethod
    def getAllOrdersByStores(store):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct * from orders o where o.store_id = %s"""

        cursor.execute(query, (store, ))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results



        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(store, k, idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)

        query = """select distinct o1.order_id as id1 , o2.order_id as id2, count(oi1.quantity+oi2.quantity) as cnt
                    from orders o1, orders o2, order_items oi1, order_items oi2  
                    where o1.store_id = %s
                    and o1.store_id = o2.store_id
                    and o1.order_date > o2.order_date
                    and o1.order_id = oi1.order_id
                    and o2.order_id = oi2.order_id
                    and DATEDIFF(o1.order_date,o2.order_date )< %s
                    group by o1.order_id, o2.order_id"""

        cursor.execute(query, (store, k, ))
        for row in cursor:
            results.append((idMap[row["id1"]], idMap[row["id2"]], row["cnt"]))

        cursor.close()
        conn.close()
        return results
