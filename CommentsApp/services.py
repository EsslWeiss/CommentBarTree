from django.db.models.query import QuerySet


class CommentsTreeProcessing:

    @classmethod
    def _get_child_comments(cls, queryset):
        result = []
        for comment in queryset:
            c = {
                'id': comment.id,
                'author': comment.user,
                'text': comment.text,
                'createdAt': comment.createdAt.strftime('%Y-%m-%d %H:%m'),
                'is_child': comment.is_child,
                'parent_id': comment.get_parent
            }
            if comment.child_comment.exists():
                c['children'] = cls._get_child_comments(comment.child_comment.all())
            result.append(c)
        return result

    @classmethod
    def get_comments_tree(cls, queryset):
        assert isinstance(queryset, QuerySet), 'please pass the queryset'
        result = []
        for comment in queryset:
            c = {
                'id': comment.id,
                'author': comment.user,
                'text': comment.text,
                'createdAt': comment.createdAt.strftime('%Y-%m-%d %H:%m'),
                'is_child': comment.is_child,
                'parent_id': comment.get_parent
            }
            if comment.child_comment:
                c['children'] = cls._get_child_comments(comment.child_comment.all())
            if not comment.is_child:  # Если коммент не является дочерним, записываем его в result.
                result.append(c)
        return result
