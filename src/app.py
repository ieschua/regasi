#region Paquetes
import hashlib
from re import I
from flask import Flask, request, jsonify, render_template
from werkzeug.wrappers import response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin
from whitenoise import WhiteNoise
import datetime
import simplejson as json

#endregion


#region Cadenas de conexion

#** Remota
#? mysql+pymysql://ufm6ohqpk3z6u01x:vmqMrny5SSm375jCdag0@bbz9acjqx8sgk9hqdcgl-mysql.services.clever-cloud.com:3306/bbz9acjqx8sgk9hqdcgl

#** Local
#? mysql+pymysql://root:hC5K*M0OSvrNjxaI@localhost/dbregasi

#endregion


#region Configuración de conexión
app = Flask(__name__)
app.wsgi_app = WhiteNoise(app.wsgi_app, root="static/")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hC5K*M0OSvrNjxaI@localhost/dbregasi' #Cadena de conexion
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #Interactuar con la db
ma = Marshmallow(app) #Definir esquema de interaccion
#endregion


#region Especificacion de la base de datos 
class cestads(db.Model):
    NIDESTA = db.Column(db.Numeric(2,0), nullable = False, primary_key = True)
    CNOMEST = db.Column(db.VARCHAR(25), nullable = True)

    def __init__(self, NIDESTA, CNOMEST):
        self.NIDESTA = NIDESTA
        self.CNOMEST = CNOMEST

class chorars(db.Model):
    NIDHORA = db.Column(db.Numeric(5,0), nullable = False, primary_key = True)
    CDESCHR = db.Column(db.VARCHAR(100), nullable = True)
    CSTATUS = db.Column(db.CHAR(1), nullable = True)

    def __init__(self, NIDHORA, CDESCHR, CSTATUS):
        self.NIDHORA = NIDHORA
        self.CDESCHR = CDESCHR
        self.CSTATUS = CSTATUS

class cmunics(db.Model):
    NIDMUNI = db.Column(db.Numeric(4,0), nullable = False, primary_key = True)
    NIDESTA = db.Column(db.Numeric(2,0), db.ForeignKey('cestads.NIDESTA'), nullable = False, primary_key = True)
    CNOMMUN = db.Column(db.VARCHAR(50), nullable = True)

    def __init__(self, NIDESTA, NIDMUNI, CNOMMUN):
        self.NIDESTA = NIDESTA
        self.NIDMUNI = NIDMUNI
        self.CNOMEST = CNOMMUN

class ddatemp(db.Model):
    CCVEEMP = db.Column(db.CHAR(6), nullable = False, primary_key = True)
    CNOMBRE = db.Column(db.VARCHAR(35), nullable = False)
    CAPEUNO = db.Column(db.VARCHAR(35), nullable = True)
    CAPEDOS = db.Column(db.VARCHAR(35), nullable = True)
    CCURPEM = db.Column(db.CHAR(18), nullable = True)
    DFECING = db.Column(db.DATE, nullable = True)
    CNMCALL = db.Column(db.VARCHAR(35), nullable = True)
    CNUMEXT = db.Column(db.VARCHAR(15), nullable = True)
    CNUMINT = db.Column(db.VARCHAR(15), nullable = True)
    CCOLONI = db.Column(db.VARCHAR(50), nullable = True)
    CCODPOS = db.Column(db.CHAR(5), nullable = True)
    NIDESTA = db.Column(db.Numeric(2,0), db.ForeignKey('cmunics.NIDESTA'), nullable = True)
    NIDMUNI = db.Column(db.Numeric(4,0), db.ForeignKey('cmunics.NIDMUNI'), nullable = True)
    CSTATUS = db.Column(db.CHAR(1), nullable = True)

    def __init__(self, CCVEEMP, CNOMBRE, CAPEUNO, CAPEDOS, CCURPEM, DFECING, CNMCALL, CNUMEXT, CNUMINT, CCOLONI, CCODPOS, NIDESTA, NIDMUNI, CSTATUS):
        self.CCVEEMP = CCVEEMP
        self.CNOMBRE = CNOMBRE
        self.CAPEUNO = CAPEUNO
        self.CAPEDOS = CAPEDOS
        self.CCURPEM = CCURPEM
        self.DFECING = DFECING
        self.CNMCALL = CNMCALL
        self.CNUMEXT = CNUMEXT
        self.CNUMINT = CNUMINT
        self.CCOLONI = CCOLONI
        self.CCODPOS = CCODPOS
        self.NIDESTA = NIDESTA
        self.NIDMUNI = NIDMUNI
        self.CSTATUS = CSTATUS

