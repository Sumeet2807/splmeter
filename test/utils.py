import csv
from pathlib import Path
path = Path("../data/test.csv").parent

def get_tolerance_dict_from_csv(csvpath):
    tolerance_dict  ={}
    base_path = Path(__file__).parent
    file_path = (base_path / csvpath).resolve()

    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            tolerance_dict[float(row[0])] = {'A':float(row[1]),
                                        'C':float(row[2]),
                                        'class1':[float(row[4]),float(row[3])],
                                        'class2':[float(row[6]),float(row[5])]

                                        }
    
    if len(tolerance_dict)<=0:
        raise Exception('Tolerance file could not be processed.')            
    return tolerance_dict
