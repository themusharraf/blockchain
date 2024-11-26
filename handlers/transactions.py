from aiogram import Router, F
from aiogram.types import Message
from models.user import Transaction
from services.user import get_user,check_address

router = Router()


@router.message(F.text == "Send Coin")
async def send_coin(message: Message):
    await message.answer("Referral address")
    user = await get_user(message.from_user.id)
    @router.message()
    async def get_addr(msg: Message):
        address = msg.text
        addr = await check_address(address)
        if addr:
            @router.message()
            async def get_amount(msgs: Message):
                amount = msgs.text
                transaction = await Transaction.create_transaction(sender=user, receiver=addr, amount=amount, note="Gift")
        else:
            await message.answer("Wrong address")

