import os, cx_Oracle, datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField, DateField, DateTimeField
from wtforms.validators import InputRequired, ValidationError, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
os.chdir("C:\Oracle\instantclient_12_2")
con = cx_Oracle.connect('patelkb27', 'V00653755', 'jasmine.cs.vcu.edu:20037/xe')


@app.route('/', methods = ['GET'])
def index():
    address = request.remote_addr
    return render_template('index.html', user_address=address)

class InsertRoomForm(Form):
    RoomId = StringField('Room Number:', validators=[InputRequired()])
    PrisonName = StringField('Prison Name:', validators=[InputRequired()])
    Type_of_room = StringField('Room Type:', validators=[InputRequired()])

class DeleteRoomForm(Form):
    RoomId = StringField('Room Id:', validators=[InputRequired()])
    PrisonName = StringField('Prison Name:', validators=[InputRequired()])

class UpdateRoomForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    RoomId = StringField('Room Id:', validators=[InputRequired()])
    PrisonName = StringField('Prison Name:', validators=[InputRequired()])


@app.route('/PrisonRoomTable/', methods=['GET', 'POST'])
def list_room_table():
    cur = con.cursor()  
    insertPrisonRoom()
    deletePrisonRoom()
    updatePrisonRoom()
    cur.execute("select * from RoomInThePrisonInfo")
    rows = cur.fetchall()  
    return render_template('room_table.html', rows=rows, iform = InsertRoomForm(), dform = DeleteRoomForm(), uform = UpdateRoomForm())
    cur.close()


@app.route('/insertPrisonRoom', methods=['GET', 'POST'])
def insertPrisonRoom():
    cur = con.cursor()
    form1 = InsertRoomForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        RoomId = request.form['RoomId']
        PrisonName = request.form['PrisonName']
        Type_of_room = request.form['Type_of_room']
        cur.execute("INSERT INTO RoomInThePrisonInfo(RoomId, PrisonName, Type_of_room) VALUES (:1,:2,:3)", (RoomId, PrisonName, Type_of_room))
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('list_room_table'))
    

@app.route('/deletePrisonRoom', methods=['GET', 'POST'])
def deletePrisonRoom():
    cur = con.cursor()
    form2 = DeleteRoomForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        RoomId = request.form['RoomId2']
        PrisonName = request.form['PrisonName2']
        statement = "Delete from RoomInThePrisonInfo WHERE RoomId=:rid AND PrisonName=:pname"
        cur.execute(statement, {'rid': RoomId, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('list_room_table'))

@app.route('/updatePrisonRoom',methods=['GET','POST'])
def updatePrisonRoom():
    cur = con.cursor()
    form3 = UpdateRoomForm(request.form, prefix ='updateForm')
    if request.method=='POST':
        Selection = request.form['UpdateColumn']
        Value = request.form['Value']
        RoomId = request.form['RoomId3']
        PrisonName = request.form['PrisonName3']
        cur.execute("UPDATE RoomInThePrisonInfo SET " + Selection + "=:1 WHERE RoomId=:2 AND PrisonName=:3", (Value, RoomId, PrisonName))
        con.commit()
        return redirect(url_for('list_room_table'))


@app.route('/prisonTable/')
def prisonTable():
    cur = con.cursor()
    insertPrisonRoom()
    deletePrisonRoom()
    updatePrisonRoom()
    cur.execute("select * from PrisonInfo")
    rows = cur.fetchall()
    return render_template('prison_table.html',rows=rows)
    cur.close()

class InsertPrisonForm(Form):
    PrisonName = StringField('Prison Name', validators=[InputRequired()])
    PrisonLocation = StringField('Location', validators=None)
    PrisonSize = IntegerField("Size", validators=None)
    PrisonGender = StringField("Gender", validators=None)
    Director = StringField("Director", validators=None)

class DeletePrisonForm(Form):
    PrisonName = StringField('Prison Name: ', validators=[InputRequired()])

class UpdatePrisonForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    PrisonName = StringField('Prison Name:', validators=[InputRequired()])

@app.route('/insertPrison', methods=['GET', 'POST'])
def insertPrison():
    cur = con.cursor()
    form1 = InsertPrisonForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        PrisonName = request.form['PrisonName']
        Location = request.form['PrisonLocation']
        Size = request.form['PrisonSize']
        Gender = request.form['Gender']
        DirectorId = request.form['Director']
        cur.execute("INSERT INTO PrisonInfo(PrisonName, Location_of_prison, size_of_prison, PrisonGender, Director) VALUES (:1,:2,:3, :4, :5)", (PrisonName, Location, Size, Gender, DirectorId))
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('prisonTable'))



