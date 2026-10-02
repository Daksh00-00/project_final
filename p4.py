import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime
import backend
#window
window=ttk.Window(themename="minty")

window.geometry("900x600")
window.config(background="#F3F6EA")
window.title("Green care")

#image ig
og_image=Image.open("school_practical\\school_project\\back.png")

#canvas
canvas=ttk.Canvas(master=window,highlightthickness=0)
canvas.pack(fill="both",expand=True)

#resize the background 
def back_ground(event):
    new_image=og_image.resize((event.width,event.height))
    new_image=ImageTk.PhotoImage(new_image)

    canvas.itemconfig(background,image=new_image)
    canvas.image=new_image
background=canvas.create_image(0,0,image=ImageTk.PhotoImage(og_image),
                               anchor="nw")
canvas.bind("<Configure>",back_ground)

#frame style
style = ttk.Style()
style.configure("Green.TFrame",
                 background="#F3F6EA")
#button style
style.configure("Zap.TButton",
                 background="#215A17",
                 foreground="#C1DAC3",
                 bordercolor="#21471A")
style.map("Zap.TButton",
          background=[("active", "#25561B")],
          foreground=[("active", "#FFFFFF")])
#main frame
main_frame=ttk.Frame(master=window,
                     style="Green.TFrame",
                     width=400,height=400)
#title frame 
frame1=ttk.Frame(master=main_frame,
                 style="Green.TFrame")
#title
title_label=ttk.Label(master=frame1,text="Green Care",
                     font=("Segoe UI",25,"bold"),
                     background="#F3F6EA",
                     foreground="#2F5D50")
title_label.pack(pady=30,padx=10)

#welcome
welcome_label=ttk.Label(master=frame1,
                        text="Welcome",
                        font=("roboto",20,"bold"),
                        background="#F3F6EA",
                        foreground="#2F5D50")
welcome_label.pack(pady=20)
##
frame1.pack()

#button frame 
frame2=ttk.Frame(master=main_frame,
                 style="Green.TFrame")
#button
admin_button=ttk.Button(master=frame2,text="Admin",
                        width=20,
                        style="Zap.TButton",
                        command= lambda:open_login("Admin"))
admin_button.pack(pady=20)

client_button=ttk.Button(master=frame2,text="Client",
                         width=20,style="Zap.TButton",
                         command= lambda:open_login("Client"))
client_button.pack(pady=20)

about_button=ttk.Button(master=frame2,text="About",style="Zap.TButton",
                        command=lambda:messagebox.showinfo("About","Green Care is an establishment started on 2026 ,which aims to focus on providing quality health care."))
about_button.pack(pady=10)
##
frame2.pack(pady=25)
##
main_frame.place(relx=0.5,rely=0.5,anchor="center")


#admin and client and whoever  login thingy
current_user=""
def open_login(user_type):
    global current_user
    current_user=user_type
    main_frame.place_forget()
    login_title.config(text=user_type + " Login")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

def back_ig():
    login_frame.place_forget()
    main_frame.place(relx=0.5,rely=0.5,anchor="center")

#login frame
login_frame = ttk.Frame(
    master=window,style="Green.TFrame",width=400,
    height=400)

#login title
login_title = ttk.Label(master=login_frame,text="Admin Login",
font=("Segoe UI", 25, "bold"),background="#F3F6EA",foreground="#2F5D50")
login_title.pack(pady=30)

#username
username_label = ttk.Label(master=login_frame,text="Username",
font=("Segoe UI", 12, "bold"),background="#F3F6EA",foreground="#2F5D50")
username_label.pack()

login_user_var=ttk.StringVar()

username_entry = ttk.Entry(master=login_frame, width=30,textvariable=login_user_var)
username_entry.pack(pady=5,padx=50)

#password
password_label = ttk.Label(master=login_frame,text="Password",
        font=("Segoe UI", 12, "bold"),background="#F3F6EA",foreground="#2F5D50")
password_label.pack(pady=(15, 0))

login_pass_var=ttk.StringVar()

password_entry = ttk.Entry(master=login_frame,width=30,show="*",
    textvariable=login_pass_var)
password_entry.pack(pady=5,padx=50)

#login button
login_button = ttk.Button(master=login_frame,text="Login",
    width=20,style="Zap.TButton",command=lambda:login_user())
login_button.pack(pady=20)

#register
def register():
    login_frame.place_forget()
    regi_title.config(text=current_user + " account")

    #Show pass key only for Admin
    if current_user == "Admin":
        create_frame.pack_forget()
        passkey_frame.pack()
        create_frame.pack()
    else:
        passkey_frame.pack_forget()
    
    regi_frame.place(relx=0.5, rely=0.5, anchor="center")

# register button
register_button = ttk.Button(master=login_frame,text="Register",
    width=20,style="Zap.TButton",command=lambda:register())
register_button.pack()

#back button
back_button = ttk.Button(master=login_frame,text="← Back",
    bootstyle="link-success",command=back_ig)
back_button.pack(pady=15)

#registreing function
def create_account():
    username=regi_username_var.get()
    password=regi_pass_var.get()
    con_password=regi_passcon_var.get()
    passkey=pass_key.get()

    if username=="" or password=="" or con_password=="":
        messagebox.showwarning("Missing Informaion","Please fill all the fields")
        return

    if password != con_password:
        messagebox.showerror("Password error","Passwords do not match")
        return

    if current_user=="Admin" and passkey=="":
        messagebox.showwarning("Missing Information","Please enter the Pass Key")
        return
    ok,message=backend.create_user(username.strip(),password,passkey,current_user)
    if ok:
        messagebox.showinfo("Success",message)
    else:
        messagebox.showerror("Error",message+
            "\nReceived: "+repr(passkey)+
            "\nExpected: "+repr(backend.ADMIN_PASSKEY)+
            "\nBackend file: "+backend.__file__)
