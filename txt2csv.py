import argparse
import glob
import os
import cv2
from csv import DictWriter

def generate_csv(img_dir, output_csv):
    
    if not output_csv.endswith('.csv'):
        output_csv += '.csv'
        
    if not os.path.isfile(output_csv):
        output_file = open(output_csv, 'w')
        output_file.close()
    
    tgt_images = sorted(glob.glob(os.path.join(img_dir, '*.png')))

    for i in range(len(tgt_images)):
        
        filename = os.path.basename(tgt_images[i])
        filename = os.path.splitext(filename)[0]
        split_filename = filename.split('_')
        
        fontname = split_filename[0]
        typeno = split_filename[1]
        unicode = split_filename[2]
        
        image = cv2.imread(tgt_images[i])
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        
        print("{}, {}, {}, {}, {}, {}".format(i,fontname,typeno,unicode,chr(int(unicode,16)), len(contours)))
        
        field_names = ['Index', 'Fontname', 'Type', 'Unicode', 'Character', 'len(contours)']

        contents = {'Index': i, 'Fontname': fontname, 'Type': typeno, 'Unicode': unicode, 'Character': chr(int(unicode, 16)), 'len(contours)': (len(contours))}
        
        with open(output_csv, newline='', mode='a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(contents)
            f_object.close()
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str, dest='img_dir', help='')
    parser.add_argument('--output-file', type=str, dest='output_csv', help='')
    args = parser.parse_args() 
    generate_csv(args.img_dir, args.output_csv)