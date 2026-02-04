import json
from datetime import datetime
def calculate_age(year_born,month_born,day_born):
    today =datetime.now()
    age = today.year-year_born
    if (month_born, day_born )> (today.month, today.day):
        age -=1
    return age
def convert_temperature(city_name,data):
    if city_name in data:
        temp = data[city_name]
        if temp > 45:
            celsius = (temp - 32)/1.8
            return f"{temp} F = {celsius} C"
        else :
            return f"{temp} C"
    return "Not in data.json"
def main():
    now = datetime.now()
    print(f"--Day, Month, Year: {now.strftime('%d/%m/%Y')}")
    try :
        print("\n[Born in]")
        y= int(input('Year:'))
        m= int(input("Month: "))
        d= int(input("Day :"))
        age =calculate_age(y,m,d)
        print(f"Your exact age as of today is : {age}")
    except ValueError:
        print("Error: Please enter only integers for the day/month/year ")
    try :
        with open('data.json','r',encoding='utf-8') as f:
            city_data=json.load(f)
        print("--Temperature--")
        city=input("City(Hanoi, Saigon, New York, London): ")
        print(convert_temperature(city,city_data))
    except FileNotFoundError:
        print("Error: data.json was not found!")
if __name__=="__main__":
    main()