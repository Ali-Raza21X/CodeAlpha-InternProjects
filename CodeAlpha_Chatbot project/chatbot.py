def chatbot(user_input):
    user_input = user_input.lower()

    if 'hello' in user_input or 'hi' in user_input:
        return 'hello! how may i help u today.'

    elif 'how are you' in user_input or 'how the day is going' in user_input:
        return 'i am good what about u.'

    elif 'what is your name' in user_input or 'name' in user_input:
        return 'i am a chat bot'

    elif 'tell me the new news' in user_input or 'any news about IT' in user_input:
        return 'yes the market is building up day by day using ai'

    elif 'weather' in user_input or 'temp' in user_input:
        return 'weather is looking normal today'

    elif 'quit' in user_input or 'bye' in user_input:
        return 'GoodBye! have a good day'

    else:
        return 'sorry, i did not understand it'


print('Welcome to our chatbot')
print('Chatbot: Hello! Type something (type bye to exit)')


while True:

    user = input('you: ')

    response = chatbot(user)

    print('chatbot:', response)

    if "bye" in user.lower():
        break