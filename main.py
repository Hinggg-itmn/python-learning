import json
from datetime import datetime,timedelta,timezone
from services import cout_all_user,cout_all_city
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