@app.route('/deletePrison', methods=['GET', 'POST'])
def deletePrison():
    cur = con.cursor()
    form2 = DeletePrisonForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from PrisonInfo WHERE PrisonName=:pname"
        cur.execute(statement, {'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('prisonTable'))

@app.route('/updatePrison',methods=['GET','POST'])
def updatePrison():
    cur = con.cursor()
    form3 = UpdatePrisonForm(request.form, prefix ='updateForm')
    if request.method=='POST':
        Selection = request.form['UpdateColumn']
        Value = request.form['Value']
        PrisonName = request.form['PrisonName3']
        cur.execute("UPDATE PrisonInfo SET " + Selection + "=:1 WHERE PrisonName=:2", (Value, PrisonName))
        con.commit()
        return redirect(url_for('prisonTable'))


@app.route('/prisonerTable/')
def prisonerTable():
    cur = con.cursor()
    insertPrisoner()
    deletePrisoner()
    updatePrisoner()
    cur.execute("select * from PrisonerInfo")
    rows = cur.fetchall()
    return render_template('prisoner_table.html',rows=rows)
    cur.close()

class InsertPrisonerForm(Form):
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    RoomId = StringField('RoomId', validators=None)
    PrisonName = StringField('PrisonName', validators=None)
    FirstName = StringField('Gender', validators=None)
    LastName = StringField('Director', validators=None)
    BirthDate = DateField('BirthDate', validators=None)
    Height = IntegerField('Height', validators=None)
    Weight = IntegerField('Weight', validators=None)
    Race = StringField('Race', validators=None)

class DeletePrisonerForm(Form):
    PrisonerId = StringField('Prisoner Id: ', validators=[InputRequired()])
    PrisonName = StringField('Prison Name: ', validators=[InputRequired()])

class UpdatePrisonerForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId:', validators=[InputRequired()])
    PrisonName = StringField('Prison Name: ', validators=[InputRequired()])

@app.route('/insertPrisoner', methods=['GET', 'POST'])
def insertPrisoner():
    cur = con.cursor()
    form1 = InsertPrisonerForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        PrisonerId = request.form['PrisonerId']
        RoomId = request.form['RoomId']
        PrisonName = request.form['PrisonName']
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Birthdate = request.form['BirthDate']
        Height = request.form['Height']
        Weight = request.form['Weight']
        Race = request.form['Race']
        statement = "INSERT INTO PrisonerInfo(PrisonerId, RoomId, PrisonName, FirstName, LastName, Birthdate, Height, Weight, Race) VALUES (:1,:2,:3,:4,:5,TO_DATE(:6, 'YYYY-DD-MM'),:7,:8,:9)"
        cur.execute(statement, {'1': PrisonerId, '2': RoomId, '3': PrisonName, '4': FirstName, '5': LastName, '6': Birthdate, '7': Height, '8': Weight, '9': Race})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('prisonerTable'))

@app.route('/deletePrisoner', methods=['GET', 'POST'])
def deletePrisoner():
    cur = con.cursor()
    form2 = DeletePrisonerForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        PrisonerId = request.form['PrisonerId2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from PrisonerInfo WHERE PrisonerId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'pid': PrisonerId, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('prisonerTable'))

@app.route('/updatePrisoner',methods=['GET','POST'])
def updatePrisoner():
    cur = con.cursor()
    form3 = UpdatePrisonerForm(request.form, prefix ='updateForm')
    if request.method=='POST':
        Selection = request.form['UpdateColumn']
        Value = request.form['Value']
        PrisonerId = request.form['PrisonerId3']
        PrisonName = request.form['PrisonName3']
        statement = "UPDATE PrisonerInfo SET " + Selection + "=:value WHERE PrisonerId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'value': Value, 'pid': PrisonerId, 'pname': PrisonName})
        con.commit()
        return redirect(url_for('prisonerTable'))


@app.route('/employeeTable/')
def employeeTable():
    insertEmployee()
    deleteEmployee()
    updateEmployee()
    cur = con.cursor()
    cur.execute("select * from EmployeeInfo")
    rows = cur.fetchall()
    return render_template('employee_table.html',rows=rows)
    cur.close()

class InsertEmployeeForm(Form):
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=None)
    FirstName = StringField('Gender', validators=None)
    LastName = StringField('Director', validators=None)
    Email = StringField('Email' ,validators=None)
    HireDate = DateField('HireDate', validators=None)
    BirthDate = DateField('BirthDate', validators=None)
    JobType = StringField('JobType', validators=None)

class DeleteEmployeeForm(Form):
    Eid = StringField('Prisoner Id: ', validators=[InputRequired()])
    PrisonName = StringField('Prison Name: ', validators=[InputRequired()])

class UpdateEmployeeForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    Eid = StringField('Eid:', validators=[InputRequired()])
    PrisonName = StringField('Prison Name: ', validators=[InputRequired()])

@app.route('/insertEmployee', methods=['GET', 'POST'])
def insertEmployee():
    cur = con.cursor()
    form1 = InsertEmployeeForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        Eid = request.form['Eid']
        PrisonName = request.form['PrisonName']
        FirstName = request.form['FirstName']
        LastName = request.form['LastName']
        Email = request.form['Email']
        HireDate = request.form['HireDate']
        BirthDate = request.form['BirthDate']
        JobType = request.form['JobType']
        statement = "INSERT INTO EmployeeInfo(Eid, PrisonName, FirstName, LastName, Email, HireDate, BirthDate, JobType) VALUES (:1,:2,:3,:4,:5, TO_DATE(:6, 'YYYY-MM-DD'), TO_DATE(:7, 'YYYY-MM-DD'),:8)"
        cur.execute(statement, {'1': Eid, '2': PrisonName, '3': FirstName, '4': LastName, '5': Email, '6': HireDate, '7': BirthDate, '8': JobType})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('employeeTable'))

