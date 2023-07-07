# photometacleaner by rootshellace

This is a Python tool that can be used to clear metadata from photos.

## Usage

There is 1 argument required by this script, and it is mandatory:

- Type of input (path to file/path to directory)

If you run it without any arguments, it will show an error message saying one is required.

```
usage: photometacleaner.py [-h] (-f FILE_PATH | -d DIRECTORY)
photometacleaner.py: error: one of the arguments -f/--file -d/--directory is required
```

To see the help message, just execute the script with *-h* argument.
```bash
./photometacleaner.py -h
```
It will display the full message, just like below:
```
usage: photometacleaner.py [-h] (-f FILE_PATH | -d DIRECTORY)

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
                    

optional arguments:
  -h, --help            show this help message and exit
  -f FILE_PATH, --file FILE_PATH
                        Select this option if you want to pass a file as input
  -d DIRECTORY, --directory DIRECTORY
                        Select this option if you want to pass a directory as input
```
## Arguments

* **FILE_PATH/DIRECTORY**

The path you provide, file or directory, must be valid. Otherwise, it will throw an error at validation step and a message will be shown in the output. Also, if you pass a path for a file and it is not a photo, again, an error message will be displayed in the same section.

In case you pass as argument a path which does not contain any photos, a message will pop up, saying there are not any files in that directory. If there are files, it will only perform cleanup on photos, it will not affect other type of files.

For each photo, it will create a copy with metadata cleared. The naming convention for this new photo is:

```
cleared_<creation_timestamp>_<original_file_name>
```

The format for <creation_timestamp> is YYYYMMDD-HHMMSS.

## Prerequisites

First, you must have Python 3 installed. I have tested the tool on Python 3.9.2 version. 
I have also used a couple of modules : *argparse*, *exif*, *os*, *PIL*, *sys*, *datetime*. 


Many of them are default Python modules (or they should be), except *exif* and, maybe, *PIL*. These must be installed separately. 
Using pip3, just run this command:

```
pip3 install exif
pip3 install Pillow
```

On my Linux distribution, Pillow was already installed, but on my Windows machine, I had to install it before.

In case any of the earlier mentioned modules is missing on your side, just run the same command as above, replacing *exif* or *Pillow* with the name of your missing module.

## Suggestion

Even though it is almost impossible, make sure you do not have photos which match the naming convetion for the new photo with metadata cleared, just to avoid a possible overwriting.
