import json
import datetime
from collections import Counter

def format_num(num):
    return '{:,}'.format(num).replace(',', ' ')


with open('result.json', 'r') as f:
    data = json.load(f)

chat_name = data['name']
chat_type = data['type']
chat_id = data['id']
messages = data['messages']

if messages[0].get('action') == 'create_group':
    created_at = "момента создания группы"
else:
    created_at = messages[0]['date']
    created_at = datetime.date.fromisoformat(created_at.split('T')[0]).strftime('%d.%m.%Y')

allthe_messages = []
avtory_messages = {}
for message in messages:
    msg_txt = message['text']
    if msg_txt:
        if type(msg_txt) != str:
            for i in msg_txt:
                text = ""
                # print(i)
                if type(i) != str:
                    text += i['text'] + " "
                else:
                    text += i + " "
            allthe_messages.append(text)

        else:
            text = message['text']
            allthe_messages.append(text)
                 
        actor = message.get('from')
        if actor not in avtory_messages:
            avtory_messages[actor] = 1
        else:
            avtory_messages[actor] += 1

words = " ".join(allthe_messages).split()
counted_words = Counter(words).most_common(100)
avtory_messages = {k: v for k, v in sorted(avtory_messages.items(), key=lambda item: item[1])}
unique_messages = set(allthe_messages)

voice = 0
video = 0
for message in messages:
    media_type = message.get('media_type')
    seconds = message.get('duration_seconds')
    if media_type:
        if media_type == 'voice_message':
            if not seconds:
                voice += 1
            else:
                voice += seconds
        if media_type == 'video_message':
            if not seconds:
                video += 1
            else:
                video += seconds
        
invites = 0
link_join = 0
kicked = 0
leaved = 0
for message in messages:
    if message.get('action') == 'invite_members':
        invites += 1
    elif message.get('action') == 'join_group_by_link':
        link_join += 1
    elif message.get('action') == 'remove_members':
        if message.get('actor') == message.get('members')[0]:
            leaved += 1
        else:
            kicked += 1


print(f"Статистика сообщений в чате \"{chat_name}\" начиная с {created_at}\n")  
print(f"— {format_num(len(messages))} сообщений")
print(f"— {format_num(len(unique_messages))} уникальных сообщения")

video = [video // 60, video % 60]
voice = [voice // 60, voice % 60]
if video[0] > 60 and voice[0] > 60:
    video = [video[0] // 60, video[0] % 60, video[1]]
    voice = [voice[0] // 60, voice[0] % 60, voice[1]]
    print(f"— Аудиосообщения: {format_num(voice[0])} часов {voice[1]} минут {voice[2]} секунд")
    print(f"— Видеосообщения: {format_num(voice[0])} часов {video[1]} минут {video[2]} секунд")  
elif video[0] > 60:
    video = [video[0] // 60, video[0] % 60, video[1]]
    print(f"— Аудиосообщения: {format_num(voice[0])} минут {voice[1]} секунд")
    print(f"— Видеосообщения: {format_num(video[0])} часов {video[1]} минут {video[2]} секунд")
elif voice[0] > 60:
    voice = [voice[0] // 60, voice[0] % 60, voice[1]]
    print(f"— Аудиосообщения: {format_num(voice[0])} часов {voice[1]} минут {voice[2]} секунд")
    print(f"— Видеосообщения: {format_num(video[0])} минут {video[1]} секунд")
else:
    print(f"— Аудиосообщения: {voice[0]} минут {voice[1]} секунд")
    print(f"— Видеосообщения: {video[0]} минут {video[1]} секунд")

print(f"— Пригласили в беседу {format_num(invites)} раз")
print(f"— Присоединили по ссылке {format_num(link_join)} раз")
print(f"— Покинули беседу {format_num(leaved)} раз")
print(f"— Кикнули из беседы {format_num(kicked)} раз\n")

print(f"— Топ слов:")
stop_words = ['есть', 'меня', 'почему']
allow_words = ['бля']
counter = 10
for i in counted_words:
    if i[0].lower() in allow_words or i[0].lower() not in stop_words and len(i[0]) > 3:  
        print(f"{i[0]} - {i[1]}")
        counter -= 1
    if counter == 0:
        break
print(f"\n- Топ пользователей:")
# print(avtory_messages)
for avtor in range(len(avtory_messages), 1, -1):
    avtor_name = list(avtory_messages.keys())[avtor-1]
    print(avtor_name + " - " + str(avtory_messages[list(avtory_messages.keys())[avtor-1]]))
