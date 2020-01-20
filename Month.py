import calendar
from datetime import date
today = date.today()
this_month = today.strftime("%m")
this_year = today.strftime("%Y")

def get_business_days(date):
    
    month = int(date.split("/")[0])
    year = int(date.split("/")[1])
    
    weekday_count = 0
    cal = calendar.Calendar()

    for week in cal.monthdayscalendar(year, month):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            if day == 0 or i >= 5:
                continue
            # or some other control if desired...
            weekday_count += 1

    return (weekday_count)


timeFactorMap = {"day" : 365,
                "days" : 365,
                "month" : 12,
                "months" : 12,
                "year" : 1,
                "years" : 1              
                }

months_map = {"jan" : 1,
              "feb" : 2,
               "mar" : 3,
               "apr" : 4,
               "may" : 5,
               "jun" : 6,
               "jul" : 7,
               "aug" : 8,
               "sep" : 9,
               "oct" : 10,
               "nov" : 11,
               "dec" : 12              
              }#I should probably refactor these names.. they are pretty bad tbh...

        
class Month():
    def __init__(self,
                 income,
                 savings = 0,
                 non_worked_days = 0,
                 month = this_month,
                 year = this_year
                ):
        
        self.savings = savings
        self.non_worked_days = non_worked_days
        self.income = income
        
        if(type(month) == int and month in range(1,13)):
            self.month = month
        elif(type(month) == str and (str(month).lower() in months_map.keys())):
            self.month = months_map[month.lower()]
        else:
            self.month = 1
            
        self.year = year
        
        self.earnings = { "Net Income" : self.deduct(), "VR" :self.get_vr()}
        self.fixedExpenses = {}
        self.regularExpenses = {}
        self.expenses = {}
        
    def update(self):
        self.earnings["Net Income"] = self.deduct()
        self.earnings["VR"] = self.get_vr()
        self.expenses = dict(self.fixedExpenses)
        self.expenses.update(self.regularExpenses)
        
    def addFixedExpense(self,expenses):
        
        if(type(expenses) == dict):
            self.fixedExpenses.update(expenses)
            
        elif(type(expenses) == float or type(expenses) == int):
            name = "Unspecified 0"
            counter = 0
            while(("Unspecified " + str(counter)) in list(self.fixedExpenses.keys())):
                counter += 1

            name = "Unspecified " + str(counter)
                
            self.fixedExpenses[name] = float(expenses)
        
    def addRegularExpense(self,expenses):
        
        if(type(expenses) == dict):
            self.regularExpenses.update(expenses)
            
        elif(type(expenses) == float or type(expenses) == int):
            name = "Unspecified 0"
            counter = 0
            while(("Unspecified " + str(counter)) in self.regularExpenses):
                counter += 1

            name = "Unspecified " + str(counter)
                
            self.regularExpenses[name] = float(expenses)
            
    def addExpense(self,expenses,mode = "regular"):
        
        if(mode in ["regular","reg"]):
            self.addRegularExpense(expenses)
        elif(mode in ["expected","fixed"]):
            self.addFixedExpense(expenses)

        self.update()
        
            
    def totalDebt(self):
        
        discount = 0 #this is just an awful way of doing this,
                        #but I am very lazy and it should work for now
        
        for i in range(len(self.fixedExpenses.keys())):
            if(list(self.fixedExpenses.keys())[i] in list(self.regularExpenses.keys())):
                discount -= list(self.fixedExpenses.values())[i]
                
        
        return sum(self.fixedExpenses.values()) + sum(self.regularExpenses.values()) + discount
    
    def totalEarnings(self):
        
        return sum(self.earnings.values())
            
        
    def yields(self,
                timePeriod,
                amount = 0,
                rate = 4.4,
                timeScale = "month",
                rateTimeScale = "year"
               ):
        
        rate = rate/100
        rate = (1+rate)**((timePeriod*timeFactorMap[rateTimeScale])/timeFactorMap[timeScale])
            
        if(amount == 0):
            return (float) ("%.2f" %  (rate*self.savings))
        else:
            return (float) ("%.2f" % (rate*amount))
        
    def deduct(self, 
            retirementTax = 9/100,
            incomeTax = 7.5/100,
            increment = 142.8,
            vt = True
            ):
        
        baseTaxed = (1-retirementTax)*(1-incomeTax)*self.income + increment
        
        vtTax = 0
        non_worked_loss = 0
        
        if(vt):
            vtTax = 6/100
        
        if(not(self.non_worked_days == 0)):
            
            business_days = get_business_days(str(self.month) + "/" + str(self.year))
            non_worked_frac = self.non_worked_days/business_days
            non_worked_loss = non_worked_frac*baseTaxed
        
        
        Net = baseTaxed - vtTax*self.income - self.non_worked_days - non_worked_loss
        
        return (float) ("%.2f" % (Net))
    
    def get_vr(self,vr_daily = 21):
        
        try:
            vr_value = vr_daily*(get_business_days(str(self.month) + "/" + str(self.year)) - self.non_worked_days)
        except:
            vr_value = 0
        
        return vr_value
    
    def receipt(self):
        return float("%.2f" % (self.totalEarnings() - self.totalDebt()))
    
