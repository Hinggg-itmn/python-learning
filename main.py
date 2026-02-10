import json
from datetime import datetime,timedelta,timezone
from services import cout_all_user,cout_all_city
def show_menu():
    print("\n" + "="*10 + " YOUR CHOICE " + "="*10)
    print("1. View user info")
    print("2. View all cities")
    print("3. Search city by name")
    print("4. Add new city")
    print("5. Update city temperature")
    print("6. Delete city")
    print("7. Update user info")
    print("8. Exit")
    print("="*33)
    return input("Your choice: ")
def main():
    now = datetime.now()
    print(f"--Day, Month, Year: {now.strftime('%d/%m/%Y')}")
    try :
        load_data(data.json)
    except FileNotFoundError:
        print("Error: data.json was not found!")
        return
    while True:
        choice = show_menu()
        if choice=='1':
            cout_all_user(city_data)
        elif choice=='2':
            cout_all_city(city_data)
        elif choice =='3':
            #SEARCH
            pass
        elif choice=='4':
            #ADDNEWCITY
            pass
        elif choice=='5':
            #update city temperature
            pass
        elif choice =='6':
            #Delete city
            pass
        elif choice =='7':
            #update user info
            pass
        elif choice =='8':
            print("The console is closing.....See Yah!")
            break
        else:
            print("Invalid Choice, The range of your select (1-8).")
        input("\n Press Enter to continue...")
if __name__=="__main__":
    main()