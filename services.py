from utils import *
def print_avrtpr_last7days(data):
    print("Cities : ")
    city_map={}
    for i ,city_name in emurate(data['cities']):
        city_map[i]=city_name
        print(f"{i} : {city_name}")
    choice =int(input("Select the city you want to see the average temperature for the last 7 days :"))
    selected_city=city_map.get(choice)
    if selected_city:
        history= data["cities"][selected_city]["last_7_days_history"]
        avg = calculate_avr_temperature(history)
        print(f"Avrage last 7 days: {avg}")
    else:
        print("Invalid Choice")
def search_city(data):
    query=input("Your city(or 1 part): ")
    result ={k:v for k,v in data['cities'].items() if query in k.lower()}
    if not result:
        print("Your city name not in data")
    else :
        print(f"Find {len(result)} city")
        for name,info in result.items():
            print_city_card(name, info)
def add_new_city(data):
    print("\n Add new city ")
    name = input("City name: ").strip()
    if not name:
        print("Invalid Input Name")
        return
    if check_city_in_data(name,data) is True:
        print("Your city is been in data")
        return
    try:
        temp=float(input("Current temperature: "))
        if temp<-100 or temp>100:
            print("Warning :Your Current temperature is not real ")
        unit = input("Unit (C/F): ").upper().strip()
        if unit not in ['C','F']:
            print("Error: Your unit must be C or F")
            return
        lat = float(input("Latitude: "))
        lon = float(input("Longitude: "))
        timezone=input("Timezone (e.g.., GMT +7): ").strip()
        new_city_data={
            "current_temperature":temp,
            "unit": unit,
            "last_7_days_history":[temp]*7,
            "coordinates_and_timezone":[lat,lon,timezone]
        }
        data['cities'][name]=new_city_data
        save_data(data,'data.json')
        print(f"The {name} city is push")
    except ValueError:
        print("Error: Temperatur and coordinates must be interger!")
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