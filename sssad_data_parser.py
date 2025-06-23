import pandas as pd
from noramalize_functions import normalize_sssad_events, normalize_trackie_events, normalize_sssad_category
from io import StringIO

class SSSadDataParserError(Exception):
    pass

class SSSadDataParser:
    def __init__(self, csv_file, meet_file_path):
        self.csv_file = csv_file
        self.meet_file_path = meet_file_path

        # get the event input
            # meets/SSSAD Twilight Meet #4 - May 20th, 2025.csv
        event_input = self.meet_file_path.split(" - ")[0].split("/")[1]
            # -> SSSAD Twilight Meet #4

        self.event_input = event_input
        self.category_map = {
            'IG': "Intermediate",
            'JG': "Junior",
            'SG': "Senior",
            'IB': "Intermediate",
            'JB': "Junior",
            'SB': "Senior",
        }
        self.gender_map = {
            'IG': "female",
            'JG': "female",
            'SG': "female",
            'IB': "male",
            'JB': "male",
            'SB': "male",
        }
    def parse_twilight_schedule(self):
        '''
        the first snippet wil delete the first row unptil the index of Rolling Schedule 
        to remove all the use less data that is not needed
        '''
        with open(self.csv_file, 'r') as file:
            file_content = file.read()

        row_to_remove = file_content[file_content.find('\n') + 1:file_content.find("Rolling Schedule - All Times are Approximate")]
        file_content = file_content.replace(row_to_remove, "")

        # write back to the file to then later read it as a csv
        with open(self.csv_file, "w") as file:
            file.write(file_content)

        '''
        after the content is retrived, we can now parse the data
        and use it to make final rolling schedule
        '''
        data_frame_sssad = pd.read_csv(self.csv_file)
        '''
        this is what the current csv should look like
        https://ibb.co/N06Bxgv

        in the picture there should also be purple outline which indicates where the important data is
        and the part we should parse, so now we are going to parse the first part which is the track and field part then agerated it data
        first inorder to do that we need to get the content of the coresponding SSSAD meet and normalize it to a common format
        '''
        data_frame_trackie = pd.read_csv(self.meet_file_path)
        data_frame_trackie['Time'] = ' '

        # normalize all the user event of the corresponding csv
        data_frame_trackie['Gender'] = ' '
        data_frame_trackie['NormalizedRowIgnored'] = ' '
        data_frame_trackie['Specific-Location'] = ' '
        data_frame_trackie['Event-Type'] = ' '
        for idx, row in data_frame_trackie.iterrows():
            event = row['Event']
            gender = None
            if event[0] == "M":
                gender = "male"
                event = event.replace("Male", "").strip()
            else:
                gender = "female"
                event = event.replace("Female", "").strip()
            data_frame_trackie.loc[idx, 'NormalizedRowIgnored'] = normalize_trackie_events(event) 
            data_frame_trackie.loc[idx, 'Gender'] = gender
        '''
        start iterating over track and field from row 3 and the first column 
        should be the time the second one sould be the category the second one shoul dbe the events
        '''
        # resetting the index to make it easier to iterate over
        data_frame_sssad = data_frame_sssad.iloc[3:]
        data_frame_sssad = data_frame_sssad.reset_index(drop=True)
        # iterating
        current_time = None

        for _, row in data_frame_sssad.iterrows():
            time = row.iloc[0]

            # if there is no row then just skip it
            if pd.isna(row.iloc[1]) or pd.isna(row.iloc[2]):
                continue

            if current_time == None: 
                current_time = time
            elif pd.notna(time) and current_time != time: 
                current_time = time

            categories = normalize_sssad_category(row.iloc[1])
            event = row.iloc[2]
            event, _ = normalize_sssad_events(event)

            for category in categories:
                if category not in self.category_map:
                    continue
                gender = self.gender_map[category]
                category = self.category_map[category]
                # print(event, category, gender)

                # get the rows and column with the corresponding normalized row and category 
                match_filter = (
                    (data_frame_trackie['NormalizedRowIgnored'] == event) &
                    (data_frame_trackie['Category'] == category) &
                    (data_frame_trackie['Gender'] == gender)
                )

                # fill in the time for the matching rows
                data_frame_trackie.loc[match_filter, 'Time'] = current_time
                match_filter_event = (
                    (data_frame_trackie['NormalizedRowIgnored'] == event)
                )
                data_frame_trackie.loc[match_filter_event, 'Event-Type'] = "Track"


        '''
        after done parsing for the track  part
        now continue on to the field part using the same logic this should also be the new data frame
                       Unnamed: 3   Unnamed: 4   Unnamed: 5 Updated: May 6, 2025 Unnamed: 7  Unnamed: 8
0                     NaN  TJ - NW Pit  TJ - SE Pit               Discus  High Jump  Pole Vault
1                 4:30 PM           IG           IB                   JB         IB    IG/JG/SG
2                 5:00 PM          NaN          NaN                  NaN        NaN         NaN
3                 5:30 PM           JG           JB                   SB         JB         NaN
4                 6:00 PM          NaN          NaN                  NaN        NaN    IB/JB/SB
5                 6:30 PM           SG           SB                   IB         SB         NaN
6                 7:00 PM          NaN          NaN                  NaN        NaN         NaN
7                     NaN          NaN          NaN                  NaN        NaN         NaN
8                     NaN          NaN          NaN                  NaN        NaN         NaN
9   High Jump Progression          NaN          NaN                  NaN        NaN         NaN
10               IG/JG/SG       1.25 M      1.35 M                1.40 M     1.45 M      1.50 M
11                     IB       1.40 M       1.45 M               1.50 M     1.55 M      1.60 M
12                  JB/SB       1.50 M       1.55 M               1.60 M     1.65 M      1.70 M
13                    NaN          NaN          NaN                  NaN        NaN         NaN
14                    NaN          NaN          NaN                  NaN        NaN         NaN
15                    NaN          NaN          NaN                  NaN        NaN         NaN
16                    NaN          NaN          NaN                  NaN        NaN         NaN
17                    NaN          NaN          NaN                  NaN        NaN         NaN
        '''
        # trim off some part of a data frame
        data_frame_sssad = data_frame_sssad.iloc[:, 3:]
        data_frame_sssad = data_frame_sssad.reset_index(drop=True)

        # get the len of the current row
        row_len = data_frame_sssad.shape[1] - 1
        events_list = [None] * row_len
        events_row = data_frame_sssad.iloc[0, 1:]
        for i, event in enumerate(events_row):
            events_list[i] = normalize_sssad_events(event)
        events_list.insert(0, None)
        # now iterate over each row, assign it proper time aswell as event and location
        data_frame_sssad = data_frame_sssad.iloc[1:]
        data_frame_sssad = data_frame_sssad.reset_index(drop=True)
        for _, row in data_frame_sssad.iterrows():
            time = row.iloc[0]
            
            if pd.isna(time):
                break
            for i in range(1,row_len + 1):
                raw_category = row.iloc[i]
                if pd.isna(raw_category):
                    continue
                # convert everything to proper trackie format
                categories = normalize_sssad_category(raw_category)
                event, location = events_list[i]

                
                for category in categories:
                    if category not in self.gender_map or category not in self.category_map:
                        continue
                    gender = self.gender_map[category]
                    category = self.category_map[category]
                    # get the matching queries
                    match_filter = (
                        (data_frame_trackie['NormalizedRowIgnored'] == event) &
                        (data_frame_trackie['Category'] == category) &
                        (data_frame_trackie['Gender'] == gender)
                    )

                    # fill in the time for the matching rows aswell as the additional spefici location if there is any
                    # location also will be none if there is no specific location
                    data_frame_trackie.loc[match_filter, 'Time'] = time
                    data_frame_trackie.loc[match_filter, 'Specific-Location'] = location 

                    match_filter_event = (
                        (data_frame_trackie['NormalizedRowIgnored'] == event)
                    )
                    data_frame_trackie.loc[match_filter_event, 'Event-Type'] = "Field"
        # output everything
        output_path = self.meet_file_path.replace("meets/", "rolling_schedule/")
        data_frame_trackie.to_csv(output_path, index=False)
    def parse_championship(self):
        pass
    def parse_data(self):
        if self.event_input == "SSSAD City Championships":
            self.parse_championship()
        else:
            self.parse_twilight_schedule()

# example usage
if __name__ == '__main__':
    data_parser = SSSadDataParser(csv_file="sssad_data/Twilight Meet 4 - 2025.csv", meet_file_path="meets/SSSAD Twilight Meet #4 - May 20th, 2025.csv")
    data_parser.parse_data()
