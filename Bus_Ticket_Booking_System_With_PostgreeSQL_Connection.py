import psycopg2 
from datetime import datetime
con = psycopg2.connect(host='127.0.0.1',database='postgres',user='postgres',password='Alterego@2',port = 5432)
cur = con.cursor()



class Booking:

    def Confirm_check(choice):
        return choice == 'Y'
    
    @classmethod
    def book_seats(self):
        insert_query = """insert into public."Booked"("BusId","SeatId","CustomerId") values(%s,%s,%s)"""
        price_query = """select "SeatPrice" from public."Seat" where "BusId" = %s and "SeatId" = %s;"""
        search_query = """select "BusId","SeatId" from public."Seat";"""
        i=0
        n=int(input("Enter number of Seat to Book:"))
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
                        cur.execute(insert_query,(BusId,SeatId,logged_in_customer_id))
                        con.commit()
                        cur.execute(price_query,(BusId,SeatId))
                        price = cur.fetchone()[0]
                        price = price - price * ( Discount.discount_rate(BusId,SeatId) / 100 )
                        BookingHistory.Insert_Rows_Into_Booking_History(BusId,SeatId,price,Discount.discount_rate(BusId,SeatId))
                        cart[i] = [BusId,SeatId,price,Discount.discount_rate(BusId,SeatId)]
                        i=i+1
                    else:
                        print("You cancelled the booking")
                else:
                    print("You Enter Wrong Id")
            else:
                print("The Seat is already Booked")
        Display.display_bill(cart)

class BookingHistory:

    @classmethod
    def Insert_Rows_Into_Booking_History(self,BusId,SeatId,Price,DiscountRate):
        insert_query = """ insert into public."BookingRecords"("BusId","SeatId","Price","DiscountRate","DateTime","CustomerId")values(%s,%s,%s,%s,%s,%s)  ;"""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        cur.execute(insert_query,(BusId,SeatId,Price,DiscountRate,current_date,logged_in_customer_id))
        con.commit()


class Discount:

    @classmethod
    def discount_rate(self,BusId,SeatId):
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

class Customer:

    @classmethod
    def authorize_customer(self):
       search_query = """ select "CustomerName" from public."Customer" where "CustomerEmail" = %s and "LoginPassword" = %s;  """
       customer_id_query = """select "CustomerId" from public."Customer" where "CustomerEmail" = %s and "LoginPassword" = %s;"""
       customer_email = str(input("Enter your Email:"))
       customer_login_password = str(input("Enter your login Password :"))
       cur.execute(customer_id_query,(customer_email,customer_login_password))
       global logged_in_customer_id
       logged_in_customer_id = cur.fetchone()[0]
       cur.execute(search_query,(customer_email,customer_login_password))
       customer_name = cur.fetchone()[0]
       return customer_name
    
    @classmethod
    def create_new_cutomer(self):
        create_customer_query = """ insert into public."Customer"("CustomerName","CustomerMobileNo","CustomerEmail","LoginPassword","DateJoined") values(%s,%s,%s,%s,%s) """
        customer_name = str(input("Enter your Name:"))
        customer_mobile_no = str(input("Enter your Mobile No:"))
        customer_email = str(input("Enter your Email:"))
        customer_login_password = str(input("Enter your Choice of Password to login:"))
        date_joined = datetime.now().strftime('%Y-%m-%d')
        cur.execute(create_customer_query,(customer_name,customer_mobile_no,customer_email,customer_login_password,date_joined))
        con.commit()

    @classmethod
    def customers_details(self):
        customer_details_query = """ select "CustomerName","CustomerMobileNo","CustomerEmail" from public."Customer" where "CustomerId" = %s;  """
        cur.execute(customer_details_query,(logged_in_customer_id,))
        customer_details = cur.fetchone()
        return customer_details
    
    @classmethod
    def update_customer_details(self,choice):
        if choice == 1:
            update_name_query = """update public."Customer" set "CustomerName" = %s where "CustomerId" = %s; """
            new_name = str(input("Enter new name to update:"))
            cur.execute(update_name_query,(new_name,logged_in_customer_id))
            con.commit()
            print("Updated Successfully!!")
        elif choice == 2:
            update_mobile_no_query = """update public."Customer" set "CustomerMobileNo" = %s where "CustomerId" = %s; """
            new_mobile_no = str(input("Enter new Mobile No to update:"))
            cur.execute(update_mobile_no_query,(new_mobile_no,logged_in_customer_id))
            con.commit()
            print("Updated Successfully!!")
        elif choice == 3:
            update_email_query = """update public."Customer" set "CustomerEmail" = %s where "CustomerId" = %s; """
            new_email = str(input("Enter new Email  to update:"))
            cur.execute(update_email_query,(new_email,logged_in_customer_id))
            con.commit()
            print("Updated Successfully!!")
        elif choice == 4:
            update_login_password_query = """update public."Customer" set "LoginPassword" = %s where "CustomerId" = %s; """
            new_login_password = str(input("Enter new Login Password  to update:"))
            cur.execute(update_login_password_query,(new_login_password,logged_in_customer_id))
            con.commit()
            print("Updated Successfully!!")
        else:
            print("Enter a valid Option")



