from flask import Flask, jsonify, request, url_for, redirect, render_template
import sqlite3

app = Flask(__name__)

with sqlite3.connect("database.db") as con:
  con.row_factory = sqlite3.Row
  cur = con.cursor()
  rows = cur.execute("select * from contacts").fetchall()
  contacts = []

  for row in rows:
    contact={
      'id': row[0],
      'name':  row[1], 
      'contact': row[2],
    }
    contacts.append(contact)



@app.route('/')
def index():
  return render_template('index.html', data=contacts)



@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template('login.html')

  elif request.method == "POST":
    print(request.form.get('usermail'))
    print(request.form.get('password'))

    return redirect(url_for('index'))



@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == "GET":
    return render_template('signup.html')

  elif request.method == "POST":
    print(request.form.get('username'))
    print(request.form.get('usermail'))
    print(request.form.get('password'))
    print(request.form.get("confirm_password"))

    return redirect(url_for('index'))



@app.route('/add-data', methods=["POST"])
def add_contact():
  con = sqlite3.connect("database.db")
  cur = con.cursor()

  if len(contacts) == 0:
    Id = 1
    
  else:
    Id = contacts[-1]['id'] + 1

  name = request.form.get('name')
  contact = request.form.get('contact')
  
  contacts.append({
    'id': int(Id),
    'name':  name, 
    'contact': int(contact),
  })

  cur.execute("INSERT INTO contacts (name,contact) VALUES (?,?)", (name, int(contact)))
  con.commit()
  con.close()

  return redirect(url_for('index'))



@app.route('/get-data')
def get_data():
  return jsonify({"data" : contacts})



@app.route('/delete-data', methods=["POST"])
def delete_data():
  contacts.remove(request.get_json())

  with sqlite3.connect("database.db") as con:
    cur = con.cursor()
    cur.execute("DELETE FROM contacts WHERE id=?", (int(request.get_json()['id']), ))
    con.commit()
  
  return jsonify({"data" : contacts})


if __name__ == '__main__':
  app.run(debug=True)