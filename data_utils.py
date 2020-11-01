import os 
import datetime
import calendar
import csv
import cv2

START_DATE = datetime.date(2015, 8, 8)
CSV_FILE = "teeth_summary.csv"
INPUT_DIR = "../Teeth_Original/"
OUTPUT_DIR = "../Teeth/"
TEET_VIEWS = ['Fontal', 'Right', 'Left', 'Right', 'Upper', 'Lower']


def clean_data():
    """
    Create all file names with same length
    For examples: 
    1435_8251.jpg -> 1435_008251.jpg
    """


    for img_file in sorted(os.listdir(INPUT_DIR)):
        if '.jpg' in img_file:
            img_name = img_file.split('.')[0]

            first_part, second_part = img_name.split('_')[0], img_name.split('_')[1]

            if len(second_part) == 4:
                second_part = '00' + second_part 
            elif len(second_part) == 5:
                second_part = '0' + second_part
            else:
                seconda_part = second_part

            img_name = first_part + '_' + second_part + '.jpg'

            image = cv2.imread(INPUT_DIR + img_file)
            cv2.imwrite(OUTPUT_DIR + img_name, image)

def add_month(startdate, months=1):
    """
    Increase date time after every 6 images.
    """
    month = startdate.month - 1 + months
    year = startdate.year + month // 12 
    month = month % 12 + 1
    day = min(startdate.day, calendar.monthrange(year, month)[1]) 

    print(datetime.date(year, month, day))
    return datetime.date(year, month, day)

def create_csv():
    # create csv file
    with open(CSV_FILE, 'a', newline='') as input_file:
        csv_writer = csv.writer(input_file, delimiter=',')
        csv_writer.writerow(['Date Time', 'Image Path', 'Image Name', 'View'])

    # read all file
    count = 0
    date_time = START_DATE
    print(datetime.date(2015, 8, 8))
    for img_file in sorted(os.listdir(OUTPUT_DIR)):
        print('[INFO] Writing file ... {}'.format(img_file))

        with open(CSV_FILE, 'a', newline='') as input_file:
            csv_writer = csv.writer(input_file, delimiter=',')
            csv_writer.writerow([date_time, OUTPUT_DIR + img_file, img_file, TEET_VIEWS[count % 6]])
        
        count += 1
        if count % 6 == 0:
            date_time = add_month(startdate=date_time, months=1)
        

if __name__ == '__main__':
    clean_data()
    create_csv()
    