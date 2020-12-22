# program will scrape the Dark Souls 3 fextralife wiki page for detailed 
# weapon information. data will then be formatted and saved into this programs
# folder, as a CSV file. 

from requests import get
from requests.compat import urljoin
from time import time, sleep
from bs4 import BeautifulSoup as bs
from csv import writer

class Timer:
    def __init__(self):
    # simple timer.

        pass
        # do nothing.

    def start(self):
    # start timing.

        self.start_time = time()
        # get time since epoch.

    def stop(self):
    # stop timing and return elapsed time.

        self.stop_time = time()
        # get time since epoch.

        self.exact_elapsed_time = self.stop_time - self.start_time
        self.elapsed_time = float("{:.2f}".format(self.exact_elapsed_time))
        # calculate and round elapsed time to 2 decimal places.

        return self.elapsed_time
        # return elapsed time. 

class DarkSouls3WeaponScraper:
    def __init__(self):
    # scraper for dark souls 3 weapon information.

        self.TIME_DELAY = 5
        # delay (in seconds) between requests to prevent throttling.

        self.BASE_URL = "https://darksouls3.wiki.fextralife.com"
        # base URL for ds3 wiki.

        self.CSV_LOG = "ds3_weapon_data.csv"
        # csv output file. 

        self.weapon_types = []
        # list for weapon types.

        self.weapon_entries = []
        # list for weapons.

        self.timer = Timer()
        self.timer.start()
        print("starting scrape now...")

        self.typeScrape()
        # begin scrape.

    def parsePage(self, page):
    # go to desired page on ds3 wiki and return parsed page object.

        url = urljoin(self.BASE_URL, page)
        # construct URL for page scrape. 

        sleep(self.TIME_DELAY)
        # pause to prevent throttling.

        timer = Timer()
        timer.start()
        print(f"requesting {page} info...")
        # start timer and display request notification.

        raw_page = get(url)
        parsed_page = bs(raw_page.content, 'html.parser')
        # make request and parse returned html.

        print(f"received {page} info in approx {timer.stop()} seconds...")
        # display receipt notification.

        return parsed_page
        # return parsed page results. 

    def typeScrape(self):
    # scrape weapon types.

        main_weapon_page = self.parsePage("Weapons")
        raw_type_list = main_weapon_page.findAll("h3")
        # navigate to weapons page and get weapon types. 

        for entry in raw_type_list:
        # loop through types.

            if entry.text == "How to choose a weapon in Dark Souls?" or \
                entry.text == "\nJoin the page discussion\nTired of anon "+\
                "posting? Register!\n":
                    pass
            # filter out results that arent weapon types. 

            elif entry.text == "Whips & Flails":
                self.weapon_types.append("Whips")
            # change "whips & flails" entry to just "whips" for proper navigation.

            elif entry.text == "Flames, Talismans & Chimes":
                self.weapon_types.append("Flames")
                self.weapon_types.append("Talismans")
                self.weapon_types.append("Chimes")
            # split "flames, talismans & chimes" entry into 3 seperate entries.
 
            else:
                self.weapon_types.append(entry.text)
            # add entry to type list. 

        self.weaponScrape()
        # scrape weapon info.

    def weaponScrape(self):
    # scrape weapon info.

        for weapon_type in self.weapon_types:
            weapon_type_page = self.parsePage(weapon_type)
            weapon_table = weapon_type_page.find("tbody")
            table_rows = weapon_table.findAll("tr")
        # locate weapon table and rows. 

            for row in table_rows:
                individual_entry = []
                cells = row.findAll("td")
                raw_weapon_name = cells[0].text
                weapon_name = raw_weapon_name.strip()
                individual_entry.append(weapon_name)
                individual_entry.append(weapon_type)
            # weapon name and type parsed from table row. 

                cell_number = 0
                for cell in cells:
                    if cell_number < 1:
                        pass
                    elif cell_number > 6:
                        break
                    else:
                        raw_cell = cell.text.strip()
                        split_cell = raw_cell.split(" ")
                        try:
                            damage_value = int(split_cell[0])
                        except:
                            damage_value = int(0)
                # damage values parsed from table cell. 

                        individual_entry.append(damage_value)
                        # append damage value to weapon entry. 

                    cell_number += 1
                    # increment counter. 

                self.weapon_entries.append(individual_entry)
                # append full weapon entry to weapon entry list.
        
        print(f"finished scrape in approx {self.timer.stop()} seconds.")
        # stop timer and display finish time notification.

        self.logOutput()
        # log output to csv file. 

    def logOutput(self):
    # creat csv file to store weapon info.

        csv_file = open(self.CSV_LOG, encoding="utf-8", mode="w")
        # open file to write. 

        file_writer = writer(csv_file, delimiter="\t", lineterminator="\n")
        # create csv writer. tab delimited.

        file_writer.writerow([  "Name", "Type", "Physical DMG", "Magic DMG",
                                "Fire DMG", "Lightning DMG", "Dark DMG",
                                "Crit DMG"])
        # write column headings. 

        for row in self.weapon_entries:
            file_writer.writerow(row)
        # write weapon entries to csv file. 

        csv_file.close()
        # close file. 

DS = DarkSouls3WeaponScraper()