

from multiprocessing.reduction import duplicate
import os
import shutil
import datetime




SOURCEDIR = 'H:\\13.09.18'
DEST_DIR = 'H:\\DEST'
#file count
files = 0
#folder count
folders = 0
duplicates = 0
USER = os.environ['USERPROFILE']



def folder_recursive_check(sourcedir):
    with os.scandir(sourcedir) as entries:
        global files, folders, duplicates
        #for a file in folder
        for entry in entries:
            #if entry is a file
            if os.path.isfile(entry):
                #extract file extension
                root_ext = os.path.splitext(entry)[1]
                #extract creation time
                c_time = os.path.getmtime(entry)
                #transform epoch time to date
                dt_c = datetime.datetime.fromtimestamp(c_time)
                #reformat time to YYYY format
                f_year = dt_c.strftime("%Y")
                #create directory path: destinationfolder\extension\date
                fin_path = os.path.join(DEST_DIR,  f_year, root_ext)
                #get file name
                file_name = entry.name
                #create directory path: destinationfolder\extension\date\filename
                fin_file_path = os.path.join(fin_path, file_name)
                #if destination directory doesn't exist create directory and copy file
                if not os.path.exists(fin_path):
                    os.makedirs(fin_path)
                    shutil.copy(entry.path, fin_path)
                #if file already relacated print information about duplicate
                elif os.path.exists(fin_file_path):
                    print(f"{entry.name} already copied, duplicate count {duplicates}")
                    duplicates += 1
                #if directory exists and file is not there copy file
                else:
                    shutil.copy(entry.path, fin_path)
                files +=1
                print(f"file {files} copied")
            else:
                folder_recursive_check(entry.path)
                folders +=1
                print(f"folder {folders} copied")

folder_recursive_check(SOURCEDIR)