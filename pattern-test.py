from germalemma import GermaLemma

lemma = GermaLemma()
singular = "Karotten"
print(singular)
singular = singular.capitalize()
print(singular)
plural = lemma.find_lemma(singular,"N")

print(plural)