from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from trackie_scrapper import TrackieTracker
from sssad_scrapper import SSSadTracker 
from sssad_data_parser import SSSadDataParser

def run_all_scrapper():
    # creating the folder which will be use for storing data from the tracker
    dir_path1 = Path("meets")
    dir_path1.mkdir(parents=True, exist_ok=True)

    dir_path2 = Path("rolling_schedule")
    dir_path2.mkdir(parents=True, exist_ok=True)

    dir_path3 = Path("sssad_data")
    dir_path3.mkdir(parents=True, exist_ok=True)

    # turn on headless mdoe and made the driver faster
    options = Options()
    options.add_argument("--headless") 
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=800,600")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--log-level=3")
    options.page_load_strategy = 'eager' 

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    options = ["SSSAD City Championships", "SSSAD Twilight Meet #4", "SSSAD Twilight Meet #3", "SSSAD Twilight Meet #2", "SSSAD Twilight Meet #1"]
    
    print("Starting the scrapper...")
    for option in options:
        print(f"Starting to track {option}")
        print("Getting info from trackie.com")
        # start the trackie tracker
        trackie_tracker = TrackieTracker(driver=driver,
                                     event_input=option,
                                     base_website="https://www.trackie.com/calendar")
        meet_file_path = trackie_tracker.run_scrapper()
        
        print("Getting info from sssad.net/track-field")
        # start the SSSAD.net scrapper
        sssad_tracker = SSSadTracker(driver=driver,
                                 base_url="https://sssad.net/track-and-field/",
                                 event_input=option)
        csv_to_parse = sssad_tracker.run_scrapper()

        print("Processing Trackie and SSSad data")
        # parse the data got from the sssad tracker
        sssad_data_parser = SSSadDataParser(csv_file=csv_to_parse, meet_file_path=meet_file_path)
        sssad_data_parser.parse_data()
        print(f"Finish processing {option}")
        print("-" * 40)
    # close the driver after being done
    driver.quit()
