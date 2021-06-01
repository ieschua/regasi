#region Paquetes
import hashlib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt import JWT, jwt_required, current_identity
import datetime


#endregion


#region Cadenas de conexion

#** Remota
#? mysql+pymysql://ufm6ohqpk3z6u01x:vmqMrny5SSm375jCdag0@bbz9acjqx8sgk9hqdcgl-mysql.services.clever-cloud.com:3306/bbz9acjqx8sgk9hqdcgl

#** Local
#? mysql+pymysql://root:hC5K*M0OSvrNjxaI@localhost/dbregasi

#endregion

#region Configuración de conexión
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hC5K*M0OSvrNjxaI@localhost/dbregasi' #Cadena de conexion
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #Interactuar con la db
ma = Marshmallow(app) #Definir esquema de interaccion
#endregion


#region Especificacion de la base de datos 
class cestads(db.Model):
    NIDESTA = db.Column(db.DECIMAL(2,0), nullable = False, primary_key = True)
    CNOMEST = db.Column(db.VARCHAR(25), nullable = True)

    def __init__(self, NIDESTA, CNOMEST):
        self.NIDESTA = NIDESTA
        self.CNOMEST = CNOMEST

class chorars(db.Model):
    NIDHORA = db.Column(db.DECIMAL(5,0), nullable = False, primary_key = True)
    CDESCHR = db.Column(db.VARCHAR(100), nullable = True)
    CSTATUS = db.Column(db.CHAR(1), nullable = True)

    def __init__(self, NIDHORA, CDESCHR, CSTATUS):
        self.NIDHORA = NIDHORA
        self.CDESCHR = CDESCHR
        self.CSTATUS = CSTATUS

class cmunics(db.Model):
    NIDMUNI = db.Column(db.DECIMAL(4,0), nullable = False, primary_key = True)
    NIDESTA = db.Column(db.DECIMAL(2,0), db.ForeignKey('cestads.NIDESTA'), nullable = False, primary_key = True)
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
    NIDESTA = db.Column(db.DECIMAL(2,0), db.ForeignKey('cmunics.NIDESTA'), nullable = True)
    NIDMUNI = db.Column(db.DECIMAL(4,0), db.ForeignKey('cmunics.NIDMUNI'), nullable = True)
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
    NIDHORA = db.Column(db.DECIMAL(5,0), db.ForeignKey('chorars.NIDHORA'), nullable = False, primary_key = True)
    NDIASEM = db.Column(db.DECIMAL(1,0), nullable = False, primary_key = True)
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
    NIDHORA = db.Column(db.DECIMAL(5,0), db.ForeignKey('chorars.NIDHORA'), nullable = False, primary_key = True)
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
    CNUMBIO = db.Column(db.DECIMAL(2,0), nullable = True)
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


#region Configuracion JWT

app.config['SECRET_KEY'] = 'wefawnefWAEFwaefu43655$&#45623463rgGSEggs'

app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=1)

def authenticate(username, password):
    user = identif.query.filter_by(ECORREO = username).first()

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
@jwt_required()
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

@app.route('/', methods=['GET'])
def index():
    return jsonify({'Message': 'GET Works'})
#endregion

#region usuarios

@app.route('/myuser/<CCVEEMP>', methods=['GET'])
def get_user(CCVEEMP):
  ddatemp_v = ddatemp.query.get(CCVEEMP)
  ddatemp_v = ddatemp.query.with_entities(ddatemp.CCVEEMP, ddatemp.CNOMBRE, ddatemp.CAPEUNO, ddatemp.CAPEDOS, ddatemp.CSTATUS).filter(ddatemp.CCVEEMP == CCVEEMP)
  return ddatemp_schema.jsonify(ddatemp_v)

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

  return ddethor_schema.jsonify(new_horario)

@app.route('/horarios', methods=['GET'])
def get_horarios():
  all_horarios = ddethor.query.all()
  result = ddethor_s_schema.dump(all_horarios)
  return jsonify(result)

@app.route('/horarios/<NDIASEM>/<NIDHORA>', methods=['GET'])
def get_horario(NDIASEM, NIDHORA):
  horario = ddethor.query.get((NDIASEM, NIDHORA))
  return ddethor_schema.jsonify(horario)

@app.route('/horarios/<NDIASEM>/<NIDHORA>', methods=['PUT'])
def update_horario(NDIASEM, NIDHORA):
  horario = ddethor.query.get((NDIASEM, NIDHORA))

  NIDHORA_R = request.json['NIDHORA']
  NDIASEM_R = request.json['NDIASEM']
  CHORENT = request.json['CHORENT']
  CHORSAL = request.json['CHORSAL']
  CSTATUS = request.json['CSTATUS']

  horario.NIDHORA = NIDHORA
  horario.NDIASEM = NDIASEM
  horario.CHORENT = CHORENT
  horario.CHORSAL = CHORSAL
  horario.CSTATUS = CSTATUS

  db.session.commit()

  return ddethor_schema.jsonify(horario)

@app.route('/horarios/<NDIASEM>/<NIDHORA>', methods=['DELETE'])
def delete_horario(NDIASEM, NIDHORA):
  horario = ddethor.query.get((NDIASEM, NIDHORA))
  db.session.delete(horario)
  db.session.commit()
  
  return ddethor_schema.jsonify(horario)

#endregion

#endregion


# Inicio de Aplicación
if __name__ == "__main__":
    app.run(debug=True)