from csv import reader
from math import sqrt
from math import exp
from math import pi

def load_csv(filename, allData):
    dataset = list()
    with open(filename, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue

            totalTest = 50
            if(len(row) >= totalTest):
                floatRow = list()
                objectType = -1;

                for cell in row:
                    if(cell == 'wall'):
                        objectType = 0
                        continue
                    if (cell == 'car'):
                        objectType = 1
                        continue
                    if (cell == 'human'):
                        objectType = 2
                        continue
                    else:
                        floatRow.append(float(cell))
                floatRow.sort(reverse = True)

                slice = floatRow[:totalTest]
                slice.append(objectType)
                allData.append(slice)

    return allData

# Convert string column to integer
def str_column_to_int(dataset, column):
    class_values = [row[column] for row in dataset]
    unique = set(class_values)
    lookup = dict()
    for i, value in enumerate(unique):
        lookup[value] = i
        print('[%s] => %d' % (value, i))
    for row in dataset:
        row[column] = lookup[row[column]]
    return lookup

# Convert string column to float
def str_column_to_float(dataset, column):
    for row in dataset:
        row[column] = float(row[column].strip())

wallFilename = 'ml/wallpeak.csv'
humanFilename = 'ml/humanpeak.csv'
carFilename = 'ml/carpeak.csv'

allData = list()

allData = load_csv(wallFilename, allData)
allData = load_csv(humanFilename, allData)
allData = load_csv(carFilename, allData)






