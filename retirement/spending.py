class SpendingEngine:
    def total_spending(self, year:int)->float:
        yrs=year-2026
        housing=33600*(1.03**yrs)
        living=60000*(1.025**yrs)
        travel=(120000 if yrs<10 else 60000)*(1.03**yrs)
        healthcare=(23000 if year<2029 else 10000)*(1.05**yrs)
        charity=5000*(1.025**yrs)
        events=20000 if year==2027 else 50000 if year==2028 else 0
        return housing+living+travel+healthcare+charity+events
