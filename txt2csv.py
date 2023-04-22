import csv
import os


# export 디렉토리 없으면 생성
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(os.path.join(output_dir))


