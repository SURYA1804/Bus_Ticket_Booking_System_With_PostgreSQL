
class Discount:

    @classmethod
    def discount_rate(self,BusId,SeatId,cur):
        search_query = """select "BusId","SeatType" from public."Seat" where "BusId" = %s and "SeatId" = %s; """
        discount_query = """select  "DiscountRate" from public."Discount" where "BusId" = %s and "SeatType" = %s;  """
        cur.execute(search_query,(BusId,SeatId))
        list_of_Seats = cur.fetchall()
        cur.execute(discount_query,(BusId,list_of_Seats[0][1]))
        discount_list = cur.fetchall()
        if len(discount_list) == 0:
            return 0
        else:
            return discount_list[0][0]
