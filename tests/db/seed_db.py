from faker import Faker

from profiles.models import Profile

faker = Faker()
faker.seed(10)


def get_parsed_address():
    address = faker.address().split(" ")
    zipcode = address[-1]
    state = address[-2]
    city = address[-3].split("\n")
    street = city[0]
    city = city[-1].replace(",", "")
    street = ' '.join(address[0:-3]) + ' ' + street
    return street, city, state, zipcode


def add_users():
    for x in range(20):
        pass


def add_profiles():
    for x in range(10):
        Profile.objects.create(title=faker.job(), description=faker.text())


if __name__ == "__main__":
    add_profiles()
