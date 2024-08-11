import psycopg2
class Connection:
    @classmethod
    def connection(self): 
        con = psycopg2.connect(host='127.0.0.1',database='postgres',user='postgres',password='Alterego@2',port = 5432)
        cur = con.cursor()
        return cur,con