#login function (og)
def login_user():

    username=login_user_var.get().strip()
    password=login_pass_var.get()

    if username=="" or password=="":
        messagebox.showwarning("Missing information!",
                               "PLease enter both username and password")
        return
    result=backend.check_login(username,password,current_user)

    if result:
        login_frame.place_forget()
        if current_user=="Admin":
            open_admin_window()

        elif current_user=="Client":
            open_client_window(username)
    else:
        messagebox.showerror("Login failed!","Incorrect username or password")

#register frame
regi_frame=ttk.Frame(master=window,style="Green.TFrame",
    width=400,height=500)

#reistre title
regi_title = ttk.Label(master=regi_frame,text="Register",
    font=("Segoe UI", 25, "bold"),background="#F3F6EA",
    foreground="#2F5D50")
regi_title.pack(pady=30)

#register username
regi_username_label = ttk.Label(master=regi_frame,text="Username",
    font=("Segoe UI", 12, "bold"),background="#F3F6EA",
    foreground="#2F5D50")
regi_username_label.pack()

regi_username_var=ttk.StringVar()

regi_username_entry = ttk.Entry(master=regi_frame,width=30,
                                textvariable=regi_username_var)
regi_username_entry.pack(pady=5,padx=50)

#registering password
regi_password_label1 = ttk.Label(master=regi_frame,text="Password",
    font=("Segoe UI", 12, "bold"),background="#F3F6EA",
    foreground="#2F5D50")
regi_password_label1.pack(pady=(15, 0))

regi_pass_var=ttk.StringVar()

regi_password_entry1 = ttk.Entry(master=regi_frame,width=30,
    show="*",textvariable=regi_pass_var)
regi_password_entry1.pack(pady=5,padx=50)

#pass confirmation

regi_passcon_var=ttk.StringVar()

regi_password_label2 = ttk.Label(master=regi_frame,text="Confirm Password",
    font=("Segoe UI", 12, "bold"),background="#F3F6EA",
    foreground="#2F5D50")
regi_password_label2.pack(pady=(15, 0))

regi_password_entry2 = ttk.Entry(master=regi_frame,width=30,
    show="*",textvariable=regi_passcon_var)
regi_password_entry2.pack(pady=5,padx=50)

#pass key frame
passkey_frame=ttk.Frame(master=regi_frame,style="Green.TFrame",)
passkey_frame.pack(pady=15)

#create account frame
create_frame=ttk.Frame(master=regi_frame,style="Green.TFrame")
create_frame.pack(side="top",pady=10)

#pass key 
regi_key = ttk.Label(master=passkey_frame,text="Pass Key",
        font=("Segoe UI", 12, "bold"),background="#F3F6EA",
        foreground="#2F5D50")
regi_key.pack(pady=(15, 0))

#pass key for admin
pass_key=ttk.StringVar()

pass_key_entry=ttk.Entry( master=passkey_frame,
width=30, textvariable=pass_key,show='*')
pass_key_entry.pack(pady=15)

#create account
create_button = ttk.Button(master=create_frame,text="Create Account",
    width=20,style="Zap.TButton",command=create_account)
create_button.pack(pady=10)

#registration back button ,the function
def register_back():
    regi_frame.place_forget()

    login_frame.place(relx=0.5,rely=0.5,anchor="center")

#registration back button 
regi_back_button = ttk.Button(master=create_frame,text="← Back",
    bootstyle="link-success",command=lambda: register_back())
regi_back_button.pack(pady=15)

def logout(current_window):
    current_window.destroy()
    window.deiconify()
    main_frame.place(relx=0.5,rely=0.5,anchor="center")

