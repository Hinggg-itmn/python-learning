import json
from datetime import datetime,timedelta,timezone
def age_classification(age):
    if age < 13:
        return"Children"
    elif age <18:
        return "Young"
    elif age <25:
        return "Adolescent"
    else:
        return"Old"
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
def cout_all_city(data):
    print("All-City-Information")

    preferred_unit = data["user"]["preferred_temperature_unit"]

    for city_name, info in data["cities"].items():

        print(f"\n{city_name}")

        lat, lon, time_zone = info["coordinates_and_timezone"]
        temperature = info["current_temperature"]
        origin_unit = info["unit"]

        converted_temp = convert_temperature(
            temperature,
            origin_unit,
            preferred_unit
        )

        print(f"Location: {lat}, {lon}")
        print(f"Timezone: {time_zone}")
        print(f"Temperature: {round(converted_temp,2)} {preferred_unit}")
def cout_all_user(data):
    print("All-User-Information")
    user =data["user"]
    birthday=data["user"]["birthday"]
    age=calculate_age(birthday["year"],birthday["month"],birthday["day"])
    age_class=age_classification(age)
    print(f"Name : {user['name']}")
    print(f"Birthday : {birthday['day']:02d}/{birthday['month']:02d}/{birthday['year']}")
    print(f"Age : {age} ({age_class})")
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
def main():
    now = datetime.now()
    print(f"--Day, Month, Year: {now.strftime('%d/%m/%Y')}")
    try :
        with open('data.json','r',encoding='utf-8') as f:
            city_data=json.load(f)
    except FileNotFoundError:
        print("Error: data.json was not found!")
        return
    cout_all_user(city_data)
    cout_all_city(city_data)
if __name__=="__main__":
    main()