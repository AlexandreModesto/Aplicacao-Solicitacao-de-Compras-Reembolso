import mysql.connector
import os
from flask import Flask, make_response, jsonify, request, redirect, url_for, render_template, Request, send_from_directory, send_file,session,flash
from flask_cors import  CORS, cross_origin
from werkzeug.utils import secure_filename
import win32com.client as win32
import pythoncom


app =Flask(__name__)
CORS(app, supports_credentials=True, resources=r'/*', allow_headers='*', origins='*')

UPLOAD_FOLDER = './static/files'
ALLOWED_EXTENSIONS = {'pdf'}
mydb= mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='Solicitacao')
app.config['JSON_SORT_KEYS']=False
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
mycursor = mydb.cursor(buffered=True)
# ------------------------------------------------------------------COTAÇÃO---------------------
# -------------------------------------------------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        mycursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = mycursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to some page
            if account[0] == 1:# ID do perfil do diretor
                return redirect(url_for('diretor'))
            elif account[0] == 2:# ID do perfil do financeiro
                return redirect(url_for('financeiro'))
            else: return  redirect(url_for('gestor'))# ID logado é dos gestores

        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Nome de Usuário/senha incorreto!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/login/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS #extensão para o arquivo baixado

@app.route('/file/<url>/<who>',methods=['GET','POST'])
def get_file(url,who):
    if request.method=='POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if url=='cota':
                if who == 'gestor':
                    return redirect(url_for('get_gestr'))
                elif who == 'diretor':
                    return redirect(url_for('finaliza_pedido'))# Gestor Aprova o pedido e encaminha para o diretor
            elif url=='soli':
                if who == 'gestor':
                    return redirect(url_for('post_solicitacao_gestor'))
                elif who == 'diretor':
                    return redirect(url_for('post_diretoria'))
    return render_template('file.html')

