# program will scrape the Dark Souls 3 fextralife wiki page for detailed 
# weapon information. data will then be formatted and saved into this programs
# folder, as a TSV file. 
#
# execution time reduced from 367 seconds to 226 seconds. 
#

import requests
import threading
import time
from bs4 import BeautifulSoup

DS3_WIKI = "https://darksouls3.wiki.fextralife.com/"
# Dark Souls 3 Wiki page base URL + /.

TSV_FILE = "Dark_Souls_3_Weapons_List.tsv"
# title of file to be created. 

TIME_DELAY = 5
# amount of time in seconds to pause between requests. prevents throttling. 

weaponEntries = []
# weapon entry list. global to allow easier access from both threads. 

def main():

    startTime = time.time()
    print('starting timer now.')
    # display timer notification.

    weapon_types = weaponTypeScraper()
    # scrape weapon types from main weapon page. 

    scraper(weapon_types)
    # scrape weapon tables from weapon type pages.

    # weaponTableScraper(weapon_types)
    # scrape weapon tables from weapon type pages.
    # NOTE this function has multithreading that causes throttling.

    elapsedTime = time.time() - startTime
    print('total execution time is {:.2f}'.format(elapsedTime))
    # stop timer and display execution time. 

    logOutput()
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
# scrape table info from weapon tables and add info to weaponEntries list.

    listLength = int(len(weaponTypeList))
    halfPoint = int(listLength / 2)
    listOne = list(weaponTypeList[0 : halfPoint])
    listTwo = list(weaponTypeList[halfPoint : listLength])
    # divide list into 2 for multithreading to increase execution speed.

    thread1 = threading.Thread(target= scraper, args= (listOne,))
    thread2 = threading.Thread(target= scraper, args= (listTwo,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    # create 2 threads, run scrapers simultaneously then wait to finish.

def scraper(typeList):
# scrape type pages for weapon information.

    for weaponType in typeList:
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
                if cellNumber < 1:
                    pass
                elif cellNumber > 6:
                    break
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
            print(f'processed {individualEntry[0]}.')
            # append full weapon entry to weapon entry list.

def logOutput():
# takes nested list and writes info to .tsv file.

    file = open(TSV_FILE, "w")
    # open file to write. 

    file.write("Name\tType\tPhysical DMG\tMagic DMG\tFire DMG\tLightning DMG"+
                "\tDark DMG\tCrit DMG\n")
    # write column headings before contents.
    
    for row in weaponEntries:
        file.write(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}\t" +
                    f"{row[5]}\t{row[6]}\t{row[7]}\n")
    # write values to table. 

    file.close()
    # close file. 

def pageParser(page):
# go to desired page on ds3 wiki and return parsed page object.

    url = f'{DS3_WIKI}{page.replace(" ", "+")}'
    # construct url.

    time.sleep(TIME_DELAY)
    # pause to prevent throttling. 

    startTime = time.time()
    print(f'requesting {page} page...')
    # display requesting status and start timer.

    rawPage = requests.get(url)
    parsedPage = BeautifulSoup(rawPage.content, 'html.parser')
    # make request and parse resulting html.

    elapsedTime = time.time() - startTime
    print('received {} page info in {:.2f} seconds.'.format(page, elapsedTime))
    # display page receipt and display total request time. 

    return parsedPage
    # return parsed results. 

main()