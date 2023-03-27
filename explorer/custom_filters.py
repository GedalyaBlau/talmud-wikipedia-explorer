from django import template
from explorer.models import Comment

register = template.Library()

@register.filter
def get_comment_for_article(comments, article_id):
    return comments.filter(wikipedia_article_id=article_id)
