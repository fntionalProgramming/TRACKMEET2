from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from trackie_scrapper import TrackieTracker
from sssad_scrapper import SSSadTracker 
from sssad_data_parser import SSSadDataParser


if __name__ == "__main__":
    # creating the folder which will be use for storing data from the tracker
    dir_path1 = Path("meets")
    dir_path1.mkdir(parents=True, exist_ok=True)

    dir_path2 = Path("rolling_schedule")
    dir_path2.mkdir(parents=True, exist_ok=True)

    dir_path3 = Path("sssad_data")
    dir_path3.mkdir(parents=True, exist_ok=True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    options = ["SSSAD City Championships", "SSSAD Twilight Meet #4", "SSSAD Twilight Meet #3", "SSSAD Twilight Meet #2", "SSSAD Twilight Meet #1"]
    print("Welcome to the track meet manager!")
    print("You can start tracking your athletes through these meets\n" + "\n".join(f"{i+1}: {options[i]}" for i in range(len(options))))
    user_option = int(input("Please enter your option right here: "))
    if user_option > len(options) or user_option < 1: 
        print("The option is Invalid please run the program again")
        driver.quit()
        exit()
    
    option = options[user_option-1]
    # start the trackie tracker
    trackie_tracker = TrackieTracker(driver=driver,
                                     event_input=option,
                                     base_website="https://www.trackie.com/calendar")
    meet_file_path = trackie_tracker.run_scrapper()

    # start the SSSAD.net scrapper
    sssad_tracker = SSSadTracker(driver=driver,
                                 base_url="https://sssad.net/track-and-field/",
                                 event_input=option)
    csv_to_parse = sssad_tracker.run_scrapper()
    
    # parse the data got from the sssad tracker
    sssad_data_parser = SSSadDataParser(csv_file=csv_to_parse, meet_file_path=meet_file_path)
    sssad_data_parser.parse_data()
    # close the driver after being done
    driver.quit()
