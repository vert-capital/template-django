import json

from django_kafka.consumer import Consumer, Message


def user_consumer(consumer: Consumer, msg: Message) -> None:

    user_data = json.loads(msg.value())

    try:
        create_or_update_user(user_data)
        consumer.commit(message=msg)
        print(f"User {user_data['email']} created/updated")
    except Exception as e:
        print(e)


def create_or_update_user(user_data: dict) -> None:
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if User.objects.filter(email=user_data["email"]).exists():
        user = User.objects.get(email=user_data["email"])
    else:
        user = User()

    if "image" in user_data:
        user.image = user_data["image"]

    user.email = user_data["email"]
    user.name = user_data["name"]
    user.is_superuser = user_data["is_superuser"]
    user.is_staff = user_data["is_staff"]
    user.is_active = user_data["is_active"]
    user.save()
