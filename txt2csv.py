import argparse
import glob
import os
import cv2
from csv import DictWriter

def generate_csv(img_dir, output_csv):
    
    output_file =  output_csv+'.csv'
    if not os.path.isfile(output_file):
        output_file = open(output_file, 'w')
        output_file.close()
    
    tgt_images = sorted(glob.glob(os.path.join(img_dir, '*.png')))

    for i in range(len(tgt_images)):
        
        image = cv2.imread(tgt_images[i])
        filename = tgt_images[i]
        
        # The idx must be checked
        character_unicode = filename[-8:-4]
        font_name = filename[27:-11]
        character_type = filename[-10:-9]
        
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        
        #print("{}, Naver, {}, {}, {}, {}, {}".format(i,font_name,character_type,character_unicode,chr(int(character_unicode,16)), len(contours)))
        
        field_names = ['Index', 'Fontname', 'Type', 'Unicode', 'Character', 'len(contours)']

        contents = {'Index': i, 'Fontname': font_name, 'Type': character_type, 'Unicode': character_unicode, 'Character': chr(int(character_unicode, 16)), 'len(contours)': len(contours)}
        
        with open(output_file, newline='', mode='a') as f_object:
            dictwriter_object = DictWriter(f_object, fieldnames=field_names)
            dictwriter_object.writerow(contents)
            f_object.close()
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str, dest='img_dir', help='')
    parser.add_argument('--output-file', type=str, dest='output_file', help='')
    args = parser.parse_args() 
    generate_csv(args.img_dir, args.output_file)