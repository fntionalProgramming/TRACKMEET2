from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from time import sleep
import re

class TrackieError(Exception):
    pass

class TrackieTracker:
    def __init__(self, driver, event_input, base_website):
        self.driver = driver
        self.event_input = event_input
        self.driver.get(base_website)
        self.base_website = base_website
    def run_scrapper(self):
        def find_and_enter_search_button(self: TrackieTracker, id_name, search_key):
            '''
            find the button with the corresponding id
            clear the search field
            search using the string something like SSSAD Twlight 4 or City Championships
            '''
            search_field = self.driver.find_element(By.ID, id_name)
            search_field.clear()
            search_field.send_keys(search_key)
            search_field.send_keys(Keys.RETURN)
        def find_and_go_to_event(self: TrackieTracker, id_name, search_key, sleep_duration=2):
            '''
            find the calender list which contains the list of events
            check for upcoming events and see if the event is in there, other wise if it is not in there then go to the past section to check
            also usually there are
            twilight meet 1 - 4 and a champion ship for each year
            so if there is multiple instance of twlight meet the first one is the right one
            '''
            sleep(sleep_duration) # waiting for two second is fine because all of the data should be there already
            calendar_list = self.driver.find_element(By.ID, id_name) # should be a td html element
            events = calendar_list.find_elements(By.TAG_NAME, "tr") # should be a list of trs
            # if there is nothing in the upcoming tab then try to go the second tab
            if events[0].text == "We did not find any events that match your search criteria...":
                # goes to past events if cannot find event in upcoming section
                past_link = self.driver.find_element(By.XPATH, "//a[text()='Past']")
                past_link.click()
                sleep(sleep_duration)
                # get the calendar list again since the last one does not work
                calendar_list = self.driver.find_element(By.ID, id_name) # should be a td html element
                events = calendar_list.find_elements(By.TAG_NAME, "tr") # should be a list of trs
                # iterate to find the first instnace of the event use search for then click on it right away
                # click right away on the first event
            # if the events in past is empty then raise an error because the events user is earching for does not exxits
            if events[0].text == "We did not find any events that match your search criteria...":
                raise TrackieError(f"Error, event: '{search_key}' does not exits")
            for event in events: 
                if search_key in event.text:
                    participants_list_link = event.get_attribute("onclick") 
                        # -> location.href='/event/sssad-twilight-meet-4/1019615/'; something like this always
                    participants_list_link = f"https://www.trackie.com/entry-list/{participants_list_link.replace("location.href='/event/", "")[:-2]}" 
                        # -> https://www.trackie.com/entry-list/sssad-twilight-meet-4/1019615/
                    return participants_list_link
            if self.driver.current_url == self.base_website:
                raise TrackieError(f"Error, event: '{search_key}' does not exits or hasnnot comes up yet!")
            # function should not return here
        def get_all_parcipitant(self: TrackieTracker, participant_list_link, entries_list_csss, entry_class, tr_row_class, date_class):
            '''
            function will use the participant link extracted from event
            then this should go in there and get all the runners in such events and convert it to csv
            function aditionally will return a sting that talks about the information of the meet
            for later use case
            '''
            # go to the new link
            self.driver.get(participant_list_link)
            data = []

            for entries_list_css in entries_list_csss:
                # process the right part of the trackie website by first getting the entry list for everything
                entries_list = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, entries_list_css))
                ).find_elements(By.CLASS_NAME, entry_class)
                '''
                https://www.trackie.com/entry-list/sssad-twilight-meet-4/1019615/
                In each entries_list
                there should be a force_full_mobile class
                in force_full_mobile there should be a h4 which is the name of the race
                in force_full_mobile there should be a thead (which will be ignored) and a tbody
                in the tbody, there should be a list of tr which represents each runner stats, also in the middle sometimes there is stuff 
                    like a tr that category should i have to becareful about that

                there is a girl side aswell 
                '''
                for entry in entries_list:
                    try:
                        # get the current type of event through the heading 4
                        event_name = entry.find_element(By.TAG_NAME, "h4").text
                            # -> Male 200m - Entries: 170
                        event_name = event_name.split(" - ")[0]
                            # -> Male 200m
                        participants_list = entry.find_element(By.TAG_NAME, "tbody").find_elements(By.CLASS_NAME, tr_row_class)
                        for participant in participants_list:
                            '''
                            participant when.text will be in this format
                            Ygnacio, Chris Unknown
                            HCHS
                            NT
                            to extract the first name the catergory the school and the seed mark
                            one thing we could do is first normalized all the white spaces then just use
                            a simple rsplit and stopping before an instance of a name
                            '''
                            name, category, school, seed_mark = re.sub(r'\s+', ' ', participant.text).strip().rsplit(" ", 3)
                            current_data_column = [name, category, school, seed_mark, event_name]
                            # append the current data to overall data
                            data.append(current_data_column)
                    except Exception:
                        print("Skipping Malformed Data")
                        continue
                '''
                find the date of meet by first finding the content div
                then after that find the div with the class right
                '''
            date_of_meet = self.driver.find_element(By.CLASS_NAME, date_class).text
            return data, date_of_meet

        find_and_enter_search_button(self=self,
                                     id_name="filter_by_title",
                                     search_key=self.event_input)
        participants_list_link = find_and_go_to_event(self=self,
                                                     id_name="calendar_list",
                                                     search_key=self.event_input)
        data, date_of_meet = get_all_parcipitant(self=self,
                                             participant_list_link=participants_list_link,
                                             entries_list_csss=[".entries_list", ".entries_list.floatRight"],
                                             entry_class="force_full_mobile",
                                             tr_row_class="tr_row_inner",
                                             date_class="date"
                                             )
        # conver the data to csv using pandas
        output_path = f"meets/{self.event_input} - {date_of_meet}.csv"
        df = pd.DataFrame(data, columns=["Name", "Category", "Team", "Seed-mark", "Event"])
        df.to_csv(output_path, index=False)

        # real quick fix the realy error
        self.fix_relay_error(file_path=output_path)

        # return the meet name fo later usage 
        return output_path
    '''
    some part in the csv will h ave comptetant event stateed as "This person will compete a relay only"
    and one good thing is that after messing with the historic data for Trackie
    I've found that there is only one kind of event which is 4 x 100 M event
    so we can just filter out for 'This person will compete in a relay only" and change it to 
    4 x 100 M which is real nice
    '''
    def fix_relay_error(self, file_path):
        df = pd.read_csv(file_path)
        df['Event'] = df['Event'].apply(
            lambda s: "4x100m" if isinstance(s, str) and (
                "Female This registrant is competing on a relay only" in s or 
                "Male This registrant is competing on a relay only" in s
            ) else s
        )
        df.to_csv(file_path, index=False)


if __name__ == "__main__":
    # example usage
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    s = TrackieTracker(driver=driver, event_input="SSSAD Twilight Meet #4", base_website="https://www.trackie.com/calendar")
    meet_file_path = s.run_scrapper()
    print(meet_file_path)
    driver.quit()
