
# import google.generativeai as genai

# # genai.configure(api_key="AIzaSyDGEhvcZdGAUZXl2wFsw_IpCLpqLb9zaac")
# #AIzaSyCEPxUHNpuBrX85pcf_J0Bp5vK09fPX9xQ - sriram
# #AIzaSyBN-3dcpfRnysyExc8W7jWbsti8chYc6kQ
# #AIzaSyA9jyoCXwuWeohJNfjUHyH8-J0eH4ajjqI - Narasimha
# genai.configure(api_key="AIzaSyA9jyoCXwuWeohJNfjUHyH8-J0eH4ajjqI")

# model = genai.GenerativeModel('gemini-1.5-pro')

# def ramayandata(prompt):
#     response = model.generate_content(prompt)
#     # print(response.text)
#     # with open('ayodhyakanda.txt', 'a') as f:
#     #     f.write("jai_balayya_ew\n")
#     #     f.write(response.text)
#     #     f.write("jai_balayya_ew\n")
#     return response.text

from google import genai

client = genai.Client(api_key="AIzaSyCLT8WNalj3i7VKXPMf2GJetseRLyWf0Eo")

def ramayandata(prompt):
    # response = client.models.generate_content(
    # model="models/gemini-2.5-flash",
    # contents=prompt
    # )
    pp = ""
    try:
        pp = prompt.split("---------\n")[1]
    except:
        pp = prompt
    return pp