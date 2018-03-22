# Tianyi Lan #
# Challenge2: crime-data #

import psycopg2, sys
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

conn = psycopg2.connect(host="localhost", database="tianyi_lan",
                       user="tianyi_lan", password="LanTY661231")

cur = conn.cursor()

#produce a table of counts of crimes each week, split up by type of crime
cur.execute("""SELECT section as section, description as crime_type, 
		count(*) as count FROM blotter 
		WHERE date_part('day', (SELECT max(arrest_time) from blotter)-arrest_time)<=7
		GROUP BY section, crime_type ORDER BY count""")

# headers for table
headers = ['Section', 'Crime Type', 'Count']
all_rows = []
for row in cur:
    all_rows.append(row)

# print table with title
print('Table 1: crime counts by crime type', file = open('weekly_report.txt', 'a'))  
print('\n' + tabulate(all_rows, headers), file = open('weekly_report.txt', 'a'))

# list the changes in number of crimes between this week and last week
# split up by police zone
cur.execute("""SELECT latest.zone as latest_zone, last.zone as last_zone,
	latest.latest_count as latest_count, last.last_count as last_count INTO temp1 FROM
	(SELECT zone, count(*) as latest_count FROM blotter 
	WHERE date_part('day', (SELECT max(arrest_time) from blotter)-arrest_time)<=7
	group by zone) latest FULL OUTER JOIN
	(SELECT zone, count(*) as last_count from blotter 
	WHERE date_part('day', (SELECT max(arrest_time) FROM blotter) - arrest_time)
	BETWEEN 7 and 14 GROUP BY zone) last ON latest.zone = last.zone
	ORDER BY latest.zone""")
cur.execute("""UPDATE temp1 SET latest_zone=last_zone, latest_count=0 WHERE latest_zone is NULL""")
cur.execute("""UPDATE temp1 SET last_zone=latest_zone, last_count=0 WHERE last_zone is NULL""")
cur.execute("""SELECT latest_zone as zone, latest_count-last_count as change FROM temp1 ORDER BY zone""")

# headers for table
header1 = ['Police Zone', 'Changes in number of crimes \n (latest week - last week)']
rows_by_zone = []
for row in cur:
    rows_by_zone.append(row)
    
# print table with title   
print('\n\nTable2: changes in number of crimes between this week and last week by police zone',
      file = open('weekly_report.txt', 'a'))     
print('\n' + tabulate(rows_by_zone, header1), file = open('weekly_report.txt', 'a'))

# split up by neighborhood
cur.execute("""SELECT latest.neighborhood as latest_neighborhood, last.neighborhood as last_neighborhood,
	latest.latest_count as latest_count, last.last_count as last_count into temp2 FROM
	(SELECT neighborhood, count(*) as latest_count FROM blotter 
	WHERE date_part('day', (SELECT max(arrest_time) FROM blotter)-arrest_time)<=7
	GROUP BY neighborhood) latest FULL OUTER JOIN
	(SELECT neighborhood, count(*) as last_count FROM blotter 
	WHERE date_part('day', (SELECT max(arrest_time) FROM blotter)-arrest_time) BETWEEN 7 and 14
	GROUP BY neighborhood) last ON latest.neighborhood = last.neighborhood
	ORDER BY latest.neighborhood""")
cur.execute("""UPDATE temp2 SET latest_neighborhood=last_neighborhood, latest_count=0 WHERE latest_neighborhood is NULL""")
cur.execute("""UPDATE temp2 SET last_neighborhood=latest_neighborhood, last_count=0 WHERE last_neighborhood is NULL""")
cur.execute("""SELECT latest_neighborhood as neighborhood, latest_count-last_count as change FROM temp2 ORDER BY neighborhood""")

# headers for table
header2 = ['Neighborhood', 'Changes in number of crimes \n (latest week - last week)']
rows_by_neighborhood = []
for row in cur:
    rows_by_neighborhood.append(row)

# print table with title
print('\n\nTable 3: changes in number of crimes between this week and last week by neighborhood',
      file = open('weekly_report.txt', 'a'))  
print('\n' + tabulate(rows_by_neighborhood, header2), file = open('weekly_report.txt', 'a'))

# Graph the total number of crimes per day over the past month
cur.execute("""SELECT arrest_time::date as day, count(*) as count FROM blotter 
  WHERE date_part('day', (SELECT max(arrest_time) FROM blotter)) - date_part('day', arrest_time)<=30
  GROUP BY day ORDER BY day""")
		
date =[]
freq =[]
for row in cur:
    date.append(row[0])
    freq.append(row[1])

plt.title('Crimes Counts by Day')
plt.xlabel('Date')
plt.ylabel('Count')
plt.bar(date, freq, align='center')
plt.xticks(date, rotation=90)
formatter = DateFormatter('%y/%m/%d')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.subplots_adjust(left=0.07, right=0.98, bottom=0.2)
plt.show()
