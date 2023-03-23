import asyncio
from aiogram.utils import executor
from bs4 import BeautifulSoup
import requests
from cost import *

url = 'https://www.tesmanian.com/blogs/tesmanian-blog?page='


def add_bd(data):
    cur.executemany("INSERT INTO article VALUES(?, ?)", data)
    con.commit()


@dp.message_handler(commands=['start'])
async def send_message_to_channel(message: aiogram.types.Message):
    n1, n2 = 0, 0
    while True:
        response = requests.get(f"""{url}{n1}""")
        html = response.content
        # Створюємо об'єкт BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        i = soup.find_all('span', class_='pagination__current')
        for n in i:
            n1 = int(n.text.strip()[0])
            n2 = int(n.text.strip()[-3::])
            articles = soup.find_all('p', class_='h3')
            for article in articles:
                title = article.text.strip()  # Заголовок статті
                link = f"""https://www.tesmanian.com/{article.a['href']}"""  # Посилання на статтю
                name = cur.execute("SELECT Назва FROM article WHERE Назва = ?", (title,)).fetchone()
                data = [
                    (
                        title, link
                    )
                ]

                try:
                    if title != name[0]:
                        add_bd(data)
                        message = f"""Назва статі - {title}\n Силка: {link}"""
                        await bot.send_message(chat_id=CHANNEL_ID, text=message)
                        await asyncio.sleep(15)
                except TypeError:
                    add_bd(data)
                    message = f"""Назва статі - {title}\n Силка: {link}"""
                    await bot.send_message(chat_id=CHANNEL_ID, text=message)
                    await asyncio.sleep(15)
            n1 += 1 if n1 < n2 else n1 == 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
