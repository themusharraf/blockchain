from aiogram import Router, F
from aiogram.types import Message
from models.user import Transaction
from aiogram.fsm.context import FSMContext
from services.notif import send_notification
from services.user import get_user, check_address
from state.tran import TranState

router = Router()


# @router.message(F.text == "Send Coin")
# async def send_coin(message: Message):
#     await message.answer("Referral address")
#     user = await get_user(message.from_user.id)
#     @router.message()
#     async def get_addr(msg: Message):
#         address = msg.text
#         addr = await check_address(address)
#         if addr:
#             @router.message()
#             async def get_amount(msgs: Message):
#                 amount = msgs.text
#                 transaction = await Transaction.create_transaction(sender=user, receiver=addr, amount=amount, note="Gift")
#         else:
#             await message.answer("Wrong address")
#

@router.message(F.text == "Send Coin")
async def send_coin(message: Message, state: FSMContext):
    await message.answer("Referral address:")
    await state.set_state(TranState.token)


@router.message(TranState.token)
async def get_address(message: Message, state: FSMContext):
    address = message.text
    addr = await check_address(address)
    if addr:
        await state.update_data(address=address)
        await message.answer("Enter the amount to send:")
        await state.set_state(TranState.amount)
    else:
        await message.answer("Noto‘g‘ri referral address. Qayta kiriting.")  # noqa


@router.message(TranState.amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer("Miqdorni kritish da xatolik bor. Qayta kiriting.")  # noqa
        await state.update_data(amount=amount)
        await message.answer("Tranzaktsiya uchun izoh qo‘shing (ixtiyoriy):")  # noqa
        await state.set_state(TranState.note)
    except ValueError:
        await message.answer("Noto‘g‘ri miqdor. Faqat son kiriting.")  # noqa


@router.message(TranState.note)
async def get_note(message: Message, state: FSMContext):
    note = message.text
    data = await state.get_data()
    address = data['address']
    addr = await check_address(address)
    amount: int = int(data['amount'])
    user = await get_user(message.from_user.id)

    transaction = await Transaction.create_transaction(
        sender=user,
        receiver=addr,
        amount=amount,
        note=note or "Gift"
    )

    await message.answer(
        f"Transaction successful!\n\n"
        f"📤 From:  {user.referral_code}\n"
        f"📍 To:    {address}\n"
        f"🌕 Coin:  {amount}\n"
        f"✏️ Note:  {note or "Gift"}"
    )
    caption = f""" 
    🎉✨ Sizga yangi tangalar keldi! ✨🎉

    💰 Yuborilgan tanga miqdori: 🌕 {amount} 
    🤝 Yuboruvchi: 📤 {user.referral_code} 

    💡 Tangalaringizni to'plang va imkoniyatlardan foydalaning! 🚀
    """
    img_url = "https://unsplash.com/photos/three-gold-bitcoins-sitting-on-top-of-a-wooden-table-qRRv6nQyNmk"
    await send_notification(addr.tg_id, img_url, caption)
    await state.clear()
