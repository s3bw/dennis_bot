import spacy
import markovify

import en_core_web_sm
nlp = en_core_web_sm.load()
# nlp = spacy.load('en')


class PosifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        tagged_words = [word.split("::") for word in words]
        sentence = ''
        for word, pos_tag in tagged_words:
            if pos_tag == "PUNCT":
                sentence += word
            else:
                word = " " + word
                sentence += word

        return sentence.lstrip()

    def make_sentence_with_conjunction():
        pass
        # conj = get_conj
        # return self.make_sentence_with_start(conj)



def create_tweet(model):
    return model.make_short_sentence(120, tries=25)


def create_reponse(model):
    return model.make_sentence_with_conjunction()


def train(corpus):
    return PosifiedText(corpus)

