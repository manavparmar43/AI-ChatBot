from flask import Blueprint, request,render_template,redirect,url_for,flash
from app  import db,app,socketio
from models.user_db import UserRegister
from models.chat_db import FileStore,Chat_communication
from datetime import datetime
from openai import OpenAI
from flask_socketio import emit
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from langchain_openai import ChatOpenAI
from store_data.store_data import *
from config.config_template import OPENAI_KEY
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
messages = [
    SystemMessage(content="You are a helpful assistant."),
]

chat=ChatOpenAI(
    openai_api_key=OPENAI_KEY,
    model="gpt-3.5-turbo"
)

view_blueprint=Blueprint("user",__name__)

bcrypt = Bcrypt(app) 
llm=ChatOpenAI(openai_api_key=OPENAI_KEY,model="gpt-3.5-turbo",temperature=0.7)
output_parser = StrOutputParser()

login_manager = LoginManager(app)
login_manager.login_view = 'user.Login'
msg_data=[
    ("system", "You are a helpful assistant."),
    ("user","{input}")
]



@login_manager.user_loader
def load_user(user_id):
     return UserRegister.query.get(user_id)


 
@socketio.on("connect")
def handle_connect():
    """Here, this funcation can connect 
       the web server to socketio"""
    pass


@socketio.on("message")
def handle_connect(message):
    
    """ Here, in this funcation use 
        to get user request and generate the responce """
        
    msg_data.append(("user", message))
    prompt = ChatPromptTemplate.from_messages(msg_data)
    chain = prompt | llm | output_parser
    response = chain.invoke({"input": message})
    msg_data.append(("assistant", response))
    store_chat_data([{"role":"user","content":message},{"role":"assistant","content":response}],current_user.id)
    emit("ai_res",{"message":response},broadcast=True)




@socketio.on("rag_check_file")
def handle_rag_check_file():
    """
      Here, this funcation can check the file 
      is how many files exists to perticular user
    """
    document=[]
    files=FileStore.query.filter_by(user_id=current_user.id).all()
    for file in files:
        document.append(file.collection_name)    
    emit("rag_check_file_res",{"data":document},broadcast=True)
    


@socketio.on("rag_doc_select")
def handle_rag_document_select(message):
    
    """
        Here, in this funcation can select the document 
        example user send a message is "Python" 
        it can search get document is Python
    """
    
    files=FileStore.query.filter_by(collection_name=message.capitalize()).first()
    if files:
        emit("rag_doc_res",{"message":"Ask Question",'collection_name':files.collection_name},broadcast=True)
    else:
        emit("rag_doc_res",{"message":"Enter valid input"},broadcast=True) 
        


def augment_prompt(db,query: str):
    
    results = db.similarity_search(query)
    source_knowledge = results[0].page_content
    augmented_prompt = f"""Using the contexts below, answer the query.
    Contexts:
    {source_knowledge}
    Query: {query}"""
    return augmented_prompt        
        
        
        
@socketio.on("rag_message")
def handle_rag_message(message,collection_name):
    
    """
        Here, this funcation is handle the RAG message 
        user send question it can related document so AI 
        generate the responce
    """
    
    
    file=FileStore.query.filter_by(collection_name=collection_name).first()
    db = create_retrieve_database(file.document_file_path,file.collection_id)
    humanprompt = HumanMessage(
            content=augment_prompt(db,message)
    )
    messages.append(humanprompt)
    res = chat(messages)
    messages.append(AIMessage(content=str(res.content)))
    emit("rad_message_res",{"rag_message":res.content},broadcast=True)
        


@view_blueprint.route("/register",methods=['GET',"POST"])
def Register():
    
    """
        This funcation use to Register user
    """
    
    if request.method == "POST":       
        [msg,status]=store_user_data(
            request.form['name'],
            request.form['username'],
            request.form['email'],
            request.form['password']
        )
        if status == "error":
            flash(msg,status)
            return redirect(url_for('user.Register'))
        flash(msg,status)
        return redirect(url_for('user.Register'))
    return render_template("register.html")



@view_blueprint.route("/",methods=['GET',"POST"])
def Login():
    """
        This funcation use to Login user
    """
    if request.method == 'POST':
        user = UserRegister.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('user.Chat'))
        else:
            flash('Login detail invalid', 'error') 
            return render_template("login.html")
    return render_template("login.html")



@view_blueprint.route("/chat",methods=['GET',"POST"])
@login_required
def Chat():
    """
        This funcation Render and display chat page
    """
    file_data=FileStore.query.filter_by(user_id=current_user.id).all()
    return render_template("chat.html",files=file_data,name=current_user.name.capitalize())
    

@view_blueprint.route("/logout",methods=['GET'])
@login_required
def Logout():
    """
        This funcation is use to logout the login user
    """
    logout_user()
    return redirect(url_for('user.Login'))        
    
    
@view_blueprint.route("/choose-file",methods=['GET','POST'])
@login_required
def ChooseFile():
    
    """
        Here,This funcation is use to display the, 
        Choose file page for RAG implementation
    """
    
    if request.method == 'POST':
        [msg,status]=store_file_data(request.files['file'],current_user.id,request.form['collection'])
        if status == "error":
            flash(msg,status)
            return redirect(url_for('user.ChooseFile'))
        flash(msg,status)
        return redirect(url_for("user.ChooseFile"))
    return render_template("choose_file.html")


    



