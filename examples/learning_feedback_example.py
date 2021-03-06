"""
This example shows how to create a chat bot that
will learn responses based on an additional feedback
element from the user.
"""

from chatterbot import ChatBot
from chatterbot.conversation import Statement


# Uncomment the following line to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    'Feedback Learning Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter'
)


def get_feedback(response_text: str, input_statement_text: str):
    """Get feedback

    Confirm whether response generated by bot is acceptable
    :param response_text : response text generated by bot
    :type response_text : str
    :param input_statement_text: input statement text
    :type input_statement_text: str
    :return: True or False
    :rtype: bool
    """

    text = input('\n Is "{}" a coherent response to "{}"? \n'.format(
        response_text,
        input_statement_text
    ))

    if 'yes' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback(response_text=response_text, input_statement_text=input_statement_text)


print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        input_statement = Statement(text=input("User: "))
        response = bot.get_response(
            input_statement
        )

        if not get_feedback(response_text=response.text, input_statement_text=input_statement.text):
            response = Statement(text=input("Please input the correct response: "))

        bot.learn_response(response, input_statement)
        print("Bot: {} # Added to bot".format(response.text))

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
