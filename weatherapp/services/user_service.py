from models.user import User
from repository import DataRepository
class UserService:
    def __init__(self, repo: DataRepository):
        self._repo= repo
    def get_user(self) -> User  | None :
        return self._repo.user
    def update_user(self, name: str, year: int, month: int, day: int, unit: str) -> bool:
        if unit.upper() not in ("C", "F"):
            return False
        try:
            from datetime import datetime
            datetime(year, month, day)
        except ValueError:
            return False
        user = self._repo.user
        if user is None:
            return False
        if name:
            user.name = name
        user.birth_year = year
        user.birth_month = month
        user.birth_day = day
        user.preferred_temperature_unit = unit.upper()
        self._repo.save()
        return True
            