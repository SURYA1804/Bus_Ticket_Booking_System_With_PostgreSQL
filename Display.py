import Booking
import Customer

class Display:

    @classmethod
    def display_available_seats(self,customer_id,cur,con):
        display_bus_query = """select * from public."Bus";"""
        cur.execute(display_bus_query)
        print("BusID\tBusName\tBusType\tBusSeatCount")
        print("-------------------------------------")
        total_bus = cur.fetchall()
        for i in total_bus:
            print(f"{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}")
        print("-------------------------------------")

        display_bus_id = str(input("Enter the Bus Id to view:"))
        display_seats_query = """select * from public."Seat" where "BusId" = %s and "SeatId" not in (select "SeatId" from public."Booked") ;"""
        cur.execute(display_seats_query, (display_bus_id,))
        total_seats = cur.fetchall()
        print("\nSeatId\tBusID\tSeatType\t\tSeatPrice\tSeatPlace")
        print("-------------------------------------------------------------------")
        for i in total_seats:
            print(f"{i[0]}\t{i[1]}\t{i[2]}||\t\t{i[3]}\t\t{i[4]}")
        print("-------------------------------------------------------------------")

    @classmethod
    def display_booked_seats(self,customer_id,cur,con):
        cur.execute("""select "BusId","SeatId" from public."Booked";""")
        booked_seats = cur.fetchall()
        print("-------------------------------------------")
        print("|               BOOKED SEATS              |")
        print("-------------------------------------------")
        if len(booked_seats) == 0:
            print("No Seats are Booked")
        else:
            cur.execute("""select "BusId","SeatId" from public."Booked";""")       
            print("\tBusId\tSeatId")
            print("|---------------------|")
            booked_seats = cur.fetchall()
            for i in booked_seats:
                print(f"\t{i[0]} \t{i[1]} ")
            print("|---------------------|")

    @classmethod
    def display_discount_details(self,customer_id,cur,con):
        query = """ select * from public."Discount"; """
        print("-------------------------------------------")
        print("|            DISCOUNT OFFERS              |")
        print("-------------------------------------------")
        print("BusId\tSeatType\tDiscountRate")
        print("----------------------------------")
        cur.execute(query)
        discount_details  = cur.fetchall()
        for i in discount_details:
            print(f" {i[0]}\t{i[1]}||\t{i[2]}")
        print("----------------------------------")

    @classmethod
    def display_bill(self,cart):
        total=0
        print("--------------------------------------------------")
        print("|                      BILL                      |")
        print("--------------------------------------------------")
        print("S.No\tBusId\tSeatId\tDiscountRate\tFinal Price")
        print("--------------------------------------------------")

        for i in cart:
            print(f"{i+1}\t{cart[i][0]}\t{cart[i][1]}\t{cart[i][3]}\t\t{cart[i][2]}")
            total  = total + cart[i][2]
        print("---------------------------------------------------")
        print(f"|Total Amount to pay :-\t\t\t{total}|")
        print("---------------------------------------------------")

    @classmethod
    def display_login_page(self,cur,con):
        print("-------------------------------------------")
        print("|        WELCOME TO BUS BOOKING           |")
        print("-------------------------------------------")
        while  True:
            print("1.Create a New Account")
            print("2.Login")
            print("3.Exit")
            try:
                choice = int(input("Enter your option:"))
            except ValueError:
                print("===================")
                print("Enter integer only")
                print("===================")
            else:
                if choice == 1:
                    if Customer.Customer.create_new_cutomer(cur,con):
                        print("=================================================")
                        print("Account Created Successfully!!\nNow you can login")
                        print("=================================================")
                    else:
                        print("=================================================")
                        print("You Entered Email Already Registered")
                        print("=================================================")
                elif choice == 2:
                    customer_details = Customer.Customer.authorize_customer(cur,con)
                    if customer_details:
                        customer_name,customer_id = customer_details
                        print("===========================================")
                        print(f"Welcome {customer_name}!!")
                        print(f"You Successfully Logged In")
                        print("===========================================")
                        Display.display_user_menu(customer_id,cur,con)
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
    def display_user_menu(self,customer_id,cur,con):
        while True:
            print("-----------------------------------")
            print("|          MAIN SECTION           |")
            print("-----------------------------------")
            print("1.To view Your Details")
            print("2.To Update Your Details")
            print("3.Booking Section")
            print("4.Booking History")
            print("5.Logout")
            try:
                choice = int(input("Enter your option:"))
            except ValueError:
                print("===================")
                print("Enter integer only")
                print("===================")
            else:
                if choice == 1:
                    Display.display_customer_details(customer_id,cur,con)
                elif choice == 2:
                    Display.display_update_section(customer_id,cur,con)
                elif choice == 3:
                    Display.display_booking_section(customer_id,cur,con)
                elif choice == 4:
                    Display.display_customer_booking_history(customer_id,cur,con)
                elif choice == 5:
                    print("===========================")
                    print("Thank You!!! Visit Again!!!")
                    print("===========================")
                    con.close()
                    break
                else:
                    print("Enter the Valid choice")
    
    @classmethod
    def display_customer_booking_history(self,customer_id,cur,con):
        booking_history = Customer.Customer.customer_booking_history(customer_id,cur,con)
        print("--------------------------------------")
        print("|          BOOKING HISTORY           |")
        print("--------------------------------------")        
        if len(booking_history) == 0:
            print("Since You have No Booking History")
        else:
            print("BusName\tSeatType\t\tSeatPlace\tPrice\tDiscountRate\tDate")
            print("------------------------------------------------------------------------------")
            for i in booking_history:
                print(f"{i[0]}\t{i[1]}||\t\t{i[2]}\t{i[3]}\t{i[4]}\t  {i[5]}")
            print("------------------------------------------------------------------------------")

    @classmethod
    def display_customer_details(self,customer_id,cur,con):
        customer_details = Customer.Customer.customers_details(customer_id,cur,con)
        print("--------------------------------------")
        print("|            YOUR DETAILS            |")
        print("--------------------------------------")
        print(f"Name           :{customer_details[0]}")
        print(f"MobileNo       :{customer_details[1]}")
        print(f"Email          :{customer_details[2]}")
        print("--------------------------------------")

    @classmethod
    def display_update_section(self,customer_id,cur,con):
        print("-----------------------------------")
        print("|        UPDATE SECTION           |")
        print("-----------------------------------")
        print("1.Update Name")
        print("2.Update Mobile No")
        print("3.Update Email")
        print("4.Update LoginPassword")
        print("5.Go Back")                  
        try:
            choice = int(input("Enter your option:"))
        except ValueError:
            print("===================")
            print("Enter integer only")
            print("===================")
        else:
            if choice == 5:
                Display.display_user_menu(customer_id,cur,con)
            else:
                Customer.Customer.update_customer_details(choice,customer_id,cur,con)

    @classmethod
    def display_booking_section(self,customer_id,cur,con):
        while True:
            print("-----------------------------------")
            print("|        BOOKING SECTION          |")
            print("-----------------------------------")
            print("1.To View Available Seats")
            print("2.To Book the Seats")
            print("3.To View Discount Offers")
            print("4.To View the Booked Seats")
            print("5.Go Back")
            try:
                choice = int(input("Enter your option:"))
            except ValueError:
                print("===================")
                print("Enter integer only")
                print("===================")
            else:
                if choice == 1:
                    Display.display_available_seats(customer_id,cur,con)
                elif choice == 2: 
                    Booking.Booking.book_seats(customer_id,cur,con)
                elif choice == 3:
                    Display.display_discount_details(customer_id,cur,con)
                elif choice == 4:
                    Display.display_booked_seats(customer_id,cur,con)
                elif choice == 5:
                    Display.display_user_menu(customer_id,cur,con)
                    break
                else:
                    print("Enter the valid choice")