class ddethor(db.Model):
    NIDHORA = db.Column(db.Numeric(5,0), db.ForeignKey('chorars.NIDHORA'), nullable = False, primary_key = True)
    NDIASEM = db.Column(db.Numeric(1,0), nullable = False, primary_key = True)
    CHORENT = db.Column(db.CHAR(5), nullable = True)
    CHORSAL = db.Column(db.CHAR(5), nullable = True)
    CSTATUS = db.Column(db.CHAR(1), nullable = True)

    def __init__(self, NIDHORA, NDIASEM, CHORENT, CHORSAL, CSTATUS):
        self.NIDHORA = NIDHORA
        self.NDIASEM = NDIASEM
        self.CHORENT = CHORENT
        self.CHORSAL = CHORSAL
        self.CSTATUS = CSTATUS

class dhremps(db.Model):
    NIDHORA = db.Column(db.Numeric(5,0), db.ForeignKey('chorars.NIDHORA'), nullable = False, primary_key = True)
    CCVEEMP = db.Column(db.CHAR(6), db.ForeignKey('ddatemp.CCVEEMP'), nullable = False, primary_key = True)
    DFECAIS = db.Column(db.DATE, nullable = True)
    CSTATUS = db.Column(db.CHAR(1), nullable = True)


    def __init__(self, NIDHORA, CCVEEMP, DFECAIS, CSTATUS):
        self.NIDHORA = NIDHORA
        self.CCVEEMP = CCVEEMP
        self.DFECAIS = DFECAIS
        self.CSTATUS = CSTATUS
        
class pregasi(db.Model):
    CCVEEMP = db.Column(db.CHAR(6), db.ForeignKey('ddatemp.CCVEEMP'), nullable = False, primary_key = True)
    DFECREG = db.Column(db.DATETIME, nullable = False, primary_key = True)
    CNUMBIO = db.Column(db.Numeric(2,0), nullable = True)
    CSTATUS = db.Column(db.CHAR(1), nullable = True)

    def __init__(self, CCVEEMP, DFECREG, CNUMBIO, CSTATUS):
        self.CCVEEMP = CCVEEMP
        self.DFECREG = DFECREG
        self.CNUMBIO = CNUMBIO
        self.CSTATUS = CSTATUS

class tincemp(db.Model):
    CCVEEMP = db.Column(db.CHAR(6), db.ForeignKey('ddatemp.CCVEEMP'), nullable = False, primary_key = True)
    DFECINC = db.Column(db.DATE, nullable = False, primary_key = True)
    CTIPINC = db.Column(db.CHAR(1), nullable = True)
    CSTATUS = db.Column(db.CHAR(1), nullable = True)

    def __init__(self, CCVEEMP, DFECINC, CTIPINC, CSTATUS):
        self.CCVEEMP = CCVEEMP
        self.DFECINC = DFECINC
        self.CTIPINC = CTIPINC
        self.CSTATUS = CSTATUS

class identif(db.Model):
    NIDCRED = db.Column(db.INTEGER, nullable = False, primary_key = True, autoincrement = True)
    CCVEEMP = db.Column(db.CHAR(6), db.ForeignKey('ddatemp.CCVEEMP'), nullable = False, primary_key = True)
    USUARIO = db.Column(db.VARCHAR(45), nullable = True)
    PSSWORD = db.Column(db.VARCHAR(40), nullable = True)
    ECORREO = db.Column(db.VARCHAR(45), nullable = True)
    MACCESO = db.Column(db.CHAR(3), nullable = True)
    
    def __init__(self, CCVEEMP, USUARIO, PSSWORD, ECORREO, MACCESO):
        self.CCVEEMP = CCVEEMP
        self.USUARIO = USUARIO
        self.PSSWORD = hashlib.sha1(PSSWORD.encode('utf-8')).hexdigest()
        self.ECORREO = ECORREO
        self.MACCESO = MACCESO

