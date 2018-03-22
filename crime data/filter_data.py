# Tianyi Lan #
# Challenge2: crime-data #

import csv, sys

def filter_data(filename):
    ''' This function takes in a csv file and keep only OFFENSE 2.0
        reports with non-empty zone
    '''
    result = csv.writer(sys.stdout, lineterminator='\n')
    with open(filename, 'r', encoding = 'utf-8') as file:
        next(file)
        types = ['3304', '2709', '3502', '13(a)(16)', '13(a)(30)',
                 '3701','3921', '3921(a)', '3934','3929', '2701',
                 '2702', '2501']
        for row in csv.reader(file):
            if row[1] != 'ARREST':
                if row[1] is None:
                    row[1] = 'OFFENSE 2.0'
                if row[7] and row[2] in types:
                    result.writerow(row)
    return result

if __name__ == "__main__" and len(sys.argv) > 1:
    filename = sys.argv[1]
    filter_data(filename)
