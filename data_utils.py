import os 
import datetime
import calendar
import csv
import cv2
import numpy as np
import skimage
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg 
import os 


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
        

def load_data(dir_name=None, img_list=None):
    gray_imgs = []
    color_imgs = []

    if dir_name is not None:
        for filename in sorted(os.listdir(dir_name)):
            if '.jpg' in filename:
                img = cv2.imread(dir_name + '/' + filename)
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                gray_img = cv2.imread(filename, 0)

                color_imgs.append(img)
                gray_imgs.append(gray_img)
    
    if img_list is not None:
        for filename in img_list:
            img = cv2.imread(filename)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            gray_img = cv2.imread(filename, 0)

            color_imgs.append(img)
            gray_imgs.append(gray_img)

    return color_imgs, gray_imgs

def visualize_image(imgs, img_titles, gray=False):
    rows, cols = 3, 3
    plt.figure(figsize=(20, 20))
    for i, img in enumerate(imgs):

        plt.add_subplot(rows, cols, i+1)
        if gray:
            plt.imshow(img, cmap='gray')
        else:
            plt.imshow(img)

        plt.title(img_titles[i])

    plt.show()


if __name__ == '__main__':
    clean_data()
    create_csv()
    