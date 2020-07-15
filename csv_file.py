import csv


def create_csv(file_name, file_header):
    with open(file_name,'w') as f:
        print(f"file_name: {file_name}")
        csv_write = csv.writer(f)
        csv_write.writerow(file_header)

def write_csv(file_name, file_header, row):
    with open(file_name,'a+') as f:
        csv_write = csv.writer(f)

        list_data = []
        for key_name in file_header:
            list_data.append(row.get(key_name, "-"))
        # print(list_data)
        csv_write.writerow(list_data)

