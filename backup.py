from datetime import datetime, timezone
import logging
import sys
import os
import shutil
import pathlib
from pathlib import Path
import smtplib
import pytz
import backupcfg

tz = pytz.timezone("Australia/Melbourne") #Sets the timezone to Melbourne, AUS.
dateTimeStamp = datetime.now(tz).strftime("%Y%m%d-%H%M%S")
dateToday = datetime.now(tz).strftime("%Y-%m-%d")

apikey = "#" #mailjet API key
secretkey = "#" #mailjet Secret key
smtp = {"sender": "30026663@students.sunitafe.edu.au",    #mailjet.com verified sender
        "recipient": "30026663@students.sunitafe.edu.au", # mailjet.com verified recipient
        "server": "in-v3.mailjet.com",      #mailjet.com SMTP server
        "port": 587,                           #mailjet.com SMTP port
        "user": apikey,      #mailjet.com user
        "password": secretkey} #mailjet.com password
        
srcFile = os.path.normpath(backupcfg.file_location) #Sets up filepath for individual files
srcFileLoc = srcFile
srcFilePath = pathlib.PurePath(srcFileLoc)

srcDir = os.path.normpath(backupcfg.directory_location) #Sets up filepath for directories
srcDirLoc = srcDir
srcDirPath = pathlib.PurePath(srcDirLoc)

srcLog = os.path.normpath(backupcfg.backup_log_location) #Sets up filepath for the backup log file
srcLogLoc = srcLog
srcLogPath = pathlib.PurePath(srcLogLoc)
        
dstDir = os.path.normpath(backupcfg.backup_location) #Sets up the filepath for the destination directory
newDstDir = os.path.normpath(dstDir + "/" + dateToday)

dstFileLoc = newDstDir + "/" + srcFilePath.name + "-" + dateTimeStamp #Renames copied files
dstDirLoc = newDstDir + "/" + srcDirPath.name + "-" + dateTimeStamp #Renames copied directory
dstLogLoc = newDstDir + "/" + srcLogPath.name + "-" + dateTimeStamp #Renames copied log file

fileExists = srcFile
dirExists = srcDir
logExists = srcLog

def sendEmail(message):
    
    """These line control how the automated emails are sent and what the basic structure of the email should be."""
    
    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'

    # connects to email server and then sends email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
        print(email)
    except Exception as e:
        print("ERROR: An error occurred.")

def copyLog():
    
    """This function copies the log file to its backup folder and should be called after all other files have been backed up."""
    
    if not os.path.exists(logExists):
        print("ERROR: file " + logExists + " does not exist.")
        f = open(os.path.normpath(backupcfg.backup_log_location), "a")
        f.write("FAIL - " + logExists + " does not exist. \n")
        f.close()
        sendEmail("ERROR: file " + dirExists + " does not exist. \nGenerated @ " + dateTimeStamp + ".")
    else:
        print("ERROR: file " + logExists + " does exist.")
        f = open(os.path.normpath(backupcfg.backup_log_location), "a")
        f.write("SUCCESS - " + logExists + " does exist. \n")
        f.close()
        if pathlib.Path(srcLogLoc).is_dir():
            shutil.copytree(srcLogLoc, dstLogLoc)
            f = open(dstLogLoc, "a")
            f.write("FAIL - " + logExists + " copied to " + newDstDir + ". \n")
            f.close()
            print("nope")
        else:
            shutil.copy2(srcLogLoc, dstLogLoc)
            f = open(dstLogLoc, "a")
            f.write("SUCCESS - " + logExists + " copied to " + newDstDir + ". \n")
            f.close()
            print("end")
    
