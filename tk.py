#############################
import ch
from tkinter import *
from tkinter import ttk
import threading

RaumListeEintritt=[]
RaumListeVerlassen=[]
#FreundesListe=[]

class TestBot(ch.RoomManager):
  
  def onInit(self):
    pass


  def onConnect(self, room):
    print("Connected to "+room.name)
    BotGUI.Text_Input(str("Connected to "+room.name))
    BotGUI.Text_Go()
    self.setFontColor("000000")
    RaumListeEintritt.insert(0, room.name)
    BotGUI.Room_Usercount()




  def onReconnect(self, room):
    print("Reconnected to "+room.name)
    BotGUI.Text_Input(str("Reconnected to "+room.name))
    BotGUI.Text_Go()


  def onDisconnect(self, room):
    print("Disconnected from "+room.name)
    BotGUI.Text_Input(str("Disconnected from "+room.name))
    BotGUI.Text_Go()
 
   
  def onPMConnect(self, pm):
    print("Connected to "+NICK+"'s PM's")
    BotGUI.PM_Input(str("Connected to "+NICK+"'s PM's"))
    BotGUI.PM_Go()
    self.joinRoom(THEROOM)

  def onPMDisconnect(self, pm):
    print("Disonnected from "+NICK+"'s PM's")
    BotGUI.PM_Input(str("Disconnected from "+NICK+"'s PM's"))
    BotGUI.PM_Go()

  def onMessage(self, room, user, message):
    BotGUI.Text_Input(str(user.name+": "+message.body))
    BotGUI.Text_Go()
    try:
      print(user.name+":"+message.body)
    except UnicodeError:
      print(user.name+"'s message caused a Unicode Error")


    


  def onFloodWarning(self, room):
    print("Reconnecting to avoid flood ban.")
    BotGUI.Text_Input("Reconnecting to avoid flood ban.")
    BotGUI.Text_Go()
    room.reconnect()


  def onFloodBanRepeat(self, room):
    print("You are flood banned.")
    BotGUI.Text_Input("You are flood banned.")
    BotGUI.Text_Go()

  def onHistoryMessage(self, room, user, message):
    BotGUI.Text_Input(user.name+": "+message.body)
    BotGUI.Text_Go()


  def onUserCountChange(self, room):
    BotGUI.Room_Usercount()


  def onPMMessage(self, pm, user, body):
    BotGUI.PM_Input(user.name+": "+body)
    BotGUI.PM_Go()
    try:
      print(user.name+": "+body)
      with open("PM Log (because otherwise the chat history couldn't be saved).txt","a+") as PMLog:
        PMLog.write(user.name+": "+body+"\n")
    except UnicodeError:
      print(user.name+"'s message caused a Unicode Error.")
      with open("PM Log (because otherwise the chat history couldn't be saved).txt","a+") as PMLog:
        PMLog.write(user.name+"'s message caused a Unicode Error. \n")

  def onPMOfflineMessage(self, pm, user, body):
    print("You got a PM while you were offline:")
    try:
      print(user.name+": "+body)
    except UnicodeError:
      print(user.name+"'s message caused a Unicode Error.")
    BotGUI.PM_Input("You got a PM while you were offline:")
    BotGUI.PM_Go()
    BotGUI.PM_Input(user.name+": "+body)
    BotGUI.PM_Go()
    BotGUI.PM_Input("----------")
    BotGUI.PM_Go()
    try:
      with open("PM Log (because otherwise the chat history couldn't be saved).txt","a+") as PMLog:
        PMLog.write(user.name+": "+body+"\n")
    except UnicodeError:
      with open("PM Log (because otherwise the chat history couldn't be saved).txt","a+") as PMLog:
        PMLog.write(user.name+"'s message caused a Unicode Error. \n")

  def onPMContactOnline(self, pm, user):
    #if user.name.lower() in FreundesListe:
    BotGUI.PM_Input("---"+user.name+" is online---")
    BotGUI.PM_Go()

  def onPMContactOffline(self, pm, user):
    #if user.name.lower() in FreundesListe:
    BotGUI.PM_Input("---"+user.name+" is offline---")
    BotGUI.PM_Go()

    

THEROOM=input("Enter ONE roomname: ")
NICK=input("Account name: ")
PASS=input("Password: ")

TestBot = TestBot(NICK,PASS)