@app.route('/file2/<id>',methods=['GET','POST'])
def get_file2(id):
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = 'Financeiro-'+id +'.pdf'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))# Gestor Aprova o pedido e encaminha para o diretor
            return redirect('/')
    return render_template('file.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
# -------------------------------------------------------ARQUIVOS BAIXADOS----------------------
def enviarEmail(to_email,status,tipo,id,who):
    #cria a integração
    outlook = win32.Dispatch('Outlook.Application',pythoncom.CoInitialize())
    #cria o email
    email = outlook.CreateItem(0)
    #configuração
    email.To = f'{to_email}'
    email.Subject = f'{status}'
    email.HTMLBody = f"""
            <html>
                <body>
                    <p>Olá!<br>
                    Este é um email automático referente ao seu pedido de <strong>{tipo}</strong> de número <strong>{id}</strong><br>
                    Seu pedido foi <strong>{status}</strong> pela {who}
                    </p>
                </body>
            </html>"""
    email.Send()
    return flash('Email Enviado')
def enviarEmailFinan():
    #cria a integração
    outlook = win32.Dispatch('Outlook.Application',pythoncom.CoInitialize())
    #cria o email
    email = outlook.CreateItem(0)
    #configuração
    email.To = 'financeiro@cooperemb.com.br'
    email.Subject = "Não responder"
    email.HTMLBody = f"""
            <html>
                <body>
                    <p>Olá!<br>
                    Este é um email automático referente à um <strong>novo pedido</strong> encaminhado para o financeiro<br>
                    Lembrando que esta pedido já foi autorizado pela gestão e diretoria.
                    </p>
                </body>
            </html>"""
    return email.Send()
def enviarEmailConclu(to_email):
    #cria a integração
    outlook = win32.Dispatch('Outlook.Application',pythoncom.CoInitialize())
    #cria o email
    email = outlook.CreateItem(0)
    #configuração
    email.To = to_email
    email.Subject = 'Não responder'
    email.HTMLBody = f"""
            <html>
                <body>
                    <p>Olá!<br>
                    Este é um email automático referente à finalização do seu pedido<br>
                    Seu pedido foi <strong>Concluído</strong> pelo financeiro
                    </p>
                </body>
            </html>"""
    return email.Send()
def delete_query(db,id):
    sql = f'DELETE FROM {db} WHERE id_pedido = {id}'
    mycursor.execute(sql)
    mydb.commit()
    mycursor.execute('COMMIT')
    mydb.commit()


@app.route('/diretor/pendencias', methods=['GET', 'POST']) # JAVASCRIPT PEGA OS DADOS PARA MOSTRAR NO HTML
def diretor():
    if 'loggedin' in session and session['username'] == 'diretoria':
        return render_template('diretor.html')
    else:
        return redirect(url_for('login'))

@app.route('/gestor/pendencias', methods=['GET', 'POST'])  # JAVASCRIPT PEGA OS DADOS PARA MOSTRAR NO HTML
def gestor():
    if 'loggedin' in session:
        return render_template('gestor.html')
    else:
        return redirect(url_for('login'))

@app.route('/pedido/reprovado/<tipo>/<db>/<int:id>', methods=['GET','POST'])# ROTA PARA REPROVAR QUALQUER PEDIDO
def delete(tipo,db,id):
    if 'loggedin' in session:
        if tipo == 'cotacao':
            sql =f"DELETE FROM cota_{db} WHERE (id_pedido = {id})"
            mycursor.execute(sql)
            mydb.commit()
            if db == 'diretoria':
                return redirect(url_for('diretor'))
            else: return redirect(url_for('gestor'))
        elif tipo == 'solicitacao':
            sql = f"DELETE FROM soli_{db} WHERE (id_pedido = {id})"
            mycursor.execute(sql)
            mydb.commit()
            if db == 'diretoria':
                return redirect(url_for('diretor'))
            else: return redirect(url_for('gestor'))
        elif tipo == 'reembolso':
            sql = f"DELETE FROM rem_{db} WHERE (id_pedido = {id})"
            mycursor.execute(sql)
            mydb.commit()
            if db == 'diretoria':
                return redirect(url_for('diretor'))
            else: return redirect(url_for('gestor'))
    else:return redirect(url_for('login'))

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/cotacao/pedido', methods=['GET','POST'])# CRIA UMA COTAÇÃO
def create_cotacao():
    if request.method == 'POST':
        nome = request.form['nome']
        setor = request.form['setor']
        pa = request.form['PA']
        motivo = request.form['motivo']
        solicitacao1 = request.form['solicitacao1']
        valor1 = request.form['valor1']
        solicitacao2 = request.form['solicitacao2']
        valor2 = request.form['valor2']
        solicitacao3 = request.form['solicitacao3']
        valor3 = request.form['valor3']
        solicitacao4 = request.form['solicitacao4']
        valor4 = request.form['valor4']
        email = request.form['email']
        if solicitacao3 == '':
            sql = f"INSERT INTO cota_Pendencia (nome,email,PA,setor,motivo,solicitacao1,valor1,solicitacao2,valor2)" \
                  f" VALUES ('{nome}','{email}','{pa}','{setor}','{motivo}','{solicitacao1}'," \
                  f"'{valor1}','{solicitacao2}','{valor2}')"
            mycursor.execute(sql)
            mydb.commit()
            mycursor.execute(f'UPDATE cota_Pendencia SET solicitacao3 = NULL, valor3 = NULL, solicitacao4=NULL, valor4=NULL')
            mydb.commit()
        elif solicitacao4 == '':
            sql = f"INSERT INTO cota_Pendencia (nome,email,PA,setor,motivo,solicitacao1,valor1,solicitacao2,valor2,solicitacao3,valor3)" \
                  f" VALUES ('{nome}','{email}','{pa}','{setor}','{motivo}','{solicitacao1}'," \
                  f"'{valor1}','{solicitacao2}','{valor2}','{solicitacao3}','{valor3}')"
            mycursor.execute(sql)
            mydb.commit()
            mycursor.execute(
                f'UPDATE cota_Pendencia SET solicitacao4 = NULL, valor4 = NULL')
            mydb.commit()
        else:
            sql=f"INSERT INTO cota_Pendencia (nome,email,PA,setor,motivo,solicitacao1,valor1,solicitacao2,valor2,solicitacao3,valor3,solicitacao4,valor4)" \
                f" VALUES ('{nome}','{email}','{pa}','{setor}','{motivo}','{solicitacao1}'," \
                f"'{valor1}','{solicitacao2}','{valor2}','{solicitacao3}','{valor3}','{solicitacao4}','{valor4}')"
            mycursor.execute(sql)
            mydb.commit()
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = 'Cotacao-'+ nome +'.pdf'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('index'))
    return render_template('cota_pendencia.html')

@app.route('/cotacao/pendencias/<db>', methods=['GET'])# JAVASCRIPT PEGA OS DADOS PARA MOSTRAR NO HTML
def get_DB(db):
    mycursor.execute(f'SELECT * FROM cota_{db}')
    resu = mycursor.fetchall()
    resultados = list()
    for pedido in resu:
        resultados.append({
                'id': pedido[0],
                'email':pedido[1],
                'nome': pedido[2],
                'PA':pedido[3],
                'setor': pedido[4],
                'motivo': pedido[5],
                'solicitacao1': pedido[6],
                'valor1': pedido[7],
                'solicitacao2': pedido[8],
                'valor2':pedido[9],
                'solicitacao3': pedido[10],
                'valor3': pedido[11],
                'solicitacao4': pedido[12],
                'valor4': pedido[13]
        })
    return make_response(jsonify(resultados))


