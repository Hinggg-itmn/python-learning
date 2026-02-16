from datetime import datetime,timedelta,timezone
import json
import csv
import re 
#VALIDATE NUMBER
def validate_temperature(temp,unit):
    unit=unit.upper()
    if unit =="C":
        return -50 <= temp<=60
    elif unit=="F":
        return -60 <=temp<=140
    return False
def validate_coordiantes(lat,lon):
    return (-90 <= lat<=90) and (-180 <= lon <= 180)
def validate_city_name(name):
    if not name or not (2<=len(name.strip())<=0):
        return False
    return bool(re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", name))
def age_classification(age):
    if age < 13:
        return"Children"
    elif age <18:
        return "Young"
    elif age <25:
        return "Adolescent"
    else:
        return"Old"
def load_data(path: str):
    with open(path,"r",encoding="utf-8" ) as f:
        return json.load(f)
def save_data(data:dict,path:str):
    with open(path,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
def calculate_avr_temperature(list_temperature):
    if len(list_temperature) ==0:
        return 0
    return round(sum(list_temperature)/len(list_temperature),1)
def calculate_city_time(time_zone_gmt):
    hours_utc=datetime.now(timezone.utc)
    try:
        offset_value=int(time_zone_gmt.replace("GMT","").replace("+",""))
        hours_city=hours_utc + timedelta(hours=offset_value)
        return hours_city.strftime("%H:%M:%S")
    except ValueError:
        return "Invalid GMT format"
def calculate_age(year_born,month_born,day_born):
    today =datetime.now()
    age = today.year-year_born
    if (month_born, day_born )> (today.month, today.day):
        age -=1
    return age
def convert_temperature(temp, from_unit, to_unit):
    if from_unit == to_unit:
        return temp
    if from_unit == "F" and to_unit == "C":
        return (temp - 32) / 1.8
    if from_unit == "C" and to_unit == "F":
        return temp * 1.8 + 32
    raise ValueError("Invalid unit")
def print_city_card(name, info):
    """This function is specifically for printing city 
    information for aesthetic purposes."""
    print(f"\n CITY: {name.upper()}")
    print(f"   ------------------------------")
    print(f"   🌡️  TEMPERATURE: {info['current_temperature']}°{info['unit']}")
    print(f"   🌍  COORDINATES:  {info['coordinates_and_timezone'][0]}, {info['coordinates_and_timezone'][1]}")
    print(f"   🕒  TIME ZONE: {info['coordinates_and_timezone'][2]}")
    print(f"   ------------------------------")
#CHECK
def check_city_in_data(name, data):
    return name in data['cities']
def update_info_user(data):
    name=input("Your Name: ").strip()
    if name:
        data["user"]["name"]= name
    try:
        print("\n Your Birthday : ")
        year = int(input("Year: "))
        month=int(input("Month: "))
        day= int(input("Day: "))
        data["user"]["birthday"] = {
            "year":year,
            "month":month,
            "day":day
        }
    except ValueError:
        print("Error: Please enter an integer!")
        return False
    unit= input("\nYour preffered temperature unit (C/F): ").upper()
    if unit in ["C","F"]:
        data["user"]["preferred_temperature_unit"] = unit
    return True
def delete_city(data):
    print("\n Delete city ")
    name = input("Your city name which you want delete: ").strip()
    if check_city_in_data(name,data) is True:
        confirm=input(f"Are you want to delete {name}? (y/n): ").lower()
        if confirm == 'y':
            data['cities'].pop(name)
            save_data(data,'data.json')
            print(f"The {name}city is deleted")
        else:
            print("Cancel the operation")
    else:
        print(f"The {name} does not exits.")
def export_to_csv(path:str):
    with open(path,mode = 'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['City', 'Temperature', 'Unit', 'Avg_7days', 'Lat', 'Lon', 'Timezone'])
        for city,info in data['cities'].item():
            avg_7days=calculate_avr_temperature(info['last_7_days_history'])
            lat,lon,timezone=info['coordinates_and_timezone']
            
    print(f"{path} conversion to csv was succesfully ")
def update_city_temperature(data):
    print("\n Update Temperature")
    name = input("Enter the name of the city to be updated: ").strip()
    if check_city_in_data(name,data) is False:
        print(f"The cities not in data {name}")
        return
    try:
        new_temp=float(input(f"New temperature {name}: "))
        data['cities'][name]['current_temperature'] = new_temp
        history =data['cities'][name]['last_7_days_history']
        history.pop(0)
        history.append(new_temp)
        save_data(data,'data.json')
        print(f"Updated data for {name}")
    except ValueError:
        print("Error: The temperature must be interger!") 
        