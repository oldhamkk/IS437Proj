import pymysql
from baseObject import baseObject
class productList(baseObject):
    #this is the assignment
    def __init__(self):
        self.setupObject('products')

    def verifyNew(self,n=0):
        self.errorList = []
        pf = None

        try:
            pf = float(self.data[n]['productPrice'])
        except:
            self.errorList.append("productPrice cannot be blank.")
        if pf is not None:
            if pf > 0:
                self.data[n]['productPrice']
            else:
                self.errorList.append("productPrice cannot be negative.")

        if len(self.data[n]['productName']) == 0:
            self.errorList.append("productName name cannot be blank.")

        #Add if statements for validation of other fields
        if len(self.data[n]['SKU']) == 0:
            self.errorList.append("SKU cannot be blank.")

        if len(self.data[n]['email']) == 0:
            self.errorList.append("Email cannot be blank.")
        elif '.' and '@' not in self.data[n]['email']:
            self.errorlist.append("Email must contain a '.' and '@'")

        if len(self.data[n]['password']) < 0:
            self.errorList.append("Password must be more than 4 characters.")

        if len(self.data[n]['subscribed']) < 0:
            self.errorList.append("Subscribed status must be indicated.")
        elif 'True' or 'False' not in self.data[n]['subscribed']:
            self.errorList.append("Subscribed status must be True or False.")

        if len(self.errorList) > 0:
            return False
        else:
            return True
