import asyncio
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

# --- НАСТРОЙКИ ---
BOT_TOKEN = "7118251316:AAGYccJFGhszenxmyeXM4mUDIaD_lACcgnU"
ADMIN_USERNAME = "@Syr_bu"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- БАЗА ДАННЫХ МАТРАСОВ И ЦЕН (Р ПМР) ---
MATTRESS_PRICES = {
    "ОРИОН": {
        "70x200": 1700,
        "80x200": 1900,
        "90x200": 2100,
        "100x200": 2300,
        "110x200": 2400,
        "120x200": 2400,
        "130x200": 2800,
        "140x200": 2800,
        "150x200": 3150,
        "160x200": 3150,
        "170x200": 3550,
        "180x200": 3550,
        "190x200": 3950,
        "200x200": 3950,
    },
    "СИРИУС": {
        "70x200": 1850,
        "80x200": 2100,
        "90x200": 2300,
        "100x200": 2550,
        "110x200": 2650,
        "120x200": 2650,
        "130x200": 3100,
        "140x200": 3100,
        "150x200": 3550,
        "160x200": 3550,
        "170x200": 4000,
        "180x200": 4000,
        "190x200": 4450,
        "200x200": 4450,
    },
    "ПОЛАРИС": {
        "70x200": 2200,
        "80x200": 2450,
        "90x200": 2700,
        "100x200": 2950,
        "110x200": 3200,
        "120x200": 3200,
        "130x200": 3750,
        "140x200": 3750,
        "150x200": 4250,
        "160x200": 4250,
        "170x200": 4800,
        "180x200": 4800,
        "190x200": 5300,
        "200x200": 5300,
    },
    "ЭРГО": {
        "70x200": 2250,
        "80x200": 2500,
        "90x200": 2750,
        "100x200": 3000,
        "110x200": 3250,
        "120x200": 3250,
        "130x200": 3800,
        "140x200": 3800,
        "150x200": 4350,
        "160x200": 4350,
        "170x200": 4900,
        "180x200": 4900,
        "190x200": 5450,
        "200x200": 5450,
    },
    "СОФТ ⭐": {
        "70x200": 2400,
        "80x200": 2700,
        "90x200": 2950,
        "100x200": 3250,
        "110x200": 3550,
        "120x200": 3550,
        "130x200": 4150,
        "140x200": 4150,
        "150x200": 4700,
        "160x200": 4700,
        "170x200": 5300,
        "180x200": 5300,
        "190x200": 5900,
        "200x200": 5900,
    },
    "КОМФОРТ": {
        "70x200": 2550,
        "80x200": 2850,
        "90x200": 3200,
        "100x200": 3500,
        "110x200": 3850,
        "120x200": 3850,
        "130x200": 4450,
        "140x200": 4450,
        "150x200": 5100,
        "160x200": 5100,
        "170x200": 5750,
        "180x200": 5750,
        "190x200": 6400,
        "200x200": 6400,
    },
    "ОРТО": {
        "70x200": 2750,
        "80x200": 3050,
        "90x200": 3400,
        "100x200": 3800,
        "110x200": 4150,
        "120x200": 4150,
        "130x200": 4800,
        "140x200": 4800,
        "150x200": 5500,
        "160x200": 5500,
        "170x200": 6200,
        "180x200": 6200,
        "190x200": 6900,
        "200x200": 6900,
    },
    "ДУО": {
        "70x200": 3000,
        "80x200": 3350,
        "90x200": 3750,
        "100x200": 4200,
        "110x200": 4550,
        "120x200": 4550,
        "130x200": 5300,
        "140x200": 5300,
        "150x200": 6100,
        "160x200": 6100,
        "170x200": 6850,
        "180x200": 6850,
        "190x200": 7600,
        "200x200": 7600,
    },
    "ВЕЛЬВЕТ": {
        "70x200": 3100,
        "80x200": 3450,
        "90x200": 3850,
        "100x200": 4300,
        "110x200": 4700,
        "120x200": 4700,
        "130x200": 5500,
        "140x200": 5500,
        "150x200": 6300,
        "160x200": 6300,
        "170x200": 7050,
        "180x200": 7050,
        "190x200": 7850,
        "200x200": 7850,
    },
    "РОЯЛ": {
        "70x200": 3100,
        "80x200": 3450,
        "90x200": 3850,
        "100x200": 4300,
        "110x200": 4700,
        "120x200": 4700,
        "130x200": 5500,
        "140x200": 5500,
        "150x200": 6300,
        "160x200": 6300,
        "170x200": 7050,
        "180x200": 7050,
        "190x200": 7850,
        "200x200": 7850,
    },
    "АИР": {
        "70x200": 3500,
        "80x200": 3950,
        "90x200": 4400,
        "100x200": 5000,
        "110x200": 5450,
        "120x200": 5450,
        "130x200": 6350,
        "140x200": 6350,
        "150x200": 7250,
        "160x200": 7250,
        "170x200": 8150,
        "180x200": 8150,
        "190x200": 9050,
        "200x200": 9050,
    },
    "ГРАНД": {
        "70x200": 3750,
        "80x200": 4200,
        "90x200": 4700,
        "100x200": 5350,
        "110x200": 5850,
        "120x200": 5850,
        "130x200": 6800,
        "140x200": 6800,
        "150x200": 7800,
        "160x200": 7800,
        "170x200": 8750,
        "180x200": 8750,
        "190x200": 9750,
        "200x200": 9750,
    },
    "МЕМОРИ ⭐": {
        "70x200": 5050,
        "80x200": 5700,
        "90x200": 6350,
        "100x200": 7350,
        "110x200": 8050,
        "120x200": 8050,
        "130x200": 9400,
        "140x200": 9400,
        "150x200": 10700,
        "160x200": 10700,
        "170x200": 12050,
        "180x200": 12050,
        "190x200": 13400,
        "200x200": 13400,
    },
    "ЛАТЕКС": {
        "70x200": 6950,
        "80x200": 6950,
        "90x200": 7750,
        "100x200": 9050,
        "110x200": 11550,
        "120x200": 11550,
        "130x200": 11550,
        "140x200": 11550,
        "150x200": 13200,
        "160x200": 13200,
        "170x200": 14850,
        "180x200": 14850,
        "190x200": 16450,
        "200x200": 16450,
    },
    "НАТУРЕ": {
        "70x200": 7450,
        "80x200": 7450,
        "90x200": 8350,
        "100x200": 9800,
        "110x200": 12500,
        "120x200": 12500,
        "130x200": 12500,
        "140x200": 12500,
        "150x200": 14250,
        "160x200": 14250,
        "170x200": 16050,
        "180x200": 16050,
        "190x200": 17850,
        "200x200": 17850,
    },
}

