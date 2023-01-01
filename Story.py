def get_input(word_type:str):
    """
    This file is about to create a story with given nouns and verbs.
    """
    user_input = input(f"Enter a {word_type}: ")
    
    return user_input

noun1 = get_input("noun")
verb1 = get_input("verb")
noun2 = get_input("noun")
verb2 = get_input("verb")

story = f'''
{noun1}: Hey {noun2}, what are you up to today?
{noun2}: Hi {noun1}! I was thinking about going to the park to {verb1}. What about you?
{noun1}: Oh, that sounds nice! I was planning to {verb2} some cookies. Want to join me after you're done?
{noun2}: Sure! I’ll bring my book, and we can relax together while eating cookies.
{noun1}: Perfect! Let’s meet at my place around 3 PM?
{noun2}: Sounds like a plan. See you then!
'''
print(story)