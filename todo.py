from flask import Flask,render_template,redirect,url_for,request

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Arif-Kübra/Desktop/ARİF/PYTHON/TodoApp/todo.db'
db = SQLAlchemy(app)
# index response'u  ve sonradan eklenen todo verilerini veritabanından alıp html sayfasında gönderme response'u
@app.route("/")
def index():
    todos = todo.query.all() # veritabanından tüm todo tablosu verileri alındı.
    return render_template("index.html", todos = todos) # index sayfasna gönderildi.

# todo ekleme response'u
@app.route("/add", methods=["POST"]) # GET REQUEST İLE ULAŞILAMASIN. SADECE KULLANICI POST REQUESTTEN SONRA BU SAYFAYA ULABİLSİN
def add():
    title = request.form.get("title") # html sayfasında namesi "title" olan yere girilen veriyi al.
    newTodo = todo(title = title, complete = False) # sql sorgu kodu olarak ele alabilirsiniz. ORm olarak çalıştığımız için orm isteğine göre yeni bir todo objesi oluşturduk ve içerisine kullanıcıdan aldığımız veriyi ekledik.
    db.session.add(newTodo) # cursor execute kodu olarak düşünebilirsiniz. oluşturduğumuz sorgunun(objemizin/class'mızın) çalışması için içerisine ekliyoruz.
    db.session.commit() # veritabanında değişiklik yaptığımız için 
    return redirect(url_for("index"))

# Tamamla butonu response'u ve Değer değiştirme (True= False) Butona basıldığında /complete/id'ye gideceği için burada bu adrese gidildiğinde durum değiştir dedik.
@app.route("/complete/<string:id>")
def complete(id):
    Todo = todo.query.filter_by(id = id).first() # todo tablosundan id'si kullanıcı tarafından seçilen tamamla butonuna basılan id ile benzeyeni al dedik.
   
    Todo.complete = not Todo.complete
    db.session.commit()
    return redirect(url_for("index"))
    
# Todo Silme Butonuna basıldığında dönecek olan dinamik  delete response'u
@app.route("/delete/<string:id>")
def deleteTodo(id):
    Todo = todo.query.filter_by(id = id).first() 
    db.session.delete(Todo)
    db.session.commit()
    return redirect(url_for("index"))

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(80)) 
    complete = db.Column(db.Boolean)


if __name__ == "__main__":
    db.create_all() # oluşturduğumuz classlarn form olarak veritabanına eklenmesini sağlar. 
    app.run(debug=True)
