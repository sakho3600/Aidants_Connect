import factory

from .models import Usager


class UsagerFactory(factory.DjangoModelFactory):
    given_name = "Homer"
    family_name = "Simpson"
    birthdate = "1902-06-30"
    gender = Usager.GENDER_MALE
    birthplace = "27681"
    birthcountry = Usager.BIRTHCOUNTRY_FRANCE
    email = "homer@simpson.com"
    sub = factory.Sequence(lambda n: f"avalidsub{n}")

    class Meta:
        model = Usager
