from channels.auth import channel_session_user_from_http, channel_session_user
import json
import random
from play.frequent_variables import DISCONNECT_MESSAGE, WIN_GAME, WIN_ADD_SCORE, LOSE_ADD_SCORE, DRAW_ADD_SCORE, \
    DRAW_GAME, SYSTEM_MESSAGE, LOOKING_FOR_PLAYER, MATCHING_MESSAGE
from register.models import UserModel
from .models import OnlineUsers, PairUsers, ThemesForDebate
from django.db.models import Q
from channels import Channel
from . import score_argument
from django.shortcuts import get_object_or_404


@channel_session_user_from_http
def ws_connect(message):
    username = message.user.username
    reply_channel_name = message.reply_channel.name

    waiting_users = OnlineUsers.objects.all()

    # If there are waiting users connect to one of them
    if waiting_users.exists():
        user_topair = waiting_users.first()
        PairUsers.objects.create(username_a=username, reply_channel_a=reply_channel_name,
                                 username_b=user_topair.username,
                                 reply_channel_b=user_topair.reply_channel_name)
        random_idx = random.randint(0, ThemesForDebate.objects.count() - 1)
        theme_to_debate = ThemesForDebate.objects.all()[random_idx].theme
        message.reply_channel.send({'accept': True})
        other_channel = Channel(user_topair.reply_channel_name)
        other_channel.send({'accept': True})

        message.reply_channel.send({'text': json.dumps({
            "message": MATCHING_MESSAGE + " " + user_topair.username,
            "theme": theme_to_debate,
            "user": SYSTEM_MESSAGE, }),
        })

        other_channel.send({'text': json.dumps({
            "message": MATCHING_MESSAGE + " " + username,
            "theme": theme_to_debate,
            "user": SYSTEM_MESSAGE, }),
        })
        user_topair.delete()

    else:
        # else put the user on the waiting list
        OnlineUsers.objects.create(username=username, reply_channel_name=reply_channel_name)
        message.reply_channel.send({'text': json.dumps({
            "message": LOOKING_FOR_PLAYER,
            "user": SYSTEM_MESSAGE, }),
        })


