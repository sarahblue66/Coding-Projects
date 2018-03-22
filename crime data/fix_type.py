# Tianyi Lan #
# Challenge2: crime-data #

def fix_type(row):
   """ This functions takes in a row and change id, zone columns to integer,
       and change arrest_time to timestamp format
   """
   row[0] = int(row[0])
   row[4] = row[4].replace("T", " ")
   row[7] = int(row[7])