@app.route('/pedido/cotacao/aprovado/gestor/<int:id>', methods=['GET'])#GESTOR APROVA O PEDIDO E REDICIONA PARA  PAGINA PARA ENVIAR O PDF
def avanca_cota(id):
    if 'loggedin' in session:
        sql = f"INSERT INTO cota_diretoria (id_pedido,nome,email,PA,setor,motivo,solicitacao1,valor1,solicitacao2,valor2,solicitacao3,valor3,solicitacao4,valor4) " \
              f"SELECT id_pedido,nome,email,PA,setor,motivo,solicitacao1,valor1,solicitacao2,valor2,solicitacao3,valor3,solicitacao4,valor4 FROM cota_Pendencia " \
              f"WHERE id_pedido ='{id}'"
        mycursor.execute(sql)
        mydb.commit()
        scatch_mail = mycursor.execute(f'SELECT email FROM cota_diretoria WHERE id_pedido = {id}')
        catch_mail = mycursor.fetchone()
        delete_query('cota_Pendencia', id)
        enviarEmail(catch_mail[0], 'Não responder', 'Cotação', id, 'Gestão')
        return redirect('/file/cota/gestor')
    else:
        return redirect(url_for('login'))

@app.route('/cotacao/pendencia/diretor', methods=['POST'])
def finaliza_pedido():
    if 'loggedin' in session and session['username'] == 'diretoria':
            pedido=request.json
            id=pedido['id']
            sql=f"INSERT INTO fase2 (id_pedido,email,nome,PA,setor,motivo,solicitacao,valor) VALUES ('{pedido['id']}','{pedido['email']}','{pedido['nome']}','{pedido['PA']}','{pedido['setor']}'," \
                f"'{pedido['motivo']}','{pedido['solicitacao']}','{pedido['valor']}')"
            mycursor.execute(sql)
            mydb.commit()
            scatch_mail = mycursor.execute(f'SELECT email FROM cota_diretoria WHERE id_pedido = {pedido["id"]}')
            catch_mail = mycursor.fetchone()
            delete_query('cota_diretoria', pedido['id'])
            enviarEmail(catch_mail[0],'Não responder','Cotação',pedido['id'],'Diretoria')
            return redirect(f"/file2/{id}")
    else:return redirect(url_for('login'))

# ------------------------------------------------------------------SOLICITAÇÃO---------------------
# --------------------------------------------------------------------------------------------------
@app.route('/solicitacao/pedido', methods=['GET','POST'])# CRIA PEDIDO DE SOLICITAÇÃO
def post_solicitacao():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        setor = request.form['setor']
        pa = request.form['PA']
        motivo = request.form['motivo']
        solicitacao = request.form['solicitacao']
        valor = request.form['valor']
        sql=f"INSERT INTO soli_Pendencia (nome,email,PA,setor,motivo,solicitacao,valor) VALUES ('{nome}','{email}','{pa}','{setor}','{motivo}','{solicitacao}','{valor}')"
        mycursor.execute(sql)
        mydb.commit()
        file = request.files['arquivo']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = 'Solicitacao-'+nome+ '.pdf'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/')
    return render_template('soli_pendencia.html')

@app.route('/solicitacao/pendencias/<db>', methods=['GET'])
def get_solicitacao_db(db):
    mycursor.execute(f"SELECT * FROM soli_{db}")
    resu = mycursor.fetchall()
    resultados = list()
    for pedido in resu:
        resultados.append({
            'id': pedido[0],
            'email':pedido[1],
            'nome': pedido[2],
            'PA': pedido[3],
            'setor': pedido[4],
            'motivo': pedido[5],
            'solicitacao': pedido[6],
            'valor': pedido[7],
        })
    return make_response(jsonify(resultados))

