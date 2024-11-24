WelcomeText = \
"""\
Hi **%(first_name)s**, send me a file to instantly generate file links.

**Commands:**
/privacy - View bot's privacy policy.
/log - Get bot's log file. (owner only)
/help - Show this message.
"""

PrivacyText = \
"""
**Privacy Policy**

**1.Data Storage:** Files you upload/send are securely saved in the bot's private Telegram channel.

**2.Download Links:** Links include a secret code to prevent unauthorized access.

**3.User Control:** You can revoke links anytime using the "Revoke" button.

**4.Moderation:** The bot owner can view and delete your files if necessary.

**5.Open Source:** The bot is [open source](https://github.com/TheCaduceus/FileStreamBot). Deploy your own instance for maximum privacy.

**6.Retention:** Files are stored until you revoke their links.

__By using this bot, you agree to this policy.__
"""

FileLinksText = \
"""
**Download Link:**
`%(dl_link)s`
"""

MediaLinksText = \
"""
**Download Link:**
`%(dl_link)s`
**Stream Link:**
`%(stream_link)s`
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

UserNotInAllowedList = \
"""
You are not allowed to use this bot.
"""
