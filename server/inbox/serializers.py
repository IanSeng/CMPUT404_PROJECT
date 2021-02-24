from rest_framework import serializers
from .models import Inbox
from posts.serializers import PostSerializer
from main import utils
from ast import literal_eval
from django.core.paginator import Paginator

class InboxSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('paginated_items')
    author = serializers.SerializerMethodField()

    def get_items(self, obj):
        data = []
        items = obj.items
        # print(items)
        # print(eval(items[0]))
        for item in items:
            data.append(literal_eval(item))
        # items = [JSONRenderer().render(item) for item in items ]
        # print(JSONRenderer().render(items[0]))
        # items = [deserialize('json', item) for item in items]
        # print(items)
        # x = []
        # for obj in deserialize('json', items[0]):
        #     x.append(obj.object)
        # # print(items[0].)
        # print(type(items[0]))
        # data = PostSerializer(obj.items.all(), many=True).data
        # return PostSerializer(x, many=True).data
        # return [{1:"ada"}, {1:"ada"}]
        # for item in items:
        #     for obj in deserialize('json', item):
        #         data.append(obj.object)
        # return json.loads(items[0])
        return data

    def get_author(self, obj):
        return f"{utils.HOST}/author/{obj.author.id}"

    def paginated_items(self, obj):
        data = []
        page_size = self.context['request'].query_params.get('size') or 10
        page = self.context['request'].query_params.get('page') or 1
        paginator = Paginator(obj.items, page_size)

        items = paginator.page(page)
        for item in items:
            data.append(literal_eval(item))
        return data


    class Meta:
        model = Inbox
        fields = ('type', 'author', 'items')