import os
import cx_Oracle
from flask import Flask, render_template,request
from datetime import date
from app import app
app = Flask(__name__)
os.chdir("C:\oracle_oracle\instantclient_12_2")
con = cx_Oracle.connect('username','password','localhost:20037/xe')


@app.route('/')
def index():
    address = request.remote_addr
    return render_template('index.html', user_address=address)


@app.route('/RoomInThePrisonTable')
def list_room_table():
    cur = con.cursor()
    cur.execute("select * from RoomInThePrisonInfo")
    rows = cur.fetchall()
    return render_template('room_table.html',rows=rows)
    cur.close()


@app.route('/prisonTable')
def list_prison_table():
    cur = con.cursor()
    cur.execute("select * from PrisonInfo")
    rows = cur.fetchall()
    return render_template('prison_table.html',rows=rows)
    cur.close()


@app.route('/prisonerTable')
def list_prisoner_table():
    cur = con.cursor()
    cur.execute("select * from PrisonerInfo")
    rows = cur.fetchall()
    return render_template('prisoner_table.html',rows=rows)
    cur.close()


@app.route('/employeeTable')
def list_employee_table():
    cur = con.cursor()
    cur.execute("select * from EmployeeInfo")
    rows = cur.fetchall()
    return render_template('employee_table.html',rows=rows)
    cur.close()


@app.route('/supervisorTable')
def list_supervisor_table():
    cur = con.cursor()
    cur.execute("select * from Supervisor")
    rows = cur.fetchall()
    return render_template('supervisor_table.html',rows=rows)
    cur.close()


@app.route('/phoneNumberTable')
def list_phonenumber_table():
    cur = con.cursor()
    cur.execute("select * from phoneNumberInfo")
    rows = cur.fetchall()
    return render_template('phoneNumber_table.html', rows=rows)
    cur.close()


@app.route('/eventTable')
def list_event_table():
    cur = con.cursor()
    cur.execute("select * from EventInfo")
    rows = cur.fetchall()
    return render_template('event_table.html', rows=rows)
    cur.close()


@app.route('/inventoryTable')
def list_inventory_table():
    cur = con.cursor()
    cur.execute("select * from InventoryInfo")
    rows = cur.fetchall()
    return render_template('inventory_table.html', rows=rows)
    cur.close()


@app.route('/clothingTable')
def list_clothing_table():
    cur = con.cursor()
    cur.execute("select * from ClothingInfo")
    rows = cur.fetchall()
    return render_template('clothing_table.html', rows=rows)
    cur.close()


@app.route('/eventgradeTable')
def list_grade_table():
    cur = con.cursor()
    cur.execute("select * from Event_gradeInfo")
    rows = cur.fetchall()
    return render_template('grade_table.html', rows=rows)
    cur.close()


@app.route('/guardTable')
def list_guard_table():
    cur = con.cursor()
    cur.execute("select * from GuardInfo")
    rows = cur.fetchall()
    return render_template('guard_table.html', rows=rows)
    cur.close()


if __name__ == '__main__':
    app.run(debug=True)


