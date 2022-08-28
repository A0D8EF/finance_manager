"""
def monthly_calc(balances, selected_date):

        data    = []

        for i in range(0,12):
            dic             = {}
            dic["year"]     = int(selected_date.year)
            dic["month"]    = int(selected_date.month)-i
            if dic["month"] < 1:
                dic["year"]  = int(selected_date.year)-1
                dic["month"] = 12 + dic["month"]
            dic["amount"]   = 0
            dic["income"]   = 0
            dic["spending"] = 0

            data.append(dic)

        data.reverse()

        for balance in balances:
            year    = balance.use_date.year
            month   = balance.use_date.month
            income  = balance.expense_item.income
            amount  = balance.amount

            for d in data:
                if d["year"] != year or d["month"] != month:
                    continue
                
                if income:
                    d["amount"] += amount
                    d["income"] += amount
                else:
                    d["amount"] -= amount
                    d["spending"] += amount
                
                break
        
        return data


def daily_calc(balances):
    
        data    = []

        for i in range(1,32):
            dic             = {}
            dic["day"]      = i
            dic["amount"]   = 0

            data.append(dic)
        
        for balance in balances:
            day   = balance.use_date.day
            income  = balance.expense_item.income
            amount  = balance.amount

            for d in data:
                if d["day"] != day:
                    continue
                
                if income:
                    d["amount"] += amount
                else:
                    d["amount"] -= amount
                
                break
        
        return data
"""
