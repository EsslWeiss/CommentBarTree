from django.template import Library
from django.utils.html import mark_safe

register = Library()

@register.filter
def comments_filter(comments):
    result = """
        <ul style="list-style-type: none;">
            <div class="col-ad-12 mt-2">
                {comment}
            </div>
        </ul>
        """
    i = ""
    for comment in comments:
        i += """
            <li>
                <div class="col-md-12 mb-2 mt-2 p-0">
                    <small>{author}</small> | publish at {createdAt}
                    <p>{text}</p>
                    <a href="#" class="reply" data-id="{id}" data-parent="{parent_id}">answer</a><hr>
                    <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display: none;">
                        <textarea type="text" class="form-control" name="comment-text"></textarea><br>
                        <input type="submit" class="btn btn-primary submit-reply" data-id="{id}" data-submit-reply="{parent_id}" value="send">
                    </form>
                </div>
            </li>
            """.format(author=comment['author'],
                       createdAt=comment['createdAt'],
                       text=comment['text'],
                       id=comment['id'],
                       parent_id=comment['parent_id']
                    )
        if comment.get('children'):
            i += comments_filter(comment['children'])

    return mark_safe(result.format(comment=i))

