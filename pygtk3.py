################################################################
 
# File: CClient.py
 
# Title: Chatango Client
 
# Author: ASL97 <asl97@outlook.com>
 
# Current Maintainers: ASL97
 
# Version: 1.01
 
# Description:
 
#  A Chatango Client for linux
 
# Update:
 
#  It will print to the PM view to say it is disconnect when it disconnect
 
################################################################
 
 
 
################################################################
 
# License
 
################################################################
 
# Copyright 2013 ASL97
 
# This program is distributed under the terms of the GNU GPL.
 
################################################################
 
import chlib as ch
 
import sys
 
import time
 
import threading
 
from gi.repository import Gtk, Gdk, GLib, WebKit, GObject
 
class Login(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Login Panel", parent,
            Gtk.DialogFlags.MODAL, buttons=(
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))
 
        box = self.get_content_area()
 
        label1 = Gtk.Label("Insert your user name:")
        box.add(label1)
 
        self.entry1 = Gtk.Entry()
        box.add(self.entry1)
 
        label2 = Gtk.Label("Insert your password:")
        box.add(label2)
 
        self.entry2 = Gtk.Entry()
        box.add(self.entry2)
 
        self.show_all()
 
class Client(Gtk.Window):
 
  def __init__(self):
    Gtk.Window.__init__(self, title="asl97's chatango client")
    self.set_border_width(0)
    self.set_default_size(800,500)
 
    dialog = Login(self)
    response = dialog.run()
    if response == Gtk.ResponseType.OK:
      global nickusername
      nickusername = dialog.entry1.get_text()
      global nickpassword
      nickpassword = dialog.entry2.get_text()
    elif response == Gtk.ResponseType.CANCEL:
      sys.exit()
    dialog.destroy()
    global loginalready
    loginalready = True
 
    self.create_layout()
    self.create_msgview()
    self.create_userlist()
    self.create_pmviewer()
    self.create_entrybox()
    self.create_buttons()
    self.create_label()
 
    global client
    client = self
    self.oldroom=None
 
 
  def create_layout(self):
    self.grid = Gtk.Grid()
    self.grid.set_column_spacing(2)
    self.add(self.grid)
 
#  def create_jl(self):
#    self.scrolledwindow1 = Gtk.ScrolledWindow()
    #self.scrolledwindow1.set_hexpand(True)
    #self.scrolledwindow1.set_vexpand(True)
