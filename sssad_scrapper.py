from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from datetime import datetime


class SSSadTracker:
    def __init__(self, driver, base_url, event_input):
        self.driver = driver
        self.base_url = base_url
        self.event_input = event_input
        self.driver.get(self.base_url)
    def go_to_csv_page_TWLIGHT(self):
        '''
        https://sssad.net/track-and-field/
        to go to the csv page with twilight first we need to go to et_pb_column et_pb_column_1_5 et_pb_column_3 et_pb_css_mix_blend_mode_passthrough
            which is actually the twilight meet button
        there will also be an a tag in ththe twlight meet schedule element which is the link to the google docs
        '''
        twilight_meet_schedule_element = self.driver.find_element(By.CSS_SELECTOR, ".et_pb_column.et_pb_column_1_5.et_pb_column_3.et_pb_css_mix_blend_mode_passthrough")
        twilight_meet_schedule_element_link = twilight_meet_schedule_element.find_element(By.TAG_NAME, "a").get_attribute("href")
        self.driver.get(twilight_meet_schedule_element_link)
        event_input_for_sssad = self.event_input.replace("#", "").replace("SSSAD ", "")
            # -> SSSAD Twilight Meet #4 to Twilight Meet 4
        '''
        now we should be in the SSSAD page and the access the column where SSSAD
        host the meets we can go to docs-sheet-container goog-inline-block to get the list of bottom elments
        then in such element we can ust find elements to get all the bottom elements
        '''
        google_sheet_bar_elements = self.driver.find_element(By.CSS_SELECTOR, ".docs-sheet-container-bar.goog-toolbar.goog-inline-block")
        meets = google_sheet_bar_elements.find_elements(By.XPATH, "./div")
        for meet in meets: 
            if event_input_for_sssad.strip() == meet.text.strip():
                meet.click()
                current_url = self.driver.current_url
                download_url = current_url[:current_url.rfind("/") + 1] + f"export?format=csv&{current_url[current_url.find("#gid="):]}".replace("#", "")
                df = pd.read_csv(download_url)
                if df.iloc[:, 0].isna().all():
                    df = df.iloc[:, 1:]
                file_name = f"sssad_data/{event_input_for_sssad} - {datetime.now().year}.csv"
                df.to_csv(file_name, index=False)
                return file_name

    def go_to_csv_page_CHAMPIONSHIP(self):
        self.driver.find_element(By.CSS_SELECTOR, ".et_pb_row.et_pb_row_1.et_pb_row_5col")

    def run_scrapper(self):
        '''
        if the user wants twilight meet 1 - 4 go to the twilight meet schedule 
        if the user wants champion ship go the champion ship which will also be parsed differently
        '''
        csv_to_parse = None
        if self.event_input == "SSSAD City Championships":
            csv_to_parse = self.go_to_csv_page_CHAMPIONSHIP()
        else:
            csv_to_parse = self.go_to_csv_page_TWLIGHT()
        return csv_to_parse
        
if __name__ == "__main__":
    # example usage
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    sssad_tracker = SSSadTracker(driver=driver, base_url="https://sssad.net/track-and-field/", event_input="SSSAD Twilight Meet #4")
    sssad_tracker.run_scrapper()