@app.route('/deleteEmployee', methods=['GET', 'POST'])
def deleteEmployee():
    cur = con.cursor()
    form2 = DeleteEmployeeForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        Eid = request.form['Eid2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from EmployeeInfo WHERE Eid=:eid AND PrisonName=:pname"
        cur.execute(statement, {'eid': Eid, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('employeeTable'))

@app.route('/updateEmployee',methods=['GET','POST'])
def updateEmployee():
    cur = con.cursor()
    form3 = UpdateEmployeeForm(request.form, prefix ='updateForm')
    if request.method == 'POST':
        Selection = request.form['UpdateColumn']
        Value = request.form['Value']
        Eid = request.form['Eid3']
        PrisonName = request.form['PrisonName3']
        statement = "UPDATE EmployeeInfo SET " + Selection + "=:value WHERE Eid=:eid AND PrisonName=:pname"
        cur.execute(statement, {'value': Value, 'eid': Eid, 'pname': PrisonName})
        con.commit()
        return redirect(url_for('employeeTable'))


@app.route('/supervisorTable/')
def supervisorTable():
    cur = con.cursor()
    insertSupervisor()
    deleteSupervisor()
    cur.execute("select * from Supervisor")
    rows = cur.fetchall()
    return render_template('supervisor_table.html', rows=rows)
    cur.close()

class InsertSupervisorForm(Form):
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=None)
    Supervisor_ID = StringField("Supervisor", validators=None)

class DeleteSupervisorForm(Form):
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonName = StringField('Prison Name', validators=[InputRequired()])


@app.route('/insertSupervisor', methods=['GET', 'POST'])
def insertSupervisor():
    cur = con.cursor()
    form1 = InsertSupervisorForm(request.form, prefix='insertForm')  
    if request.method == 'POST':
        Eid = request.form['Eid']
        PrisonName = request.form['PrisonName']
        Supervisor_ID = request.form['SupervisorId']
        cur.execute("INSERT INTO Supervisor( Eid, PrisonName, Supervisor_ID) VALUES (:eid, :pname, :sid)", {'eid': Eid, 'pname': PrisonName, 'sid': Supervisor_ID})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('supervisorTable'))

