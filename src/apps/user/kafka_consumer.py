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


def save_image_from_url_to_model(user, url) -> None:
    from io import BytesIO

    import requests
    from PIL import Image

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    file_name = f"{user.id}.png"
    img.save(f"media/{file_name}")
    user.image = file_name
    user.save()


def create_or_update_user(user_data: dict) -> None:
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if User.objects.filter(email=user_data["email"]).exists():
        user = User.objects.get(email=user_data["email"])
    else:
        user = User()

    user.email = user_data["email"]
    user.name = user_data["name"]
    user.is_active = user_data["is_active"]
    user.save()

    if "image" in user_data:
        try:
            save_image_from_url_to_model(user, user_data["image"])
        except Exception as e:
            print("error on save image: ", e)