# Составы матрасов
MATTRESS_SPECS = {
    "ОРИОН": "🛏 **ОРИОН**\n• Трикотаж, жаккард стёганный\n• Пенополиуретан 12 мм\n• Термовойлок\n• Пружинный блок «Бонель»\n• Габаритная высота: 21-22 см",
    "СИРИУС": "🛏 **СИРИУС**\n• Трикотаж, жаккард стёганный\n• Пенополиуретан 20 мм\n• Термовойлок\n• Пружинный блок «Бонель»\n• Габаритная высота: 21-22 см",
    "ПОЛАРИС": "🛏 **ПОЛАРИС**\n• Трикотаж глубокой стёжки\n• Пенополиуретан 20 мм\n• Термовойлок / Спанбонд\n• Блок независимых пружин\n• Премиальный велюровый бурлет",
    "ЭРГО": "🛏 **ЭРГО**\n• Эргономичный состав с усиленной поддержкой\n• Блок независимых пружин\n• Анатомический пенополиуретан",
    "СОФТ ⭐": "🛏 **СОФТ (Рекомендуемая модель ⭐)**\n• Трикотаж глубокой стёжки\n• Пенополиуретан 20 мм\n• Спанбонд\n• Блок независимых пружин (TFK)\n• Премиальный велюровый бурлет\n• Габаритная высота: 21-22 см",
    "КОМФОРТ": "🛏 **КОМФОРТ**\n• Повышенный комфорт и мягкость\n• Блок независимых пружин\n• Термовойлок и анатомическая пена",
    "ОРТО": "🛏 **ОРТО**\n• Ортопедическая жесткость\n• Усиленный пружинный блок\n• Плотный наполнитель для идеальной поддержки спины",
    "ДУО": "🛏 **ДУО**\n• Двусторонняя жесткость (Зима/Лето)\n• Независимые пружины\n• Комбинированные наполнители",
    "ВЕЛЬВЕТ": "🛏 **ВЕЛЬВЕТ**\n• Люксовый трикотаж с велюровой отделкой\n• Премиальная анатомическая система",
    "РОЯЛ": "🛏 **РОЯЛ**\n• Премиум класс\n• Анатомическая поддержка и высочайший комфорт",
    "АИР": "🛏 **АИР**\n• Дышащие наполнители с микроциркуляцией воздуха\n• Блок независимых пружин",
    "ГРАНД": "🛏 **ГРАНД**\n• Высокий премиальный матрас\n• Усиленный каркас и максимальная нагрузка",
    "МЕМОРИ ⭐": "🛏 **МЕМОРИ (Рекомендуемая модель ⭐)**\n• Инновационная пена Memory Foam (с эффектом памяти)\n• Идеально повторяет контуры тела\n• Блок независимых пружин\n• Абсолютный комфорт для сна",
    "ЛАТЕКС": "🛏 **ЛАТЕКС**\n• Натуральный латекс\n• Максимальная эластичность и долговечность",
    "НАТУРЕ": "🛏 **НАТУРЕ**\n• Экологичные натуральные наполнители (кокосовая койра / натуральный латекс)\n• Премиальное качество",
}


