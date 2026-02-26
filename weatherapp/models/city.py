from dataclasses import dataclass, field
from typing import List

@dataclass
class City:
    name :str
    current_temperature: int
    unit :str
    last_7_days_temperatures: List[float]
    lattitude: float
    longitude: float
    timezone: str
    @classmethod
    def from_dict(cls,name:str, data:dict) -> 'City':
        lat,log,tz=data['coordinates_and_timezone']
        return cls(
            name=name,
            current_temperature=data['current_temperature'],
            unit=data['unit'].upper(),
            last_7_days_temperatures=list(data.get("last_7_days_history",[])),
            lattitude=lat,
            longitude=log,
            timezone=tz,
        )
    def to_dict(self) -> dict:
        return {
            "current_temperature": self.current_temperature,
            "unit": self.unit,
            "last_7_days_temperatures": self.last_7_days_temperatures,
            "coordinates_and_timezone": (self.lattitude,self.longitude,self.timezone)
        }
    def temperature_in(self, target_unit:str) ->float:
        if self.unit == target_unit.upper():
            return self.current_temperature
        elif self.unit == "C" and target_unit.upper() == "F":
            return self.current_temperature * 1.8 + 32
        elif self.unit == "F" and target_unit.upper() == "C":
            return (self.current_temperature - 32) / 1.8
        else:
            raise ValueError(f"Unsupported unit conversion from {self.unit} to {target_unit}")
    def average_temperature(self)-> float:
        if not self.last_7_days_temperatures:
            return self.current_temperature
        return round(sum(self.last_7_days_temperatures) / len(self.last_7_days_temperatures),1)
    def temperature_range(self) -> float:
        if len(self.last_7_days_temperatures) <2:
            return 0.0
        return max(self.last_7_days_temperatures) - min(self.last_7_days_temperatures)
    def is_valid_temperature(self) -> bool:
        if self.unit == "C":
            return -90 <= self.current_temperature <= 60
        elif self.unit == "F":
            return -130 <= self.current_temperature <= 140
        else:
            raise ValueError(f"Unsupported unit: {self.unit}")
    def is_valid_coordinates(self) -> bool:
        return -90 <= self.lattitude <= 90 and -180 <= self.longitude <= 180  
    def update_temperature(self, new_temperature: int, unit: str) -> None:
        if unit.upper() != self.unit:
            raise ValueError(f"Unit mismatch: expected {self.unit}, got {unit}")
        self.current_temperature = new_temperature
        self.last_7_days_temperatures.append(new_temperature)
        if len(self.last_7_days_temperatures) > 7:
            self.last_7_days_temperatures.pop(0)
    def display_card(self,preferred_unit:str | None= None )->None:
        temp = self.current_temperature
        unit = self.unit
        if preferred_unit and preferred_unit.upper() != self.unit:
            temp = self.temperature_in(preferred_unit)
            unit = preferred_unit.upper()
        print(f"City: {self.name}")
        print(f"Current Temperature: {temp}°{unit}")
        print(f"Average Temperature (last 7 days): {self.average_temperature()}°{self.unit}")
        print(f"Temperature Range (last 7 days): {self.temperature_range()}°{self.unit}")
        print(f"Coordinates: ({self.lattitude}, {self.longitude})")
        print(f"Timezone: {self.timezone}")