#    self.grid.attach(self.scrolledwindow, 0, 0, 3, 1)
#    self.room1 = Gtk.TextView()
#    self.roombuffer1 = self.room1.get_buffer()
#    self.room1.set_wrap_mode(Gtk.WrapMode.WORD)
#    self.scrolledwindow1.add(self.room1)
 
  def create_msgview(self):
    self.scrolledwindow1 = Gtk.ScrolledWindow()
    self.scrolledwindow1.set_hexpand(True)
    self.scrolledwindow1.set_vexpand(True)
    self.grid.attach(self.scrolledwindow1, 0, 0, 3, 1)
    self.room1 = Gtk.TextView()
    self.roombuffer1 = self.room1.get_buffer()
    self.room1.set_wrap_mode(Gtk.WrapMode.WORD)
    self.scrolledwindow1.add(self.room1)
 
  def create_userlist(self):
    self.scrolledwindow2 = Gtk.ScrolledWindow()
    self.scrolledwindow2.set_hexpand(True)
    self.scrolledwindow2.set_vexpand(True)
    self.grid.attach(self.scrolledwindow2, 3, 0, 2, 1)
    self.userlist1 = Gtk.TextView()
    self.userlistbuffer1 = self.userlist1.get_buffer()
    self.userlist1.set_wrap_mode(Gtk.WrapMode.WORD)
    self.scrolledwindow2.add(self.userlist1)
 
  def create_pmviewer(self):
    self.scrolledwindow3 = Gtk.ScrolledWindow()
    self.scrolledwindow3.set_hexpand(True)
    self.scrolledwindow3.set_vexpand(True)
    self.grid.attach(self.scrolledwindow3, 5, 0, 2, 1)
    self.pm1 = Gtk.TextView()
    self.pmbuffer1 = self.pm1.get_buffer()
    self.pm1.set_wrap_mode(Gtk.WrapMode.WORD)
    self.scrolledwindow3.add(self.pm1)
    self.pmbuffer1.set_text("connecting...\n")
 
  def create_entrybox(self):
    self.addressbar1 = Gtk.Entry()
    self.grid.attach(self.addressbar1, 0, 1, 2, 1)
 
    self.addressbar2 = Gtk.Entry()
    self.grid.attach(self.addressbar2, 0, 2, 2, 1)
 
    self.addressbar3 = Gtk.Entry()
    self.grid.attach(self.addressbar3, 5, 1, 1, 1)
 
    self.addressbar4 = Gtk.Entry()
    self.grid.attach(self.addressbar4, 5, 2, 1, 1)
 
  def create_buttons(self):
    self.joinbutton = Gtk.Button("JOIN")
    self.grid.attach(self.joinbutton, 2, 1, 1, 1)
    self.joinbutton.connect('clicked', self.join_but)
 
    self.messagebutton = Gtk.Button("MESSAGE")
    self.grid.attach(self.messagebutton, 2, 2, 1, 1)
    self.messagebutton.connect("clicked", self.message_but)
 
    self.messagebutton = Gtk.Button("update\nuserlist")
    self.grid.attach(self.messagebutton, 3, 1, 2, 2)
    self.messagebutton.connect("clicked", self.userlist_but)
 
    self.messagebutton = Gtk.Button("Send")
    self.grid.attach(self.messagebutton, 6, 2, 1, 1)
    self.messagebutton.connect("clicked", self.pm_but)
 
  def create_label(self):
    self.userlabel = Gtk.Label()
    self.userlabel.set_text("PM Recipient")
    self.grid.attach(self.userlabel, 6, 1, 1, 1)
 
  def join_but(self, widget):
    room = self.addressbar1.get_text()
    self.checkroom(room)
 
  def message_but(self, widget):
    room = TestBot.getRoom(self.addressbar1.get_text())
    room.message(self.addressbar2.get_text())
 
  def userlist_but(self, widget):
    room = TestBot.getRoom(self.addressbar1.get_text())
    userlist = room.usernames
    Client.getuserlist(room, userlist)
 
  def pm_but(self, widget):
    user = ch.User(self.addressbar3.get_text())
    pmMsg = self.addressbar4.get_text()
    TestBot.pm.message(user, pmMsg)
    Client.getpm("you:"+pmMsg)
 
  def printmsg(self, widget, msg):
    Gdk.threads_enter()
    endoftext = self.roombuffer1.get_end_iter()
    self.roombuffer1.insert(endoftext,msg+"\n")
    mark = self.roombuffer1.get_insert()
    self.room1.scroll_mark_onscreen(self.roombuffer1.get_insert())
    Gdk.threads_leave()
 
  def getmsg(msg):
    global client
    Client.printmsg(client,Client.printmsg,msg)
 
  def printpm(self, widget, pm):
    endoftext = self.pmbuffer1.get_end_iter()
    self.pmbuffer1.insert(endoftext,pm+"\n")
    mark = self.pmbuffer1.get_insert()
    self.pm1.scroll_mark_onscreen(self.pmbuffer1.get_insert())
 
  def getpm(pm):
    global client
    Client.printpm(client,Client.printpm,pm)
 
  def printuserlist(self, widget, room, userlist):
    nowroom = TestBot.getRoom(self.addressbar1.get_text())
    if nowroom == room:
      user = "\n".join(sorted(userlist))
      self.userlistbuffer1.set_text(user)
 
  def getuserlist(room, userlist):
    global client
    Client.printuserlist(client,Client.printuserlist,room,userlist)
 
  def checkroom(self, room):
    self.roombuffer1.set_text("connecting...\n")
    newroom = room
    if self.oldroom != None:
      TestBot.leaveRoom(self.oldroom)
    TestBot.joinRoom(newroom)
    self.oldroom = newroom
   
 
  def run():
    win = Client()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    GObject.threads_init()
    GLib.threads_init()
    Gdk.threads_init()
    Gdk.threads_enter()
    Gtk.main()
    Gdk.threads_leave()
 
Client_thread = threading.Thread(target=Client.run,)
Client_thread.setDaemon(True)
Client_thread.start()
 
global loginalready
loginalready = False
while loginalready == False:
  pass
 
 
class TestBot(ch.RoomManager):
 
  def onConnect(self, room):
 
    Client.getmsg("Connected to "+room.name)
 
 
  def onReconnect(self, room):
 
    print("Reconnected to "+room.name)
 
 
  def onDisconnect(self, room):
 
    print("Disconnected from "+room.name)
 
   
  def onPMConnect(self, pm):
   
    Client.getpm("PM Connected")
 
  def onPMDisconnect(self, pm):
 
    Client.getpm("PM Disconnected")
 
  def onHistoryMessage(self, room, user, message):
 
    Client.getmsg(user.name+": "+message.body)
 
   
  def onMessage(self, room, user, message):
 
    Client.getmsg(user.name+": "+message.body)
 
 
  def onFloodWarning(self, room):
 
    Client.getmsg("you have been flood ban")
 
 
  def onFloodBanRepeat(self, room):
 
    Client.getmsg("you are still flood ban")
 
 
  def onPMMessage(self, pm, user, body):
 
   Client.getpm(user.name+": "+body)
 
  def onUserCountChange(self, room):
 
    userlist = room.usernames
    Client.getuserlist(room, userlist)
 
  def onPMOfflineMessage(self, pm, user, body):
 
    Client.getpm("old:"+user.name+": "+body)
 
  def onJoin(self, room, user):
 
    pass
 
  def onJoin(self, room, user):
 
    pass
 
global nickusername
global nickpassword
NICK = nickusername
PASS = nickpassword
 
TestBot = TestBot(NICK,PASS)
 
TestBot._userlistMode = ch.Userlist_All
 
TestBot_thread = threading.Thread(target=TestBot.main,)
TestBot_thread.setDaemon(True)