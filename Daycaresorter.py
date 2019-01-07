import csv
import sys
def main():
	if len(sys.argv) == 4:
		cityString = sys.argv[1] + " " + sys.argv[2]
		stateString = sys.argv[3].upper()
	elif len(sys.argv) == 3:
		cityString = sys.argv[1]
		stateString = sys.argv[2].upper()
	regularCity = cityString[0].upper() + cityString[1:].lower() #makes a city with the first letter capitalized
	with open("DaycareJerry.csv", "w") as csv_file:
		writer = csv.writer(csv_file, lineterminator="\n")
		writer.writerow(["Day Care Center", "Street Name", "City", "State", "Zip Code", "License/Registration ID", "Contact Name", "Phone Number"])
		file = open("Daycare.txt", "r")
		data = file.readlines() #puts the Daycare.txt lines into a list
		lst = [] #temporary list used to write daycare file information into DaycareJerry.csv
		print(data)
		for i in range(len(data)):
			data[i] = data[i].strip() #takes away excess spaces, and type commands
			if len(lst) == 8: #when the temporary list is "full", it writes it over to the csv file, then sets the temporary list back to nothing in order to get the other daycares' info
				writer.writerow(lst) #writes the temporary list into the csv file
				lst = [] #sets the temporary list back to nothing
#-------------------------------------------------------------------------------------------------------------------------
			if len(lst) == 0: #if the temporary list is empty/has no items
				if "Click here for additional program information" in data[i]:
					daycareName = data[i].replace("Click here for additional program information", "") #gets rid of the "click here" portion
					daycareName = daycareName.strip() #gets rid of unnecessary spaces
					lst.append(daycareName) #adds daycarename
					if "For information on contacting this provider, contact your local referral agency" in data[i+2]: #if the line two down from the name is the line that, if it is a certain string
						location = "" #location: nothing (empty string)
						string = data[i+1].strip()
						if len(string.split(" ")) == 3:
							city, state, zipcode = string.split(" ") #splits the string by the spaces, creating three items, which you set to city, state, and zipcode
						else:
							city1, city2, state, zipcode = string.split(" ")
							city = city1 + " " + city2
						city = city.replace(",", "") #get rid of the comma
						lst.append(location)
						lst.append(city)
						lst.append(state)
						zipcode = zipcode.strip()
						lst.append(zipcode)

					else:
						if "%s, %s" % (regularCity, stateString) in data[i+1]: #"regular"
							location, zipcode = data[i+1].split(", %s, %s " % (regularCity, stateString))
							zipcode = zipcode.replace(" Map", "")
							city = regularCity
							state = stateString

						elif "%s, %s" % (cityString.lower(), stateString) in data[i+1]: #all lowercase
							location, zipcode = data[i+1].split(", %s, %s " % (cityString.lower(), stateString))
							zipcode = zipcode.replace(" Map", "")
							city = regularCity
							state = stateString

						elif "%s, %s" % (cityString.upper(), stateString) in data[i+1]: #all caps
							location, zipcode = data[i+1].split(", %s, %s " % (cityString.upper(), stateString))
							zipcode = zipcode.replace(" Map", "")
							city = regularCity
							state = stateString

						else: #if it is another state, city, or both
							splitStr = data[i+1].split(", ")
							city = splitStr[len(splitStr)-1-1]
							if len(splitStr[len(splitStr)-1].split(" ")) == 3:
								state, zipcode, var = splitStr[len(splitStr)-1].split(" ")
							else:
								state, zipcode = splitStr[len(splitStr)-1].split(" ")
							location, zipcode = data[i+1].split(", %s, %s " % (city, state)) #might work: test over multiple times
							zipcode = zipcode.replace(" Map", "")
							city = city[0].upper() + city[1:]
						lst.append(location)
						lst.append(city)
						lst.append(state)
						zipcode = zipcode.strip()
						lst.append(zipcode)
#-------------------------------------------------------------------------------------------------------------------------
			elif len(lst) == 5: #if you have the name, street name, city, state, and zipcode in your temporary list
				if "License/Registration ID:" in data[i]: #if it is the line that contains the license/registration id
					ID = data[i].replace("License/Registration ID: ", "") #remove the ID: portion (you just want the number)
					lst.append(ID)
#-------------------------------------------------------------------------------------------------------------------------
			elif len(lst) == 6: #if you have the first five and the license/registration id in your temporary list
				if "Contact Name/Title:" in data[i]: #if it is the line that contains the contact name/title
					string = data[i].replace("Contact Name/Title: ", "") #remove the contact name/title portion
					listString = string.split(" , ") #split it so that listString[0] is the name and listString[1] is not needed
					contactName = listString[0] #takes the one that you want of the two
					lst.append(contactName)
#-------------------------------------------------------------------------------------------------------------------------
			elif len(lst) == 7: #if you have the first 6 and the contact name/title in your temporary list
				if "Phone:" in data[i]: #shows that this is the line that contains the phone number
					phoneNumber = data[i].replace("Phone:", "") #gets rid of the phone: portion, leaving you with the phone number, and if there is nothing after phone::, then the phone number is "", or nothing
					lst.append(phoneNumber)

main()