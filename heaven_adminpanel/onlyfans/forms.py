from django.forms import ModelForm, ChoiceField, Form
from users.models import User, Client


class CreateOnlyfansTable(Form):

    all_users = User.objects.all()
    all_clients = Client.objects.all()
    page_choice = (
        ('0', 'OP'),
        ('1', 'FP+PP')
    )
    users_choise = (
        ((i.id, i) for i in all_users)
    )
    client_choise = (
        ((i.id, i.name) for i in all_clients)
    )
    month_list = (("1", 'Январь'),("2", 'Февраль'), ("3", 'Март'), ("4", 'Апрель'), ("5",'Май'), ("6", 'Июнь'), ("7", 'Июль'),
             ("8", 'Август'),  ("9", 'Сентябрь'), ("10", 'Октябрь'), ("11", 'Ноябрь'),  ("12", 'Декабрь'))

    month = ChoiceField(choices=month_list)
    operator = ChoiceField(choices=users_choise)
    client = ChoiceField(choices=client_choise)
    table_type = ChoiceField(choices=page_choice)



