
import streamlit as st
import pandas as pd

# Dicionários do cardápio
menu_bebidas = {
    "Item": ["Skol 600ml", "Original 600ml", "Brahma 600ml", "Skol Lata"],
    "Preço": [12.00, 13.00, 14.00, 6.00]
}

menu_refeicoes = {
    "Item": ["Espetinho Completo", "Filé de Frango", "Feijoada Completa"],
    "Preço": [20.00, 22.00, 30.00]
}

# Criando DataFrames para melhor visualização
df_bebidas = pd.DataFrame(menu_bebidas)
df_refeicoes = pd.DataFrame(menu_refeicoes)

# Inicializa a conta do cliente, garantindo que todos os atributos existam
if "pedidos_por_mesa" not in st.session_state:
    st.session_state.pedidos_por_mesa = {}  # Dicionário para armazenar pedidos por mesa
    st.session_state.total_por_mesa = {}  # Dicionário para armazenar o total de cada mesa

st.title("Cardápio Digital")

# Entrada do número da mesa
mesa = st.text_input("Número da mesa:", value="")
if mesa:
    st.session_state.mesa = mesa

# Exibir o cardápio com pandas
st.subheader("Bebidas")
st.dataframe(df_bebidas, hide_index=True)

st.subheader("Refeições")
st.dataframe(df_refeicoes, hide_index=True)

# Seleção do pedido
opcoes = df_bebidas["Item"].tolist() + df_refeicoes["Item"].tolist()
pedido = st.selectbox("Escolha seu pedido:", [""] + opcoes)

# Botão para adicionar pedido
if st.button("Adicionar Pedido"):
    if pedido and mesa:
        # Buscar preço do item
        preco = df_bebidas.loc[df_bebidas["Item"] == pedido, "Preço"]
        if preco.empty:
            preco = df_refeicoes.loc[df_refeicoes["Item"] == pedido, "Preço"]
        preco = preco.values[0]

        # Se a mesa ainda não estiver no dicionário, inicializa
        if mesa not in st.session_state.pedidos_por_mesa:
            st.session_state.pedidos_por_mesa[mesa] = []
            st.session_state.total_por_mesa[mesa] = 0
        
        # Adicionando pedido e somando total para a mesa
        st.session_state.pedidos_por_mesa[mesa].append((pedido, preco))
        st.session_state.total_por_mesa[mesa] += preco
        st.success(f"{pedido} adicionado para a mesa {mesa}!")
    elif not mesa:
        st.error("Por favor, informe o número da mesa antes de fazer o pedido.")

# Exibir pedidos atuais com número da mesa
if mesa in st.session_state.pedidos_por_mesa and st.session_state.pedidos_por_mesa[mesa]:
    st.subheader(f"Pedidos da Mesa {mesa}")
    df_pedidos = pd.DataFrame(st.session_state.pedidos_por_mesa[mesa], columns=["Item", "Preço"])
    st.dataframe(df_pedidos, hide_index=True)

# Mostrar total para a mesa selecionada
if mesa in st.session_state.total_por_mesa:
    st.subheader(f"Total da Mesa {mesa}: R$ {st.session_state.total_por_mesa[mesa]:.2f}")

# Botão para encerrar a conta da mesa
if st.button("Encerrar Conta"):
    if mesa:
        st.success(f"Conta da Mesa {mesa} encerrada! Total a pagar: R$ {st.session_state.total_por_mesa[mesa]:.2f}")
        st.session_state.pedidos_por_mesa[mesa] = []  # Limpa os pedidos dessa mesa
        st.session_state.total_por_mesa[mesa] = 0  # Zera o total dessa mesa
        st.session_state.mesa = ""  # Limpa a mesa atual (opcional)
    else:
        st.error("Nenhuma mesa selecionada para encerrar a conta.")