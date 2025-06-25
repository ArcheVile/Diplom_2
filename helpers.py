from faker import Faker

fake = Faker('ru_RU')

def generate_random_user():
    return {
        "email": fake.email(),
        "password": fake.password(length=10),
        "name": fake.first_name()
    }
