import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.upload import VkUpload
import requests
import config

token = config.token
group_id = config.group_id

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
upload = VkUpload(vk)
longpoll = VkBotLongPoll(vk_session, group_id)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        message = event.obj.message
        user_id = message['from_id']
        text = message.get('text', '')
        attachments = message.get('attachments', [])
        subscribers = vk.groups.getMembers(group_id = group_id)['items']

        # Проверяем, что сообщение содержит хотя бы одно изображение
        images = [attachment for attachment in attachments if attachment['type'] == 'photo']
        if images:
            if len(images) == 1:
                for image in images:
                    # Получаем URL изображения
                    photo_url = image['photo']['sizes'][-1]['url']
                    
                    response = requests.get(photo_url)
                    if response.status_code == 200:
                        # Открываем файл в режиме записи в двоичном формате
                        with open('photo_archive\\res.png', 'wb') as file:
                            # Записываем содержимое ответа в файл
                            file.write(response.content)
                        print('Изображение успешно сохранено.')
                    else:
                        print('Ошибка при загрузке изображения.')

                    # Получаем список подписчиков группы
                    subscribers = vk.groups.getMembers(group_id = group_id)['items']
                    attachments = []

                    # Загрузка изображения на сервер VK
                    upload = vk_api.VkUpload(vk_session)
                    photo = upload.photo_messages('photo_archive\\res.png')
                    
                    # Добавление фото во вложение сообщения
                    attachments.append(f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}')

                    while True:
                        if user_id in config.list_admin_id:
                            answer = input("Выполнить отправку сообщений? (Да/Нет)")
                            if answer == 'Да':
                                # Ретранслируем сообщение с изображением всем подписчикам
                                for subscriber_id in subscribers:
                                    if subscriber_id != user_id:
                                        try:
                                            # Отправка сообщения
                                            vk.messages.send(
                                                random_id = vk_api.utils.get_random_id(),
                                                user_id=subscriber_id,
                                                attachment=','.join(attachments),
                                                message = text if text else ' '
                                            )
                                        except: 
                                            pass
                                break
                            elif answer == 'Нет':
                                break
            elif len(images) > 1:
                attachments = []
                for image in images:
                    # Получаем URL изображения
                    photo_url = image['photo']['sizes'][-1]['url']
                    
                    response = requests.get(photo_url)
                    if response.status_code == 200:
                        # Открываем файл в режиме записи в двоичном формате
                        with open('photo_archive\\res.png', 'wb') as file:
                            # Записываем содержимое ответа в файл
                            file.write(response.content)
                        print('Изображение успешно сохранено.')
                    else:
                        print('Ошибка при загрузке изображения.')

                    # Получаем список подписчиков группы
                    subscribers = vk.groups.getMembers(group_id = group_id)['items']

                    # Загрузка изображения на сервер VK
                    upload = vk_api.VkUpload(vk_session)
                    photo = upload.photo_messages('photo_archive\\res.png')
                    
                    # Добавление фото во вложение сообщения
                    attachments.append(f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}')

                while True:
                    if user_id in config.list_admin_id:
                        answer = input("Выполнить отправку сообщений? (Да/Нет)")
                        if answer == 'Да':
                            # Ретранслируем сообщение с изображением всем подписчикам
                            for subscriber_id in subscribers:
                                if subscriber_id != user_id:
                                    try:
                                        # Отправка сообщения
                                        vk.messages.send(
                                            random_id = vk_api.utils.get_random_id(),
                                            user_id=subscriber_id,
                                            attachment=attachments,
                                            message = text if text else ' '
                                        )
                                    except: 
                                        pass
                            break
                        elif answer == 'Нет':
                            break
        else:
            while True:
                if user_id in config.list_admin_id:
                    answer = input("Выполнить отправку сообщений? (Да/Нет)")
                    if answer == 'Да':
                        # Ретранслируем сообщение всем подписчикам
                        for subscriber_id in subscribers:
                            if subscriber_id != user_id:
                                try:
                                    vk.messages.send(
                                        user_id=subscriber_id,
                                        random_id=get_random_id(),
                                        message=text
                                    )
                                except:
                                    pass
                        break
                    elif answer == 'Нет':
                        break                   