# --- FSM СОСТОЯНИЯ ---
class OrderState(StatesGroup):
  choosing_model = State()
  choosing_size = State()
  choosing_delivery = State()
  entering_name = State()
  entering_phone = State()


# --- КЛАВИАТУРЫ ---
def get_models_keyboard():
  builder = InlineKeyboardMarkup(inline_keyboard=[])
  models = list(MATTRESS_PRICES.keys())
  for i in range(0, len(models), 2):
    row = [
        InlineKeyboardButton(
            text=models[i], callback_data=f"model_{models[i]}"
        )
    ]
    if i + 1 < len(models):
      row.append(
          InlineKeyboardButton(
              text=models[i + 1], callback_data=f"model_{models[i+1]}"
          )
      )
    builder.inline_keyboard.append(row)
  return builder


def get_sizes_keyboard(model_name):
  sizes = list(MATTRESS_PRICES[model_name].keys())
  builder = InlineKeyboardMarkup(inline_keyboard=[])
  for i in range(0, len(sizes), 3):
    row = []
    for s in sizes[i : i + 3]:
      price = MATTRESS_PRICES[model_name][s]
      row.append(
          InlineKeyboardButton(
              text=f"{s} ({price}Р)", callback_data=f"size_{s}"
          )
      )
    builder.inline_keyboard.append(row)
  builder.inline_keyboard.append([
      InlineKeyboardButton(
          text="⬅️ Назад к моделям", callback_data="back_to_models"
      )
  ])
  return builder


def get_delivery_keyboard():
  return InlineKeyboardMarkup(
      inline_keyboard=[
          [
              InlineKeyboardButton(
                  text="Доставка на дом", callback_data="deliv_yes"
              )
          ],
          [
              InlineKeyboardButton(
                  text="Самовывоз", callback_data="deliv_no"
              )
          ],
          [
              InlineKeyboardButton(
                  text="⬅️ Назад", callback_data="back_to_models"
              )
          ],
      ]
  )


# --- ХЕНДЛЕРЫ ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
  await state.clear()
  await message.answer(
      "👋 Здравствуйте! Добро пожаловать в каталог матрасов «Сладкий"
      " сон».\n\nВыберите интересующую модель матраса, чтобы узнать состав и"
      " стоимость:",
      reply_markup=get_models_keyboard(),
  )