#Creacion de la base de datos
db.create_all()

#endregion


#region Esquemas
#Definicion de Esquemas
class cestadsSchema(ma.Schema):
    class Meta:
        fields = ('NIDESTA', 'CNOMEST')

class chorarsSchema(ma.Schema):
    class Meta:
        fields = ('NIDHORA', 'CDESCHR', 'CSTATUS')

class cmunicsSchema(ma.Schema):
    class Meta:
        fields = ('NIDESTA', 'NIDMUNI', 'CNOMMUN')

class ddatempSchema(ma.Schema):
    class Meta:
        fields = ('CCVEEMP', 'CNOMBRE', 'CAPEUNO', 'CAPEDOS', 'CCURPEM', 'DFECING', 'CNMCALL', 'CNUMEXT', 'CNUMINT', 'CCOLONI', 'CCODPOS', 'NIDESTA', 'NIDMUNI', 'CSTATUS')

class ddethorSchema(ma.Schema):
    class Meta:
        fields = ('NIDHORA', 'NDIASEM', 'CHORENT', 'CHORSAL', 'CSTATUS')

class dhrempsSchema(ma.Schema):
    class Meta:
        fields = ('NIDHORA', 'CCVEEMP', 'DFECAIS', 'CSTATUS')

class pregasiSchema(ma.Schema):
    class Meta:
        fields = ('CCVEEMP', 'DFECREG', 'CNUMBIO', 'CSTATUS')

class tincempSchema(ma.Schema):
    class Meta:
        fields = ('CCVEEMP', 'DFECINC', 'CTIPINC', 'CSTATUS')

class identifSchema(ma.Schema):
    class Meta:
        fields = ('NIDCRED', 'CCVEEMP', 'USUARIO', 'PSSWORD', 'ECORREO', 'MACCESO')

#Creacion de Esquemas
cestads_schema = cestadsSchema()
cestads_s_schema = cestadsSchema(many=True)

chorars_schema = chorarsSchema()
chorars_s_schema = chorarsSchema(many=True)

cmunics_schema = cmunicsSchema()
cmunics_s_schema = cmunicsSchema(many=True)

ddatemp_schema = ddatempSchema()
user_data = ['CCVEEMP','CNOMBRE', 'CAPEUNO', 'CAPEDOS', 'CSTATUS']
ddatemp_user_schema = ddatempSchema(many = False, only = user_data)
ddatemp_s_schema = ddatempSchema(many=True)

ddethor_schema = ddethorSchema()
ddethor_s_schema = ddethorSchema(many=True)

dhremps_schema = dhrempsSchema()
dhremps_s_schema = dhrempsSchema(many=True)

pregasi_schema = pregasiSchema()
pregasi_s_schema = pregasiSchema(many=True)

tincemp_schema = tincempSchema()
tincemp_s_schema = tincempSchema(many=True)

identif_schema = identifSchema()
identif_s_schema = identifSchema(many=True)

#endregion


#region Configuracion CORS

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#endregion


#region Configuracion JWT

app.config['SECRET_KEY'] = 'wefawnefWAEFwaefu43655$&#45623463rgGSEggs'

app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)

def authenticate(username, password):
    user = identif.query.filter_by(USUARIO = username).first()

    if user is not None and user.PSSWORD == hashlib.sha1(password.encode('utf-8')).hexdigest():
        user.id = user.USUARIO
        return user

def identity(payload):
    user_id = payload['identity']
    return identif.query.filter_by(USUARIO = user_id).first()

jwt = JWT(app, authenticate, identity)

#endregion


#region Rutas


#region identifs
#Definicion de rutas "Endpoints"
@app.route('/identifs', methods=['POST'])
def create_identif():
  CCVEEMP = request.json['CCVEEMP']
  USUARIO = request.json['USUARIO']
  PSSWORD = request.json['PSSWORD']
  ECORREO = request.json['ECORREO']
  MACCESO = request.json['MACCESO']

  new_identif = identif(CCVEEMP, USUARIO, PSSWORD, ECORREO, MACCESO)

  db.session.add(new_identif)
  db.session.commit()

  return identif_schema.jsonify(new_identif)

