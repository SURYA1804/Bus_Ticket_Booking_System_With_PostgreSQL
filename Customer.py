from datetime import datetime
import psycopg2
class Customer:

    @classmethod
    def authorize_customer(self,cur,con):
       customer_name_id_query = """ select "CustomerName","CustomerId" from public."Customer" where "CustomerEmail" = %s and "LoginPassword" = %s;  """
       extract_customer_list_query = """ select "CustomerEmail","LoginPassword" from public."Customer";  """
       cur.execute(extract_customer_list_query)
       customer_list = cur.fetchall()
       customer_email = str(input("Enter your Email:"))
       customer_login_password = str(input("Enter your login Password :"))
       if (customer_email,customer_login_password) in customer_list:
           cur.execute(customer_name_id_query,(customer_email,customer_login_password))
           customer_name,customer_id = cur.fetchone()
           return (customer_name,customer_id) 

    @classmethod
    def create_new_cutomer(self,cur,con):
        create_customer_query = """ insert into public."Customer"("CustomerName","CustomerMobileNo","CustomerEmail","LoginPassword","DateJoined") values(%s,%s,%s,%s,%s) """
        customer_name = str(input("Enter your Name:"))
        customer_mobile_no = str(input("Enter your Mobile No:"))
        customer_email = str(input("Enter your Email:"))
        customer_login_password = str(input("Enter your Choice of Password to login:"))
        date_joined = datetime.now().strftime('%Y-%m-%d')
        try:
            cur.execute(create_customer_query,(customer_name,customer_mobile_no,customer_email,customer_login_password,date_joined))
            con.commit()
        except psycopg2.errors.UniqueViolation:
            return None

    @classmethod
    def customers_details(self,customer_id,cur,con):
        customer_details_query = """ select "CustomerName","CustomerMobileNo","CustomerEmail" from public."Customer" where "CustomerId" = %s;  """
        cur.execute(customer_details_query,(customer_id,))
        customer_details = cur.fetchone()
        return customer_details
    
    @classmethod
    def update_customer_details(self,choice,customer_id,cur,con):
        if choice == 1:
            update_name_query = """update public."Customer" set "CustomerName" = %s where "CustomerId" = %s; """
            new_name = str(input("Enter new name to update:"))
            cur.execute(update_name_query,(new_name,customer_id))
            con.commit()
            print("Updated Successfully!!")
        elif choice == 2:
            update_mobile_no_query = """update public."Customer" set "CustomerMobileNo" = %s where "CustomerId" = %s; """
            new_mobile_no = str(input("Enter new Mobile No to update:"))
            cur.execute(update_mobile_no_query,(new_mobile_no,customer_id))
            con.commit()
            print("Updated Successfully!!")
        elif choice == 3:
            try:
                update_email_query = """update public."Customer" set "CustomerEmail" = %s where "CustomerId" = %s; """
                new_email = str(input("Enter new Email  to update:"))
                cur.execute(update_email_query,(new_email,customer_id))
                con.commit()
                print("Updated Successfully!!")
            except psycopg2.errors.UniqueViolation:
                print("Email Already Exits")

        elif choice == 4:
            get_old_password = """ select "LoginPassword" from public."Customer" where "CustomerId" = %s; """
            update_login_password_query = """update public."Customer" set "LoginPassword" = %s where "CustomerId" = %s; """
            cur.execute(get_old_password,(customer_id,))
            old_login_password = cur.fetchone()[0]
            user_enterd_old_login_password = str(input("Enter Old Login Password  to Verify:"))
            if old_login_password == user_enterd_old_login_password:
                new_login_password = str(input("Enter new Login Password  to update:"))
                cur.execute(update_login_password_query,(new_login_password,customer_id))
                con.commit()
                print("Updated Successfully!!")
            else:
                print("You Entered the Wrong Password")
        else:
            print("Enter a valid Option")

    @classmethod
    def customer_booking_history(self,customer_id,cur,con):
        query_to_get_booking_history_of_customer = """select "Bus"."BusName","s"."SeatType","s"."SeatPlace","b"."Price","b"."DiscountRate","b"."DateTime" from   
                                                     public."BookingRecords" "b" inner join public."Bus"  on "Bus"."BusId" = "b"."BusId" inner join public."Seat" "s"
                                                    on "b"."SeatId" = "s"."SeatId" and "b"."BusId" = "s"."BusId"  where b."CustomerId" = %s ;"""
        cur.execute(query_to_get_booking_history_of_customer,(customer_id,))
        booking_history = cur.fetchall()
        return booking_history