#!/usr/bin/python3

import exif
import argparse
import os
from PIL import Image
import sys
import datetime


parser_description = '''
                    photometacleaner tool by rootshellace

                    This is a tool used to clear metadata from photos.

                    You must pass one argument, either a full path of 
                    a file or a full one for a directory. In case you 
                    want to clear the metadata for a single file, use
                    -f or --file and provide the path to that file. If
                    you want to clear a full batch of photos at once,
                    use -d or --directory and provide the path to that
                    directory where all the photos are located.

                    [•] Usage example for single file [•]

                    ./photometacleaner.py -f /home/rootshellace/my_photo.jpg

                    It will create a copy of the original image, in the
                    same location, having metadata deleted, and with 
                    the following type of name, based on the timestamp
                    of the execution:

                    cleared_20230203-142321_my_photo.jpg

                    [•] Usage example for directory [•]

                    ./photometacleaner.py -d /home/rootshellace/Pictures

                    It applies the same logic as above to all photos 
                    found in the mentioned directory and its sub
                    directories. Naming convention is the same as in 
                    the example for single file.
                    '''

colorset = {'red':"\033[91m{}\033[00m", 'green':"\033[92m{}\033[00m", 'yellow':"\033[93m{}\033[00m", 'purple':"\033[95m{}\033[00m",
            'blue':"\033[94m{}\033[00m", 'light_gray':"\033[97m{}\033[00m"}


def get_arguments():

    parser = argparse.ArgumentParser(description=parser_description, 
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    input_group_args = parser.add_mutually_exclusive_group(required=True)

    input_group_args.add_argument('-f', '--file', type=str, metavar='FILE_PATH', 
                                    help='Select this option if you want to pass a file as input')

    input_group_args.add_argument('-d', '--directory', type=str, metavar='DIRECTORY', 
                                    help='Select this option if you want to pass a directory as input')

    args = parser.parse_args()

    return args


def show_header(msg, color):

    print(color.format("=" * 80))
    print(color.format("=" * 3 + str(msg).center(74) + "=" * 3))
    print(color.format("=" * 80))


def show_footer(color):

    print(color.format("=" * 80))

def show_option_header(file_flag, directory_flag, color):

    show_header("OPTIONS SECTION", color)

    try:
        if file_flag:
            print(color.format("[+] Option chosen : FILE"))
            print(color.format("[+] File name : " + file_flag))
        else:
            print(color.format("[+] Option chosen : DIRECTORY"))
            print(color.format("[+] Directory name : " + directory_flag))
    
    except Exception as exc:
        print(color.format("[-] <SHOW OPTIONS ERROR> " + str(exc)))

    show_footer(color)


def check_is_file(file_name):

    return os.path.isfile(file_name)


def check_is_dir(dir_name):

    return os.path.isdir(dir_name)


def check_file_is_photo(file_name):

    try:
        current_img = Image.open(file_name)
        msg = str(current_img.format)
        current_img.close()
        is_photo = True

    except Exception as exc:
        msg = str(exc)
        is_photo = False

    return is_photo, msg

def get_file_list(root_dir):

    try:
        file_list = []
        full_items = os.walk(root_dir) 
        for root, dirs, files in full_items:
            for file in files:
                file_list.append(os.path.join(root, file))

    except Exception as exc:
        print("[-] <GET FILE LIST ERROR> " + str(exc))

    return file_list

def clean_photo_meta(photo_path):

    try:
        photo_name = os.path.basename(photo_path)
        print("[+] Photo name:", photo_name)
        photo_dir = os.path.dirname(photo_path)
        print("[+] Photo directory:", photo_dir)

        print("[+]", photo_name, ": attempting to clear metadata...")

        try:

            current_image = exif.Image(photo_path)
            
            for metavar in current_image.list_all():
                current_image.delete(metavar)
            
            print("[+]", photo_name, ": succesfully cleared metadata!")
        
        except Exception as exc:
            print("[-] <CLEAN FILE ERROR> ", str(exc))
            show_footer(colorset['red'])
            sys.exit()

        clear_photo_name_prefix = "cleared_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + "_"
        cleared_photo_name = clear_photo_name_prefix + photo_name
        cleared_image_path = os.path.join(photo_dir, cleared_photo_name)

        try:
            print("[+] Attempting to create", cleared_image_path, '...')
            new_image = open(cleared_image_path, 'wb')
            new_image.write(current_image.get_file())
            new_image.close()
            print("[+] Successfully created", cleared_image_path, "!")
        
        except Exception as exc:
            print("[-] <CREATE CLEARED PHOTO ERROR> ", str(exc))
            show_footer(colorset['red'])
            sys.exit()

    except Exception as exc:
        print("[-] <CLEAN SECTION FILE PARAMETER SET ERROR> ", str(exc))
        show_footer(colorset['red'])
        sys.exit()

if __name__ == '__main__':

    args = get_arguments()

    show_header("photometacleaner by rootshellace", colorset['red'])
    show_option_header(args.file, args.directory, colorset['green'])
    
    if args.file:
        show_header("VALIDATION SECTION", colorset['purple'])
        
        if check_is_file(args.file):
            print("[+]", args.file, ": exists and is file")
            is_photo, msg = check_file_is_photo(args.file)
        
            if is_photo:
                print("[+]", args.file, ": is photo with", msg, "format")
                show_footer(colorset['purple'])
                show_header("CLEANING SECTION", colorset['yellow'])
                clean_photo_meta(args.file)
                show_footer(colorset['yellow'])
        
            else:
                print("[-]", args.file, ": is not a photo!")
                show_footer(colorset['purple'])
                sys.exit()
        
        else:
            print("[-]", args.file, ": not a file or file does not exist!")
            show_footer(colorset['purple'])
            sys.exit
    
    else:
        show_header("VALIDATION SECTION", colorset['purple'])
    
        if check_is_dir(args.directory):
            print("[+]", args.directory, ": exists and is directory")
            show_footer(colorset['purple'])
            show_header("CLEANING SECTION", colorset['yellow'])
            print("")
            file_list = get_file_list(args.directory)

            if file_list:
                for item in file_list:
                    is_photo, msg = check_file_is_photo(item)
    
                    if is_photo:
                        print("[+]", item, ": is photo with", msg, "format")
                        clean_photo_meta(item)
    
                    else:
                        print("[+]", item, ": is not a photo!")
    
                    print("")
    
            else:
                print("[+] No files found in", args.directory)
                print("")
            
            show_footer(colorset['yellow'])
    
        else:
            print("[-]", args.directory, ": not a directory or directory does not exist!")
            show_footer(colorset['purple'])
            sys.exit()
        

