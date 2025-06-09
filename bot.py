import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import sheets, config, json

# Настроим logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

with open('questions.json', encoding='utf-8') as f:
    QUESTIONS = json.load(f)

# FSM-состояния
class ReportFSM(StatesGroup):
    waiting_for_answers = State()

# Старт и кнопка отчёта
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Отправить отчёт", callback_data="report_start")
    await message.answer("Привет! Нажми, чтобы отправить отчёт.", reply_markup=kb.as_markup())

# Обработка кнопки
@dp.callback_query(StateFilter(None), F.data == "report_start")
async def start_report(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(ReportFSM.waiting_for_answers)
    await state.update_data(answers={}, q_index=0)
    await ask_next_question(call.message, state)

async def ask_next_question(message, state):
    data = await state.get_data()
    q_index = data['q_index']
    if q_index < len(QUESTIONS):
        q = QUESTIONS[q_index]['text']
        await message.answer(q)
    else:
        # Всё собрано, пишем в таблицу
        user = message.from_user
        answers = data['answers']
        sheets.save_report(user.id, user.username, answers)
        await message.answer("Спасибо, отчёт принят! ✨\n\nP.S. Итог за месяц: {}₽".format(sheets.get_stats()))
        await state.clear()

@dp.message(ReportFSM.waiting_for_answers)
async def process_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    q_index = data['q_index']
    answers = data['answers']
    answers[QUESTIONS[q_index]['id']] = message.text
    await state.update_data(answers=answers, q_index=q_index+1)
    await ask_next_question(message, state)

# Рассылка по расписанию (раз в месяц)
async def monthly_report_reminder():
    users = sheets.sheet.col_values(2)[1:]  # Все user_id из таблицы, кроме заголовка
    for uid in set(users):
        try:
            kb = InlineKeyboardBuilder()
            kb.button(text="Отправить отчёт", callback_data="report_start")
            await bot.send_message(int(uid), "Напоминание! Пора отправить отчёт 📝", reply_markup=kb.as_markup())
        except Exception as e:
            logging.warning(f"Не могу отправить {uid}: {e}")

async def scheduler_start():
    sched = AsyncIOScheduler(timezone="Europe/Moscow")
    sched.add_job(monthly_report_reminder, "cron", day=1, hour=10, minute=0)
    sched.start()

async def main():
    await scheduler_start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
