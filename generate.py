import os, random, struct
from Crypto.Cipher import AES

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
	if not out_filename:
		out_filename = in_filename + '.enc'
	iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	encryptor = AES.new(key, AES.MODE_CBC, iv)
	filesize = os.path.getsize(in_filename)
	with open(in_filename, 'rb') as infile:
		with open(out_filename, 'wb') as outfile:
			outfile.write(struct.pack('<Q', filesize))
			outfile.write(iv)
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				elif len(chunk) % 16 != 0:
					chunk += ' ' * (16-len(chunk) % 16)
				outfile.write(encryptor.encrypt(chunk))

def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
	if not out_filename:
		out_filename = os.path.splitext(in_filename)[0]
	with open(in_filename, 'rb') as infile:
		origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
		iv = infile.read(16)
		decryptor = AES.new(key, AES.MODE_CBC, iv)
		with open(out_filename, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break
				outfile.write(decryptor.decrypt(chunk))
			outfile.truncate(origsize)

def encrypt_list(key, list_of_file_names):
	for file_name in list_of_file_names:
		encrypt_file(key, file_name)
		os.remove(file_name)

def decrypt_list(key, list_of_file_names):
	for file_name in list_of_file_names:
		decrypt_file(key, file_name+'.enc')
		os.remove(file_name+'.enc')

def deleteline(line_to_remove, file_name):
	f = open(file_name)
	output = []
	for line in f:
		if line_to_remove != line.strip():
			output.append(line)
	f.close()
	f = open(file_name, 'w')
	f.writelines(output)
	f.close()
	
if __name__ == "__main__":
	password = raw_input("What is the password? ")
	key = '0123456789abcdef'
	#encrypt_file(key, 'rp5.txt')
#	encrypt_file(key, 'passcode.txt')
	decrypt_file(key, 'passcode.txt.enc')
	with open("passcode.txt", "r") as myfile:
		data = myfile.read().replace('\n', '')
		os.remove('passcode.txt')
		#print(data)
	with open("encoded.txt", "r") as myfile2:
		encoded = myfile2.read().replace('\n', '')
		#print(encoded)
	if password == data:
		print("Welcome, comrade. How may I help you?")
		print("1. Conceal all information.")
		print("2. Reveal all information.")
		print("3. New story.")
		print("4. Remove a story")
		print("5. Change password.")
		print("6. Alter a single file. (MORE SECURE)")
		print("7. Nothing.")
		option = raw_input("Select an option. ")
		if option == '1':
			if encoded == 'True':
				print("The file is already encrypted.")
				exit()
			string = []
			with open("files.txt", "r") as files:
				string = files.read().split()
			#print(string)
			encrypt_list(key, string)
			#encrypt_file(key, 'rp.txt')
			#os.remove('rp.txt')
			print("Files have been encrypted.")
			f = open("encoded.txt", "w")
			f.write("True")
			f.close()
		elif option == '2':
			if encoded == 'False':
				print("The file is already decrypted.")
				exit()
			string = []
			with open("files.txt", "r") as files:
				string = files.read().split()
			decrypt_list(key, string)
			#decrypt_file(key, 'rp.txt.enc')
			#os.remove('rp.txt.enc')
			print("Files have been decrypted.")
			f = open("encoded.txt", "w")
			f.write("False")
			f.close()
		elif option == '3':
			#print("This has not been implemented yet.")
			if encoded == 'True':
				string = []
				with open("files.txt", "r") as files:
					string = files.read().split()
				decrypt_list(key, string)
				z = open("encoded.txt", "w")
				z.write("False")
				z.close()
				#decrypt_file(key, 'rp.txt.enc')
				#os.remove('rp.txt.enc')
			f = open("encoded.txt", "w")
			f.write("False")
			f.close()
			print("")
			print("What is the name of the new file that you wish to create?")
			print("Guidelines:")
			print("1. Make sure that you place .txt at the end of the name.")
			print("2. Please do not use names that will give away any information about the contents of the file.")
			filename = raw_input("New File: ")
			#print(filename)
			newfile = open(filename, "w")
			newfile.close()
			filelist = open('files.txt', 'a')
			filelist.write("\n"+filename)
			print("New file has been created.")
		elif option == '4':
			print("This method has not been implemented yet.")
			print("What is the name of the file you would like to delete?")
			oldfile = raw_input("Old file: ")
			confirmation = raw_input("Are you sure you want to delete the file "+oldfile+"? ")
			if confirmation == 'yes':
				if encoded == 'True':
					string = []
					with open("files.txt", 'r') as files:
						string = files.read().split()
					decrypt_list(key, string)
					z = open("encoded.txt", "w")
					z.write("False")
					z.close()
				deleteline(oldfile, "files.txt")	
				os.remove(oldfile)
				print("The file has been deleted.")
			else:
				print("You have cancelled the operation.")	
		elif option == '5':
			tries = 5
			while tries > 0:
				confirmation = raw_input("Please confirm your password: ")
				if confirmation == data:
					newpassword = raw_input("New password: ")
					os.remove("passcode.txt.enc")
					passcode = open("passcode.txt", "w")
					passcode.write(newpassword)
					passcode.close()
					encrypt_file(key, "passcode.txt")
					os.remove("passcode.txt")
					print("New password has been set.")
					exit()
				else:
					print("Incorrect password.")
					tries = tries - 1
			print("Too many wrong passwords. You have been locked out.")
		elif option == '6':
			print("What is the name of the file that you wish to edit?")
			print("Note: Do not include the .enc extension.")
			filetoedit = raw_input("Edit file: ")
			if encoded == 'True':
				decrypt_file(key, filetoedit+'.enc')
				os.remove(filetoedit+'.enc')
				os.system("vim "+filetoedit)
				encrypt_file(key, filetoedit)
				os.remove(filetoedit)
				print("Has not been implemented yet.")
				
		else:
			print("You have cancelled the operation.")

	else:
		print("You are not the authorized person.")
		exit()