@channel_session_user
def ws_receive(message):
    username = message.user.username
    text = json.loads(message['text']).get('text')

    # find the room with our users
    current_room = get_object_or_404(PairUsers, Q(username_a=username) | Q(username_b=username))

    # check which user you got and send the message to the other
    if current_room:
        if current_room.username_b == username:
            other_channel = Channel(current_room.reply_channel_a)
            if current_room.args_count_b < 2:
                current_room.args_count_b += 1
                current_room.save()
                # Use my algorithm here
                score = round(score_argument.get_rating(text), 4)
                current_room.score_b += score

                # send message to both channels
                message.reply_channel.send({'text': json.dumps({
                    "message": text,
                    "user": username, }),
                })
                message.reply_channel.send({'text': json.dumps({
                    "score": score,
                    "user": username, }),
                })
                other_channel.send({'text': json.dumps({
                    "message": text,
                    "user": username, }),
                })
                other_channel.send({'text': json.dumps({
                    "score": score,
                    "user": username, }),
                })

                # if the has already written 2 arguments and the other user too,
                # compare their score and choose the winner,
                # sending the coresponding messages to both channels and disconnect

            if current_room.args_count_b == 2 and current_room.args_count_a == 2:
                if current_room.score_a / 2 < current_room.score_b / 2:
                    other_channel.send({'text': json.dumps({
                        "message": username + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    message.reply_channel.send({'text': json.dumps({
                        "message": username + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    wining_user = get_object_or_404(UserModel, username=username)
                    wining_user.score += WIN_ADD_SCORE
                    wining_user.save()
                    losing_user = get_object_or_404(UserModel, username=current_room.username_a)
                    losing_user.score += LOSE_ADD_SCORE
                    losing_user.save()
                elif current_room.score_a / 2 == current_room.score_b / 2:
                    other_channel.send({'text': json.dumps({
                        "message": DRAW_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    message.reply_channel.send({'text': json.dumps({
                        "message": DRAW_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    draw_user = get_object_or_404(UserModel, username=username)
                    draw_user.score += DRAW_ADD_SCORE
                    draw_user.save()
                    draw_user_2 = get_object_or_404(UserModel, username=current_room.username_a)
                    draw_user_2.score += DRAW_ADD_SCORE
                    draw_user_2.save()
                else:
                    other_channel.send({'text': json.dumps({
                        "message": current_room.username_a + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    message.reply_channel.send({'text': json.dumps({
                        "message": current_room.username_a + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    wining_user = get_object_or_404(UserModel, username=current_room.username_a)
                    wining_user.score += WIN_ADD_SCORE
                    wining_user.save()
                    losing_user = get_object_or_404(UserModel, username=username)
                    losing_user.score += LOSE_ADD_SCORE
                    losing_user.save()
                ws_disconnect(message)

        # same logic as above
        else:
            other_channel = Channel(current_room.reply_channel_b)
            if current_room.args_count_a < 2:
                current_room.args_count_a += 1
                current_room.save()
                score = round(score_argument.get_rating(text), 4)
                current_room.score_a += score

                message.reply_channel.send({'text': json.dumps({
                    "message": text,
                    "user": username, }),
                })
                message.reply_channel.send({'text': json.dumps({
                    "score": score,
                    "user": username, }),
                })
                other_channel.send({'text': json.dumps({
                    "message": text,
                    "user": username, }),
                })
                other_channel.send({'text': json.dumps({
                    "score": score,
                    "user": username, }),
                })
            if current_room.args_count_a == 2 and current_room.args_count_b == 2:
                if current_room.score_b / 2 < current_room.score_a / 2:
                    other_channel.send({'text': json.dumps({
                        "message": username + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    message.reply_channel.send({'text': json.dumps({
                        "message": username + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    wining_user = get_object_or_404(UserModel, username=username)
                    wining_user.score += WIN_ADD_SCORE
                    wining_user.save()
                    losing_user = get_object_or_404(UserModel, username=current_room.username_b)
                    losing_user.score += LOSE_ADD_SCORE
                    losing_user.save()

                elif current_room.score_b / 2 == current_room.score_a / 2:
                    other_channel.send({'text': json.dumps({
                        "message": DRAW_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })

                    message.reply_channel.send({'text': json.dumps({
                        "message": DRAW_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })
                    draw_user = get_object_or_404(UserModel, username=username)
                    draw_user.score += DRAW_ADD_SCORE
                    draw_user.save()
                    draw_user_2 = get_object_or_404(UserModel, username=current_room.username_b)
                    draw_user_2.score += DRAW_ADD_SCORE
                    draw_user_2.save()
                else:
                    other_channel.send({'text': json.dumps({
                        "message": current_room.username_b + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })

                    message.reply_channel.send({'text': json.dumps({
                        "message": current_room.username_b + " " + WIN_GAME,
                        "user": SYSTEM_MESSAGE, }),
                    })

                    wining_user = get_object_or_404(UserModel, username=current_room.username_b)
                    wining_user.score += WIN_ADD_SCORE
                    wining_user.save()
                    losing_user = get_object_or_404(UserModel, username=username)
                    losing_user.score += LOSE_ADD_SCORE
                    losing_user.save()
                ws_disconnect(message)


@channel_session_user
def ws_disconnect(message):
    username = message.user
    message.reply_channel.send({'text': json.dumps({
        "message": DISCONNECT_MESSAGE,
        "user": SYSTEM_MESSAGE, }),
    })

    # deleting the room if it still exist and if the person wasn't
    # matched and  disconnects delete their UsersOnline record

    current_room = PairUsers.objects.filter(Q(username_a=username) | Q(username_b=username)).first()
    online_user_record = OnlineUsers.objects.filter(username=username).first()
    if current_room:
        if current_room.username_a == username:
            other_channel = Channel(current_room.reply_channel_b)
            other_channel.send({'text': json.dumps({
                "message": DISCONNECT_MESSAGE,
                "user": SYSTEM_MESSAGE, }),
            })
        if current_room.username_b == username:
            other_channel = Channel(current_room.reply_channel_a)
            other_channel.send({'text': json.dumps({
                "message": DISCONNECT_MESSAGE,
                "user": SYSTEM_MESSAGE, }),
            })

        current_room.delete()
    if online_user_record:
        online_user_record.delete()
