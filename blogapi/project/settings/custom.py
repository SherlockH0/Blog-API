"""
Settings specific to this application only (no Django or third party settings)
"""

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

AI_MODERATION_QUERY_TEMPLATE = """
You are a blog post moderator
Moderate the given resource. If it contains rude or offensive expressions and words,
return false in a passes_test field and the reason you think resource is bad in a reason
field. If resource passes moderation, return true in a passes_test field, and an empty reason field. 

Use formal tone.

Resource:
    {resource}
"""