TestBot_thread = threading.Thread(target=TestBot.main)
TestBot_thread.setDaemon(True)
TestBot_thread.start()
#######################################################################
class BotGUI:

  def Text_Go():
    text.insert("end", str(chvariable.get())+"\n")
    text.see(END)

  def Text_Input(arg):
    chvariable.set(arg)

  def PM_Go():
    texttwo.insert("end", str(pmvariable.get())+"\n")
    texttwo.see(END)

  def PM_Input(args):
    pmvariable.set(args)

  def Post_Message():
    room=TestBot.getRoom(RaumListeEintritt[0])
    room.message(str(Nachricht.get()))
    entry.delete(0, END)

  def Post_PMMessage():
    TestBot.pm.message(ch.User(str(PMReceiver.get())), str(PMNachricht.get()))
    BotGUI.PM_Input("You > "+str(PMReceiver.get())+": "+str(PMNachricht.get()))
    BotGUI.PM_Go()
    try:
      print("You > "+str(PMReceiver.get())+": "+str(PMNachricht.get()))
      with open("PM Log (because otherwise the chat history couldn't be saved).txt","a+") as PMLog:
        PMLog.write("You > "+str(PMReceiver.get())+": "+str(PMNachricht.get())+"\n")
    except UnicodeError:
      print("Your message to "+str(PMReceiver.get())+" caused a Unicode Error.")
      with open("PM Log (because otherwise the chat history couldn't be saved).txt","a+") as PMLog:
        PMLog.write("Your message to "+str(PMReceiver.get())+" caused a Unicode Error. \n")
    entry2.delete(0, END)

  def Switch_Room():
    RaumListeVerlassen.insert(0, RaumListeEintritt[0])
    RaumListeEintritt.insert(0, str(roomvariable.get()))
    text.delete("1.0", "end")
    TestBot.joinRoom(str(RaumListeEintritt[0]))
    TestBot.setTimeout(3, TestBot.leaveRoom, RaumListeVerlassen[0])
    
    

  def Switch_Bgmode_On():
    try:
      room=TestBot.getRoom(RaumListeEintritt[0])
      room.setBgMode(1)
      ChBgMode.set("Background is on.")
    except Exception:
      print("Error")

  def Switch_Bgmode_Off():
    try:
      room=TestBot.getRoom(RaumListeEintritt[0])
      room.setBgMode(0)
      ChBgMode.set("Background is off.")
    except Exception:
      print("Error")
      
  def Switch_Fontcolor():
    user=TestBot.getUser()
    if user.getFontColor()=="000000":
      TestBot.setFontColor("FFFFFF")
      TestBot.setNameColor("FFFFFF")
      Fontcolor.set("Font color is white. Click to change it to black")
    elif user.getFontColor()=="FFFFFF":
      TestBot.setFontColor("000000")
      TestBot.setNameColor("000000")
      Fontcolor.set("Font color is black. Click to change it to white")

  def Switch_Fontsize():
    user=TestBot.getUser()
    if user.getFontSize()>9:
      TestBot.setFontSize(9)
      Fontbutton.set("The fontsize is 9. Click to set it to 12")
    else:
      TestBot.setFontSize(12)
      Fontbutton.set("The fontsize is 12. Click to set it to 9")

  def Room_Usercount():
    room=TestBot.getRoom(RaumListeEintritt[0])
    Zahl=room.getUserCount()
    if Zahl==1:
      UserZahl.set("There is "+str(Zahl)+" person in "+str(room.name)+" now.")
    else:
      UserZahl.set("There are "+str(Zahl)+" people in "+str(room.name)+" now.")
    



  root=Tk()
  root.title("Chatango")

  frame=Frame(root)
  frame.grid(column=0, row=0)


  ######################################
  ##########Variablen###################
  global Nachricht
  global chvariable
  global pmvariable
  global PMNachricht
  global PMReceiver
  global roomvariable
  global Fontbutton
  global Fontcolor
  global ChBgMode
  global UserZahl
  Nachricht=StringVar()
  chvariable=StringVar()
  pmvariable=StringVar()
  PMNachricht=StringVar()
  PMReceiver=StringVar()
  roomvariable=StringVar()
  Fontbutton=StringVar()
  Fontcolor=StringVar()
  ChBgMode=StringVar()
  UserZahl=StringVar()

  ######################################
  global text
  global texttwo
  global entry
  global entry2


  label2=Label(frame, text="PM Recipient")
  label2.grid(column=2, row=2)

  label3=Label(frame, text="PM Message")
  label3.grid(column=2,row=4)

  label4=Label(frame, text="Message")
  label4.grid(column=1,row=2)

  label5=Label(frame, text="Room")
  label5.grid(column=1,row=5)

  label6=Label(frame, textvariable=Fontbutton)
  label6.grid(column=1,row=10,sticky=(N,W))

  label7=Label(frame, textvariable=Fontcolor)
  label7.grid(column=1,row=8, sticky=(N,W))

  label8=Label(frame, textvariable=ChBgMode)
  label8.grid(column=2,row=10)

  label9=Label(frame, textvariable=UserZahl)
  label9.grid(column=2,row=11)

  entry=Entry(frame, textvariable=Nachricht, width=60)
  entry.grid(column=1, row=3)

  entry2=Entry(frame, textvariable=PMNachricht, width=50)
  entry2.grid(column=2, row=5, sticky=(N,))

  entry3=Entry(frame, textvariable=PMReceiver)
  entry3.grid(column=2,row=3)

  entry4=Entry(frame, textvariable=roomvariable)
  entry4.grid(column=1,row=6)


  button2=Button(frame, text="Send", command=Post_Message)
  button2.grid(column=1,row=4)


  button4=Button(frame, text="Send", command=Post_PMMessage)
  button4.grid(column=2,row=6)

  button5=Button(frame, text="Switch Room", command=Switch_Room)
  button5.grid(column=1,row=7)

  button6=Button(frame, text="Turn bg on", command=Switch_Bgmode_On)
  button6.grid(column=2,row=8)

  button7=Button(frame, text="Turn bg off", command=Switch_Bgmode_Off)
  button7.grid(column=2,row=9)

  button8=Button(frame, text="Change font size", command=Switch_Fontsize)
  button8.grid(column=1,row=11, sticky=(N,W))

  button9=Button(frame, text="Change font color", command=Switch_Fontcolor)
  button9.grid(column=1,row=9, sticky=(N,W))

  ###################Text###########
  text=Text(frame, width=40, height=20, bg="#CCCCCC", font="Ariel",wrap=WORD)
  text.grid(column=1, row=1, sticky=(N, W), padx=10)

  texttwo=Text(frame,width=40,height=20,bg="#CCCCCC", font="Ariel", wrap=WORD)
  texttwo.grid(column=2,row=1, sticky=(N, E))

  scrollbar=Scrollbar(frame,orient=VERTICAL,command=text.yview,width=10)
  scrollbar.grid(column=1,row=1, sticky=(N,S,W))
  text.configure(yscrollcommand=scrollbar.set)


gui_thread = threading.Thread(target=mainloop())
gui_thread.setDaemon(True)
gui_thread.start()