def main():
    
    """Creates a folder titled 'Backup' and a sub-folder with today's date within said 'Backuo' folder.
    If the 'Backup' folder already exists, it will create a new sub folder wqith the current date.
    If both the 'backup' and current date folders are present, nothing happens.
    All outcomes are noted in the log file."""
    
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
        os.makedirs(dstDir + "/" + dateToday)
        print(dstDir)
        f.write(dstDir + " was created successfully. \n" + dstDir + "/" + dateToday + " was created successfully. \n" + 200*"=" + "\n\n")
    else:
        f.write(dstDir + " already exists. \n")
        print(dstDir)
        try:
            os.makedirs(dstDir + "/" + dateToday)
            f.write(dstDir + "/" + dateToday + " was created. \n\n" + 200*"=" + "\n\n")
        except:
            print("ERROR: " + dstDir + "/" + dateToday + " already exists")
            f.write(dstDir + "/" + dateToday + " already exists. \n\n" + 200*"=" +  "\n\n")
            
    """Checks if an individual file exists. If it doesn't exist, an email alert will be send.
    If it is found to exist, the program will attempt to copy it to the destination. If it
    can't/ fails, it sends an email alert. All outcomes are noted in the log file."""
    
    if not os.path.exists(fileExists):
        print("ERROR: file " + fileExists + " does not exist.")
        f.write("FAIL - " + fileExists + " does not exist. \n\n" + 200*"=" + "\n\n")
        sendEmail("ERROR: file " + fileExists + " does not exist. \nGenerated @ " + dateTimeStamp + ".")
    else:
        print("ERROR: file " + fileExists + " does exist.")
        f.write("SUCCESS - " + fileExists + " does exist. \n")
        if pathlib.Path(srcFileLoc).is_dir():
            shutil.copytree(srcFileLoc, dstFileLoc)
            f.write("FAIL - " + fileExists + " copied to " + newDstDir + ".")
            sendEmail("ERROR: " + fileExists + " was not copied to " + newDstDir + ". \nGenerated @ " + dateTimeStamp + ".")
        else:
            shutil.copy2(srcFileLoc, dstFileLoc)
            f.write("SUCCESS - " + fileExists + " copied to " + newDstDir + ". \n\n" + 200*"=" + "\n\n")
    
    """Checks if directory exists. If it doesn't exist, an email alert with be send, but if found it will attempt to copy
    to destination. If copying fails an email alert with be send and the outcomes will be noted in the log file.."""
    
    if not os.path.exists(dirExists):
        print("ERROR: file " + dirExists + " does not exist.")
        f.write("FAIL - " + dirExists + " does not exist. \n\n" + 200*"=" + "\n\n")
        sendEmail("ERROR: file " + dirExists + " does not exist. \nGenerated @ " + dateTimeStamp + ".")
    else:
        print("ERROR: file " + dirExists + " does exist.")
        f.write("SUCCESS - " + dirExists + " does exist. \n")
        if pathlib.Path(srcDirLoc).is_dir():
            shutil.copytree(srcDirLoc, dstDirLoc)
            f.write("SUCCESS - " + dirExists + " copied to " + newDstDir + ". \n\n" + 200*"=" + "\n\n")
            sendEmail("ERROR: " + dirExists + " was not copied to " + newDstDir + ". \nGenerated @ " + dateTimeStamp + ".")
        else:
            shutil.copy2(srcDirLoc, dstDirLoc)
            f.write("FAIL - " + dirExists + " was not copied to " + newDstDir + ". \n\n" + 200*"=" + "\n\n")
            
            
    """Checks if files exist and their locations. With each file if not found an email alert is send. When found will attempt
    to copy to destination specified, and if that failed an email alert with be send. Outcomes can be seen in the log file."""
    
    for file in backupcfg.multiple_file_location:
        srcMultiple = os.path.normpath(file)
        srcMultipleLoc = os.path.normpath(backupcfg.source_folder + srcMultiple)
        srcMultiplePath = pathlib.PurePath(srcMultipleLoc)
        multipleExists = os.path.normpath(backupcfg.source_folder + file)
        dstMultipleLoc = newDstDir + "/" + srcMultiplePath.name + "-" + dateTimeStamp
        #print(multipleExists)
        if not os.path.exists(multipleExists):
            print("ERROR: file " + multipleExists + " does not exist.")
            f.write("FAIL - " + multipleExists + " does not exist. \n\n" + 200*"=" + "\n\n")
            sendEmail("ERROR: file " + fileExists + " does not exist. \nGenerated @ " + dateTimeStamp + ".")
        else:
            print("ERROR: file " + multipleExists + " does exist.")
            f.write("SUCCESS - " + multipleExists + " does exist. \n")
            if pathlib.Path(srcMultipleLoc).is_dir():
                print("yes")
                shutil.copytree(srcMultipleLoc, dstMultipleLoc)
                f.write("FAIL - " + multipleExists + " copied to " + newDstDir + ". \n\n" + 200*"=" + "\n\n")
                sendEmail("ERROR: " + multipleExists + " was not copied to " + newDstDir + ". \nGenerated @ " + dateTimeStamp + ".")
            else:
                shutil.copy2(srcMultipleLoc, dstMultipleLoc)
                f.write("SUCCESS - " + multipleExists + " copied to " + newDstDir + ". \n\n" + 200*"=" + "\n\n")
    f.close()
    copyLog()
    
try:
    argCount = len(sys.argv)
    program = sys.argv[0]
    arg1 = sys.argv[1]
    x = str(arg1)


    if x in ['1', '2', '3']:
        f = open(os.path.normpath(backupcfg.backup_log_location), "w")
        f.write("SUCCESS - Job " + x + " started. \n")
        main()
    
    else:
        print("Job not found")
        try:
            jobNumber = input("Enter a job number: ")
            f = open(os.path.normpath(backupcfg.backup_log_location), "w") #Opens the backup.log file in write mode

            if jobNumber in ['1', '2', '3']:
                f.write("SUCCESS - Job " + jobNumber + " started. \n")
                main()
            else:
                print("Job not found")
                f.write("FAIL - Job not found. Job Terminated.")
                sendEmail("ERROR: Job " + jobNumber + " was not found. \nGenerated @ " + dateTimeStamp + ".")
                f.close()
        except:
            print("fail")

except:
    jobNumber = input("Enter a job number: ")
    f = open(os.path.normpath(backupcfg.backup_log_location), "w") #Opens the backup.log file in write mode

    if jobNumber in ['1', '2', '3']:
        f.write("SUCCESS - Job " + jobNumber + " started. \n")
        main()
    else:
        print("Job not found")
        f.write("FAIL - Job not found. Job Terminated.")
        sendEmail("ERROR: Job " + jobNumber + " was not found. \nGenerated @ " + dateTimeStamp + ".")
        f.close()
        
finally:
    pass
    
