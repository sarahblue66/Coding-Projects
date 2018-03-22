# Tianyi Lan #
# Challenge2: crime-data #

import psycopg2

conn = psycopg2.connect(host="localhost", database="tianyi_lan",
                       user="tianyi_lan", password="LanTY661231")

cur = conn.cursor()

# get neighborhood name list
cur.execute("""SELECT hood FROM neighborhoods;""")
all_neighborhoods = [hood[0] for hood in cur.fetchall()]
   
def fix_neighborhood(row):
   '''
   This function takes a string(neighborhood name) in a row
   and modify it according to sub and contain, then update,
   log the ones can't be fixed
   '''
   # only run if not matching
   if row[6] not in all_neighborhoods:
      cur.execute("""SELECT hood from neighborhoods where lower(hood) ilike '%%%s%%'""" %row[6])              
      substr = [val[0] for val in cur.fetchall()]
      cur.execute("""SELECT hood from neighborhoods where '%s' ilike format('%%%%%%s%%%%', lower(hood))""" %row[6])
      contain = [val[0] for val in cur.fetchall()]

      # update neighborhood names based on matching result
      if len(substr) != 0 or len(contain) != 0:
         if len(substr) == 1:
            print(str(row) + 'changed to ' + str(substr[0]), file = open('fixed_neighborhoods.txt','a'))
            return substr[0]
         elif len(contain) == 1:
            print(str(row) + 'changed to ' + str(contain[0]), file = open('fixed_neighborhoods.txt','a'))
            return contain[0]
         else:
            print('Warning:' + str(row) + 'have more than 1 neighborhood matches.\n')
            print(str(row), file = open('multiple_matches.txt','a'))
            return False

      # log unmatched ones
      else:
         print(str(row), file = open('no_neighborhood_match.txt','a'))
         return False
   else:
      return row[6]

