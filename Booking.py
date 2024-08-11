import BookingHistory
import Discount
import Display


class Booking:

    def Confirm_check(choice):
        return choice == 'Y' or 'y'
    
    @classmethod
    def book_seats(self,customer_id,cur,con,):
        insert_query = """insert into public."Booked"("BusId","SeatId","CustomerId") values(%s,%s,%s)"""
        price_query = """select "SeatPrice" from public."Seat" where "BusId" = %s and "SeatId" = %s;"""
        search_query = """select "BusId","SeatId" from public."Seat";"""
        i=0
        try:
           n=int(input("Enter number of Seat to Book:"))
        except ValueError:
            print("Enter only interger")
        else:
            cart = dict()
            while i<n:
                cur.execute("""select "BusId","SeatId" from public."Booked";""")
                BusId = str(input("Enter the bus Id:"))
                SeatId = str(input("Enter the Seat Id:"))
                Booked_Seats = cur.fetchall()
                if (BusId,SeatId) not in Booked_Seats:
                    cur.execute(search_query)
                    Valid_seats = cur.fetchall()
                    if (BusId,SeatId) in Valid_seats:
                        if self.Confirm_check(choice=str(input("Enter Y to confirm:"))):
                            cur.execute(insert_query,(BusId,SeatId,customer_id))
                            con.commit()
                            cur.execute(price_query,(BusId,SeatId))
                            price = cur.fetchone()[0]
                            price = price - price * ( Discount.Discount.discount_rate(BusId,SeatId) / 100 )
                            BookingHistory.Insert_Rows_Into_Booking_History(BusId,SeatId,price,Discount.Discount.discount_rate(BusId,SeatId,cur),customer_id,cur,con)
                            cart[i] = [BusId,SeatId,price,Discount.Discount.discount_rate(BusId,SeatId)]
                            i=i+1
                        else:
                            print("You cancelled the booking")
                    else:
                        print("You Enter Wrong Id")
                else:
                    print("The Seat is already Booked")
            Display.Display.display_bill(cart)