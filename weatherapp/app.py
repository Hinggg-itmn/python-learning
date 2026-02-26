from datetime import datetime
from models import City
from repository import DataRepository
from services import WeatherService
from services import UserService
class WeatherApp:
    MENU = """
╔══════════════════════════════╗
║       WEATHER APP            ║
╠══════════════════════════════╣
║  1. USER INFORMATION         ║
║  2. PRINT ALL CITIES         ║
║  3. SEARCH CITIES            ║
║  4. ADD CITY                 ║
║  5. UPDATE TEMPERATURE       ║
║  6. DELETE CITY              ║
║  7. UPDATE USER INFO         ║
║  8. WEATHER ALERT            ║
║  9. EXPORT TO CSV            ║
║  0. EXIT                     ║
╚══════════════════════════════╝
SELECT: """
    def __init__(self, data_path: str = "data.json"):
        self._repo = DataRepository(data_path)
        self._weather = WeatherService(self._repo)
        self._user_svc = UserService(self._repo)
    def run(self) -> None:
        print(f"\n📅  {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        self._repo.load()

        handlers = {
            "1": self._show_user,
            "2": self._show_all_cities,
            "3": self._search_city,
            "4": self._add_city,
            "5": self._update_temperature,
            "6": self._delete_city,
            "7": self._update_user,
            "8": self._show_alerts,
            "9": self._export_csv,
            "0": None,  # exit
        }

        while True:
            choice = input(self.MENU).strip()

            if choice == "0":
                print("\n GOODBYE!\n")
                break

            handler = handlers.get(choice)
            if handler:
                try:
                    handler()
                except (KeyboardInterrupt, EOFError):
                    print("\n CANCEL OPERATION\n")
            else:
                print("❌ INVALID SELECTION (0-9).")

            input("\n  [Enter] For Continue...")
    def _show_user(self) -> None:
        print("\n USER INFORMATION")
        user = self._user_svc.get_user()
        if user:
            user.display()
        else:
            print(" No user found.")
    def _show_all_cities(self) -> None:
        print("\n ALL CITIES")
        unit = self._repo.user.preferred_temperature_unit if self._repo.user else "C"
        for city in self._repo.cities.values():
            city.display_card(preferred_unit=unit)
    def _search_city(self) -> None:
        query = input(" Enter city name to search: ").strip()
        results = self._weather.search(query)
        if not results:
            print(f"\n  No cities found matching '{query}'.")
            return
        print(f" Found {len(results)} city(ies) matching '{query}':")
        unit=self._repo.user.preferred_temperature_unit if self._repo.user else "C"
        for city in results.values():
            city.display_card(preferred_unit=unit)
    def _add_city(self) -> None:
        print("\n══   ADD CITY  ══")
        name = input("  City name: ").strip()
        if not name:
            print("  NAME CANOT BE EMPTY.")
            return

        if self._repo.city_exists(name):
            print(f"  '{name}' already exists in data.")
            return

        try:
            temp  = int(float(input("  Current Temperature: ")))
            unit  = input("  Unit (C/F): ").upper().strip()
            if unit not in ("C", "F"):
                print("  Unit must be 'C' or 'F'.")
                return
            lat   = float(input("  Latitude : "))
            lon   = float(input("  Longitude: "))
            tz    = input("  Timezone (Ex: GMT+7): ").strip()
        except ValueError:
            print("  value must be a number.")
            return

        city = City(
            name=name,
            current_temperature=temp,
            unit=unit,
            last_7_days_temperatures=[temp] * 7,
            lattitude=lat,
            longitude=lon,
            timezone=tz,
        )

        if not city.is_valid_coordinates():
            print("  Coordinates are out of range.")
            return

        self._weather.add_city(city)
        print(f"  Add '{name}' succesfully!")
    def _update_temperature(self) -> None:
        print("\n══ UPDATE TEMPERATURE ══")
        name = input("  City name: ").strip()
        try:
            temp = int(float(input(f"  New temperature {name}: ")))
        except ValueError:
            print("  Temperature must be a number.")
            return

        if self._weather.update_city_temperature(name, temp,unit=self._repo.user.preferred_temperature_unit if self._repo.user else "C"):
            print(f"  Updated '{name}' → {temp}°")
        else:
            print(f"  Not be found '{name}'.")

    def _delete_city(self) -> None:
        print("\n══ DELETE CITY ══")
        name = input("  City name: ").strip()
        if not self._repo.city_exists(name):
            print(f"  ❌  '{name}' dont exists.")
            return
        confirm = input(f"  Delete '{name}'? (y/n): ").lower()
        if confirm == "y":
            self._weather.delete_city(name)
            print(f" '{name}' be deleted.")
        else:
            print("  Cancel operation.")

    def _update_user(self) -> None:
        print("\n══ UPDATE USER ══")
        name = input("  New Name (Enter for keep): ").strip()
        try:
            year  = int(input("  Year: "))
            month = int(input("  Month: "))
            day   = int(input("  Day: "))
        except ValueError:
            print("  Bỉrthdate must be a number.")
            return
        unit = input("  Preferred temperature unit (C/F): ").upper().strip()

        if self._user_svc.update_user(name, year, month, day, unit):
            print("  Update user succesfully!")
        else:
            print("  Information dont valid .")

    def _show_alerts(self) -> None:
        print("\n══ WEATHER ALERT ══")
        alerts = self._weather.get_weather_alert()
        if not alerts:
            print("  Dont have any weather alerts today.")
            return
        for city_name, msgs in alerts:
            print(f"\n  📍 {city_name}:")
            for msg in msgs:
                print(f"      {msg}")

    def _export_csv(self) -> None:
        path = input("  CSV file name (df: cities_export.csv): ").strip()
        self._repo.export_to_csv(path or "cities_export.csv")
