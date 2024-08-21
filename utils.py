def get_result(prompt):
    import requests
    URL = "http://127.0.0.1:8000/post"
    PARAMS = {'post':prompt}
    r = requests.post(url = URL, params = PARAMS)
    return r.json().get('response'), r.json().get('source_nodes')


def detectlanguageandanswer(question):

    # from translate import Translator
    import langid
    from deep_translator import GoogleTranslator

    language = langid.classify(question)[0]

    # sentence = "एंड्राइड फोन यूजर्स के लिए अच्छी खबर है। दरअसल, इन दिनों गूगल अपने लेटेस्ट फीचर पर काम कर रहा है। ये समझ लीजिए कि इस फीचर के इंट्रोड्यूज होने पर आपका फोन आपके इशारों पर चलेगा। जिसका मतलब हुआ कि अगर आप मुस्कुराकर ऊपर देखेंगे, तो आपका फोन अपने आप ही एक्टिव हो जाएगा। एक रिपोर्ट में गूगल के इस फीचर के बारे में जानकारी दी गई है। तो हुआ न ये मजेदार फीचर। अब ये भी बताते हैं कि इस फीचर की मदद से आप क्या-क्या कर सकते हैं ? इसकी मदद से मोबाइल यूजर स्क्रॉलिंग, सेटिंग और होम पेज पर विजिट करने तक तमाम ये काम सिर्फ इशारों से कर सकते हैं। फिलहाल, ये फीचर कब इंड्रोड्यूज होगा, इसकी खुलासा नहीं हुआ है। इस वक्त इस फीचर की टेस्टिंग पर काम चल रहा है। हालांकि, इस बीच ये जानकारी भी निकलकर सामने आई है कि हो सकता है इस साल आखिरी तक ये फीचर लॉन्च हो जाए।"

    translator = GoogleTranslator(source = "auto", target = "en")
    translation = translator.translate(question)

    try:
        response, _ = get_result(translation)
    except (Exception) as e:
        response = "Sorry, I am not able to answer this question." + str(e)

    anstransl = GoogleTranslator(source = "en", target = language)
    answer = anstransl.translate(str(response))

    print(answer)

    return answer