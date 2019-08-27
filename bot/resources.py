from import_export import resources
from .models import Users, Statements, Received, Reply
class UsersResource(resources.ModelResource):
    class Meta:
        model = Users
class StatementsResource(resources.ModelResource):
    class Meta:
        model = Statements
class ReceivedResource(resources.ModelResource):
    class Meta:
        model = Received
class ReplyResource(resources.ModelResource):
    class Meta:
        model = Reply