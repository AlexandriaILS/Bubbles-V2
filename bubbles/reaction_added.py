from bubbles.config import USERNAME, DEFAULT_CHANNEL, users_list


def reaction_added_callback(**payload):
    data = payload["data"]
    userWhoReacted = users_list[data["user"]]
    userWhoseMessageHasBeenReacted = users_list[data["item_user"]]
    reaction = data["reaction"]
    print(
        f"{userWhoReacted} has replied to one of {userWhoseMessageHasBeenReacted}'s"
        f" messages with a :{reaction}:."
    )


#    if userWhoseMessageHasBeenReacted == USERNAME:
#        response = client.chat_postMessage(
#                    channel=DEFAULT_CHANNEL,
#                    text=userWhoReacted+" has replied to one of my messages with a :"+reaction+":. Youpie!",
#                    as_user=True)
#    else:
#        print("Other message")
#        response = client.chat_postMessage(
#                    channel=DEFAULT_CHANNEL,
#                    text=userWhoReacted+" has replied to one of "+userWhoseMessageHasBeenReacted+"'s messages with a :"+reaction+":. Notice me, senpai.",
#                    as_user=True)
