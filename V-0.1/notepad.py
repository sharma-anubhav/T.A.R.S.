import speech_recognition as sr
import pickle

try:
    Notes = pickle.load(open('Notes.txt', 'rb'))
except IOError:
    Notes = []
while True:
    print()
    c=0
    wait = input("View (v) or Record (r) or Delete (d): ")
    print()
    if wait == 'v':
        print("NOTES")
        print("_________________________________________________________")
        for i in Notes:
            c+=1
            print(str(c)+". "+i)
            print(".........................................................")

    elif wait == 'r':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("speak!")
            audio = r.listen(source)
            print('done!')
        try:
            text = r.recognize_google(audio)
            print("You said: "+ text)
            confirmation = input('Would you like to add this to your notes?(y/n): ')
            if confirmation == 'yes' or confirmation == 'Yes' or confirmation == 'y':
                Notes.append(text)
                with open('Notes.txt', 'wb') as fh:
                    pickle.dump(Notes, fh)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    else:
        j=-1
        index = input("Enter the Entry Number to Delete: ")
        index = index.split(',')
        for i in index:
            j+=1
            Notes.pop(int(i) - 1 - j)
        with open('Notes.txt', 'wb') as fh:
            pickle.dump(Notes, fh)







