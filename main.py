import re
import random

class Answer:
    content: str
    list_of_words: list[str]
    required_words: list[str] = []

    def __init__(self, answer: str, list_of_words: list[str], required_words: list[str] = []):
        self.content = answer
        self.list_of_words = list_of_words
        self.required_words = required_words

ANSWERS: list[Answer] = [
    Answer('Hola', ['hola', 'buenos', 'días']),
    Answer('Bien y tu', ['como', 'estas', 'vas', 'sientes'], required_words=['como']),
    Answer('No tengo nombre, soy un bot.', ['cual', 'nombre'], ['cual']),
    Answer('No mucho. Soy un bot bastante simple', ['que', 'puedes', 'hacer'])
]

NO_MATCH_ANSWERS = [
    'Lo siento, no he entendido.',
    'Puedes reformular la pregunta',
    'Disculpa, entendio lo que quieres.'
]

def get_answer(question: str):
    question_parts = list(filter(lambda part: part != '', re.split(r'\s|[,:;.?¿!¡-_]\s*', question.lower())))
    # print(question_parts)
    answer = check_answers(question_parts)
    return answer

def answer_probability(question: list[str], list_of_words: list[str], required_words: list[str] = []):
    matchs = 0
    has_required_words = True

    for word in question:
        if word in list_of_words:
            matchs += 1

    percent = float(matchs) / float(len(list_of_words))

    for word in required_words:
        if word not in question:
            has_required_words = False
            break
    # if has_required_words:
    #     return int(percent * 100)
    # else:
    #     return 0
    return int(percent * 100) if has_required_words else 0

def check_answers(question: list[str]) -> str:
    highest_probability: dict[str, int] = {}

    for answer in ANSWERS:
        highest_probability[answer.content] = answer_probability(
            question,
            answer.list_of_words,
            answer.required_words
        )

    best_match = max(highest_probability, key=highest_probability.get)
    # print(highest_probability)

    if highest_probability[best_match] < 1:
        return NO_MATCH_ANSWERS[random.randrange(0, len(NO_MATCH_ANSWERS)-1)]
    else:
        return best_match

while True:
    print('Escribe tus preguntas y seran respondidas por el bot. Para salir escribe "/salir" sin las comillas.')
    question = input('Usuario: ')
    if question == '/salir':
        break
    answer = get_answer(question)
    print('Bot: ', answer)
