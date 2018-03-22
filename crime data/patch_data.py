# Tianyi Lan #
# Challenge2: crime-data #

import psycopg2, sys, csv, fileinput
import fix_neighborhood
import fix_type

conn = psycopg2.connect(host="localhost", database="tianyi_lan",
                       user="tianyi_lan", password="LanTY661231")
cur = conn.cursor()

#count number of patched rows
num = 0

for row in csv.reader(fileinput.input()):
    #fix data column type
    fix_type.fix_type(row)
    # modify neighborhood names if does not match 
    new_hood = fix_neighborhood.fix_neighborhood(row)
    
    if new_hood is False:
       continue
    else:
       num += 1
       row[6] = new_hood

    try:
        cur.execute("""INSERT INTO blotter
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (row))
        conn.commit()
        
    except psycopg2.Error as e:
        conn.rollback()
        # Unique id violation
        if e.pgcode == '23505':
            print(str(row), file = open('updated_ids.txt','a'))
            cur.execute("""UPDATE blotter SET report_name=%s, section=%s,
            description=%s, arrest_time=%s, address=%s, neighborhood=%s,
            zone=%s where id=%s""", (row[1], row[2], row[3], row[4],
                                     row[5], row[6], row[7], row[0]))
            conn.commit()
        else:
            num -= 1
            print(str(row) + str(e.pgcode) + str(sys.exc_info()[0]),
                  file = open('patch_unexpected_errors.txt','a'))
            
print(num)

conn.close()
