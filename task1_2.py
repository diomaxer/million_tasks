import re
import webbrowser

short_links_db = {}
new_link = 0


async def read_body(receive):
    """
    Read and return the entire body from an incoming ASGI message.
    """
    body = b''
    more_body = True

    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)

    return body


async def save_url(body):
    global new_link
    # Получаем чистую ссылку на сайт
    clear_body = re.search(r'https?:.+', body.decode('utf-8')).group(0)
    # Проверка на слеш в конце, чтобы не повторяться в базе, все приводим к общему виду
    if clear_body[-2] == '/':
        clear_body = clear_body[0: -1]
    else:
        clear_body = clear_body[0: -1] + '/'
    # Проверяем есть ли url в базе, если нет записываем
    try:
        # Пытаемся вернуть ссылку если она имеется в базе
        return str.encode(f'Short URL: http://localhost:8000/{short_links_db[clear_body]}')
    except KeyError:
        # Если ссылки в базе нет, создаем и возвращаме её
        short_links_db[clear_body] = new_link
        new_link += 1
        return str.encode(f'Short URL: http://localhost:8000/{short_links_db[clear_body]}')


async def app(scope, receive, send):
    """
    Echo the request body back in an HTTP response.
    """
    # Если запорс пришел без path: зыписываем в базу url, если пришел c path перенаправялем на юрл из базы
    if scope['path'] not in ('/', '/favicon.ico'):
        link_id = int(scope['path'][1:])
        # Получаем нужный нам url по его id в базу. Преобразуем ключи в лист и возьмем нужный нам по id.
        new_url = list(short_links_db.keys())[link_id]
        webbrowser.open(new_url)

    body = await read_body(receive)
    # Если есть тело запроса то сохраняем url
    if body:
        body = await save_url(body)

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ]
    })
    await send({
        ''
        'type': 'http.response.body',
        'body': body,
    })

