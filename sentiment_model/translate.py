from googletrans import Translator

translator = Translator()


def translate(original:str) -> str:
    translation = translator.translate(original, dest='en')
    translated, origianl = translation.text, translation.src
    return translated, origianl

# original = '''【今日のおすすめ🍽️】
# ⭐️目黒バル la casa del PINO

# 目黒駅から徒歩8分のスペイン料理店。豊かな風味のイカスミパエリアやオリジナルアヒージョをはじめ、多彩なメニューと素晴らしいワインで訪れる人々を魅了します。店内はカジュアルながらも大人ら...
# https://t.co/63RSObcnYh

# #飲食店
# #グルメ"
# '''
# translation = translate(original)
# print(translation)