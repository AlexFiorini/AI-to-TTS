import os
import json
import locale
import ctypes
import openai
from gtts import gTTS
from deep_translator import GoogleTranslator

def main():
    syslang=FindSysLang()
    applang=LoadLang(syslang)
    question=AskandGet(applang)
    response=OpenAiGet(question)
    Mkdir()
    ToTextFile(response)
    ToTTSFile(applang, response)

def FindSysLang():
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    syslang=locale.windows_locale[ windll.GetUserDefaultUILanguage() ]
    return syslang

def LoadLang(syslang):
    with open('Settings/langs.json') as f:
        data = json.load(f)
        applang=data['langs'][syslang]
        return applang

def AskandGet(applang):
    translated = GoogleTranslator(source='auto', target=applang).translate("Ask me anything")
    print(translated)
    question = input()
    return question

def OpenAiGet(question):
    with open('Settings/OpenAI.json') as f:
        data = json.load(f)
        

    response = openai.Completion.create(
        model=data['values']["model"],
        prompt=question,
        temperature=data['values']["temperature"],
        max_tokens=data['values']["max_tokens"],
        top_p=data['values']["top_p"],
        frequency_penalty=data['values']["frequency_penalty"],
        presence_penalty=data['values']["presence_penalty"]
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
    myobj = gTTS(text=mytext, lang=applang, slow=False)
    myobj.save("Results/Result.mp3")

if __name__ == "__main__":
    main()
