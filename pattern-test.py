from germalemma import GermaLemma

lemma = GermaLemma()

singular = lemma.find_lemma("Kartoffeln","N")
print(singular)