# Tianyi Lan #
# Challenge2: crime-data #

import psycopg2, sys, csv, fileinput
import fix_neighborhood
import fix_type

conn = psycopg2.connect(host="localhost", database="tianyi_lan",
                       user="tianyi_lan", password="LanTY661231")

cur = conn.cursor()

for row in csv.reader(fileinput.input()):
   # fix column data type
   fix_type.fix_type(row)
   # modify neighrborhood names if doesn't match 
   new_hood = fix_neighborhood.fix_neighborhood(row)
   if new_hood is False:
      continue
   else:
      row[6] = new_hood
               
   try:
      cur.execute("""INSERT INTO blotter
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (row))
      conn.commit()
               
   except psycopg2.Error as e:
      conn.rollback()
      # Unique id violation
      if e.pgcode == '23505':
         print(str(row), file = open('duplicated_rows.txt','a'))
         continue
      else:
         print(str(row) + str(e.pgcode) + str(sys.exc_info()[0]),
               file = open('ingest_unexpected_errors.txt','a'))
         continue

conn.close()           