@app.route('/deleteSupervisor', methods=['GET', 'POST'])
def deleteSupervisor():
    cur = con.cursor()
    form2 = DeleteSupervisorForm(request.form, prefix='deleteForm')
    if request.method == 'POST':
        Eid = request.form['Eid2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from Supervisor WHERE Eid=:eid AND PrisonName=:pname"
        cur.execute("DELETE from Supervisor WHERE Eid=:eid AND PrisonName=:pname", {'eid': Eid, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('supervisorTable'))


@app.route('/phoneNumberTable/')
def phoneNumberTable():
    cur = con.cursor()
    insertNumber()
    deleteNumber()
    updateNumber()
    cur.execute("select * from phoneNumberInfo")
    rows = cur.fetchall()
    return render_template('phoneNumber_table.html', rows=rows)
    cur.close()

class InsertNumberForm(Form):
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
    Phonenumber = StringField('Number', validators=None)
    NumberType = StringField('Type', validators=None)

class DeleteNumberForm(Form):
    Eid = StringField('Eid: ', validators=[InputRequired()])
    PrisonName = StringField('Prison Name: ', validators=[InputRequired()])
    Phonenumber = StringField('Number', validators=[InputRequired()])

class UpdateNumberForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId:', validators=[InputRequired()])
    PrisonName = StringField('Prison Name: ', validators=[InputRequired()])
    Phonenumber = StringField('Number', validators=[InputRequired()])

@app.route('/insertNumber', methods=['GET', 'POST'])
def insertNumber():
    cur = con.cursor()
    form1 = InsertNumberForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        Eid = request.form['Eid']
        PrisonName = request.form['PrisonName']
        Phonenumber = request.form['Phonenumber']
        NumberType = request.form['UpdateColumn']
        statement = "INSERT INTO phoneNumberInfo(Eid, PrisonName, Phonenumber, NumberType) VALUES (:1,:2,:3,:4)"
        cur.execute(statement, {'1': Eid, '2': PrisonName, '3': Phonenumber, '4': NumberType})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('phoneNumberTable'))

@app.route('/deleteNumber', methods=['GET', 'POST'])
def deleteNumber():
    cur = con.cursor()
    form2 = DeleteNumberForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        Eid = request.form['Eid2']
        PrisonName = request.form['PrisonName2']
        Phonenumber = request.form['Phonenumber2']
        statement = "DELETE from phoneNumberInfo WHERE Eid=:eid AND PrisonName=:pname AND Phonenumber=:pnum"
        cur.execute(statement, {'eid': Eid, 'pname': PrisonName, 'pnum': Phonenumber})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('phoneNumberTable'))

@app.route('/updateNumber',methods=['GET','POST'])
def updateNumber():
    cur = con.cursor()
    form3 = UpdateNumberForm(request.form, prefix ='updateForm')
    if request.method == 'POST':
        Selection = request.form['UpdateColumn2']
        Value = request.form['Value']
        Eid = request.form['Eid3']
        PrisonName = request.form['PrisonName3']
        Phonenumber = request.form['Phonenumber3']
        statement = "UPDATE phoneNumberInfo SET " + Selection + "=:value WHERE Eid=:eid AND PrisonName=:pname AND Phonenumber=:pnum"
        cur.execute(statement, {'value': Value, 'eid': Eid, 'pname': PrisonName, 'pnum': Phonenumber})
        con.commit()
        return redirect(url_for('phoneNumberTable'))

@app.route('/eventTable')
def eventTable():
    cur = con.cursor()
    insertEvent()
    deleteEvent()
    updateEvent()
    cur.execute("select * from EventInfo")
    rows = cur.fetchall()
    return render_template('event_table.html', rows=rows)
    cur.close()

class InsertEventForm(Form):
    EventId = StringField('EventId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId', validators=None)
    DateOfEvent = DateField('EventDate', validators=None)
    NameOfEvent = StringField('EventName', validators=None)
    CategoryOfEvent = StringField('EventCategory', validators=None)

