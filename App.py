import sqlite3
from datetime import datetime
from pacote.sub_pacote.funcoes import *




def adicionar_clientes(nome, telefone, data_nascimento, cpf):
     if not validar_cpf(cpf):
        return "CPF invalido"
     if not validar_telefone(telefone):
        return 'telefone invalido'
   
     banco = None
     try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()

        cursor.execute("""INSERT INTO clientes (nome, telefone, data_nascimento, cpf)
                        VALUES (?, ?, ?, ?) 
                        """, (nome, telefone, data_nascimento, cpf))
        banco.commit()
        return "Cliente adicionado com sucesso!"
     except sqlite3.Error as erro:
        if banco:
            banco.rollback()
        return f"Erro ao adicionar cliente: {erro}"
     finally:
        if banco:
            banco.close()



def adicionar_produtos(nome, marca, categoria, lote, validade, quantidade):
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()

        cursor.execute("""INSERT INTO produtos (nome, marca, categoria, lote, validade, quantidade)
                       VALUES(?,?,?,?,?,?)
                       """,(nome, marca, categoria, lote, validade, quantidade))
        banco.commit()
        return "produto adicionado com sucesso!"
    except sqlite3.Error as erro:
        if banco:
            banco.rollback()
        return f"Erro ao adicionar produto: {erro}"
    finally:
        if banco:
            banco.close()


def listar_produtos():
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()

        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        return produtos
    except sqlite3.Error as erro:
        return f"Erro ao listar produtos: {erro}"
    finally:
        if banco:
            banco.close()

 
def editar_produtos(id, nova_quantidade):
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()
        cursor.execute("SELECT nome, quantidade From produtos Where id = ?",(id,))
        produto = cursor.fetchone()
        if produto is None:
            print ( f"produto com {id} não encontrado.")
        else:
            nome_do_produto, quantidade_anterior = produto
            print (f"produto encontrado: {nome_do_produto}")
            print (f" quantidade antes: {quantidade_anterior} | quantidade atual {nova_quantidade}")
        
        
        cursor.execute("""
                    
                UPDATE  produtos
                SET quantidade = ? 
                WHERE id = ?
                    
                """,(nova_quantidade, id))
    
        banco.commit()
    except sqlite3.Error as erro:
        if banco:
            banco.rollback()
            return f'erro ao editar o produto: {erro}'
    finally:
        if banco:
            banco.close()

def excluir_cliente(id,):
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()
        cursor.execute (' DELETE FROM clientes WHERE id = ?',(id,))
        banco.commit()
        return True
    except sqlite3.Error as erro:
        if banco:
            banco.rollback()
        return False
    finally:
        if banco:
            banco.close()

def excluir_produto(id,):
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()
        cursor.execute (' DELETE FROM produtos WHERE id = ?',(id,))
        banco.commit()
        return True
    except sqlite3.Error as erro:
        if banco:
            banco.rollback()
        return False
    finally:
        if banco:
            banco.close()

def realizar_venda(valor, quantidade, id_cliente, id_produto):
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()

        cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,))
        cliente = cursor.fetchone()
        if not cliente:
            return "Cliente não encontrado."
        
        cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (id_produto,))
        produto = cursor.fetchone()
        if not produto:
            return "Produto não encontrado."
        if produto[0] < quantidade:
            return "Quantidade em estoque insuficiente."
        
        data_atual = datetime.now().strftime("%d/%m/%Y")
        cursor.execute("""
            INSERT INTO vendas (valor, data, id_cliente, id_produto)
            VALUES (?, ?, ?, ?)
        """, (valor, data_atual, id_cliente, id_produto))

        nova_quantidade = produto[0] - quantidade
        cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_quantidade, id_produto))

        banco.commit()
        return "Venda registrada com sucesso!"
    except sqlite3.Error as erro:
        if banco:
            banco.rollback()
        return f"Erro ao registrar venda: {erro}"
    finally:
        if banco:
            banco.close()

def listar_clientes():
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()

        cursor.execute("SELECT * FROM clientes")
        produtos = cursor.fetchall()
        return produtos
    except sqlite3.Error as erro:
        return f"Erro ao listar clientes: {erro}"
    finally:
        if banco:
            banco.close()

def editar_clientes(id, novo_telefone):
    banco = None
    try:
        banco = sqlite3.connect("estoX.db")
        cursor = banco.cursor()
        cursor.execute("SELECT nome, telefone From clientes Where id = ?",(id))
        produto = cursor.fetchone()
        if produto is None:
            return f"produto com {id} não encontrado."
        else:
            nome_do_produto, telefone_anterior = produto
            print (f"cliente encontrado: {nome_do_produto}")
            print (f" telefone anterior: {telefone_anterior} | telefone atual {novo_telefone}")
        
        
        cursor.execute("""
                    
                UPDATE clientes
                SET telefone = ? 
                WHERE id = ?
                    
                """,(novo_telefone, id))
    
        banco.commit()
    except sqlite3.Error as erro:
        if banco:
            banco.rollback()
            return f'erro ao editar o cliente: {erro}'
    finally:
        if banco:
            banco.close()

