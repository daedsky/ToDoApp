import csv

class CsvEditor:
    @staticmethod
    def read_csv(fp):
        file = open(fp, 'r')
        data = csv.DictReader(file)
        return file, data

    @staticmethod
    def append_csv(fp, datarow):
        with open(fp, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(datarow)

    @staticmethod
    def write_csv(fp, datarow):
        with open(fp, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(datarow)