@dp.callback_query(F.data == "back_to_models")
async def back_to_models(callback: types.CallbackQuery, state: FSMContext):
  await state.clear()
  await callback.message.edit_text(
      "Выберите модель матраса:", reply_markup=get_models_keyboard()
  )


@dp.callback_query(F.data.startswith("model_"))
async def select_model(callback: types.CallbackQuery, state: FSMContext):
  model_name = callback.data.replace("model_", "")
  await state.update_data(model=model_name)

  spec_text = MATTRESS_SPECS.get(model_name, f"Модель: {model_name}")

  await callback.message.edit_text(
      f"{spec_text}\n\n👇 **Выберите нужный размер:**",
      reply_markup=get_sizes_keyboard(model_name),
      parse_mode="Markdown",
  )
  await state.set_state(OrderState.choosing_size)


@dp.callback_query(OrderState.choosing_size, F.data.startswith("size_"))
async def select_size(callback: types.CallbackQuery, state: FSMContext):
  size = callback.data.replace("size_", "")
  data = await state.get_data()
  model_name = data.get("model")

  price = MATTRESS_PRICES[model_name][size]
  await state.update_data(size=size, price=price)

  width = int(size.split("x")[0])
  deliv_info = (
      "200 Р/матрас"
      if width <= 100
      else "ориентировочно 60 Р/матрас (при сборной загрузке)"
  )

  await callback.message.edit_text(
      f"📏 **Модель:** {model_name}\n📐 **Размер:** {size}\n💰 **Стоимость:**"
      f" {price} Р ПМР\n🚚 **Ориентир доставки:** {deliv_info}\n\nНужна ли вам"
      " доставка?",
      reply_markup=get_delivery_keyboard(),
      parse_mode="Markdown",
  )
  await state.set_state(OrderState.choosing_delivery)


@dp.callback_query(OrderState.choosing_delivery, F.data.startswith("deliv_"))
async def select_delivery(callback: types.CallbackQuery, state: FSMContext):
  deliv_type = "С доставкой" if callback.data == "deliv_yes" else "Самовывоз"
  await state.update_data(delivery=deliv_type)

  await callback.message.answer(
      "📝 Отлично! Для оформления заявки, напишите ваше **Имя**:",
      reply_markup=ReplyKeyboardRemove(),
  )
  await state.set_state(OrderState.entering_name)


@dp.message(OrderState.entering_name)
async def enter_name(message: types.Message, state: FSMContext):
  await state.update_data(name=message.text)

  phone_button = KeyboardButton(
      text="📱 Поделиться номером телефона", request_contact=True
  )
  keyboard = ReplyKeyboardMarkup(
      keyboard=[[phone_button]], resize_keyboard=True, one_time_keyboard=True
  )

  await message.answer(
      "Спасибо! Теперь отправьте ваш **номер телефона** (нажмите кнопку ниже"
      " или введите вручную):",
      reply_markup=keyboard,
  )
  await state.set_state(OrderState.entering_phone)


@dp.message(OrderState.entering_phone)
async def enter_phone(message: types.Message, state: FSMContext):
  phone = message.contact.phone_number if message.contact else message.text
  data = await state.get_data()

  model = data.get("model")
  size = data.get("size")
  price = data.get("price")
  delivery = data.get("delivery")
  name = data.get("name")

  user_tg = (
      f"@{message.from_user.username}"
      if message.from_user.username
      else "нет юзернейма"
  )

  await message.answer(
      f"✅ **Спасибо за заказ, {name}!**\n\nВаша заявка принята:\n• Модель:"
      f" **{model}**\n• Размер: **{size}**\n• Стоимость: **{price} Р ПМР**\n•"
      f" Вариант: **{delivery}**\n\nМы свяжемся с вами в ближайшее время для"
      " уточнения деталей!",
      reply_markup=ReplyKeyboardRemove(),
      parse_mode="Markdown",
  )

  print(
      f"--- НОВАЯ ЗАЯВКА ---\nИмя: {name}\nТел: {phone}\nTG: {user_tg}\nТовар:"
      f" {model} {size} ({price} Р ПМР)\nДоставка: {delivery}"
  )
  await state.clear()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
  asyncio.run(main())
