
class EventTimeline:

    def __init__(self):
        # Constructor of the whole EventTimeline. Contains both Event and SusFile classes.
        # Note where Susfiles would be derived from Asher
        self.timelines = []
        self.sus_files = []

    def add_timeline(self, timeline):
        self.timelines.append(timeline)

    def add_sus_file(self, sus_file):
        self.sus_files.append(sus_file)
    
    def generate_report(self):
        print('Report')
        self.generate_timelines()
        self.generate_sus_files()
        
    def generate_timelines(self):
        print('\nTimelines')
        for timeline in self.timelines:
            print(timeline)

    def generate_sus_files(self):
        print('\nSus Files')
        for sus_file in self.sus_files:
            print(sus_file)
        print("\n")    
    
    def clear_timeline(self):
        self.timelines.clear()

    def clear_susfiles(self):
        self.sus_files.clear()   

    # Above logic is for a class that creates EventTimline objects. Each containing a timeline and and array of sus files
    # Logic can hopefully be included in the report or as a txt file? lol

class Event:
    
    def __init__(self, event_name, timestamp, details):
        self.event_name = event_name
        self.timestamp = timestamp
        self.details = details

    def __str__(self):
        return f"Event: {self.event_name}, Time: {self.timestamp}, Details: {self.details}"
    
    # Events would come from a running log during analysis. Could be helpful to add in the timeline, or maybe useful as a log.
    
class SusFile:
    # Note: Subject to change values based on Asher/Tristan work
    def __init__(self, file_name, inode_number, mac_dates, hash_value):
        self.file_name = file_name
        self.inode_number = inode_number
        self.mac_dates = mac_dates
        self.hash_value = hash_value

    def __str__(self):
        return f"Sus File: {self.file_name}, Inode Number: {self.inode_number}, Mac Dates: {self.mac_dates}, Hash Value: {self.hash_value}"