def open_admin_window():

    window.withdraw()
    admin_window=ttk.Toplevel(window)

    admin_window.title("Green Care - Admin Dashboard")
    admin_window.geometry("1100x700")
    admin_window.minsize(1000,650)

    style.configure("Side.TFrame",
                    background="#163D12")

    #sidebar
    sidebar=ttk.Frame(admin_window,width=210,style="Side.TFrame" )
    sidebar.pack(side="left",fill="y")
    sidebar.pack_propagate(False)
    style.configure("Side.TButton",background="#163D12",
                foreground="#C1DAC3")
    style.map("Side.TButton",background=[("active","#25561B")],
          foreground=[("active","#FFFFFF")])
    
    logo=ttk.Label(sidebar,text="GREEN CARE",
        background="#215A17",foreground="#FFFFFF",
        font=("Arial",18,"bold"))
    logo.pack(pady=(30,40))

    dashboard_button=ttk.Button(sidebar,text="Dashboard",
        style="Side.TButton")

    dashboard_button.pack(fill="x",padx=15,pady=5)

    doctors_button=ttk.Button(sidebar,text="Doctors",
        style="Side.TButton")

    doctors_button.pack(fill="x",padx=15,pady=5)

    patients_button=ttk.Button(sidebar,text="Patients",
        style="Side.TButton")

    patients_button.pack(fill="x",padx=15,pady=5)

    medicines_button=ttk.Button(sidebar,text="medicines",
        style="Side.TButton")

    medicines_button.pack(fill="x",padx=15,pady=5)

    reports_button=ttk.Button(sidebar,text="Reports",
        style="Side.TButton")

    reports_button.pack(fill="x",padx=15,pady=5)

    settings_button=ttk.Button(sidebar,text="Settings",
        style="Side.TButton")

    settings_button.pack(fill="x",padx=15,pady=5)

    logout_button=ttk.Button(sidebar,text="Logout",
        style="Side.TButton",command=lambda:logout(admin_window))

    logout_button.pack(side="bottom",fill="x",
        padx=15,pady=20)

    #main content
    content=ttk.Frame(admin_window,padding=30)

    content.pack(side="left",fill="both",expand=True)

    dashboard_frame=ttk.Frame(content)
    dashboard_frame.pack(fill="both",expand=True)

    welcome=ttk.Label(dashboard_frame,text="Welcome, Admin",
        font=("Arial",24,"bold"))
    welcome.pack(anchor="w")

    subtitle=ttk.Label(dashboard_frame,text="Manage and monitor Green Care",
        font=("Arial",11))

    subtitle.pack(anchor="w",pady=(5,25))

    #statistics cards

    cards_frame=ttk.Frame(dashboard_frame)

    cards_frame.pack(fill="x",pady=(0,25))

    style.configure("Card.TFrame",background="#3D6732",borderwidth=3,relif="solid",
                    highlightbackground="#365D2C",highlightthickness=3)

    #doctor card
    doctor_card=ttk.Frame(cards_frame,padding=20,style="Card.TFrame")
    doctor_card.pack(side="left",fill="both",expand=True,padx=(0,10))
    doctor_title=ttk.Label(doctor_card,text="Doctors",font=("Arial",11))
    doctor_title.pack(anchor="w")
    doctor_value=ttk.Label(doctor_card,text="12",font=("Arial",24,"bold"))
    doctor_value.pack(anchor="w",pady=(8,0))

    #patient card
    patient_count_var=ttk.StringVar()
    patient_card=ttk.Frame(cards_frame,padding=20,style="Card.TFrame")
    patient_card.pack(side="left",fill="both",expand=True,padx=10)
    patient_title=ttk.Label(patient_card,text="patients",font=("Arial",11))
    patient_title.pack(anchor="w")
    patient_value=ttk.Label(patient_card,textvariable=patient_count_var,
        font=("Arial",24,"bold"))
    patient_value.pack(anchor="w",pady=(8,0)) 

    #appointment card

    appointment_card=ttk.Frame(cards_frame,padding=20,style="Card.TFrame")

    appointment_card.pack(side="left",fill="both",expand=True,padx=10)

    appointment_title=ttk.Label(appointment_card,text="Appointments",
        font=("Arial",11))

    appointment_title.pack(anchor="w")

    appointment_value=ttk.Label(appointment_card,text="82",
        font=("Arial",24,"bold"))

    appointment_value.pack(anchor="w",pady=(8,0))

    #pending card

    pending_card=ttk.Frame(cards_frame,padding=20,style="Card.TFrame")

    pending_card.pack(side="left",fill="both",expand=True,padx=(10,0))

    pending_title=ttk.Label(pending_card,text="Pending",font=("Arial",11))

    pending_title.pack(anchor="w")

    pending_value=ttk.Label(pending_card,text="14",font=("Arial",24,"bold"))

    pending_value.pack(anchor="w",pady=(8,0))

    #graph code 
    #patient graph

    style.configure("Graph.TFrame",background="#FFFFFF",
                borderwidth=3,relief="solid")

    graph_frame=ttk.Frame(dashboard_frame,padding=20,style="Graph.TFrame")
    graph_frame.pack(fill="both",expand=True,pady=(0,25))

    graph_title=ttk.Label(graph_frame,text="Patient Registrations",
        font=("Arial",16,"bold"))
    graph_title.pack(anchor="w",pady=(0,10))

    # choose how many months to show
    months_box=ttk.Combobox(graph_frame,values=["6 months","12 months"],
        state="readonly",width=12)
    months_box.set("6 months")
    months_box.pack(anchor="w",pady=(0,10))

    graph_canvas=tk.Canvas(graph_frame,height=220,background="#FFFFFF",
        highlightthickness=0)
    graph_canvas.pack(fill="both",expand=True)

    # count patients per month for the last few months
    def get_graph_data():
        months_to_show=int(months_box.get().split()[0])
        year=datetime.now().year
        month=datetime.now().month

        periods=[]
        for i in range(months_to_show):
            periods.append((year,month))
            month-=1
            if month==0:
                month=12
                year-=1
        periods.reverse()

        result=[]
        for y,m in periods:
            key=f"{y}-{m:02d}"
            count=len([p for p in patients if p[4].startswith(key)])
            label=datetime(y,m,1).strftime("%b")
            result.append((label,count))
        return result

    def draw_graph():

        graph_canvas.delete("all")

        width=graph_canvas.winfo_width()
        height=graph_canvas.winfo_height()

        # canvas not visible yet
        if width<=1:
            return

        data=get_graph_data()

        left=50
        right=30
        top=20
        bottom=40

        graph_width=width-left-right
        graph_height=height-top-bottom

        max_value=max(max(value for month,value in data),1)

        x_gap=graph_width/max(len(data)-1,1)

        points=[]

        for i,(month,value) in enumerate(data):
            x=left+(i*x_gap)

            y=top+graph_height-(value/max_value)*graph_height

            points.append((x,y))
            graph_canvas.create_oval(x-4,y-4,x+4,y+4,fill="#4F7D45",
                                     outline="")
            graph_canvas.create_text(x,y-15,text=value)
            graph_canvas.create_text(x,height-bottom+20,text=month)

        for i in range(len(points)-1):
            graph_canvas.create_line(
                points[i][0],
                points[i][1],
                points[i+1][0],
                points[i+1][1],
                fill="#4F7D45",
                width=3)

    # update the patient card and the graph together
    def refresh_dashboard():
        patient_count_var.set(str(len(patients)))
        draw_graph()
    # redraw on resize and when the dropdown changes
    graph_canvas.bind("<Configure>",lambda event:draw_graph())
    months_box.bind("<<ComboboxSelected>>",lambda event:draw_graph())
    graph_canvas.after(100,refresh_dashboard)

    #page switching
    current_page={"frame":None}

    def clear_page():
        dashboard_frame.pack_forget()
        if current_page["frame"] is not None:
            current_page["frame"].destroy()
            current_page["frame"]=None

    def show_dashboard():
        clear_page()
        dashboard_frame.pack(fill="both",expand=True)
        graph_canvas.after(100,refresh_dashboard)

    #doctors button shows all thisss
    # temporary doctor data
    doctors = [
        (1, "Dr. Alex", "Cardiology", "9876543210"),
        (2, "Dr. John", "Neurology", "9876543211"),
        (3, "Dr. Sara", "Pediatrics", "9876543212"),
        (4, "Dr. Mike", "Orthopedics", "9876543213")]

    def show_doctors():

        clear_page()

        # doctors page
        doctors_frame = ttk.Frame(content,padding=30)
        doctors_frame.pack(fill="both",expand=True)
        current_page["frame"]=doctors_frame

        # title
        doctors_title = ttk.Label(doctors_frame,text="Doctors",
                                  font=("Arial",24,"bold"))
        doctors_title.pack(anchor="w",pady=(0,20))

        # table frame
        table_frame = ttk.Frame(doctors_frame)
        table_frame.pack(fill="both",expand=True)

    # table style
        style.configure("Green.Treeview.Heading",
                        background="#215A17",
                        foreground="#FFFFFF",
                        font=("Arial",11,"bold"))
        style.map("Green.Treeview.Heading",
                    background=[("active","#25561B")])

        style.configure("Green.Treeview",
                        background="#F3F6EA",
                        fieldbackground="#F3F6EA",
                        foreground="#163D12",
                        rowheight=28)

        # doctor table
        doctor_table = ttk.Treeview(table_frame,
                            columns=("id","name","specialization","phone"),
                             show="headings",style="Green.Treeview")
        # column headings
        doctor_table.heading("id",text="ID")
        doctor_table.heading("name",text="Name")
        doctor_table.heading("specialization",text="Specialization")
        doctor_table.heading("phone",text="Phone")

        # column widths
        doctor_table.column("id",width=60)
        doctor_table.column("name",width=180)
        doctor_table.column("specialization", width=200)
        doctor_table.column("phone",width=150)

        # vertical scrollbar
        scrollbar = ttk.Scrollbar(table_frame,orient="vertical",
                                  command=doctor_table.yview)
        doctor_table.configure(yscrollcommand=scrollbar.set)

        # put table and scrollbar
        doctor_table.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