@app.route('/identifs', methods=['GET'])
def get_identifs():
  all_identifs = identif.query.all()
  result = identif_s_schema.dump(all_identifs)
  return jsonify(result)

@app.route('/identifs/<NIDCRED>/<CCVEEMP>', methods=['GET'])
def get_task(NIDCRED, CCVEEMP):
  identif_v = identif.query.get((NIDCRED, CCVEEMP))
  return identif_schema.jsonify(identif_v)

@app.route('/identifs/<NIDCRED>/<CCVEEMP>', methods=['PUT'])
def update_task(NIDCRED, CCVEEMP):
  identif_v = identif.query.get((NIDCRED, CCVEEMP))

  CCVEEMP = request.json['CCVEEMP']
  USUARIO = request.json['USUARIO']
  PSSWORD = request.json['PSSWORD']
  ECORREO = request.json['ECORREO']
  MACCESO = request.json['MACCESO']

  identif_v.CCVEEMP = CCVEEMP
  identif_v.USUARIO = USUARIO
  identif_v.PSSWORD = PSSWORD
  identif_v.ECORREO = ECORREO
  identif_v.MACCESO = MACCESO

  db.session.commit()

  return identif_schema.jsonify(identif_v)

@app.route('/identifs/<NIDCRED>/<CCVEEMP>', methods=['DELETE'])
def delete_task(NIDCRED, CCVEEMP):
  identif_v = identif.query.get((NIDCRED, CCVEEMP))
  db.session.delete(identif_v)
  db.session.commit()
  
  return identif_schema.jsonify(identif_v)
#endregion

#region usuarios

@app.route('/myuser/<CCVEEMP>', methods=['GET'])
def get_user(CCVEEMP):
  ddatemp_v = ddatemp.query.get(CCVEEMP)
  return json.dumps(ddatemp_user_schema.dump(ddatemp_v))
#endregion

#region horarios

@app.route('/horarios', methods=['POST'])
def create_horario():
  NIDHORA = request.json['NIDHORA']
  NDIASEM = request.json['NDIASEM']
  CHORENT = request.json['CHORENT']
  CHORSAL = request.json['CHORSAL']
  CSTATUS = request.json['CSTATUS']

  new_horario = ddethor(NIDHORA, NDIASEM, CHORENT, CHORSAL, CSTATUS)

  db.session.add(new_horario)
  db.session.commit()
  return json.dumps(ddethor_schema.dump(new_horario))

@app.route('/horarios', methods=['GET'])
def get_horarios():
  all_horarios = ddethor.query.all()
  result = ddethor_s_schema.dump(all_horarios)
  return json.dumps(result)

@app.route('/horarios/<NIDHORA>/<NDIASEM>', methods=['GET'])
def get_horario(NIDHORA, NDIASEM):
  horario = ddethor.query.get((NIDHORA, NDIASEM))
  return json.dumps(ddethor_schema.dump(horario))

@app.route('/horarios/<NIDHORA>/<NDIASEM>', methods=['PUT'])
def update_horario(NIDHORA, NDIASEM):
  horario = ddethor.query.get((NIDHORA, NDIASEM))

  NIDHORA = request.json['NIDHORA']
  NDIASEM = request.json['NDIASEM']
  CHORENT = request.json['CHORENT']
  CHORSAL = request.json['CHORSAL']
  CSTATUS = request.json['CSTATUS']

  horario.NIDHORA = NIDHORA
  horario.NDIASEM = NDIASEM
  horario.CHORENT = CHORENT
  horario.CHORSAL = CHORSAL
  horario.CSTATUS = CSTATUS

  db.session.commit()

  return json.dumps(ddethor_schema.dump(horario))

@app.route('/horarios/<NIDHORA>/<NDIASEM>', methods=['DELETE'])
def delete_horario(NIDHORA, NDIASEM):
  horario = ddethor.query.get((NIDHORA, NDIASEM))
  db.session.delete(horario)
  db.session.commit()
  
  return json.dumps(ddethor_schema.dump(horario))

#endregion

#region registrar_asistencias

