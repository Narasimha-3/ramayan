








sentence="रामायण किसने लिखी, और कहानी किस बारे में है?"
sentence2 = "Wer ist der Vater von Jambavantha und wie ist er gestorben?"

print(langid.classify(sentence))

lang = langid.classify(sentence2)[0]
translator=Translator(from_lang = lang, to_lang="en")
translation=translator.translate(sentence2)
print(translation)