from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import Word, Sentence
import time
from functools import wraps
from django.core.cache import cache
from django.shortcuts import render


def timer(func):
    """helper function to estimate view execution time"""

    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)

        duration = (time.time() - start) * 1000
        # output execution time to console
        print('view {} takes {:.2f} ms'.format(
            func.__name__,
            duration
        ))
        return result

    return wrapper


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@timer
def migration_data_word(request):
    with open('dictionary/word/data/vocab.txt', 'r') as f:

        for line in f:
            vocab = line.strip()
            w = Word(raw=vocab)
            w.save()

            web = requests.get("https://sentencedict.com/" + vocab + ".html")
            data = web.content
            soup = BeautifulSoup(data, features="html.parser")
            tag = soup.select_one('div#all')

            for i in tag:
                if (i.text.strip() == ''):
                    continue
                else:
                    tex = i.text.lstrip('0123456789.)(- ').strip()
                    s = Sentence(word = w, raw = tex)
                    s.save()

    return HttpResponse("test")

@timer
def findSentenceByWord(request, word):
    sentinel = object()
    isNohave = cache.get(word, sentinel) is sentinel
    if isNohave == True:
        # tim tu trong bang tu -> id
        # word = select word_id from word where word='apple'
        # word = Word.objects.get()[1]
        w = Word.objects.filter(raw=word)
        w1 = w[0]
        # print(w[1].raw)
        # print(w[2].raw)
        # print(len(w))
        print("Word Object: ", w1)
        print("Word Raw: ", w1.raw)
        print("Word Id: ", w1.id)
        sentences = Sentence.objects.filter(word_id=w1.id)
        print(len(sentences))

        caus = []

        for c in sentences:
            caus.append(c.raw)
            # print(c.raw)


        # tim cau trong bang cau tu id_word
        # cau = select * from cau where word_id=word
        cache.set(word, caus)

        return HttpResponse(caus)
    else:
        return HttpResponse(cache.get(word))


# @timer
# def findSentenceByWordCacheAll(request, word):
#     sentinel = object()
#     isNohave = cache.get(word, sentinel) is sentinel
#     if isNohave == True:
#         w = Word.objects.all()
#         w1 = w[0]
#         sentences = Sentence.objects.filter(word_id=3)
#         print(len(sentences))
#
#         for
#
#         for c in sentences:
#             caus.append(c.raw)
#             # print(c.raw)
#
#
#         # tim cau trong bang cau tu id_word
#         # cau = select * from cau where word_id=word
#         cache.set(word, caus)
#
#         return HttpResponse(caus)
#     else:
#         return HttpResponse(cache.get(word))




def show(request, word):

    sentences = Sentence.objects.filter(raw=word)
    caus = []

    for c in sentences:
        caus.append(c.raw)
        


    # tim cau trong bang cau tu id_word
    # cau = select * from cau where word_id=word
    cache.set(word, caus)
    print(word)
    return HttpResponse(caus)
    # else:
    #     return HttpResponse(cache.get(word))

    # return render(request, 'show.html')

def get_word(word):
    w = Word.objects.filter(raw=word)
    w1 = w[0]
    sentences = Sentence.objects.filter(word_id=w1.id)

    caus = []

    for c in sentences:
        caus.append(c.raw)
        # print(c.raw)
    return caus

def home(request):
    # word = request.GET.get('word')
    # caus = get_word(word)

    words = Word.objects.filter()

    words_num = {}

    for word in words:
        sens = Sentence.objects.filter(word_id=word.id)
        words_num[word] = len(sens)

    # print("wordsNum", wordsNum)
    #
    # return render(request, 'home.html', context)
    # c = ""
    # for w in words:
    #     c += w.raw + "\n"

    context = {'words_num': words_num}


    # return HttpResponse("ahihi")
    return render(request, 'home.html', context)
