from dataclasses import dataclass, field
from typing import List
from datetime import datetime
@dataclass
class User:
    name: str
    birth_year: int
    birth_month: int
    birth_day: int
    preferred_temperature_unit: str
    @classmethod
    def from_dict(cls, name: str, data: dict) -> 'User':
        bd = data['birthday']
        return cls(
            name=name,
            birth_year=bd['year'],
            birth_month=bd['month'],
            birth_day=bd['day'],
            preferred_temperature_unit=data.get("preferred_temperature_unit","C").upper()
        )
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "birthday": {
                "year": self.birth_year,
                "month": self.birth_month,
                "day": self.birth_day
            },
            "preferred_temperature_unit": self.preferred_temperature_unit,
        }
    @property
    def age(self) -> int:
        today = datetime.today()
        age = today.year - self.birth_year
        if (today.month, today.day) < (self.birth_month, self.birth_day):
            age-= 1
        return age
    @property
    def age_group(self) -> str:
        age = self.age
        if age < 18:
            return "child"
        elif 18 <= age < 65:
            return "adult"
        else:
            return "senior"
    def display(self)->None:
        print(f"Name: {self.name}")
        print(f"Age: {self.age} ({self.age_group})")
        print(f"Preferred Temperature Unit: {self.preferred_temperature_unit}")
        