@app.route('/registrar_asistencias', methods=['POST'])
def create_asistencias():

  dia = datetime.date.today() - datetime.timedelta(days=1)  
  c_horario = db.session.query(dhremps.CCVEEMP, ddethor.CHORENT, ddethor.CHORSAL)\
  .join(chorars, ddethor.NIDHORA==chorars.NIDHORA)\
  .join(dhremps, dhremps.NIDHORA==chorars.NIDHORA)\
  .filter((ddethor.NDIASEM == (dia.isoweekday())) and (ddethor.CSTATUS == "A"))

  horario = db.session.execute(c_horario).fetchall()    
  incidencia = [[0 for x in range(3)] for y in range(50)]

  for i in range(0, len(request.json)):
      pregasi_table = [0 for c in range(4)]
      tincemp_table = [0 for c in range(2)] 
      
      # Creación de registros
      pregasi_table[0] = request.json[i]['CCVEEMP']
      pregasi_table[1] = request.json[i]['DFECREG']
      pregasi_table[2] = request.json[i]['CNUMBIO']
      pregasi_table[3] = request.json[i]['CSTATUS']

      new_asistencia = pregasi(pregasi_table[0], pregasi_table[1], pregasi_table[2], pregasi_table[3])
      
      db.session.add(new_asistencia)
      db.session.commit()

      #Creación de Incidencias
      if any(pregasi_table[0] in x for x in incidencia):
        usuario = next((i, j) for i, lst in enumerate(incidencia) 
          for j, x in enumerate(lst) if x == pregasi_table[0])
        usuario_h = next((i, j) for i, lst in enumerate(horario) 
          for j, x in enumerate(lst) if x == pregasi_table[0])
        incidencia[usuario[0]][2] = pregasi_table[1]

        entrada = datetime.datetime.strptime(incidencia[usuario[0]][1][-8:],"%H:%M:%S").time()
        salida = datetime.datetime.strptime(incidencia[usuario[0]][2][-8:],"%H:%M:%S").time()
        entrada_h = datetime.datetime.strptime(horario[usuario_h[0]][1][-8:],"%H:%M")
        salida_h = datetime.datetime.strptime(horario[usuario_h[0]][2][-8:],"%H:%M")

        #Retardo Menor
        if (entrada_h + datetime.timedelta(minutes=10)).time() < entrada and (entrada_h + datetime.timedelta(minutes=20)).time() > entrada:
            tincemp_table[1] = "N"
        #Retardo Mayor
        elif (entrada_h + datetime.timedelta(minutes=20)).time() < entrada and (entrada_h + datetime.timedelta(minutes=30)).time() > entrada:
            tincemp_table[1] = "Y"
        #Falta por llegar tarde
        elif (entrada_h + datetime.timedelta(minutes=30)).time() < entrada:
            tincemp_table[1] = "T"
        #Falta por salida anticipada
        elif (salida_h + datetime.timedelta(minutes=15)).time() < salida:
            tincemp_table[1] = "A"
        #Falta por omisión de salida
        elif (salida_h + datetime.timedelta(minutes=0)).time() > salida:
            tincemp_table[1] = "O"
        
        tincemp_table[0] = datetime.datetime.today()
        new_incidencias = tincemp(pregasi_table[0], tincemp_table[0], tincemp_table[1], "A") 
        db.session.add(new_incidencias)
        db.session.commit()
        
        entrada = None
        salida = None
        usuario = None
        usuario_h = None

      else:
        incidencia[i][0] = pregasi_table[0]
        incidencia[i][1] = pregasi_table[1]

      #Limpiar registros
      pregasi_table.clear()
      tincemp_table.clear()
      new_asistencia = None
      new_incidencia = None
  
  #Falta todo el dia
  for i in range(0, len(incidencia)):
      if incidencia[i][2] == 0 and incidencia[i][0] != 0:
        new_incidencias = tincemp(incidencia[i][0], datetime.datetime.today(), "D", "A") 
        db.session.add(new_incidencias)
        db.session.commit()


  return 'success'

#endregion

#region develop routes

@app.route('/protected')
@jwt_required()
def protected():
    return identif_schema.jsonify(current_identity)

#endregion

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

#endregion

# Inicio de Aplicación
if __name__ == "__main__":
    app.run(port=5000, debug=False)