# show the doctors list in the table
        def refresh_table():
            doctor_table.delete(*doctor_table.get_children())
            for doctor in doctors:
                doctor_table.insert("","end",values=doctor)

        refresh_table()

        #the popup form (used for both Add and Update)
        def open_form(old_doctor=None):
            popup=ttk.Toplevel(window)
            popup.title("Doctor")
            popup.geometry("350x330")
            popup.grab_set()

            ttk.Label(popup,text="Name").pack(pady=(20,0))
            name_entry=ttk.Entry(popup,width=30)
            name_entry.pack()

            ttk.Label(popup,text="Specialty").pack(pady=(15,0))
            spec_entry=ttk.Entry(popup,width=30)
            spec_entry.pack()

            ttk.Label(popup,text="Phone").pack(pady=(15,0))
            phone_entry=ttk.Entry(popup,width=30)
            phone_entry.pack()

            # if updating, fill the boxes with the old details
            if old_doctor:
                name_entry.insert(0,old_doctor[1])
                spec_entry.insert(0,old_doctor[2])
                phone_entry.insert(0,old_doctor[3])

            def save():
                name=name_entry.get().strip()
                spec=spec_entry.get().strip()
                phone=phone_entry.get().strip()

                if name=="" or spec=="" or phone=="":
                    messagebox.showwarning("Missing information",
                        "Please fill all the fields",parent=popup)
                    return

                if old_doctor is None:
                    # add a new doctor
                    new_id=max([d[0] for d in doctors],default=0)+1
                    doctors.append((new_id,name,spec,phone))
                else:
                    # update the existing doctor
                    position=doctors.index(old_doctor)
                    doctors[position]=(old_doctor[0],name,spec,phone)

                refresh_table()
                popup.destroy()

            ttk.Button(popup,text="Save",width=20,
                       style="Zap.TButton",command=save).pack(pady=25)

        #find which doctor is clicked in the table
        def get_selected():
            selected=doctor_table.selection()
            if not selected:
                messagebox.showwarning("No selection",
                    "Please click a doctor in the table first")
                return None
            doctor_id=int(doctor_table.item(selected[0])["values"][0])
            for doctor in doctors:
                if doctor[0]==doctor_id:
                    return doctor

        #what each button does
        def add_doctor():
            open_form()

        def update_doctor():
            doctor=get_selected()
            if doctor:
                open_form(doctor)

        def delete_doctor():
            doctor=get_selected()
            if doctor:
                answer=messagebox.askyesno("Confirm delete",
                    f"Are you sure you want to delete {doctor[1]}?")
                if answer:
                    doctors.remove(doctor)
                    refresh_table()

        #the buttons
        button_frame = ttk.Frame(doctors_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,text="Insert",style="Zap.TButton",
                   command=add_doctor).pack(side="left",padx=10)
        ttk.Button(button_frame,text="Update",style="Zap.TButton",
                   command=update_doctor).pack(side="left",padx=10)
        ttk.Button(button_frame,text="Delete",style="Zap.TButton",
                   command=delete_doctor).pack(side="left",padx=10)

        # temporary patient data
    patients = [
        (1, "Ravi Kumar", "34", "9123456780", "2026-05-10"),
        (2, "Anita Das", "27", "9123456781", "2026-06-18"),
        (3, "Sam Thomas", "45", "9123456782", "2026-07-03"),
        (4, "Meera Nair", "52", "9123456783", "2026-07-21"),
        (5, "John Paul", "19", "9123456784", "2026-08-09"),
        (6, "Lisa Roy", "38", "9123456785", "2026-09-02")]

    def show_patients():

        clear_page()

        # page frame
        patients_frame = ttk.Frame(content,padding=30)
        patients_frame.pack(fill="both",expand=True)
        current_page["frame"]=patients_frame

        # title
        patients_title = ttk.Label(patients_frame,text="Patients",
                                   font=("Arial",24,"bold"))
        patients_title.pack(anchor="w",pady=(0,20))

        # table frame
        table_frame = ttk.Frame(patients_frame)
        table_frame.pack(fill="both",expand=True)

        # table style
        style.configure("Green.Treeview.Heading",
                        background="#215A17",
                        foreground="#FFFFFF",
                        font=("Arial",11,"bold"))
        style.map("Green.Treeview.Heading",
                  background=[("active","#25561B")])

        style.configure("Green.Treeview",
                        background="#F3F6EA",
                        fieldbackground="#F3F6EA",
                        foreground="#163D12",
                        rowheight=28)

        # table
        patient_table = ttk.Treeview(table_frame,
                            columns=("id","name","age","phone","registered"),
                            show="headings",style="Green.Treeview")

        patient_table.heading("id",text="ID")
        patient_table.heading("name",text="Name")
        patient_table.heading("age",text="Age")
        patient_table.heading("phone",text="Phone")
        patient_table.heading("registered",text="Registered")

        patient_table.column("id",width=60)
        patient_table.column("name",width=200)
        patient_table.column("age",width=80)
        patient_table.column("phone",width=150)
        patient_table.column("registered",width=120)

        # scrollbar
        scrollbar = ttk.Scrollbar(table_frame,orient="vertical",
                                  command=patient_table.yview)
        patient_table.configure(yscrollcommand=scrollbar.set)

        patient_table.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

        # refresh table
        def refresh_table():
            patient_table.delete(*patient_table.get_children())
            for patient in patients:
                patient_table.insert("","end",values=patient)
            refresh_dashboard()
        refresh_table()
        # popup form
        def open_form(old_patient=None):
            popup=ttk.Toplevel(window)
            popup.title("Patient")
            popup.geometry("350x330")
            popup.grab_set()

            ttk.Label(popup,text="Name").pack(pady=(20,0))
            name_entry=ttk.Entry(popup,width=30)
            name_entry.pack()

            ttk.Label(popup,text="Age").pack(pady=(15,0))
            age_entry=ttk.Entry(popup,width=30)
            age_entry.pack()

            ttk.Label(popup,text="Phone").pack(pady=(15,0))
            phone_entry=ttk.Entry(popup,width=30)
            phone_entry.pack()

            # prefill for update
            if old_patient:
                name_entry.insert(0,old_patient[1])
                age_entry.insert(0,old_patient[2])
                phone_entry.insert(0,old_patient[3])

            def save():
                name=name_entry.get().strip()
                age=age_entry.get().strip()
                phone=phone_entry.get().strip()

                if name=="" or age=="" or phone=="":
                    messagebox.showwarning("Missing information",
                        "Please fill all the fields",parent=popup)
                    return

                if not age.isdigit():
                    messagebox.showwarning("Invalid age",
                        "Age must be a number",parent=popup)
                    return

                if old_patient is None:
                    # add new
                    new_id=max([p[0] for p in patients],default=0)+1
                    today=datetime.now().strftime("%Y-%m-%d")
                    patients.append((new_id,name,age,phone,today))
                else:
                    # update existing
                    position=patients.index(old_patient)
                    patients[position]=(old_patient[0],name,age,phone,old_patient[4])

                refresh_table()
                popup.destroy()

            ttk.Button(popup,text="Save",width=20,
                       style="Zap.TButton",command=save).pack(pady=25)

        # get selected row
        def get_selected():
            selected=patient_table.selection()
            if not selected:
                messagebox.showwarning("No selection",
                    "Please click a patient in the table first")
                return None
            patient_id=int(patient_table.item(selected[0])["values"][0])
            for patient in patients:
                if patient[0]==patient_id:
                    return patient

        # button actions
        def add_patient():
            open_form()

        def update_patient():
            patient=get_selected()
            if patient:
                open_form(patient)

        def delete_patient():
            patient=get_selected()
            if patient:
                answer=messagebox.askyesno("Confirm delete",
                    f"Are you sure you want to delete {patient[1]}?")
                if answer:
                    patients.remove(patient)
                    refresh_table()

        # buttons
        button_frame = ttk.Frame(patients_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,text="Insert",style="Zap.TButton",
                   command=add_patient).pack(side="left",padx=10)
        ttk.Button(button_frame,text="Update",style="Zap.TButton",
                   command=update_patient).pack(side="left",padx=10)
        ttk.Button(button_frame,text="Delete",style="Zap.TButton",
                   command=delete_patient).pack(side="left",padx=10)
        # temporary medicine data
    medicines = [
        (1, "Paracetamol", "200", "2.50"),
        (2, "Amoxicillin", "120", "8.00"),
        (3, "Cetirizine", "90", "3.75")]

    def show_medicines():

        clear_page()

        # page frame
        medicines_frame = ttk.Frame(content,padding=30)
        medicines_frame.pack(fill="both",expand=True)
        current_page["frame"]=medicines_frame

        # title
        medicines_title = ttk.Label(medicines_frame,text="Medicines",
                                    font=("Arial",24,"bold"))
        medicines_title.pack(anchor="w",pady=(0,20))

        # table frame
        table_frame = ttk.Frame(medicines_frame)
        table_frame.pack(fill="both",expand=True)

        # table style
        style.configure("Green.Treeview.Heading",
                        background="#215A17",
                        foreground="#FFFFFF",
                        font=("Arial",11,"bold"))
        style.map("Green.Treeview.Heading",
                  background=[("active","#25561B")])

        style.configure("Green.Treeview",
                        background="#F3F6EA",
                        fieldbackground="#F3F6EA",
                        foreground="#163D12",
                        rowheight=28)

        # table
        medicine_table = ttk.Treeview(table_frame,
                            columns=("id","name","quantity","price"),
                            show="headings",style="Green.Treeview")

        medicine_table.heading("id",text="ID")
        medicine_table.heading("name",text="Medicine")
        medicine_table.heading("quantity",text="Quantity")
        medicine_table.heading("price",text="Price")

        medicine_table.column("id",width=60)
        medicine_table.column("name",width=200)
        medicine_table.column("quantity",width=100)
        medicine_table.column("price",width=100)

        # scrollbar
        scrollbar = ttk.Scrollbar(table_frame,orient="vertical",
                                  command=medicine_table.yview)
        medicine_table.configure(yscrollcommand=scrollbar.set)

        medicine_table.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

        # refresh table
        def refresh_table():
            medicine_table.delete(*medicine_table.get_children())
            for medicine in medicines:
                medicine_table.insert("","end",values=medicine)

        refresh_table()

        # popup form
        def open_form(old_medicine=None):
            popup=ttk.Toplevel(window)
            popup.title("Medicine")
            popup.geometry("350x330")
            popup.grab_set()

            ttk.Label(popup,text="Medicine name").pack(pady=(20,0))
            name_entry=ttk.Entry(popup,width=30)
            name_entry.pack()

            ttk.Label(popup,text="Quantity").pack(pady=(15,0))
            quantity_entry=ttk.Entry(popup,width=30)
            quantity_entry.pack()

            ttk.Label(popup,text="Price").pack(pady=(15,0))
            price_entry=ttk.Entry(popup,width=30)
            price_entry.pack()

            # prefill for update
            if old_medicine:
                name_entry.insert(0,old_medicine[1])
                quantity_entry.insert(0,old_medicine[2])
                price_entry.insert(0,old_medicine[3])

            def save():
                name=name_entry.get().strip()
                quantity=quantity_entry.get().strip()
                price=price_entry.get().strip()

                if name=="" or quantity=="" or price=="":
                    messagebox.showwarning("Missing information",
                        "Please fill all the fields",parent=popup)
                    return

                if not quantity.isdigit():
                    messagebox.showwarning("Invalid quantity",
                        "Quantity must be a whole number",parent=popup)
                    return

                try:
                    float(price)
                except ValueError:
                    messagebox.showwarning("Invalid price",
                        "Price must be a number",parent=popup)
                    return

                if old_medicine is None:
                    # add new
                    new_id=max([m[0] for m in medicines],default=0)+1
                    medicines.append((new_id,name,quantity,price))
                else:
                    # update existing
                    position=medicines.index(old_medicine)
                    medicines[position]=(old_medicine[0],name,quantity,price)

                refresh_table()
                popup.destroy()

            ttk.Button(popup,text="Save",width=20,
                       style="Zap.TButton",command=save).pack(pady=25)

        # get selected row
        def get_selected():
            selected=medicine_table.selection()
            if not selected:
                messagebox.showwarning("No selection",
                    "Please click a medicine in the table first")
                return None
            medicine_id=int(medicine_table.item(selected[0])["values"][0])
            for medicine in medicines:
                if medicine[0]==medicine_id:
                    return medicine

        # button actions
        def add_medicine():
            open_form()

        def update_medicine():
            medicine=get_selected()
            if medicine:
                open_form(medicine)

        def delete_medicine():
            medicine=get_selected()
            if medicine:
                answer=messagebox.askyesno("Confirm delete",
                    f"Are you sure you want to delete {medicine[1]}?")
                if answer:
                    medicines.remove(medicine)
                    refresh_table()

        # buttons
        button_frame = ttk.Frame(medicines_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,text="Insert",style="Zap.TButton",
                   command=add_medicine).pack(side="left",padx=10)
        ttk.Button(button_frame,text="Update",style="Zap.TButton",
                   command=update_medicine).pack(side="left",padx=10)
        ttk.Button(button_frame,text="Delete",style="Zap.TButton",
                   command=delete_medicine).pack(side="left",padx=10)
        
    # connect sidebar buttons (outside the functions)
    dashboard_button.config(command=show_dashboard)
    doctors_button.config(command=show_doctors)
    patients_button.config(command=show_patients)
    medicines_button.config(command=show_medicines)

