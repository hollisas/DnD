from selenium import webdriver
import time
import json
import shutil
import re
import os

#Need firefox/chrome driver for selenium
#Get path to firefox driver
firefox_path = r"D:/Network Share/Contributions/geckodriver.exe"
#This never changes unless you change campaigns
#Path to the journal containing the JSON of the players
path_to_external_journal = r"https://app.roll20.net/campaigns/journal/4588469/handout/-Lg30Ok5N2Xe2JO55c0n"

#Define webdriver with path
driver = webdriver.Firefox()
#Define while variable
ShouldRun = True
#Empty dictionary for character data
characterData = {}

def initializeHealth(character, data):
	incomingHP = str(data['curr_hp'])
	incomingMAX = str(data['max_hp'])

	hpfile = open(character + '_hp.txt', 'w')
	hpfile.write(incomingHP)
	hpfile.close()

	maxhpfile = open(character + '_maxhp.txt', 'w')
	maxhpfile.write(incomingMAX)
	maxhpfile.close()

	updateHealthBar(character, incomingHP, incomingMAX)

def initializeAC(character, data):
	incomingAC = str(data['ac'])
	acfile = open(character + '_ac.txt', 'w')
	acfile.write(incomingAC)
	acfile.close()

def initializeINI(character, data):
	incomingINI = str(data['initiative'])
	inifile = open(character + '_ini.txt', 'w')
	inifile.write(incomingINI)
	inifile.close()

def initializeLVL(character, data):
	incomingLVL = str(data['level'])
	levelfile = open(character + '_level.txt', 'w+')
	levelfile.write(incomingLVL)
	levelfile.close()

#Update the txt health items
def updateHealth(character, data):
	dataChanged = False
	#Grab incoming data from external journal
	incomingHP = str(data['curr_hp'])
	incomingMAX = str(data['max_hp'])
	#Grab locally stored 'previous/old' data
	hp = characterData.get(character, {}).get('curr_hp',None)
	maxhp = characterData.get(character, {}).get('max_hp',None)
	#if the incoming hp is not the same as the previous checked data => update data
	if hp != incomingHP:
		print("Updating Current Health File For ", character, "...")
		dataChanged = True
		characterData[character].update({'curr_hp': incomingHP})
		hpfile = open(character + '_hp.txt', 'w')
		hpfile.write(incomingHP)
		hpfile.close()
		print("Finished Updating Health File For ", character, "...")
	#if incoming max hp is not the same as the previous checked data => update data.
	if maxhp != incomingMAX:
		print("Updating Max Health File For ", character, "...")
		dataChanged = True
		characterData[character].update({'max_hp': incomingMAX})
		maxhpfile = open(character + '_maxhp.txt', 'w')
		maxhpfile.write(incomingMAX)
		maxhpfile.close()
		print("Finished Updating Health File For ", character, "...")
	#if either curr_hp or max_hp was changed update health bar change
	if dataChanged == True:
		print("Updating Damage For Health File For ", character, "...")
		updateHealthBar(character, incomingHP, incomingMAX)
		print("Finished Updating Health File For ", character, "...")

#Write the AC values to a file
def updateAC(character, data):
	incomingAC = str(data['ac'])
	ac = characterData.get(character, {}).get('ac',None)
	#if the incoming ac is not the same as in the file, update the file
	if ac != incomingAC:
		print("Updating AC File For ", character, "...")
		characterData[character].update({'ac': incomingAC})
		acfile = open(character + '_ac.txt', 'w')
		acfile.write(incomingAC)
		acfile.close()
		print("Finished Updating AC File For ", character, "...")

#Write the Initiative values to a file
def updateINI(character, data):
	incomingINI = str(data['initiative'])
	ini = characterData.get(character, {}).get('initiative',None)
	#if the incoming initiative is not the same as in the file, update the file
	if ini != incomingINI:
		print("Updating Initiative File For ", character, "...")
		characterData[character].update({'initiative': incomingINI})
		inifile = open(character + '_ini.txt', 'w')
		inifile.write(incomingINI)
		inifile.close()
		print("Finished Updating Initiative File For ", character, "...")

def updateHealthBar(character, hp, maxhp):
	print("Updating Damage To Health File For ", character, "...")
	healthBar = int(maxhp) - int(hp)
	updateDamage = open(character + '_damage.txt', 'w')
	updateDamage.write(str(healthBar))
	updateDamage.close()
	print("Finished Updating Damage To Health File For ", character, "...")

#Write the Level values to a file
def updateLevel(character, data):
	incomingLVL = str(data['level'])
	lvl = characterData.get(character, {}).get('level', None)
	if lvl != incomingLVL:
		print("Updating Level File For ", character, "...")
		characterData[character].update({'level': incomingLVL})
		levelfile = open(character + '_level.txt', 'w+')
		levelfile.write(incomingLVL)
		levelfile.close()
		print("Finished Updating Level File For ", character, "...")

def main():
	#Try to run script
	try:
		roll20search = re.search('Roll20: Online virtual tabletop', driver.title)
		#If the title of the page already exists (ie, the window is open), don't open a new one
		if roll20search:
			#Get the text from HTML element
			text = driver.find_element_by_xpath("""//*[@id="openpages"]/div/span""").text
			#print(text)
			varJSON = json.loads(text)
			print("Sleep Mode For 5 Seconds...")
			time.sleep(5)
			print("Waking Up From Sleep Mode...")

			if varJSON:
				print("Checking For Updates...")
				for character, value in varJSON.items():
					updateHealth(character, value)
					updateAC(character, value)
					updateINI(character, value)
					updateLevel(character, value)
				print("Finished Checking For Updates...")

		#if window is not open
		else:
			#Open URL to roll20 handout
			driver.get("https://app.roll20.net/campaigns/journal/4588469/handout/-Lg30Ok5N2Xe2JO55c0n")
			varJSON = ""
			time.sleep(5)

			while not varJSON:
				#Get the text from HTML element
				text = driver.find_element_by_xpath("""//*[@id="openpages"]/div/span""").text
				varJSON = json.loads(text)
				time.sleep(5)

			#print(varJSON)
			if varJSON:
				print("Initializing Files For Characters...")
				for character, value in varJSON.items():
					characterData.update({character: value})
					initializeHealth(character, value)
					initializeAC(character, value)
					initializeINI(character, value)
					initializeLVL(character, value)
				print("Finished Initializing Files...")

	#If you can't find the window, raise exception and exit script
	except Exception as e:
		print(str(e))
		#Stop running for loop
		ShouldRun = False
		#Quit driver
		driver.quit()
		#Exit script
		exit()

print("Running Roll20toPython Character Information Tracker Script...")
print("Do not close this window unless you are finished using this script...")
while ShouldRun:
	main()		
	time.sleep(5)
