# USAGE:

NAME: account

DESCRIPTION: handle multiple accounts of google drive and switch between accounts.

	-l : list all accounts added to pyDrive

	-a : add an account to pyDrive

	-s : switch to a different account, provide email id

	-i : print account info of the current account

	-S : switch to shared folder of the current account

	-P : switch to mydrive folder of the current account


NAME: ls

DESCRIPTION: List  information  about  the FILEs (the current directory by default).

	-m : display mime type of each file.


NAME: rm

DESCIPTION: Delete files from the drive account.

	-r : recursively delete all files in the folder

	-e : empty trash


NAME: get

DESCRIPTION: download a file or folder from the drive account

	-e : export the file as pdf.

	-d : specify the download location. By default ~/DriveDownloads

	--std-out : print the contents of the file to standard output instead of downloading.

NAME: put

DESCRIPTION: upload a file or folder to the drive account

	--std-in : upload the content from standard input to drive account


NAME: share

DESCRIPTION: share a file or folder to the given email account

	-r : read only permission

	-w : write only permission