class Display:

    @classmethod
    def display_total_seats(self):
        display_bus_query = """select * from public."Bus";"""
        cur.execute(display_bus_query)
        print("BusID\tBusName\tBusType\tBusSeatCount")
        print("-------------------------------------")
        total_bus = cur.fetchall()
        for i in total_bus:
            print(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}")
        print("-------------------------------------")

        display_bus_id = str(input("Enter the Bus Id to view:"))
        display_seats_query = """select * from public."Seat" where "BusId" = %s;"""
        cur.execute(display_seats_query, (display_bus_id,))
        total_seats = cur.fetchall()
        print("\nSeatId\tBusID\tSeatType\t\tSeatPrice\tSeatPlace")
        print("-------------------------------------------------------------------")
        for i in total_seats:
            print(f"{i[0]}\t{i[1]}\t{i[2]}||\t\t{i[3]}\t\t{i[4]}")
        print("-------------------------------------------------------------------")

    @classmethod
    def display_booked_seats(self):
        cur.execute("""select "BusId","SeatId" from public."Booked";""")
        booked_seats = cur.fetchall()
        if len(booked_seats) == 0:
            print("No Seats are Booked")
        else:
            cur.execute("""select "BusId","SeatId" from public."Booked";""")
            print("BusId\tSeatId")
            print("--------------")
            booked_seats = cur.fetchall()
            for i in booked_seats:
                print(f"{i[0]}\t{i[1]}")
            print("--------------")

    @classmethod
    def display_discount_details(self):
        query = """ select * from public."Discount"; """
        print("BusId\tSeatType\tDiscountRate")
        print("----------------------------------")
        cur.execute(query)
        discount_details  = cur.fetchall()
        for i in discount_details:
            print(f"{i[0]}\t{i[1]}||\t{i[2]}")
        print("----------------------------------")

    @classmethod
    def display_bill(self,cart):
        total=0
        print("\t\t******Bill******")
        print("S.No\tBusId\tSeatId\tDiscountRate\tFinal Price")
        print("---------------------------------------------------")

        for i in cart:
            print(f"{i+1}\t{cart[i][0]}\t{cart[i][1]}\t{cart[i][3]}\t\t{cart[i][2]}")
            total  = total + cart[i][2]
        print("---------------------------------------------------")
        print("Total Amount to pay :-\t\t\t",total)
        print("---------------------------------------------------")

    @classmethod
    def display_login_page(self):
        print("-------------------------------------------")
        print("|        WELCOME TO BUS BOOKING           |")
        print("-------------------------------------------")
        while  True:
            print("1.Create a New Account")
            print("2.Login")
            print("3.Exit")
            choice = int(input("Enter your option:"))
            if choice == 1:
                Customer.create_new_cutomer()
                print("=================================================")
                print("Account Created Successfully!!\nNow you can login")
                print("=================================================")
            elif choice == 2:
                customer_name = Customer.authorize_customer()
                if customer_name:
                    print("===========================================")
                    print(f"Welcome {customer_name}!!")
                    print(f"You Successfully Login as {customer_name}")
                    print("===========================================")
                    Display.display_user_menu()
                    break
                else:
                    print("========================================")
                    print("You Enter Wrong Details\nPlease Retry")
                    print("========================================")

            elif choice == 3:
                print("===========================")
                print("Thank You!!! Visit Again!!!")
                print("===========================")
                break
            else:
                print("Enter a Valid Choice.")

    @classmethod
    def display_user_menu(self):
        while True:
            print("-----------------------------------")
            print("|          MAIN SECTION           |")
            print("-----------------------------------")
            print("1.To view Your Details")
            print("2.To Update Your Details")
            print("3.Booking Section")
            print("4.Logout")
            choice = int(input("Enter your choice:"))
            if choice == 1:
                customer_details = Customer.customers_details()
                print("--------------------------------------")
                print("|            YOUR DETAILS            |")
                print("--------------------------------------")
                print(f"Name           :{customer_details[0]}")
                print(f"MobileNo       :{customer_details[1]}")
                print(f"Email          :{customer_details[2]}")
                print("--------------------------------------")
            elif choice == 2:
                print("-----------------------------------")
                print("|        UPDATE SECTION           |")
                print("-----------------------------------")
                print("1.Update Name")
                print("2.Update Mobile No")
                print("3.Update Email")
                print("4.Update LoginPassword")
                print("5.Go Back")                  
                choice = int(input("Enter your choice:"))
                if choice == 5:
                    Display.display_user_menu()
                else:
                    Customer.update_customer_details(choice)
            elif choice == 3:
                Display.display_booking_section()
            elif choice == 4:
                print("===========================")
                print("Thank You!!! Visit Again!!!")
                print("===========================")
                break
            else:
                print("Enter the Valid choice")
    
    @classmethod
    def display_booking_section(self):
        while True:
            print("-----------------------------------")
            print("|        BOOKING SECTION          |")
            print("-----------------------------------")
            print("1.To View the Seats")
            print("2.To Book the Seats")
            print("3.To View Discount Offers")
            print("4.To View the Booked Seats")
            print("5.Go Back")
            choice=int(input("Enter Your Choice:"))
            if choice == 1:
                Display.display_total_seats()
            elif choice == 2: 
                Booking.book_seats()
            elif choice == 3:
                Display.display_discount_details()
            elif choice == 4:
                Display.display_booked_seats()
            elif choice == 5:
                Display.display_user_menu()
            else:
                print("Enter the valid choice")

Display.display_login_page()


