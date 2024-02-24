from aiogram.fsm.state import StatesGroup, State



class DeleteCommon(StatesGroup):
    waiting_for_delete_start = State()
