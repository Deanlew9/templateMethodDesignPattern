# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
import abc
from abc import ABC
from typing import Any, List, Optional, Set
from pydantic import BaseModel

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from BaseBusinessProcess import BaseBusinessProcess, BaseBusinessProcessesFactory

# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------


class MealResponses:
    MEAL_WAS_SUCCESSFUL = "Meal was successful!"
    MISSING_INGREDIENT = "Missing ingredient..."
    FOOD_WAS_BURNED_WHILE_COOKING = "Food was burned while cooking..."
    DIDNT_EAT_FOOD_BECAUSE_IT_WAS_NOT_TASTY = "Didn't eat food because it was not tasty..."


class MealBusinessProcessNames:
    CREATE_CHICKEN_TERIYAKI = "create_chicken_teriyaki"


# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------


class Ingredient(BaseModel):
    name: str
    flavor: str
    calories: float


class Meal(BaseModel):
    name: str
    ingredients: List[Ingredient]
    flavors: Set[str]
    calories: float


class MealParams(BaseModel):
    ingredients: List[Ingredient]


# ------------------------------------------------------------------- BaseBusinessProcesses -----------------------------------------------------------


class MealCreationBaseBusinessProcess(BaseBusinessProcess, ABC):

    def _action(self, params: MealParams) -> Any:
        prepared_ingredients = self._prepare(params.ingredients)
        meal = self._cook(prepared_ingredients)
        if self._eat(meal):
            self.response = MealResponses.MEAL_WAS_SUCCESSFUL
            self.success = True
        else:
            self.response = MealResponses.DIDNT_EAT_FOOD_BECAUSE_IT_WAS_NOT_TASTY

    @abc.abstractmethod
    def _prepare(self, ingredients: List[Ingredient]) -> List[Ingredient]:
        raise NotImplementedError

    @abc.abstractmethod
    def _cook(self, prepared_ingredients: List[Ingredient]) -> Optional[Meal]:
        raise NotImplementedError

    @abc.abstractmethod
    def _eat(self, meal: Meal):
        raise NotImplementedError


# ------------------------------------------------------------------- BusinessProcesses ---------------------------------------------------------------


class CreateChickenTeriyakiBusinessProcess(MealCreationBaseBusinessProcess):

    def _verify(self, params: MealParams) -> bool:
        ingredient_names = {ingredient.name for ingredient in params.ingredients}
        required_ingredient_names = {"onion", "garlic", "chicken", "teriyaki_sauce"}
        if ingredient_names != required_ingredient_names:
            self.response = MealResponses.MISSING_INGREDIENT
            return False
        return True

    def _prepare(self, ingredients: List[Ingredient]) -> List[Ingredient]:
        """
        Preparing ingredients...
        """
        return ingredients

    def _cook(self, prepared_ingredients: List[Ingredient]) -> Optional[Meal]:
        flavors = set()
        calories = 0
        for ingredient in prepared_ingredients:
            flavors.add(ingredient.flavor)
            calories += ingredient.calories
        meal = Meal(name="chicken_teriyaki", ingredients=prepared_ingredients, flavors=flavors, calories=calories)
        return meal

    def _eat(self, meal: Meal) -> bool:
        """
        Eating food...
        """
        print(f"Yum... Ican taste: {list(meal.flavors)} !!!")
        return True


# ------------------------------------------------------------------- Factory -------------------------------------------------------------------------


class MealBusinessProcessesFactory(BaseBusinessProcessesFactory):

    def __init__(self):
        mapping = {
            MealBusinessProcessNames.CREATE_CHICKEN_TERIYAKI: CreateChickenTeriyakiBusinessProcess
        }
        super().__init__(mapping)
