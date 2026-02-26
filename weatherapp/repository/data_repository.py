import csv
import json
from pathlib import Path
from typing import Dict, List
from models import City
from models import User

class DataRepository:
    def __init__(self,json_path: str = "data.json"):
        self.json_path = Path(json_path)
        self._cities: Dict[str, City] = {}
        self._user: User | None= None
    def load(self) -> None:
        if not self.json_path.exists():
            raise FileNotFoundError (f"Data file {self.json_path} not found.")
        with open(self.json_path, "r",encoding="utf-8") as f:
            raw = json.load(f)
        self._user = User.from_dict(raw['user']['name'], raw['user'])
        self._cities = {
            name:City.from_dict(name, data) 
            for name, data in raw['cities'].items()
        }
    def save(self) -> None:
        data={
            "user": self._user.to_dict() if self._user else {},
            "cities": {name: city.to_dict() for name, city in self._cities.items()}
        }
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    def export_to_csv(self, csv_path: str="cities_export.csv") -> None:
        rows=[]
        for city in self._cities.values():
            rows.append({
                "City": city.name,
                "current_temperature": city.current_temperature,
                "unit": city.unit,
                "average_temperature": city.average_temperature(),
                "temperature_range": city.temperature_range(),
                "lattitude": city.lattitude,
                "longitude": city.longitude,
                "timezone": city.timezone
            })
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"City data exported to {csv_path}")
    @property
    def user(self) -> User | None:
        return self._user
    @user.setter
    def user(self, value: User) -> None:
        self._user = value
    @property
    def cities(self) -> Dict[str, City]:
        return self._cities
    def add_city(self, city: City) -> None:
        self._cities[city.name] = city
    def get_city(self, name: str) -> City | None:
        return self._cities.get(name)
    def delete_city(self, name: str) -> bool:
        if name in self._cities:
            del self._cities[name]
            return True
        return False
    def city_exists(self, name: str) -> bool:
        return name in self._cities
    def search_cities(self, query: str) -> Dict[str, City]:
        q = query.lower()
        return {k: v for k, v in self._cities.items() if q in k.lower()}