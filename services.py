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