#import statements
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass
from config import api_key
local_api = api_key
changes_saved = False

# setting up for scraping
def getResponse(url):
    return requests.get(url)

def getHTML(response):
    return response.text

# setting up holiday dataclass
@dataclass
class Holiday:
    name: str
    date: str
    
    def __str__ (self):
        return (print(f'{self.name} ({self.date})'))

# setting up weather dataclass
@dataclass
class Weather:
    date: str
    conditions: str

#function to get weather from API
def get_weather():
    current_time = datetime.now()
    current_date = (f'{current_time.year}-{current_time.month}-{current_time.day}')
    dt = datetime.strptime(current_date, '%Y-%m-%d')
    start_temp = dt - timedelta(days=dt.weekday())
    end_temp = start_temp + timedelta(days=6)
    start = start_temp.strftime('%Y-%m-%d')
    end = end_temp.strftime('%Y-%m-%d')

    weather_url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Brooklyn%2C%20NY/{start}/{end}?unitGroup=metric&elements=datetime%2Cconditions&include=days&key={local_api}&contentType=json'

    response = requests.get(weather_url)
    response
    json = response.json()

    global weather_list
    global weather_info
    weather_list = []
    for i in range(0,7):
        date = json['days'][i]['datetime']
        weather_desc = json['days'][i]['conditions']
        weather_info = Weather(date, weather_desc)
        weather_list.append(weather_info)

# setting up Holiday List dataclass with menu functionalities
@dataclass
class HolidayList:
    inner_holidays: list

    def add_holiday(self, new_holiday_obj):
        if new_holiday_obj in self.inner_holidays:
            return (print(f'\n{new_holiday_obj.name} ({new_holiday_obj.date}) already exists in our system.'))
        else:
            self.inner_holidays.append(new_holiday_obj)
            return (print(f'\nSuccess!\n{new_holiday_obj.name} has been added to our system.'))

    def search_holidays(self, search_obj):
        for holiday in self.inner_holidays:
            if search_obj.name == holiday.name and search_obj.date == holiday.date:
                return print(holiday)
        else:
            return (print('Holiday not found'))

    def delete_holiday(self):
        holiday_found = False
        while holiday_found == False: 
            holiday_name_search = input('\nName: ')
            print('\nReminder: Holiday date must be in format \'YYYY-MM-DD\'')
            holiday_date_search = input('\nDate: ')
            for holiday in self.inner_holidays:
                if holiday_name_search == holiday.name and holiday_date_search == holiday.date:
                    self.inner_holidays.remove(holiday)
                    return(print(f'\nSuccess!\n{holiday_name_search} has been deleted from our system.'))
            else:
                print('\nHoliday not found')
                continue

    def read_json(self):
        # you may need to update this depending on your local file repository
        f = open(R'holidays.json')
        data = json.load(f)
        for i in range(0, len(data)):
            name = data[i]['name']
            date = data[i]['date']
            new_holiday_obj = Holiday(name, date)
            print(f'Adding holiday {new_holiday_obj.name}.')
            self.add_holiday(new_holiday_obj)
            holidays.append(new_holiday_obj)

    def save_to_json(self):
        global changes_saved
        changes_saved = True
        holiday_list = [holiday.__dict__ for holiday in self.inner_holidays]
        # you may need to update this depending on your local file repository
        with open(R'holidays.json', 'w') as file:
            json.dump(holiday_list, file, indent = 4)
        return(print('Holidays were successfully saved to your file.'))

    def scrape_holidays(self):
        for i in range (2020, 2025):
            url = f'https://www.timeanddate.com/holidays/us/{i}?hol=43119487'
            print(f'Scraping holidays from {i}')

            resp = getResponse(url)
            html = getHTML(resp)

            soup = BeautifulSoup(html, 'html.parser')

            rows = soup.find_all('tr', attrs = {'showrow'})

            for row in rows:
                date = row.find('th').text
                def mdy_to_ymd(d):
                    return datetime.strptime(d, '%b %d').strftime(f'{i}-%m-%d')
                formatted_date = mdy_to_ymd(date)
                name = row.find('a').text
                holiday = Holiday(name, formatted_date)
                self.add_holiday(holiday)
    
    def get_len(self):
        return print(len(self.inner_holidays))

    def get_holidays(self, year, week_number):
        holidays_in_week = []
        for holiday in self.inner_holidays:
            from datetime import datetime
            string = holiday.date
            date = datetime.strptime(string, '%Y-%m-%d')

            y = date.year
            m = date.month
            d = date.day

            import datetime
            get_week = lambda y, m, d : datetime.date(y, m, d).isocalendar().week

            week_of_holiday = get_week(y, m, d)
            
            if y == year and week_of_holiday == week_number:
                holidays_in_week.append(holiday)
                continue
            else:
                continue
        for holiday in holidays_in_week:
            print(f'\n{holiday.name} ({holiday.date})')

    def get_current_holidays(self, year, week_number):
        get_weather()
        holidays_in_week = []
        for holiday in self.inner_holidays:
            from datetime import datetime
            string = holiday.date
            date = datetime.strptime(string, '%Y-%m-%d')

            y = date.year
            m = date.month
            d = date.day

            import datetime
            get_week = lambda y, m, d : datetime.date(y, m, d).isocalendar().week

            week_of_holiday = get_week(y, m, d)
            
            if y == year and week_of_holiday == week_number:
                holidays_in_week.append(holiday)
                continue
            else:
                continue
        for holiday in holidays_in_week:
            print(f'\n{holiday.name} ({holiday.date})')
        for weather_info in weather_list:
            print(f'\n{weather_info.date} - {weather_info.conditions}')


