import asyncio
from telegram import Bot

async def main():
      # Ganti dengan token bot Anda
      bot_token = "5989229755:AAG1wMh1a-3vlWYRJkll-mq3JR3CM5RMfro"
      
      # Ganti dengan ID grup target
      group_id = -917907649
      
      # Membuat objek bot
      bot = Bot(token=bot_token)
      
      # Mengirim pesan ke grup
      await bot.send_message(chat_id=group_id, text="Halo dari bot!")
      
      print("Pesan terkirim!")

# Menjalankan event loop asyncio
if __name__ == "__main__":
    asyncio.run(main())
