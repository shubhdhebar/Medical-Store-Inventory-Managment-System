import psycopg2

conn = psycopg2.connect("dbname=pharma user=postgres password=tiger")
cur = conn.cursor()
fname = "Shubh"
sql="select*from customer where fname = %s;"

cur.execute(sql,(fname,))
row=cur.fetchone()
print(row[0])

cur.close()
