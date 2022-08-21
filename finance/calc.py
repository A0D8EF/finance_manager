def monthly_calc(balances):

        data    = []

        for i in range(1,13):
            dic             = {}
            dic["month"]    = i
            dic["amount"]   = 0
            dic["income"]   = 0
            dic["spending"] = 0

            data.append(dic)
        
        for balance in balances:
            month   = balance.use_date.month
            income  = balance.expense_item.income
            amount  = balance.amount

            for d in data:
                if d["month"] != month:
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

