
import requests
from bs4 import BeautifulSoup

DS3_WIKI = "https://darksouls3.wiki.fextralife.com/"

TSV_FILE = "Dark_Souls_3_Weapons_List.tsv"

def main():

    weapon_types = weaponTypeScraper()
    # scrape weapon types from main weapon page. 

    weapon_table = weaponTableScraper(weapon_types)
    # use weapon types to scrape type pages, then return full weapon table. 

    logOutput(weapon_table)
    # write table to TSV file. 

    exit()
    # exit program. 

def weaponTypeScraper():
# scrape main weapons page and return list of weapon type entries. 

    typeList = []
    # initialize list for weapon types. 

    mainWeaponPage = pageParser("Weapons")
    rawTypeList = mainWeaponPage.findAll("h3")
    # navigate to weapons page and get all h3 tags. 
    
    for entry in rawTypeList:
        if entry.text == "How to choose a weapon in Dark Souls?" or \
            entry.text == "\nJoin the page discussion\nTired of anon "+\
            "posting? Register!\n":
                pass
        # filter out results that arent weapon types. 

        elif entry.text == "Whips & Flails":
            typeList.append("Whips")
        # change "whips & flails" entry to just "whips" for proper navigation.

        elif entry.text == "Flames, Talismans & Chimes":
            typeList.append("Flames")
            typeList.append("Talismans")
            typeList.append("Chimes")
        # split "flames, talismans & chimes" entry into 3 seperate entries.
 
        else:
            typeList.append(entry.text)
        # add entry to type list. 

    return typeList
    # return usable list of weapon types.

def weaponTableScraper(weaponTypeList):
# scrape table info from weapon tables and return nested list containing all
# weapons, types, and relevant stats. 

    weaponEntries = []

    for weaponType in weaponTypeList:
        print(f'scraping {weaponType} page...')
        weaponTypePage = pageParser(weaponType)
        weaponTable = weaponTypePage.find("tbody")
        tableRows = weaponTable.findAll("tr")
        # locate weapon table and rows. 

        for row in tableRows:
            individualEntry = []
            cells = row.findAll("td")
            rawWeaponName = cells[0].text
            weaponName = rawWeaponName.strip()
            individualEntry.append(weaponName)
            individualEntry.append(weaponType)
        # weapon name and type parsed from table row. 

            cellNumber = 0
            for cell in cells:
                if cellNumber < 1 or cellNumber > 6:
                    pass
                else:
                    rawCell = cell.text.strip()
                    splitCell = rawCell.split(" ")
                    try:
                        damageValue = int(splitCell[0])
                    except:
                        damageValue = int(0)
            # damage values parsed from table cell. 

                    individualEntry.append(damageValue)
                    # append damage value to weapon entry. 

                cellNumber += 1
                # increment counter. 

            weaponEntries.append(individualEntry)
            # append full weapon entry to weapon entry list. 

    return weaponEntries
    # return filled nested list with weapon information. 

def logOutput(nestedList):
# takes nested list and writes info to .tsv file.

    file = open(TSV_FILE, "w")
    # open file to write. 

    file.write("Name\tType\tPhysical DMG\tMagic DMG\tFire DMG\tLightning DMG"+
                "\tDark DMG\tCrit DMG\n")
    # write column headings before contents.
    
    for row in nestedList:
        file.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t" +
                    f"{row[5]}\t{row[6]}\t{row[7]}\n")
    # write values to table. 

    file.close()
    # close file. 

def pageParser(page):
# go to desired page on ds3 wiki and return parsed page object.

    url = f'{DS3_WIKI}{page.replace(" ", "+")}'
    rawPage = requests.get(url)
    parsedPage = BeautifulSoup(rawPage.content, 'html.parser')
    return parsedPage

main()