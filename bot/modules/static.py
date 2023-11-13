WelcomeText = \
"""
Hi **%(first_name)s**, send me a file or add me as an admin to any channel to instantly generate file links.

Add me to your channel to instantly generate links for any downloadable media. Once received, I will automatically attach appropriate buttons to the post containing the URL. If you want me to ignore a given post, you can insert `#pass` in the post.

- /start to get this message.
- /info to get user info.
- /log to get bot logs. (admin only!)
"""

UserInfoText = \
"""
**First Name:**
`{sender.first_name}`

**Last Name:**
`{sender.last_name}`

**User ID:**
`{sender.id}`

**Username:**
`@{sender.username}`
"""

FileLinksText = \
"""
**Download Link:**
`%(dl_link)s`
**Telegram File:**
`%(tg_link)s`
"""

MediaLinksText = \
"""
**Download Link:**
`%(dl_link)s`
**Stream Link:**
`%(stream_link)s`
**Telegram File:**
`%(tg_link)s`
"""

InvalidQueryText = \
"""
Query data mismatched.
"""

MessageNotExist = \
"""
File revoked or not exist.
"""

LinkRevokedText = \
"""
The link has been revoked. It may take some time for the changes to take effect.
"""

InvalidPayloadText = \
"""
Invalid payload.
"""

MediaTypeNotSupportedText = \
"""
Sorry, this media type is not supported.
"""
