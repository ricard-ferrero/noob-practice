from tkinter import *
from tkinter import messagebox
from dblink import *

class Logic():

	def __init__(self):

		self.dblink = DBLink()

		self.actual_user = ""
		self.users_list = self.get_users_list()

		self.todothings_list = {}
		self.todotoday_list = {} # Done or NotDone (True, False)

	def set_actual_user(self, name):
		self.actual_user = name

	def get_actual_user(self):
		return self.actual_user

	def get_users_list(self):
		users = self.dblink.get_users()
		clean_users = []
		for n in users:
			clean_users.append(n[0])
		return clean_users

	def ask_users_list(self):
		if len(self.users_list)>0:
			return True
		else:
			return False
	
	def select_user(self, name):
		self.actual_user = name

		todo_things = self.dblink.get_todothings(self.actual_user)

		todo_things_clean = []
		for n in todo_things:
			todo_things_clean.append((n[1], n[2]))

		self.todothings_list = todo_things_clean

	def new_user(self, name):
		self.dblink.set_user(name)
		self.users_list = self.get_users_list()

	def delete_user(self, name):
		self.dblink.delete_user(name)
		self.users_list = self.get_users_list()

	def set_todo(self, thing, comment):
		self.dblink.set_todothing((self.actual_user, thing, comment))

	def get_todothings_list(self):
		self.todothings_list = {}
		todolist = self.dblink.get_todothings(self.actual_user)
		
		for n in todolist:
			self.todothings_list[n[1]] = n[2]

		return self.todothings_list

	def get_todothings_list_array(self):
		todolist = self.get_todothings_list()
		
		things = []

		for n in todolist:
			things.append(n)

		return things

	def delete_todothing(self, thing):
		self.dblink.delete_todothing(thing)

		self.todothings_list = self.get_todothings_list()
		return self.get_todothings_list()

	def edit_todothing(self, old_thing, new_thing, new_comment):
		self.dblink.update_todothing(old_thing, new_thing, new_comment)

		self.todothings_list = self.get_todothings_list()
		return self.get_todothings_list()

	def set_todotoday_list(self, today_list):
		self.todotoday_list = {}
		self.todothings_list = self.get_todothings_list()

		for n in today_list:
			self.todotoday_list[n] = self.todothings_list[n]

	def get_todotoday_list(self):
		return self.todotoday_list

# CONSTANTES:
PX = 10
PY = 5


