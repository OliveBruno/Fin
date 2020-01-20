import Month as m

class Year():
    def __init__(self,gross_income,year = m.this_year):
        
        self.year = year
        
        if(type(gross_income) == list):
            
            #print("hey im a list")
            
            self.jan = m.Month(income = gross_income[0],month = 1,year = year)
            self.feb = m.Month(income = gross_income[1],month = 2,year = year)
            self.mar = m.Month(income = gross_income[2],month = 3,year = year)
            self.apr = m.Month(income = gross_income[3],month = 4,year = year)
            self.may = m.Month(income = gross_income[4],month = 5,year = year)
            self.jun = m.Month(income = gross_income[5],month = 6,year = year)
            self.jul = m.Month(income = gross_income[6],month = 7,year = year)
            self.aug = m.Month(income = gross_income[7],month = 8,year = year)
            self.sep = m.Month(income = gross_income[8],month = 9,year = year)
            self.octo = m.Month(income = gross_income[9],month = 10,year = year)
            self.nov = m.Month(income = gross_income[10],month = 11,year = year)
            self.dec = m.Month(income = gross_income[11],month = 12,year = year)

            
        elif(type(gross_income) in [float,int]):
            
            #print("hey im not a list")
            
            self.jan = m.Month(income = gross_income,month = 1,year = year)
            self.feb = m.Month(income = gross_income,month = 2,year = year)
            self.mar = m.Month(income = gross_income,month = 3,year = year)
            self.apr = m.Month(income = gross_income,month = 4,year = year)
            self.may = m.Month(income = gross_income,month = 5,year = year)
            self.jun = m.Month(income = gross_income,month = 6,year = year)
            self.jul = m.Month(income = gross_income,month = 7,year = year)
            self.aug = m.Month(income = gross_income,month = 8,year = year)
            self.sep = m.Month(income = gross_income,month = 9,year = year)
            self.octo = m.Month(income = gross_income,month = 10,year = year)
            self.nov = m.Month(income = gross_income,month = 11,year = year)
            self.dec = m.Month(income = gross_income,month = 12,year = year)
            
    def month(self,num):
            
        reverse_months_map = {  1:self.jan,
                                    2:self.feb,
                                    3:self.mar,
                                    4:self.apr,
                                    5:self.may,
                                    6:self.jun,
                                    7:self.jul,
                                    8:self.aug,
                                    9:self.sep,
                                    10:self.octo,
                                    11:self.nov,
                                    12:self.dec              
                                  }
            
        if(num in range(1,13)):            
            return reverse_months_map[num]
        else:
            return m.this_month
        
    def update(self):
        for i in range(1,13):
            self.month(i).update()
        
    def addfixedExpenses(self,expenses):
        
        for i in range(1,13):
            self.month(i).addExpense(expenses,mode = "expected")
    
    def nonWorkedDays(self,number_of_days,month_name = m.this_month,year = m.this_year):
        
        
        if(type(month_name) == str):
            
            self.month(m.months_map[month_name]).non_worked_days = number_of_days
            self.month(m.months_map[month_name]).update()
        
        elif(type(month_name) == int and  month_name in range(1,13)):
            
            self.month(month_name-1).non_worked_days = number_of_days
            self.month(month_name-1).update()
    def forecast(self):
        
        forecast_map = {}
        
        for i in range(1,13):
            
            forecast_map[str(list(m.months_map.keys())[i-1])] = self.month(i).receipt()
        
        return forecast_map
            
