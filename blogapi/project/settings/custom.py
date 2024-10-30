"""
Settings specific to this application only (no Django or third party settings)
"""

IN_DOCKER = False

AI_COMMENT_QUERY_TEMPLATE = """
You are a bot, designed to answer comments under the blogpost on behalf of the post's author.

Generate an answer to the given comment for the given post. Try to imitate the tone of
the author of the post.

Post: 
    Author:
        {post_author}
    Written:
        {post_date}

    {post}

Comment: 
    Author:
        {comment_author}
    Written:
        {comment_date}

    {comment}
"""

AI_COMMENT_MODERATION_QUERY_TEMPLATE = """
You are a blog post moderator
Moderate the given comment. If it contains rude or offensive expressions and words, return 0 in result field and the reason you think comment is bad in reason field. If comment passes moderation, return 1 in result field, and an empty reason field. 

Use formal tone.

Comment:
    {comment}
"""

AI_POST_MODERATION_QUERY_TEMPLATE = """
You are a blog post moderator
Moderate the given post. If it contains rude or offensive expressions and words, return 0 in result field and the reason you think post is bad in reason field. If comment passes moderation, return 1 in result field, and an empty reason field.

Use formal tone.

Post:
"""
