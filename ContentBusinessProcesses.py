# ------------------------------------------------------------------- External Imports ----------------------------------------------------------------
import uuid
from abc import ABC
from typing import Any, Optional
from pydantic import BaseModel

# ------------------------------------------------------------------- Local Imports -------------------------------------------------------------------
from BaseBusinessProcess import BaseBusinessProcess, BaseBusinessProcessesFactory

# ------------------------------------------------------------------- Constants -----------------------------------------------------------------------


class ContentResponses:
    LETTER_CREATED = "Letter created!"
    INVALID_LETTER_PARAMETERS = "Invalid letter parameters..."
    INVALID_LETTER_UUID = "Invalid letter uuid..."
    MISSING_UPDATE_LETTER_PARAMS = "Missing parameters for letter update, please give at least one value to update..."
    LETTER_UPDATED = "Letter updated!"
    LETTER_DELETED = "Letter deleted!"


class ContentBusinessProcessNames:
    CREATE_LETTER = "create_letter"
    UPDATE_LETTER = "update_letter"
    DELETE_LETTER = "delete_letter"


# ------------------------------------------------------------------- Classes -------------------------------------------------------------------------

class CreateLetterParams(BaseModel):
    author_name: str
    title: str
    body: str


class UpdateLetterParams(BaseModel):
    letter_uuid: str
    author_name: Optional[str]
    title: Optional[str]
    body: Optional[str]


class DeleteLetterParams(BaseModel):
    letter_uuid: str


# ------------------------------------------------------------------- BaseBusinessProcesses -----------------------------------------------------------


class ExistingLetterActionBaseBusinessProcess(BaseBusinessProcess, ABC):

    def _check_letter_uuid_validity_and_if_it_exists(self, letter_uuid: str) -> bool:
        if len(letter_uuid) == 0:
            self.response = ContentResponses.INVALID_LETTER_UUID
            return False
        """
        Here you can check if this letter exists in the DB (letter_uuid), if not return an appropriate false response 
        """
        return True


# ------------------------------------------------------------------- BusinessProcesses ---------------------------------------------------------------


class CreateLetterBusinessProcess(BaseBusinessProcess):

    def _verify(self, params: CreateLetterParams) -> bool:
        if len(params.author_name) * len(params.title) * len(params.body) == 0:
            self.response = ContentResponses.INVALID_LETTER_PARAMETERS
            return False
        return True

    def _action(self, params: CreateLetterParams) -> Any:
        letter = params.dict()
        print(f"Creating letter:\n{letter}")
        letter_uuid = uuid.uuid4()
        self.response = ContentResponses.LETTER_CREATED + f" (uuid: {letter_uuid})"
        self.success = True


class UpdateLetterBusinessProcess(ExistingLetterActionBaseBusinessProcess):

    def _verify(self, params: UpdateLetterParams) -> bool:
        letter_uuid_validity = self._check_letter_uuid_validity_and_if_it_exists(params.letter_uuid)
        if not letter_uuid_validity:
            return False
        if params.author_name is None and params.title is None and params.body is None:
            self.response = ContentResponses.MISSING_UPDATE_LETTER_PARAMS
            return False
        return True

    def _action(self, params: UpdateLetterParams) -> Any:
        """
        Here you can update the item in the DB using params.letter_uuid as the filter...
        """
        print(f"Updated letter {params.letter_uuid} with params:\n{params.dict()}")
        self.response = ContentResponses.LETTER_UPDATED
        self.success = True


class DeleteLetterBusinessProcess(ExistingLetterActionBaseBusinessProcess):

    def _verify(self, params: UpdateLetterParams) -> bool:
        letter_uuid_validity = self._check_letter_uuid_validity_and_if_it_exists(params.letter_uuid)
        if not letter_uuid_validity:
            return False
        return True

    def _action(self, params: UpdateLetterParams) -> Any:
        """
        Here you can delete the item in the DB using params.letter_uuid as the filter...
        """
        print(f"Deleted letter {params.letter_uuid}...")
        self.response = ContentResponses.LETTER_DELETED
        self.success = True


# ------------------------------------------------------------------- Factory -------------------------------------------------------------------------


class ContentBusinessProcessesFactory(BaseBusinessProcessesFactory):

    def __init__(self):
        mapping = {
            ContentBusinessProcessNames.CREATE_LETTER: CreateLetterBusinessProcess,
            ContentBusinessProcessNames.UPDATE_LETTER: UpdateLetterBusinessProcess,
            ContentBusinessProcessNames.DELETE_LETTER: DeleteLetterBusinessProcess
        }
        super().__init__(mapping)
