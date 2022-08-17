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
    operator = ChoiceField(choices=users_choise)
    client = ChoiceField(choices=client_choise)
    table_type = ChoiceField(choices=page_choice)



