import os
import json
import locale
import ctypes
import openai
import playsound
from gtts import gTTS
from deep_translator import GoogleTranslator

def main():
    a=True
    while (a==True) :
        syslang = FindSysLang()
        applang = LoadLang(syslang)
        question = AskandGet(applang)
        response = OpenAiGet(question)
        Mkdir()
        ToTextFile(response)
        ToTTSFile(applang, response)
        print(GoogleTranslator(source='auto', target=applang).translate("Vuoi riprodurre il file audio?"))
        a=input("Y/n")
        if (a=="Y"):
            a=True
        else:
            a=False

        playsound.playsound('/Results/Result.mp3', a)

        print(GoogleTranslator(source='auto', target=applang).translate("Vuoi chiedere un'altra domanda?"))
        a=input("Y/n")
        if (a=="Y"):
            a=True
        else:
            a=False

def FindSysLang():
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    syslang = locale.windows_locale[ windll.GetUserDefaultUILanguage() ]
    return syslang

def LoadLang(syslang):
    with open('Settings/langs.json') as f:
        data = json.load(f)
        applang = data['langs'][syslang]
        return applang

def AskandGet(applang):
    translated = GoogleTranslator(source='auto', target=applang).translate("Ask me anything")
    print(translated)
    question = input()
    return question

def OpenAiGet(question):
    with open('Settings/OpenAI.json') as f:
        data = json.load(f)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    if(openai.api_key == None):
        if(data['values']["OPENAI_API_KEY"] == ""): 
            print("The environment variable OPENAI_API_KEY is not set neither in the environment nor in the json file.")
            os.system("pause")
            raise TypeError("The environment variable OPENAI_API_KEY is not set neither in the environment nor in the json file.")
        else:
            openai.api_key = data['values']["OPENAI_API_KEY"]

    response = openai.Completion.create(
        model = data['values']["model"],
        prompt = question,
        temperature = data['values']["temperature"],
        max_tokens = data['values']["max_tokens"],
        top_p = data['values']["top_p"],
        frequency_penalty = data['values']["frequency_penalty"],
        presence_penalty = data['values']["presence_penalty"]
    )
    return response

def Mkdir():
    path = "Results"
    Exist = os.path.exists(path)
    if not Exist:
        os.makedirs(path)

def ToTextFile(response):
    f = open("Results/Temp.txt", 'w')
    f.writelines(response["choices"][0]["text"])
    f.close()
    with open("Results/Temp.txt", 'r') as r, open('Results/Result.txt', 'w') as o:
        for line in r:
            if line.strip():
                o.write(line)
    os.remove("Results/Temp.txt")
    
def ToTTSFile(applang, response):
    mytext = response["choices"][0]["text"]
    myobj = gTTS(text = mytext, lang = applang, slow = False)
    myobj.save("Results/Result.mp3")

if __name__ == "__main__":
    main()
