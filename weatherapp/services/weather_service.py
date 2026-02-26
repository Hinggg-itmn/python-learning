from typing import List, Tuple
from models.city import City
from repository import DataRepository
class WeatherService:
    def __init__(self, repo: DataRepository):
        self._repo = repo
    def get_weather_alert(self)-> List[Tuple[str,List[str]]]:
        result=[]
        for city in self._repo.cities.values():
            alerts=[]
            temp_c=city.temperature_in("C")
            if temp_c < 0:
                alerts.append("Freezing temperatures")
            elif temp_c > 35:
                alerts.append("Heatwave conditions")
            if city.temperature_range() > 15:
                alerts.append("High temperature variability")
            if alerts:
                result.append((city.name, alerts))
        return result
    def average_of(self,city_name:str)->float|None:
        city=self._repo.get_city(city_name)
        if city is None:
            return None
        return city.average_temperature()
    def add_city(self,city:City)->bool: 
        if self._repo.city_exists(city.name):
            return False
        self._repo.add_city(city)
        self._repo.save()
        return True
    def update_city_temperature(self, city_name: str, new_temp: int,unit:str) -> bool:
        city= self._repo.get_city(city_name)
        if city is None:
            return False
        city.update_temperature(new_temp, unit)
        self._repo.save()
        return True
    def delete_city(self, city_name: str) -> bool:
        deleted = self._repo.delete_city(city_name)
        if deleted:
            self._repo.save()
        return deleted
    def search(self, query: str) -> dict:
        return self._repo.search_cities(query)