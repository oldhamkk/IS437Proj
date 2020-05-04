import pymysql
from baseObject import baseObject
class eventList(baseObject):
    #this is the assignment
    def __init__(self):
        self.setupObject('events')

    def verifyNew(self,n=0):
        self.errorList = []

        if len(self.data[n]['name']) == 0:
            self.errorList.append("Event name cannot be blank.")

        #Add if statements for validation of other fields
        if len(self.data[n]['start']) == 0:
            self.errorList.append("Venue College cannot be blank.")

        if len(self.data[n]['end']) == 0:
            self.errorList.append("Venue address cannot be blank.")

        if len(self.data[n]['VenueID']) == 0:
            self.errorList.append("Must provide a venue.")

        if len(self.errorList) > 0:
            return False
        else:
            return True

    def verifyChange(self,n=0):
        self.errorList = []

        if len(self.data[n]['name']) == 0:
            self.errorList.append("Name cannot be blank.")

        if len(self.errorList) > 0:
            return False
        else:
            return True
