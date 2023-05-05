# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from ContentBusinessProcesses import ContentBusinessProcessesFactory, CreateLetterParams, ContentBusinessProcessNames, UpdateLetterParams, DeleteLetterParams
from MealCreationBusinessProcesses import MealBusinessProcessesFactory, MealBusinessProcessNames, MealParams, Ingredient

# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------

# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------

# ------------------------------------------------------------------- Program -------------------------------------------------------------------------

if __name__ == "__main__":
    onion = Ingredient(name="onion", flavor="tasty", calories=3.2)
    garlic = Ingredient(name="garlic", flavor="yummy", calories=0)
    chicken = Ingredient(name="chicken", flavor="wow", calories=26.1)
    teriyaki_sauce = Ingredient(name="teriyaki_sauce", flavor="sweet", calories=1.2)
    meal_params = MealParams(
        ingredients=[onion, garlic, chicken, teriyaki_sauce]
    )
    meal_response = MealBusinessProcessesFactory().get_business_process(MealBusinessProcessNames.CREATE_CHICKEN_TERIYAKI)().run(meal_params)
    print(meal_response)

    create_letter_params = CreateLetterParams(author_name="Jeff", title="Love letter for my wife", body="I love pizza...")
    create_letter_response = ContentBusinessProcessesFactory().get_business_process(ContentBusinessProcessNames.CREATE_LETTER)().run(create_letter_params)
    print(create_letter_response)
    update_letter_params = UpdateLetterParams(letter_uuid="1234", author_name="Jeff", title="Love letter for my wife", body="I love you, wife...")
    update_letter_response = ContentBusinessProcessesFactory().get_business_process(ContentBusinessProcessNames.UPDATE_LETTER)().run(update_letter_params)
    print(update_letter_response)
    delete_letter_params = DeleteLetterParams(letter_uuid="1234")
    delete_letter_response = ContentBusinessProcessesFactory().get_business_process(ContentBusinessProcessNames.DELETE_LETTER)().run(delete_letter_params)
    print(delete_letter_response)