@app.route('/pedido/solicitacao/aprovado/gestor/<int:id>', methods=['GET'])#GESTOR APROVA O PEDIDO E REDICIONA PARA  PAGINA PARA ENVIAR O PDF
def avanca_soli(id):
    if 'loggedin' in session:
        sql = f"INSERT INTO soli_diretoria (id_pedido,nome,email,PA,setor,motivo,solicitacao,valor) " \
              f"SELECT id_pedido,nome,email,PA,setor,motivo,solicitacao,valor FROM soli_Pendencia " \
              f"WHERE id_pedido ='{id}'"
        mycursor.execute(sql)
        mydb.commit()
        scatch_mail = mycursor.execute(f'SELECT email FROM soli_diretoria WHERE id_pedido = {id}')
        catch_mail = mycursor.fetchone()
        delete_query('cota_Pendencia', id)
        enviarEmail(catch_mail[0], 'Não responder', 'Solicitação', id, 'Gestão')
        return redirect('/file/soli/gestor')
    else:return redirect(url_for('login'))

@app.route('/pedido/solicitacao/aprovado/diretor/<int:id>', methods=['GET'])#DIRETOR APROVA O PEDIDO E REDICIONA PARA  PAGINA PARA ENVIAR O PDF
def fina_soli(id):
    if 'loggedin' in session and session['username'] == 'diretoria':
        sql = f"INSERT INTO fase2 (id_pedido,nome,email,PA,setor,motivo,solicitacao,valor) " \
              f"SELECT id_pedido,nome,email,PA,setor,motivo,solicitacao,valor FROM soli_diretoria " \
              f"WHERE id_pedido ='{id}'"
        mycursor.execute(sql)
        mydb.commit()
        scatch_mail = mycursor.execute(f'SELECT email FROM fase2 WHERE id_pedido = {id}')
        catch_mail = mycursor.fetchone()
        delete_query("cota_Pendencia", id)
        enviarEmail(catch_mail[0], 'Não Responder', 'Solicitação', id, 'Diretoria')
        return redirect('/file/soli/diretor')
    else:return redirect(url_for('login'))
# --------------------------------------------------------------------------------FASE 2 ----------------------
# -------------------------------------------------------------------------------------------------------------

@app.route('/solicitacao/fase2', methods=['GET'])
def get_fase2():
    mycursor.execute(f'SELECT * FROM fase2')
    resu = mycursor.fetchall()
    resultados=list()
    for pedido in resu:
        resultados.append({
            'id': pedido[0],
            'email': pedido[1],
            'nome': pedido[2],
            'PA': pedido[3],
            'setor': pedido[4],
            'motivo': pedido[5],
            'solicitacao': pedido[6],
            'valor':pedido[7]
        })
    return make_response(jsonify(resultados)) #Mostra para o cooperado o que falta para enviar


@app.route('/solicitacao/atualizar', methods=['GET','POST'])
def post_solicitacao_fase2():
    if request.method == 'POST':
        id = request.form['id']
        tipos = request.form.get('tipo')
        tipo = str(tipos)
        data_pgts = request.form['data']
        data_pgt = f'"{data_pgts}"'
        info = request.form['info']
        sql=f"INSERT INTO financeiro (id_pedido,email,nome,PA,setor,motivo,solicitacao,valor) SELECT id_pedido,email,nome,PA,setor,motivo,solicitacao,valor FROM fase2 WHERE (id_pedido={id})"
        mycursor.execute(sql)
        mydb.commit()
        sql2=f'UPDATE financeiro SET data_pagamento = {data_pgt}, tipo = {tipo}, categoria ="Solicitação", info = "{info}"  WHERE (id_pedido= {id})'
        mycursor.execute(sql2)
        mydb.commit()
        sql3="COMMIT"
        mycursor.execute(sql3)
        mydb.commit()
        delete_query('fase2', id)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = 'Financeiro-#' + id+ '.pdf'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            #Cooperado envia o dados atualizados para o financeiro
        enviarEmailFinan()
        return redirect(f'fase2/{id}')
    return render_template('fase2.html')
# -------------------------------------------------------------------------------FINANCEIRO------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------

@app.route('/financeiro',methods=['GET'])
def get_financeiro():
    mycursor.execute(f"SELECT * FROM financeiro")
    resu = mycursor.fetchall()
    resultados =list()
    for pedido in resu:
        resultados.append({
            'id': pedido[0],
            'email':pedido[1],
            'categoria':pedido[2],
            'nome': pedido[3],
            'PA': pedido[4],
            'setor': pedido[5],
            'motivo': pedido[6],
            'solicitacao': pedido[7],
            'descricao':pedido[8],
            'destino':pedido[9],
            'valor': pedido[10],
            'tipo':pedido[11],
            'data de pagamento': pedido[12],
            'info':pedido[13]
        })
    return make_response(jsonify(resultados)) # Financeiro olha as pendencias

