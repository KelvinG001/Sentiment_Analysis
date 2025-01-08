from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import numpy as np
from scipy.special import softmax

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
supported_languages = ('ar', 'en', 'fr', 'de', 'hi', 'it', 'es', 'pt')

model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
config = AutoConfig.from_pretrained(model_path)

############################################ only uncomment it when first running the code to save the model from hugging face to local ###########################
# model.save_pretrained(model_path)
# tokenizer.save_pretrained(model_path)
############################################ only uncomment it when first running the code to save the model from hugging face to local ###########################
# text = "Ich liebe @Kawabata Zemi um Keio Universitat https://sites.google.com/keio.jp/mizuki-seminar/"
# text = "I was admitted to Keio University. I love Keio University, but the tuition is too expensive and my parents cannot afford it. However, I will try my best to win a scholarship to pay the tuition."
# text = "The sunshine is too strong"

def preprocess(text):
    new_text = []
    for t in text.split(" "):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return " ".join(new_text)


def predict_sentiment(text: str) -> str:
    preprocessed = preprocess(text)

    encoded_input = tokenizer(preprocessed, return_tensors='pt') #tokenize the preprocessed text and return a pytorch tensor
    output = model(**encoded_input)
    # scores = output[0][0].detach().numpy()
    # scores = softmax(scores)

    # ranking = np.argsort(scores)
    # ranking = ranking[::-1]
    # for i in range(scores.shape[0]):
    #     l = config.id2label[ranking[i]]
    #     s = scores[ranking[i]]
    #     print(f"{i+1}) {l} {np.round(float(s), 4)}")
    index = output.logits.argmax().item()
    sentiment = config.id2label[index]
    # print(preprocessed)
    # print(encoded_input)
    # print(output)
    # print(index)
    # print(sentiment)
    return sentiment

# print(predict_sentiment(text))
