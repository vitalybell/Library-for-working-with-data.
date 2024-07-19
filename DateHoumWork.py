from datetime import datetime


class Superdate(datetime):
    dict_season = {(12, 1, 2): 'Winter', (3, 4, 5): 'Spring',
                   (6, 7, 8): 'Summer', (9, 10, 11): 'Autumn'}
    dict_time = {range(6, 12): 'Morning', range(12, 18): 'Day',
                 range(18, 24): 'Evening', range(0, 6): 'Night'}

    def __init__(self, year, month, day, hour):
        self.date = datetime(year, month, day, hour)

    def get_season(self):
        for i in self.dict_season:
            if self.date.month in i:
                return self.dict_season[i]

    def get_time_of_day(self):
        for a in self.dict_time:
            if self.date.hour in a:
                return self.dict_time[a]


b = Superdate(2024, 9, 30, 12)
print(b.get_season())
print(b.get_time_of_day())