# temporary client data
temp_tasks = [
    (1, "Morning ward round", "Pending"),
    (2, "Review Ravi Kumar's reports", "Pending"),
    (3, "Team meeting at 2 PM", "Done")]

temp_profiles = {}

def get_my_profile(username):
    return temp_profiles.get(username)

def save_my_profile(username,name,specialty,phone,hours):
    temp_profiles[username]=(name,specialty,phone,hours)

def get_tasks(username):
    return list(temp_tasks)

def add_task(username,text):
    new_id=max([t[0] for t in temp_tasks],default=0)+1
    temp_tasks.append((new_id,text,"Pending"))

def update_task(task_id,text,status):
    for i,t in enumerate(temp_tasks):
        if t[0]==task_id:
            temp_tasks[i]=(task_id,text,status)

def delete_task(task_id):
    temp_tasks[:]=[t for t in temp_tasks if t[0]!=task_id]

def clear_tasks(username):
    temp_tasks.clear()

def open_client_window(username):

    window.withdraw()
    client_window=ttk.Toplevel(window)

    client_window.title("Green Care - Doctor Workspace")
    client_window.geometry("1100x700")
    client_window.minsize(1000,650)

    # styles (in case the admin window was never opened)
    style.configure("Side.TFrame",background="#163D12")
    style.configure("Side.TButton",background="#163D12",
                    foreground="#C1DAC3")
    style.map("Side.TButton",background=[("active","#25561B")],
              foreground=[("active","#FFFFFF")])
    style.configure("Green.Treeview.Heading",
                    background="#215A17",
                    foreground="#FFFFFF",
                    font=("Arial",11,"bold"))
    style.map("Green.Treeview.Heading",
              background=[("active","#25561B")])
    style.configure("Green.Treeview",
                    background="#F3F6EA",
                    fieldbackground="#F3F6EA",
                    foreground="#163D12",
                    rowheight=28)

    # sidebar
    sidebar=ttk.Frame(client_window,width=210,style="Side.TFrame")
    sidebar.pack(side="left",fill="y")
    sidebar.pack_propagate(False)

    logo=ttk.Label(sidebar,text="GREEN CARE",
        background="#215A17",foreground="#FFFFFF",
        font=("Arial",18,"bold"))
    logo.pack(pady=(30,40))

    schedule_button=ttk.Button(sidebar,text="My Schedule",
        style="Side.TButton")
    schedule_button.pack(fill="x",padx=15,pady=5)

    profile_button=ttk.Button(sidebar,text="My Profile",
        style="Side.TButton")
    profile_button.pack(fill="x",padx=15,pady=5)

    logout_button=ttk.Button(sidebar,text="Logout",
        style="Side.TButton",command=lambda:logout(client_window))
    logout_button.pack(side="bottom",fill="x",padx=15,pady=20)

    # main content
    content=ttk.Frame(client_window,padding=30)
    content.pack(side="left",fill="both",expand=True)

    # remove whatever page is showing
    def clear_page():
        for widget in content.winfo_children():
            widget.destroy()

    # schedule page
    def show_schedule():
        clear_page()

        ttk.Label(content,text="My Schedule",
            font=("Arial",24,"bold")).pack(anchor="w",pady=(0,20))

        # table
        table_frame=ttk.Frame(content)
        table_frame.pack(fill="both",expand=True)

        table=ttk.Treeview(table_frame,columns=("id","task","status"),
                           show="headings",style="Green.Treeview")

        table.heading("id",text="ID")
        table.heading("task",text="Task")
        table.heading("status",text="Status")

        table.column("id",width=50)
        table.column("task",width=450)
        table.column("status",width=110)

        scrollbar=ttk.Scrollbar(table_frame,orient="vertical",
                                command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left",fill="both",expand=True)
        scrollbar.pack(side="right",fill="y")

        # refresh table
        def refresh_table():
            table.delete(*table.get_children())
            for task in get_tasks(username):
                table.insert("","end",values=task)

        refresh_table()

        # get selected task
        def get_selected():
            selected=table.selection()
            if not selected:
                messagebox.showwarning("No selection",
                    "Please click a task in the table first")
                return None
            task_id=int(table.item(selected[0])["values"][0])
            for task in get_tasks(username):
                if task[0]==task_id:
                    return task

        # popup for adding or editing a task
        def open_form(old_task=None):
            popup=ttk.Toplevel(window)
            popup.title("Task")
            popup.geometry("350x200")
            popup.grab_set()

            ttk.Label(popup,text="Task").pack(pady=(25,0))
            task_entry=ttk.Entry(popup,width=35)
            task_entry.pack(pady=5)

            # prefill for edit
            if old_task:
                task_entry.insert(0,old_task[1])

            def save():
                text=task_entry.get().strip()
                if text=="":
                    messagebox.showwarning("Missing information",
                        "Please enter a task",parent=popup)
                    return
                if old_task is None:
                    add_task(username,text)
                else:
                    update_task(old_task[0],text,old_task[2])
                refresh_table()
                popup.destroy()

            ttk.Button(popup,text="Save",width=20,
                       style="Zap.TButton",command=save).pack(pady=20)

        # button actions
        def add_new():
            open_form()

        def edit_task():
            task=get_selected()
            if task:
                open_form(task)

        def toggle_done():
            task=get_selected()
            if task:
                new_status="Pending" if task[2]=="Done" else "Done"
                update_task(task[0],task[1],new_status)
                refresh_table()

        def delete_one():
            task=get_selected()
            if task:
                answer=messagebox.askyesno("Confirm delete",
                    f"Delete the task '{task[1]}'?")
                if answer:
                    delete_task(task[0])
                    refresh_table()

        def reset_all():
            answer=messagebox.askyesno("Reset schedule",
                "This will delete ALL tasks. Continue?")
            if answer:
                clear_tasks(username)
                refresh_table()

        # buttons
        button_frame=ttk.Frame(content)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,text="Add",style="Zap.TButton",
                   command=add_new).pack(side="left",padx=5)
        ttk.Button(button_frame,text="Edit",style="Zap.TButton",
                   command=edit_task).pack(side="left",padx=5)
        ttk.Button(button_frame,text="Done / Undo",style="Zap.TButton",
                   command=toggle_done).pack(side="left",padx=5)
        ttk.Button(button_frame,text="Delete",style="Zap.TButton",
                   command=delete_one).pack(side="left",padx=5)
        ttk.Button(button_frame,text="Reset",style="Zap.TButton",
                   command=reset_all).pack(side="left",padx=5)

    # profile page
    def show_profile():
        clear_page()

        profile=get_my_profile(username)

        ttk.Label(content,text="My Profile",
            font=("Arial",24,"bold")).pack(anchor="w",pady=(0,20))

        # popup form for adding or editing details
        def open_profile_form():
            popup=ttk.Toplevel(window)
            popup.title("Profile")
            popup.geometry("350x400")
            popup.grab_set()

            ttk.Label(popup,text="Name").pack(pady=(20,0))
            name_entry=ttk.Entry(popup,width=30)
            name_entry.pack()

            ttk.Label(popup,text="Specialty").pack(pady=(15,0))
            spec_entry=ttk.Entry(popup,width=30)
            spec_entry.pack()

            ttk.Label(popup,text="Phone").pack(pady=(15,0))
            phone_entry=ttk.Entry(popup,width=30)
            phone_entry.pack()

            ttk.Label(popup,text="Working hours").pack(pady=(15,0))
            hours_entry=ttk.Entry(popup,width=30)
            hours_entry.pack()

            # prefill if details already exist
            if profile:
                name_entry.insert(0,profile[0])
                spec_entry.insert(0,profile[1])
                phone_entry.insert(0,profile[2])
                hours_entry.insert(0,profile[3])

            def save():
                name=name_entry.get().strip()
                spec=spec_entry.get().strip()
                phone=phone_entry.get().strip()
                hours=hours_entry.get().strip()

                if name=="" or spec=="" or phone=="" or hours=="":
                    messagebox.showwarning("Missing information",
                        "Please fill all the fields",parent=popup)
                    return

                save_my_profile(username,name,spec,phone,hours)
                popup.destroy()
                show_profile()

            ttk.Button(popup,text="Save",width=20,
                       style="Zap.TButton",command=save).pack(pady=25)

        # empty profile: ask for details
        if profile is None:
            ttk.Label(content,text="Your profile is empty. Please add your details.",
                font=("Arial",12)).pack(anchor="w",pady=(0,15))
            ttk.Button(content,text="Add Details",style="Zap.TButton",
                       command=open_profile_form).pack(anchor="w")
            return

        # profile card
        card=ttk.Frame(content,padding=30,relief="solid",borderwidth=1)
        card.pack(anchor="w")

        ttk.Label(card,text=profile[0],
            font=("Arial",20,"bold")).grid(row=0,column=0,columnspan=2,
                                           sticky="w",pady=(0,20))

        details=[("Specialty",profile[1]),
                 ("Phone",profile[2]),
                 ("Working hours",profile[3])]

        for i,(label,value) in enumerate(details):
            ttk.Label(card,text=label,font=("Arial",12,"bold"),
                width=16).grid(row=i+1,column=0,sticky="w",pady=8)
            ttk.Label(card,text=value,
                font=("Arial",12)).grid(row=i+1,column=1,sticky="w",pady=8)

        ttk.Button(content,text="Edit Details",style="Zap.TButton",
                   command=open_profile_form).pack(anchor="w",pady=20)

    # connect sidebar buttons
    schedule_button.config(command=show_schedule)
    profile_button.config(command=show_profile)

    #profile when clueless ,other one any other time
    if get_my_profile(username) is None:
        show_profile()
    else:
        show_schedule()
######### temporary button ,plses remember to delete ###########

test_admin_button = ttk.Button(main_frame,text="temporary button",style="Zap.TButton",command=open_admin_window)
test_client_button=ttk.Button(main_frame,text="temporary button 2",style="Zap.TButton",command=lambda:open_client_window("daksh"))

test_admin_button.pack(pady=5)
test_client_button.pack(pady=5)

########### $$$$$$$  #############
#mainloop
window.mainloop()