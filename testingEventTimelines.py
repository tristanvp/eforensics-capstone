from eventTimeline import EventTimeline, Event, SusFile

class TestCases(EventTimeline):

    def setup_method(self):
        # Create EventTimeline instance for testing
        self.timeline = EventTimeline()

    def test_events_in_report(self):
        # Add events to timeline instance, in this case we hardcode with strings, rather than taking it from an JSON-y type input
        event1 = Event("Login Event", "2024-08-01 12:00:00", "User logged in")
        event2 = Event("Network Event", "2024-08-01 12:05:00", "TCP connection from 192.168.100.2")
        self.add_timeline(event1)
        self.add_timeline(event2)       
        self.generate_report()
        
    def test_sus_files_in_report(self):
        # Add suspicious files, as above SusFiles are harcoded with strings.
        susfile1 = SusFile("malware.exe", 10234, "2024-08-01 12:00:00", "abc123hash")
        susfile2 = SusFile("trojan.dll", 20456, "2024-08-01 12:05:00", "def456hash")
        self.add_sus_file(susfile1)
        self.add_sus_file(susfile2)
        #Generate report, show sus files in event report.
        self.generate_report()

    def test_empty_report(self):
        # Create an EventTimeline object with no events or sus files
        self.generate_report()

    def test_both_in_report(self):
        # Hardcode events
        event1 = Event("File Created", "2024-08-10 14:00:00", "Created 'evidence.txt'.")
        event2 = Event("File Modified", "2024-08-11 09:30:00", "Modified 'evidence.txt'.")
        self.timeline.add_timeline(event1)
        self.timeline.add_timeline(event2)
    
        # Hardcode sus files
        file1 = SusFile("trojan.dll", 20456, "2024-08-01 12:05:00", "def456hash")
        self.timeline.add_sus_file(file1)
    
        # Generate report.
        self.timeline.generate_report()
        

case = TestCases()
case.setup_method()
case.test_events_in_report()
case.test_sus_files_in_report()
case.test_both_in_report()
case.test_empty_report()