@app.route('/financeiro/pendencias', methods=['GET','POST'])
def financeiro():
    if 'loggedin' in session and session['username'] == 'financeiro':
        if request.method == 'POST':
            id = request.form['id']
            data = request.form['data']
            obs = request.form['obs']
            sql = f"INSERT INTO Finalizados (id_pedido,nome,PA,setor,motivo,solicitacao,descricao,destino,valor,tipo,data_pagamento) " \
                  f"SELECT id_pedido,nome,PA,setor,motivo,solicitacao,descricao,destino,valor,tipo,data_pagamento FROM financeiro WHERE (id_pedido={id})"
            mycursor.execute(sql)
            mydb.commit()
            sql2 = f'UPDATE Finalizados SET pagamento_final = {data}, obs = {obs}  WHERE (id_pedido={id})'
            mycursor.execute(sql2)
            mydb.commit()
            mycursor.execute('COMMIT')
            mydb.commit()
            scatch_mail = mycursor.execute(f'SELECT email FROM financeiro WHERE id_pedido = {id}')
            catch_mail = mycursor.fetchone()
            delete_query('financeiro', id)
            enviarEmailConclu(catch_mail[0])
            return redirect(url_for('financeiro'))  # financeiro finaliza
        return render_template('financeiro.html')
    else:return redirect(url_for('login'))
# -----------------------------------------------------------------------------------REEMBOLSO---------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------
@app.route('/reembolso/pedido', methods=['GET','POST'])
def post_reembolso():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        pa = request.form['pa']
        setor = request.form['setor']
        motivo = request.form['motivo']
        desc = request.form['desc']
        dest = request.form['dest']
        valor = request.form['valor']
        sql=f"INSERT INTO rem_pendencias (nome,email,PA,setor,motivo,descricao,destino,valor) VALUES ('{nome}','{email}','{pa}','{setor}','{motivo}','{desc}','{dest}','{valor}')"
        mycursor.execute(sql)
        mydb.commit()
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = 'Reembolso-'+nome + '.pdf'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return  redirect(url_for('post_reembolso')) # Um novo pedido de reembolso é criado
    return render_template('rem_pendencia.html')

@app.route('/reembolso/pendencia/<db>', methods=['GET'])
def get_reembolso(db):
    mycursor.execute(f"SELECT * FROM rem_{db}")
    resu = mycursor.fetchall()
    resultados=list()
    for pedido in resu:
        resultados.append({
            'id': pedido[0],
            'email': pedido[1],
            'nome': pedido[2],
            'PA': pedido[3],
            'setor': pedido[4],
            'motivo': pedido[5],
            'descricao': pedido[6],
            'destino': pedido[7],
            'valor':pedido[8]
        })
    return make_response(jsonify(resultados)) # gestor observa as pendencias de reembolso

@app.route('/pedido/reembolso/aprovado/gestor/<int:id>', methods=['GET'])#GESTOR APROVA O PEDIDO E REDICIONA PARA  PAGINA PARA ENVIAR O PDF
def avanca_rem(id):
    if 'loggedin' in session:
        sql = f"INSERT INTO rem_diretoria (id_pedido,nome,email,PA,setor,motivo,descricao,destino,valor) " \
              f"SELECT id_pedido,nome,email,PA,setor,motivo,descricao,destino,valor FROM rem_pendencias " \
              f"WHERE id_pedido ='{id}'"
        mycursor.execute(sql)
        mydb.commit()
        scatch_mail = mycursor.execute(f'SELECT email FROM rem_diretoria WHERE id_pedido = {id}')
        catch_mail = mycursor.fetchone()
        delete_query('rem_pendencias', id)
        enviarEmail(catch_mail[0], 'Não Responder', 'Solicitação', id, 'Gestão')
        return redirect('/file/rem/gestor')
    else:return redirect(url_for('login'))

@app.route('/pedido/reembolso/aprovado/diretor/<int:id>', methods=['GET'])
def finaliza_rem(id):
    if 'loggedin' in session and session['username'] == 'diretoria':
        sql = f"INSERT INTO financeiro (id_pedido,nome,email,PA,setor,motivo,descricao,destino,valor) " \
              f"SELECT id_pedido,nome,email,PA,setor,motivo,descricao,destino,valor FROM rem_diretoria " \
              f"WHERE id_pedido ='{id}'"
        mycursor.execute(sql)
        mydb.commit()
        scatch_mail = mycursor.execute(f'SELECT email FROM financeiro WHERE id_pedido = {id}')
        catch_mail = mycursor.fetchone()
        delete_query('rem_diretoria', id)
        enviarEmail(catch_mail[0], 'Não Responder', 'Solicitação', id, 'Diretoria')
        return redirect('/file/rem/diretor')
    else:return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