class DeleteEventForm(Form):
    EventId = StringField('EventId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
   
class UpdateEventForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    EventId = StringField('EventId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])

@app.route('/insertEvent', methods=['GET', 'POST'])
def insertEvent():
    cur = con.cursor()
    form1 = InsertEventForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        EventId = request.form['Eid']
        PrisonName = request.form['PrisonName']
        PrisonerId = request.form['PrisonerId']
        DateOfEvent = request.form['DateOfEvent']
        NameOfEvent = request.form['NameOfEvent']
        CategoryOfEvent = request.form['UpdateColumn']
        statement = "INSERT INTO EventInfo(EventId, PrisonName, PrisonerId, DateOfEvent, NameOfEvent, CategoryOfEvent) VALUES (:1,:2,:3,TO_DATE(:4, 'YYYY-MM-DD'),:5,:6)"
        cur.execute(statement, {'1': EventId, '2': PrisonName, '3': PrisonerId, '4': DateOfEvent, '5': NameOfEvent, '6': CategoryOfEvent})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('eventTable'))

@app.route('/deleteEvent', methods=['GET', 'POST'])
def deleteEvent():
    cur = con.cursor()
    form2 = DeleteEventForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        EventId = request.form['Eid2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from EventInfo WHERE EventId=:eid AND PrisonName=:pname"
        cur.execute(statement, {'eid': EventId, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('eventTable'))

@app.route('/updateEvent',methods=['GET','POST'])
def updateEvent():
    cur = con.cursor()
    form3 = UpdateEventForm(request.form, prefix ='updateForm')
    if request.method == 'POST':
        Selection = request.form['UpdateColumn2']
        Value = request.form['Value']
        EventId = request.form['Eid3']
        PrisonName = request.form['PrisonName3']
        statement = "UPDATE EventInfo SET " + Selection + "=:value WHERE EventId=:eid AND PrisonName=:pname"
        cur.execute(statement, {'value': Value, 'eid': EventId, 'pname': PrisonName})
        con.commit()
        return redirect(url_for('eventTable'))


@app.route('/inventoryTable')
def inventoryTable():
    cur = con.cursor()
    insertInventory()
    deleteInventory()
    updateInventory()
    cur.execute("select * from InventoryInfo")
    rows = cur.fetchall()
    return render_template('inventory.html', rows=rows)
    cur.close()

class InsertInventoryForm(Form):
    ProductId = StringField('ProductId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
    Quantity = StringField('Quantity', validators=None)
    TypeOfProduct = StringField('ProductType', validators=None)
    NameOfProduct = StringField('NameOfProduct', validators=None)
    Eid = StringField('Eid', validators=None)

class DeleteInventoryForm(Form):
    ProductId = StringField('ProductId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
   
class UpdateInventoryForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    ProductId = StringField('ProductId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])

@app.route('/insertInventory', methods=['GET', 'POST'])
def insertInventory():
    cur = con.cursor()
    form1 = InsertInventoryForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        ProductId = request.form['Pid']
        PrisonName = request.form['PrisonName']
        Quantity = request.form['Quantity']
        TypeOfProduct = request.form['UpdateColumn']
        NameOfProduct = request.form['NameOfProduct']
        Eid = request.form['Eid']
        statement = "INSERT INTO InventoryInfo(ProductId, PrisonName, Quantity, TypeOfProduct, NameOfProduct, Eid) VALUES (:1,:2,:3,:4,:5,:6)"
        cur.execute(statement, {'1': ProductId, '2': PrisonName, '3': Quantity, '4': TypeOfProduct, '5': NameOfProduct, '6': Eid})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('inventoryTable'))

@app.route('/deleteInventory', methods=['GET', 'POST'])
def deleteInventory():
    cur = con.cursor()
    form2 = DeleteInventoryForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        ProductId = request.form['Pid2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from InventoryInfo WHERE ProductId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'pid': ProductId, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('inventoryTable'))

@app.route('/updateInventory',methods=['GET','POST'])
def updateInventory():
    cur = con.cursor()
    form3 = UpdateInventoryForm(request.form, prefix ='updateForm')
    if request.method == 'POST':
        Selection = request.form['UpdateColumn2']
        Value = request.form['Value']
        ProductId = request.form['Pid3']
        PrisonName = request.form['PrisonName3']
        statement = "UPDATE InventoryInfo SET " + Selection + "=:value WHERE ProductId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'value': Value, 'pid': ProductId, 'pname': PrisonName})
        con.commit()
        return redirect(url_for('inventoryTable'))


@app.route('/clothingTable')
def clothingTable():
    cur = con.cursor()
    insertClothing()
    deleteClothing()
    updateClothing()
    cur.execute("select * from ClothingInfo")
    rows = cur.fetchall()
    return render_template('clothing_table.html', rows=rows)
    cur.close()
    
class InsertClothingForm(Form):
    ProductId = StringField('ProductId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
    sizeOfClothing = StringField('Size', validators=None)
    Quantity = StringField('Quantity', validators=None)
    TypeOfProduct = StringField('ProductType', validators=None)
    NameOfProduct = StringField('NameOfProduct', validators=None)
    Eid = StringField('Eid', validators=None)

class DeleteClothingForm(Form):
    ProductId = StringField('ProductId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
   
class UpdateClothingForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    ProductId = StringField('ProductId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])

@app.route('/insertClothing', methods=['GET', 'POST'])
def insertClothing():
    cur = con.cursor()
    form1 = InsertClothingForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        ProductId = request.form['Pid']
        PrisonName = request.form['PrisonName']
        sizeOfClothing = request.form['sizeOfClothing']
        Quantity = request.form['Quantity']
        TypeOfProduct = request.form['TypeOfProduct']
        NameOfProduct = request.form['NameOfProduct']
        Eid = request.form['Eid']
        statement = "INSERT INTO ClothingInfo(ProductId, PrisonName, sizeOfClothing, Quanitity, TypeOfProduct, NameOfProduct, Eid) VALUES (:1,:2,:3,:4,:5,:6,:7)"
        cur.execute(statement, {'1': ProductId, '2': PrisonName, '3': sizeOfClothing,'4': Quantity, '5': TypeOfProduct, '6': NameOfProduct, '7': Eid})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('clothingTable'))

@app.route('/deleteClothing', methods=['GET', 'POST'])
def deleteClothing():
    cur = con.cursor()
    form2 = DeleteClothingForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        ProductId = request.form['Pid2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from ClothingInfo WHERE ProductId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'pid': ProductId, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('clothingTable'))

@app.route('/updateClothing',methods=['GET','POST'])
def updateClothing():
    cur = con.cursor()
    form3 = UpdateClothingForm(request.form, prefix ='updateForm')
    if request.method == 'POST':
        Selection = request.form['UpdateColumn2']
        Value = request.form['Value']
        ProductId = request.form['Pid3']
        PrisonName = request.form['PrisonName3']
        statement = "UPDATE ClothingInfo SET " + Selection + "=:value WHERE ProductId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'value': Value, 'pid': ProductId, 'pname': PrisonName})
        con.commit()
        return redirect(url_for('clothingTable'))

@app.route('/eventgradeTable')
def gradeTable():
    cur = con.cursor()
    insertGrade()
    deleteGrade()
    updateGrade()
    cur.execute("select * from Event_gradeInfo")
    rows = cur.fetchall()
    return render_template('grade_table.html', rows=rows)
    cur.close()

class InsertGradeForm(Form):
    EventId = StringField('EventId', validators=[InputRequired()])
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
    Grade = StringField('Grade', validators=[InputRequired()])

class DeleteGradeForm(Form):
    EventId = StringField('EventId', validators=[InputRequired()])
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])

class UpdateGradeForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    EventId = StringField('EventId', validators=[InputRequired()])
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])

@app.route('/insertGrade', methods=['GET', 'POST'])
def insertGrade():
    cur = con.cursor()
    form1 = InsertGradeForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        EventId = request.form['EventId']
        Eid = request.form['Eid']
        PrisonerId = request.form['PrisonerId']
        PrisonName = request.form['PrisonName']
        Grade = request.form['UpdateColumn']
        statement = "INSERT INTO Event_gradeInfo(EventId, Eid, PrisonerId, PrisonName, Grade) VALUES (:1,:2,:3,:4,:5)"
        cur.execute(statement, {'1': EventId, '2': Eid, '3': PrisonerId, '4': PrisonName, '5': Grade})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('gradeTable'))

@app.route('/deleteGrade', methods=['GET', 'POST'])
def deleteGrade():
    cur = con.cursor()
    form2 = DeleteGradeForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        EventId = request.form['EventId2']
        Eid = request.form['Eid2']
        PrisonerId = request.form['PrisonerId2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from Event_gradeInfo WHERE EventId=:ev_id AND Eid=:eid AND PrisonerId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'ev_id': EventId, 'eid': Eid, 'pid': PrisonerId, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('gradeTable'))

@app.route('/updateGrade',methods=['GET','POST'])
def updateGrade():
    cur = con.cursor()
    form3 = UpdateGradeForm(request.form, prefix ='updateForm')
    if request.method=='POST':
        Grade = request.form['UpdateColumn3']
        EventId = request.form['EventId3']
        Eid = request.form['Eid3']
        PrisonerId = request.form['PrisonerId3']
        PrisonName = request.form['PrisonName3']
        statement = "UPDATE Event_gradeInfo SET Grade=:grade WHERE EventId=:ev_id AND Eid=:eid AND PrisonerId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'grade': Grade, 'ev_id': EventId, 'eid': Eid, 'pid': PrisonerId, 'pname': PrisonName})
        con.commit()
        return redirect(url_for('gradeTable'))


@app.route('/guardTable')
def guardTable():
    cur = con.cursor()
    #insertGuard()
    #deleteGuard()
    #updateGuard()
    cur.execute("select * from GuardInfo")
    rows = cur.fetchall()
    return render_template('guard_table.html', rows=rows)
    cur.close()

class InsertGuardForm(Form):
    EventId = StringField('EventId', validators=[InputRequired()])
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])
    Grade = StringField('Grade', validators=[InputRequired()])

class DeleteGuardForm(Form):
    EventId = StringField('EventId', validators=[InputRequired()])
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])

class UpdateGuardForm(Form):
    Selection = StringField('Selection: ', validators=[InputRequired()])
    Value = StringField('Value:', validators=[InputRequired()])
    EventId = StringField('EventId', validators=[InputRequired()])
    Eid = StringField('Eid', validators=[InputRequired()])
    PrisonerId = StringField('PrisonerId', validators=[InputRequired()])
    PrisonName = StringField('PrisonName', validators=[InputRequired()])

'''@app.route('/insertGuard', methods=['GET', 'POST'])
def insertGuard():
    cur = con.cursor()
    form1 = InsertGuardForm(request.form, prefix='insertForm')   
    if request.method == 'POST':
        EventId = request.form['EventId']
        Eid = request.form['Eid']
        PrisonerId = request.form['PrisonerId']
        PrisonName = request.form['PrisonName']
        Grade = request.form['UpdateColumn']
        statement = "INSERT INTO GuardInfo(EventId, Eid, PrisonerId, PrisonName, Grade) VALUES (:1,:2,:3,:4,:5)"
        cur.execute(statement, {'1': EventId, '2': Eid, '3': PrisonerId, '4': PrisonName, '5': Grade})
        con.commit()
        #flash("Insertion successful!")
        return redirect(url_for('guardTable'))

@app.route('/deleteGuard', methods=['GET', 'POST'])
def deleteGuard():
    cur = con.cursor()
    form2 = DeleteGuardForm(request.form, prefix='deleteForm')   
    if request.method == 'POST':
        EventId = request.form['EventId2']
        Eid = request.form['Eid2']
        PrisonerId = request.form['PrisonerId2']
        PrisonName = request.form['PrisonName2']
        statement = "DELETE from GuardInfo WHERE EventId=:ev_id AND Eid=:eid AND PrisonerId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'ev_id': EventId, 'eid': Eid, 'pid': PrisonerId, 'pname': PrisonName})
        con.commit()
        #flash("Deletion successful!")
        return redirect(url_for('guardTable'))

@app.route('/updateGrade',methods=['GET','POST'])
def updateGuard():
    cur = con.cursor()
    form3 = UpdateGuardForm(request.form, prefix ='updateForm')
    if request.method=='POST':
        Grade = request.form['UpdateColumn3']
        EventId = request.form['EventId3']
        Eid = request.form['Eid3']
        PrisonerId = request.form['PrisonerId3']
        PrisonName = request.form['PrisonName3']
        statement = "UPDATE GuardInfo SET Grade=:grade WHERE EventId=:ev_id AND Eid=:eid AND PrisonerId=:pid AND PrisonName=:pname"
        cur.execute(statement, {'grade': Grade, 'ev_id': EventId, 'eid': Eid, 'pid': PrisonerId, 'pname': PrisonName})
        con.commit()
        return redirect(url_for('guardTable'))
'''


if __name__ == '__main__':
    app.run(debug=True)
