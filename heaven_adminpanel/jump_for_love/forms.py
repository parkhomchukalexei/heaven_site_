from django.forms import ChoiceField, Form, CharField
from users.models import User, Client


class CreateJumpForLoveTable(Form):

    all_clients = Client.objects.all()
    all_operators = User.objects.filter(groups__name = 'Operator')
    users_choise = (
        ((i.id, i) for i in all_operators)
    )
    client_choise = (
        ((i.id, i.name) for i in all_clients)
    )
    month_list = (("1", 'Январь'),("2", 'Февраль'), ("3", 'Март'), ("4", 'Апрель'), ("5",'Май'), ("6", 'Июнь'), ("7", 'Июль'),
             ("8", 'Август'),  ("9", 'Сентябрь'), ("10", 'Октябрь'), ("11", 'Ноябрь'),  ("12", 'Декабрь'))

    month = ChoiceField(choices=month_list)
    operator = ChoiceField(choices=users_choise)
    client = ChoiceField(choices=client_choise)
    account_id = CharField()
