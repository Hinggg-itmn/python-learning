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