class UI():

	def __init__(self):

		self.logic = Logic()

		self.root = Tk()
		self.root.title("ToDo App")
		self.root.geometry("800x600")

		self.frame_user = Frame(self.root)
		self.frame_user.pack()

		self.actualuser_var = StringVar(value=self.logic.get_actual_user())
		self.actualuser_label = Label(self.frame_user, textvariable=self.actualuser_var)
		self.actualuser_label.pack()

		self.frame_main = Frame(self.root)
		self.frame_main.pack()

		self.todotoday_label = Label(self.frame_main, text="ToDo Today:", font=("Arial",25))
		self.todotoday_label.grid(row=0, column=0, columnspan=2, pady=20)

		self.todotoday_listbox = Listbox(self.frame_main, width=60, height=20)
		self.todotoday_listbox.grid(row=1, column=0, rowspan=2, pady=20, padx=10)
		self.todotoday_done = {}

		self.button_done = Button(self.frame_main, text="Done", command=self.done)
		self.button_done.grid(row=1, column=1, padx=10)


		self.button_delete = Button(self.frame_main, text="Delete", command=self.delete)
		self.button_delete.grid(row=2, column=1, padx=10)

		self.menu = Menu(self.root)
		self.root.config(menu=self.menu)

		self.menu_file = Menu(self.menu, tearoff=0)
		self.menu_todo = Menu(self.menu, tearoff=0)
		self.menu_about = Menu(self.menu, tearoff=0)

		self.menu.add_cascade(label="File", menu=self.menu_file)
		self.menu.add_cascade(label="To Do", menu=self.menu_todo)
		self.menu.add_cascade(label="About...", menu=self.menu_about)
		
		self.menu_file.add_command(label="Log In", command=self.log_in)
		self.menu_file.add_command(label="New user", command=self.new_user)
		self.menu_file.add_command(label="Change user", command=self.change_user)
		self.menu_file.add_separator()
		self.menu_file.add_command(label="Delete user", command=self.delete_user)
		self.menu_file.add_separator()
		self.menu_file.add_command(label="Exit", command=self.exit)

		self.menu_todo.add_command(label='New "ToDo" thing', command=self.new_todo_thing)
		self.menu_todo.add_command(label='Edit "ToDo" list', command=self.edit_todo_list)
		self.menu_todo.add_separator()
		self.menu_todo.add_command(label='Create "ToDo Today" list', command=self.create_todotoday_list)
		self.menu_todo.add_command(label='Edit "ToDo Today" list', command=self.edit_todotoday_list)
		self.menu_todo.add_separator()
		self.menu_todo.add_command(label='Remove "ToDo Today" list', command=lambda:self.remove_todotoday_list(True))

		self.menu_about.add_command(label="Developer", command=self.developer)

		self.user_off()


	def mainloop(self):
		self.root.mainloop()

	def user_on(self):
		self.menu_file.entryconfig("Log In", state="disabled")
		self.menu_file.entryconfig("Change user", state="normal")

		self.menu_todo.entryconfig('New "ToDo" thing', state="normal")
		self.menu_todo.entryconfig('Edit "ToDo" list', state="normal")
		self.menu_todo.entryconfig('Create "ToDo Today" list', state="normal")
		self.menu_todo.entryconfig('Remove "ToDo Today" list', state="normal")

	def user_off(self):
		self.menu_file.entryconfig("Log In", state="normal")
		self.menu_file.entryconfig("Change user", state="disabled")

		self.menu_todo.entryconfig('New "ToDo" thing', state="disabled")
		self.menu_todo.entryconfig('Edit "ToDo" list', state="disabled")
		self.menu_todo.entryconfig('Create "ToDo Today" list', state="disabled")
		self.menu_todo.entryconfig('Edit "ToDo Today" list', state="disabled")
		self.menu_todo.entryconfig('Remove "ToDo Today" list', state="disabled")

	#
	# -------------------- FILE MENU --------------------------
	#

	def log_in(self): ############# DONE!!!!!!
		login_window = Toplevel()
		login_window.resizable(False,False)
		login_window.title("Log in")
		login_window.transient(master=self.root)
		login_window.grab_set()

		frame_radios = Frame(login_window)
		frame_radios.pack()

		frame_buttons = Frame(login_window)
		frame_buttons.pack()

		variable_radio = StringVar(value="0")

		def button_select_do():
			self.logic.set_actual_user(variable_radio.get())
			self.actualuser_var.set(variable_radio.get())
			
			self.user_on()

			login_window.destroy()

		button_select = Button(frame_buttons, text="Select", command=button_select_do, state=DISABLED)
		button_select.grid(row=0, column=0, padx=PX, pady=PY)

		cancel_select = Button(frame_buttons, text="Cancel", command=login_window.destroy)
		cancel_select.grid(row=0, column=1, padx=PX, pady=PY)

		def to_enable_button():
			button_select["state"] = "normal"

		if self.logic.ask_users_list():
			u_list = self.logic.get_users_list()
			
			for user in u_list:
				radio_button = Radiobutton(frame_radios, text=user, variable=variable_radio, value=user, command=to_enable_button)
				radio_button.pack(padx=PX, pady=PY, anchor="w")

		else:
			text = Label(frame_radios, text="No users.\nCreate a new user.")
			text.pack(padx=PX, pady=PY)#

	def new_user(self): ############### DONE!!!!!!!!!!!!
		newuser_window = Toplevel()
		newuser_window.resizable(False, False)
		newuser_window.title("New user")
		newuser_window.transient(master=self.root)
		newuser_window.grab_set()

		frame_entry = Frame(newuser_window)
		frame_buttons = Frame(newuser_window)

		frame_entry.pack()
		frame_buttons.pack()

		text_name = Label(frame_entry, text="Name:")
		text_name.grid(row=0, column=0, padx=PX, pady=PY)

		enter_name = Entry(frame_entry)
		enter_name.grid(row=0, column=1, padx=PX, pady=PY)
		enter_name.focus()

		def create_new_user():
			text = enter_name.get()
			if len(text) < 3:
				warning_label = Label(frame_entry, text="Minimum three characters.")
				warning_label.grid(row=1, column=0, columnspan=2)
			else:
				try:
					self.logic.new_user(text)
					newuser_window.destroy()
				except:
					warning_label = Label(frame_entry, text="This name already exists.\nUse other name.", fg="red")
					warning_label.grid(row=1, column=0, columnspan=2)

		button_create = Button(frame_buttons, text="Create", command=create_new_user)
		button_create.grid(row=0, column=0, padx=PX, pady=PY)

		button_cancel = Button(frame_buttons, text="Cancel", command=newuser_window.destroy)
		button_cancel.grid(row=0, column=1, padx=PX, pady=PY)

	def change_user(self): ############ DONE!!!!!!!!!!!!!!!!!!
		changeuser_window = Toplevel()
		changeuser_window.resizable(False,False)
		changeuser_window.title("Change user")
		changeuser_window.transient(master=self.root)
		changeuser_window.grab_set()

		frame_radios = Frame(changeuser_window)
		frame_radios.pack()

		frame_buttons = Frame(changeuser_window)
		frame_buttons.pack()

		variable_radio = StringVar(value=self.actualuser_var.get())

		u_list = self.logic.get_users_list()
		
		for user in u_list:
			radio_button = Radiobutton(frame_radios, text=user, variable=variable_radio, value=user)
			radio_button.pack(padx=PX, pady=PY, anchor="w")

		def button_select_do():
			self.logic.set_actual_user(variable_radio.get())
			self.actualuser_var.set(variable_radio.get())

			self.remove_todotoday_list()

			changeuser_window.destroy()

		button_select = Button(frame_buttons, text="Select", command=button_select_do)
		button_select.grid(row=0, column=0, padx=PX, pady=PY)
		button_cancel = Button(frame_buttons, text="Cancel", command=changeuser_window.destroy)
		button_cancel.grid(row=0, column=1, padx=PX, pady=PY)

	def delete_user(self): ############### DONE!!!!!!!!!!
		deleteuser_window = Toplevel()
		deleteuser_window.resizable(False,False)
		deleteuser_window.title("Delete user")
		deleteuser_window.transient(master=self.root)
		deleteuser_window.grab_set()

		frame_radios = Frame(deleteuser_window)
		frame_radios.pack()

		frame_buttons = Frame(deleteuser_window)
		frame_buttons.pack()

		def to_enable_button():
			button_delete["state"] = "normal"

		variable_radio = StringVar(value="0")

		if self.logic.ask_users_list():
			u_list = self.logic.get_users_list()

			for user in u_list:
				radio_button = Radiobutton(frame_radios, text=user, variable=variable_radio, value=user, command=to_enable_button)
				radio_button.pack(padx=PX, pady=PY, anchor="w")
		else:
			text = Label(frame_radios, text="No users to delete.")
			text.pack(padx=PX, pady=PY)

		def button_delete_do():
			text = "Do you want to delete "+variable_radio.get()+"?\nIf you accept, all user data will be lost."
			asking = messagebox.askquestion("Delete user selected", text)
			
			if asking == "yes":
				if variable_radio.get() == self.logic.get_actual_user():
					self.logic.delete_user(variable_radio.get())
					self.logic.set_actual_user("")
					self.actualuser_var.set("")
					self.user_off()
					self.remove_todotoday_list()

				else:
					self.logic.delete_user(variable_radio.get())

			deleteuser_window.destroy()

		button_delete = Button(frame_buttons, text="Delete", state=DISABLED, command=button_delete_do)
		button_delete.grid(row=0, column=0, padx=PX, pady=PY)

		button_cancel = Button(frame_buttons, text="Cancel", command=deleteuser_window.destroy)
		button_cancel.grid(row=0, column=1, padx=PX, pady=PY)

	def exit(self): ############### DONE!!!!!!!
		exit_window = messagebox.askquestion("Exit", "Are you sure?")

		if exit_window == "yes":
			self.root.destroy()

	#
	# ----------------- TO DO MENU -------------------------------
	#

	def new_todo_thing(self):
		pop_window = Toplevel()
		pop_window.resizable(False,False)
		pop_window.title('New "ToDo" thing')
		pop_window.transient(master=self.root)
		pop_window.grab_set()

		frame_data = Frame(pop_window)
		frame_data.pack()

		frame_buttons = Frame(pop_window)
		frame_buttons.pack()

		todo_label = Label(frame_data, text="ToDo:")
		todo_label.grid(row=0, column=0, padx=PX, pady=PY, sticky="w")
		todo_entry = Entry(frame_data)
		todo_entry.grid(row=0, column=1, padx=PX, pady=PY)
		todo_entry.focus()

		comment_label = Label(frame_data, text="Comment:")
		comment_label.grid(row=1, column=0, padx=PX, pady=PY, sticky="w")
		
		frame_text = Frame(frame_data)
		frame_text.grid(row=1, column=1, padx=PX, pady=PY)
		
		comment_entry = Text(frame_text, width=19, height=5)
		comment_entry.grid(row=0, column=0)

		scroll = Scrollbar(frame_text, command=comment_entry.yview)
		scroll.grid(row=0, column=1, sticky="ns")
		comment_entry.config(yscrollcommand=scroll.set)

		def create_todo():
			todothing = todo_entry.get()
			comment = comment_entry.get(1.0, END)

			if len(todothing) < 3:
				warning_label = Label(frame_buttons, text="ToDo thing must be at least three characters.", fg="red")
				warning_label.grid(row=1, column=0, columnspan=2)
			else:
				try:
					self.logic.set_todo(todothing, comment)
					pop_window.destroy()
				except:
					warning_label = Label(frame_buttons, text="This ToDo thing already exists.", fg="red")
					warning_label.grid(row=1, column=0, columnspan=2)

		button_create = Button(frame_buttons, text="Create", command=create_todo)
		button_create.grid(row=0, column=0, padx=PX, pady=PY)
		button_cancel = Button(frame_buttons, text="Cancel", command=pop_window.destroy)
		button_cancel.grid(row=0, column=1, padx=PX, pady=PY)


	def edit_todo_list(self):
		pop_window = Toplevel()
		pop_window.resizable(False,False)
		pop_window.title('Edit "ToDo" list')
		pop_window.transient(master=self.root)
		pop_window.grab_set()

		frame_listbox = Frame(pop_window)
		frame_listbox.grid(row=0, column=0, padx=PX, pady=PY)

		frame_info = Frame(pop_window)
		frame_info.grid(row=1, column=0, columnspan=2)

		frame_buttons = Frame(pop_window)
		frame_buttons.grid(row=0, column=1, rowspan=2)

		todo_listbox = Listbox(frame_listbox, width=20, height=15)

		scrollbar = Scrollbar(frame_listbox, orient=VERTICAL)
		todo_listbox.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=todo_listbox.yview)
		scrollbar.pack(side=RIGHT, fill=Y)
		todo_listbox.pack()

		info_todo_var = StringVar(value="")
		info_todo_label = Label(frame_info, textvariable=info_todo_var, justify=LEFT, font=("Arial", 12, "bold"))
		info_todo_label.pack(pady=PY, padx=PX)

		info_comment_var = StringVar(value="")
		info_comment_label = Label(frame_info, textvariable=info_comment_var, justify=LEFT)
		info_comment_label.pack(pady=PY, padx=PX)

		todo_list = self.logic.get_todothings_list()

		for n in todo_list:
			todo_listbox.insert(END, n)

		def look():
			todo_list = self.logic.get_todothings_list()
			index = todo_listbox.get(ANCHOR)
			info_todo_var.set(index)
			info_comment_var.set(todo_list[index])

		def edit():
			new_pop_window = Toplevel()
			new_pop_window.resizable(False,False)
			new_pop_window.title('Edit')
			new_pop_window.transient(master=self.root)
			new_pop_window.grab_set()

			todo = todo_listbox.get(ANCHOR)
			comment = todo_list[todo]

			title_todo = Label(new_pop_window, text="ToDo:")
			title_todo.grid(row=0, column=0)
			title_comment = Label(new_pop_window, text="Comment:")
			title_comment.grid(row=1, column=0)

			entry_todo = Entry(new_pop_window)
			entry_todo.grid(row=0, column=1)
			entry_todo.insert(0, todo)

			frame_text = Frame(new_pop_window)
			frame_text.grid(row=1, column=1, padx=PX, pady=PY)

			entry_comment= Text(frame_text, width=19, height=5)
			entry_comment.grid(row=0, column=0)
			scroll = Scrollbar(frame_text, command=entry_comment.yview)
			scroll.grid(row=0, column=1, sticky="ns")
			entry_comment.config(yscrollcommand=scroll.set)
			entry_comment.insert("1.0", comment)

			frame_buttons = Frame(new_pop_window)
			frame_buttons.grid(row=2, column=0, columnspan=2)

			def do_edit():
				edited_todo = entry_todo.get()
				edited_comment = entry_comment.get("1.0", END)

				todo_list = self.logic.edit_todothing(todo, edited_todo, edited_comment)

				todo_listbox.delete(0, END)
				for n in todo_list:
					todo_listbox.insert(END, n)
				
				new_pop_window.destroy()

			button_ok = Button(frame_buttons, text="Ok", command=do_edit)
			button_ok.grid(row=0, column=0, padx=PX, pady=PY)

			button_cancel = Button(frame_buttons, text="Cancel", command=new_pop_window.destroy)
			button_cancel.grid(row=0, column=1, padx=PX, pady=PY)


		def delete():
			asking = messagebox.askquestion("Delete", "Are you sure?")

			if asking == "yes":
				todo_list = self.logic.delete_todothing(todo_listbox.get(ANCHOR))
				
				todo_listbox.delete(0, END)
				for n in todo_list:
					todo_listbox.insert(END, n)

		look_button = Button(frame_buttons, text="Look", command=look)
		look_button.pack(padx=PX, pady=PY, fill=X)

		edit_button = Button(frame_buttons, text="Edit", command=edit)
		edit_button.pack(padx=PX, pady=PY, fill=X)

		delete_button = Button(frame_buttons, text="Delete", command=delete)
		delete_button.pack(padx=PX, pady=PY, fill=X)

	def create_todotoday_list(self):
		pop_window = Toplevel()
		pop_window.resizable(False,False)
		pop_window.title('Create "ToDo Today" list')
		pop_window.transient(master=self.root)
		pop_window.grab_set()

		frame_things = Frame(pop_window)
		frame_today = Frame(pop_window)

		frame_things.grid(row=0, column=0)
		frame_today.grid(row=0, column=1)

		Label(frame_things, text="ToDo things").pack(padx=PX, pady=PY)
		Label(frame_today, text="ToDo today").pack(padx=PX, pady=PY)

		things_listbox = Listbox(frame_things)
		things_listbox.pack(padx=PX, pady=PY)

		today_listbox = Listbox(frame_today)
		today_listbox.pack(padx=PX, pady=PY)

		things_list = self.logic.get_todothings_list_array()
		today_list = []

		for n in things_list:
			things_listbox.insert(END, n)


		def to_in():
			if things_listbox.get(ANCHOR) != "":
				today_listbox.insert(END, things_listbox.get(ANCHOR))
				things_listbox.delete(ANCHOR)

		def to_out():
			things_listbox.insert(END, today_listbox.get(ANCHOR))
			today_listbox.delete(ANCHOR)

		in_button = Button(frame_things, text="In", command=to_in)
		in_button.pack(padx=PX, pady=PY)

		out_button = Button(frame_today, text="Out", command=to_out)
		out_button.pack(padx=PX, pady=PY)

		frame_buttons = Frame(pop_window)
		frame_buttons.grid(row=1, column=0, columnspan=2)

		def to_create():
			if today_listbox.get(0) == "":
				Label(frame_buttons, text="Minimum needed one element on ToDo today list", fg="red").grid(row=1, column=0, columnspan=2)
			else:
				self.logic.set_todotoday_list(today_listbox.get(0, END))
				self.set_todotoday()
				self.menu_todo.entryconfig('Edit "ToDo Today" list', state="normal")
				pop_window.destroy()

		button_create = Button(frame_buttons, text="Create", command=to_create)
		button_create.grid(row=0, column=0, padx=PX, pady=PY)

		button_cancel = Button(frame_buttons, text="Cancel", command=pop_window.destroy)
		button_cancel.grid(row=0, column=1, padx=PX, pady=PY)

	def set_todotoday(self):
		self.remove_todotoday_list()

		array = []
		
		for n in self.logic.todotoday_list:
			text = n + ": " + self.logic.todotoday_list[n]
			text = text.replace("\n"," ")
			array.append(text)
		
		for n in array:
			self.todotoday_listbox.insert(END, n)

		self.todotoday_done = {}

		for n in array:
			self.todotoday_done[n] = False

	def edit_todotoday_list(self):
		pop_window = Toplevel()
		pop_window.resizable(False,False)
		pop_window.title('Edit "ToDo Today" list')
		pop_window.transient(master=self.root)
		pop_window.grab_set()

		frame_things = Frame(pop_window)
		frame_today = Frame(pop_window)

		frame_things.grid(row=0, column=0)
		frame_today.grid(row=0, column=1)

		Label(frame_things, text="ToDo things").pack(padx=PX, pady=PY)
		Label(frame_today, text="ToDo today").pack(padx=PX, pady=PY)

		today_listbox = Listbox(frame_today)
		today_listbox.pack(padx=PX, pady=PY)

		array = []
		
		for n in self.logic.todotoday_list:
			array.append(n)
		
		for n in array:
			today_listbox.insert(END, n)

		things_listbox = Listbox(frame_things)
		things_listbox.pack(padx=PX, pady=PY)

		things_list = self.logic.get_todothings_list_array()

		for n in things_list:
			if n not in self.logic.todotoday_list:
				things_listbox.insert(END, n)

		things_list = self.logic.get_todothings_list_array()

		def to_in():
			if things_listbox.get(ANCHOR) != "":
				today_listbox.insert(END, things_listbox.get(ANCHOR))
				things_listbox.delete(ANCHOR)

		def to_out():
			things_listbox.insert(END, today_listbox.get(ANCHOR))
			today_listbox.delete(ANCHOR)

		in_button = Button(frame_things, text="In", command=to_in)
		in_button.pack(padx=PX, pady=PY)

		out_button = Button(frame_today, text="Out", command=to_out)
		out_button.pack(padx=PX, pady=PY)

		frame_buttons = Frame(pop_window)
		frame_buttons.grid(row=1, column=0, columnspan=2)

		def to_create():
			if today_listbox.get(0) == "":
				Label(frame_buttons, text="Minimum needed one element on ToDo today list", fg="red").grid(row=1, column=0, columnspan=2)
			else:
				self.logic.set_todotoday_list(today_listbox.get(0, END))
				self.set_todotoday()
				pop_window.destroy()

		button_create = Button(frame_buttons, text="Edit", command=to_create)
		button_create.grid(row=0, column=0, padx=PX, pady=PY)

		button_cancel = Button(frame_buttons, text="Cancel", command=pop_window.destroy)
		button_cancel.grid(row=0, column=1, padx=PX, pady=PY)

	def remove_todotoday_list(self, remove_from_menu=False):
		if remove_from_menu:
			ask = messagebox.askquestion("Remove ToDo Today list", "If you selected as DONE a ToDo thing in the ToDo Today list,\nit will be removed from ToDo Things list.\nAre you sure?")
			if ask == "yes":
				self.logic.todotoday_list = {}
				self.menu_todo.entryconfig('Edit "ToDo Today" list', state="disabled")
				for n in self.todotoday_done:
				
					if self.todotoday_done[n]:
				
						string = ""
				
						for i in n:
							if i == ":":
								break
							else:
								string += i
				
						self.logic.delete_todothing(string)
		
		self.todotoday_listbox.delete(0, END)
	#
	# ------------------- ABOUT MENU ----------------------------
	#

	def developer(self):
		messagebox.showinfo("Developer", "Ricard Ferrero Conde\nr.ferrero.conde@gmail.com")

	#
	# ---------------------- MAIN BUTTONS ----------------------
	#

	def done(self):
		try:
			if self.todotoday_done[self.todotoday_listbox.get(ANCHOR)]:
				self.todotoday_listbox.itemconfigure(ANCHOR, bg="white", fg="black")
				self.todotoday_done[self.todotoday_listbox.get(ANCHOR)] = False
			else:
				self.todotoday_listbox.itemconfigure(ANCHOR, bg="green", fg="white")
				self.todotoday_done[self.todotoday_listbox.get(ANCHOR)] = True
		except:
			pass

	def delete(self):
		try:
			if self.todotoday_done[self.todotoday_listbox.get(ANCHOR)]:
				ask = messagebox.askquestion("Delete DONE thing", "This ToDo thing is DONE.\nIf you remove will be removed from ToDo Things list.\nAre you sure?")

				if ask == "yes":
					string = ""
				
					for i in self.todotoday_listbox.get(ANCHOR):
						if i == ":":
							break
						else:
							string += i
				
					self.logic.delete_todothing(string)
					self.todotoday_listbox.delete(ANCHOR)
			else:
				self.todotoday_listbox.delete(ANCHOR)

		except:
			pass

if __name__ == '__main__':
	UI = UI()
	UI.mainloop()