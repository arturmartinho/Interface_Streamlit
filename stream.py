import streamlit as st
import requests as rq

URL = "https://aps3-back.onrender.com"

def tela_inicial():
    st.title("Tela inicial")

def minhas_bikes():
    r = rq.get(f'{URL}/bikes')
    status = r.status_code
    if status == 200:
        st.table(r.json())

def meus_usuarios():
    r = rq.get(f'{URL}/usuarios')
    status = r.status_code
    if status == 200:
        st.table(r.json())

def meus_emprestimos():
    r = rq.get(f'{URL}/emprestimos')
    status = r.status_code
    if status == 200:
        st.table(r.json())

def nova_bike():
    marca = st.text_input("Marca")
    modelo = st.text_input("Modelo")
    cidade = st.text_input("Cidade")
    if st.button('Cadastrar'):
        r = rq.post(f'{URL}/bikes', json={"marca": marca, "modelo": modelo, "cidade": cidade})
        if r.status_code == 201:
            st.success('Bicicleta cadastrada com sucesso')

def novo_usuario():
    cpf = st.text_input("CPF")
    data = st.text_input("Data de Nascimento")
    nome = st.text_input("Nome")
    if st.button('Cadastrar'):
        r = rq.post(f'{URL}/usuarios', json={"cpf": cpf, "data de nascimento": data, "nome": nome})
        if r.status_code == 201:
            st.success('Usuário cadastrado com sucesso')

def novo_emprestimo():
    id_usuario = st.text_input('Id do usuario')
    id_bike = st.text_input('Id da bike')
    d = st.text_input("Data Aluguel")
    if st.button("Cadastrar"):
        r = rq.get(f'{URL}/usuarios/{id_usuario}')
        q = rq.get(f'{URL}/bikes/{id_bike}')
        if r.status_code != 200 and q.status_code != 200:
            st.error('Usuário ou bike não encontrados')
        else:
            r = rq.post(f'{URL}/emprestimos/usuarios/{id_usuario}/bikes/{id_bike}', json={'id_usuario': id_usuario, 'id_bike': id_bike, 'data_aluguel': d})
            if r.status_code == 201:
                st.success("Empréstimo cadastrado com sucesso")

def dados_usuario():
    id = st.text_input('Id do usuario')
    if st.button('Buscar Usuario'):
        r = rq.get(f'{URL}/usuarios/{id}')
        st.table(r.json())
        st.session_state['Usuario'] = r.json()
    if 'Usuario' in st.session_state:
        c = st.text_input("cpf")
        n = st.text_input("nome")
        d = st.text_input("data")
        if st.button('Atualizar Usuario'):
            r = rq.put(f'{URL}/usuarios/{id}', json={"cpf": c, "data de nascimento": d, "nome": n})
            if r.status_code == 200:
                st.success('Usuário atualizado com sucesso')
        if st.button('Apagar Usuario'):
            r = rq.delete(f'{URL}/usuarios/{id}')
            if r.status_code == 204:
                st.success('Usuário apagado com sucesso')

def dados_bike():
    id = st.text_input('Id da bike')
    if st.button('Buscar Bike'):
        r = rq.get(f'{URL}/bikes/{id}')
        st.table(r.json())
        st.session_state['Bike'] = r.json()
    if 'Bike' in st.session_state:
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
        cidade = st.text_input("Cidade")
        if st.button('Atualizar Bike'):
            r = rq.put(f'{URL}/bikes/{id}', json={"marca": marca, "modelo": modelo, "cidade": cidade})
            if r.status_code == 200:
                st.success('Bike atualizada com sucesso')
        if st.button('Apagar Bike'):
            r = rq.delete(f'{URL}/bikes/{id}')
            if r.status_code == 204:
                st.success('Bike apagada com sucesso')

def apaga_emprestimo():
    id = st.text_input('Id do emprestimo')
    if st.button('Apagar Emprestimo'):
        r = rq.delete(f'{URL}/emprestimos/{id}')
        if r.status_code == 204:
            st.success('Empréstimo apagado com sucesso')
    

if __name__ == "__main__":
    tela_inicial()
    st.sidebar.subheader("Menu")
    opcao = st.sidebar.radio("", ["Minhas Bikes", "Meus Usuários", "Meus Empréstimos", "Nova Bike", "Novo Usuário", "Novo Empréstimo", "Dados Usuário", "Dados Bike", "Apagar Emprestimo"])
    
    if opcao == "Minhas Bikes":
        minhas_bikes()
    elif opcao == "Meus Usuários":
        meus_usuarios()
    elif opcao == "Meus Empréstimos":
        meus_emprestimos()
    elif opcao == "Nova Bike":
        nova_bike()
    elif opcao == "Novo Usuário":
        novo_usuario()
    elif opcao == "Novo Empréstimo":
        novo_emprestimo()
    elif opcao == "Dados Usuário":
        dados_usuario()
    elif opcao == "Dados Bike":
        dados_bike()
    elif opcao == "Apagar Emprestimo":
        apaga_emprestimo()