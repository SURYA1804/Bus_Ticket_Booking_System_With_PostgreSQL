from datetime import datetime
class BookingHistory:

    @classmethod
    def Insert_Rows_Into_Booking_History(self,BusId,SeatId,Price,DiscountRate,customer_id,cur,con):
        insert_query = """ insert into public."BookingRecords"("BusId","SeatId","Price","DiscountRate","DateTime","CustomerId")values(%s,%s,%s,%s,%s,%s)  ;"""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        cur.execute(insert_query,(BusId,SeatId,Price,DiscountRate,current_date,customer_id))
        con.commit()

