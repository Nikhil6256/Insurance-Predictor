from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city import tier_1_cities, tier_2_cities

class UserInput(BaseModel):
    age: Annotated[int, Field( ... , gt=0, lt=120, description='Age of the user') ]
    weight: Annotated[float, Field( ... , gt=0, description='Weight of the user') ]
    height: Annotated[float, Field( ... , gt=0, lt=2.5, description='Height of the user') ]
    income_lpa: Annotated[float, Field( ... , gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field( ... , description='Is user a smoker') ]
    city: Annotated[str, Field( ... ,description='The city that the user belongs to')]
    occupation: Annotated[Literal['government_job', 'private_job', 'business_owner', 'engineer',
        'doctor', 'retired', 'freelancer', 'self_employed', 'student',
        'teacher'], Field( ... , description='occupation of the user')]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height ** 2)

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip() .title()
        return v
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "High"
        elif self.smoker or self.bmi > 27:
            return "Medium"
        return "Low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "Young"
        elif self.age < 45:
            return "Adult"
        elif self.age < 60:
            return "Middle-Aged"
        return "Senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        city_name = self.city.strip().title()
        if city_name in tier_1_cities:
            return 1
        elif city_name in tier_2_cities:
            return 2
        else:
            return 3