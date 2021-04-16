# ranking system

async def update_data(users, user, xp):
    user_list = []
    for user_id in users:
        user_list.append(user_id)

    if str(user.id) not in user_list:
        users[str(user.id)] = {}
        users[str(user.id)]['experience'] = 0
        users[str(user.id)]['level'] = 0
    elif str(user.id) in user_list:
        users[str(user.id)]['experience'] += xp


async def level_up(users, user, channel):
    experience = users[str(user.id)]['experience']
    level_start = users[str(user.id)]['level']
    end_experience = (level_start + 1) * 500
    level_end = level_start + 1

    if experience >= end_experience:
        await channel.send(f"{user.name} has leveled up to {level_end}")
        users[str(user.id)]['level'] = level_end


async def show_rank(users, user, message):
    user_list = []
    for user_id in users:
        user_list.append(user_id)

    if str(user.id) in user_list:
        experience = users[str(user.id)]['experience']
        level = users[str(user.id)]['level']
        await message.channel.send(f"{user.name} has {experience} xp and is at level {level}")
