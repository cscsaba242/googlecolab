import telegram as tg
import requests

class Messenger():
  bot = None
  chat_id = None
  logger = None

  def __init__(self, chat_id, telegram_token, logger):
    self.chat_id = chat_id
    self.telegram_token = telegram_token
    self.logger = logger
    bot=tg.Bot(token=self.telegram_token)

  async def send_telegram_image(self):
    with open('./image.jpg', 'rb') as photo:
      await self.bot.send_photo(chat_id=self.chat_id, photo=photo)

  async def send_telegram_log(self):        
          with open('./robo.log', 'rb') as doc:
                  response = await self.bot.send_document(chat_id=self.chat_id, document=doc)

  def get_telegram_info():
    global logger
    global token
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)
    logger.debug(f"{response=}")