holiday_menu = '''     
    Holiday Menu
=====================
1. Add a holiday
2. Remove a holiday
3. Save holiday list
4. View holidays
5. Exit
'''
# initialize data
holidays = []
library = HolidayList(holidays)
library.read_json()
library.scrape_holidays()

print('\nHoliday Management\n==================')
print(f'\nThere are {len(holidays)} holidays in the system.')

in_menu = True
while in_menu == True:
    print(holiday_menu)
    menu_choice = input('\nPlease choose a menu item: ')
    if menu_choice == '1':
        print('\nAdd a Holiday\n============')
        checking_holiday_date = True
        while checking_holiday_date == True:
            new_holiday_name = input('\nName: ')
            print('\nReminder: Holiday date must be in format \'YYYY-MM-DD\'')
            new_holiday_date = input('\nDate: ')  
            try:
                datetime.strptime(new_holiday_date, '%Y-%m-%d')
                new_holiday_obj = Holiday(new_holiday_name, new_holiday_date)
                library.add_holiday(new_holiday_obj)
                changes_saved = False
                checking_holiday_date = False
            except ValueError:
                print('Please format your date \'YYYY-MM-DD\'')
                continue
    if menu_choice == '2':
        print('\nRemove a Holiday\n============')
        library.delete_holiday()
        changes_saved = False

    if menu_choice == '3':
        print('\nSaving Holiday List\n======================')
        save_choice = input('\nAre you sure you want to save your changes? [y/n]: ')
        if save_choice == 'y':
            library.save_to_json()
        if save_choice == 'n':
            print('\nCanceled:\nHoliday list file save canceled.')

    if menu_choice == '4':
        print('\nView Holidays\n======================')
        current_time = datetime.now()
        current_year = current_time.year
        current_week = datetime.now().isocalendar().week
        current_year_int = int(current_year)
        current_week_int = int(current_week)
        year = int(input('\nWhich year?: '))
        week_number = int(input('\nWhich week? #[1-52, Enter 0 for the current week]: '))
        if year == current_year_int and week_number == 0:
            weather = input('\nWould you like to see this week\'s weather? [y/n]: ')
            if weather == 'n':
                print(f'\nThese are the holidays for {current_year_int} week #{current_week_int}:')
                library.get_holidays(year, current_week_int)
            if weather == 'y':
                print(f'\nThese are the holidays for {current_year_int} week #{current_week_int}:')
                library.get_current_holidays(year, current_week_int)
        if year != current_year_int and week_number == 0:
            print('\nYou must enter the current year to view the current week. Try again.')
        else:
            print(f'\nThese are the holidays for {year} week #{week_number}:')
            library.get_holidays(year, week_number)

    if menu_choice == '5':
        print('\nExit\n====')
        if changes_saved == True:
            exit_choice = input('\nAre you sure you want to exit? [y/n] ')
            if exit_choice == 'y':
                print('\nGoodbye!')
                in_menu = False
            if exit_choice == 'n':
                continue
        if changes_saved == False:
            exit_choice = input('\nAre you sure you want to exit?\nYour changes will be lost.\n[y/n] ')
            if exit_choice == 'y':
                print('\nGoodbye!')
                in_menu = False
            if exit_choice == 'n':
                continue