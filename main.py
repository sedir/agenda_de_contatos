# Importacao do modulo `pickle` para serializacao de objetos
import pickle
# Importacao do modulo `PySimpleGUI`, renomeado para `sg` (para facilitar o uso)
# usado para construcao de interfaces graficas
import PySimpleGUI as sg
# Importacao da classe Contato contida no modulo `agenda`
from agenda import Contato


# Definicao da variavel que corresponde a janela do programa
janela = None

# Loop infinito para responder as mudanças da tela
while True:

    # Tente executar o codigo a seguir
    try:
        # Abra o arquivo dados.dat em modo de leitura em bytes
        with open('dados.dat', 'rb') as arquivo:
            # Deserialize os dados do arquivo para um objeto de lista de contatos
            agenda = pickle.load(arquivo)
    # Caso seja lancado algum erro, considere que a lista de contatos
    # esta vazia
    except:
        agenda = []

    # Definicao do layout da coluna esquerda
    # Listbox considera os valores da lista de contatos `agenda` para popular
    # a listagem e determina a chave `lista` para acesso posterior 
    coluna_esquerda = [
        [sg.Listbox(agenda, key='lista', size=(30, 20), select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
    ]

    # Definicao do layout da coluna direita
    # Cria os InputText e determina as chaves `nome` e `telefone` para acesso posterior
    # e os botoes de criacao e remocao de contatos e de fechar 
    coluna_direita = [
        [sg.Text('Nome', size=(10,1)), sg.InputText(key='nome')],
        [sg.Text('Telefone', size=(10,1)), sg.InputText(key='telefone')],
        [sg.Ok('Criar contato'), sg.Ok('Remover contato selecionado'), sg.Cancel('Fechar')]
    ]

    # Layout final, unificando as colunas
    layout = [
        [sg.Column(coluna_esquerda), sg.Column(coluna_direita)],
    ]

    # Caso a janela nao tenha sido criada antes, crie-a e defina o layout
    if janela is None:
        janela = sg.Window('Agenda de Contatos', layout=layout)
    
    # Metodo que aguarda ate que o usuario tenha clicado em um botao
    # e retorna os valores da janela e qual botao foi clicado
    botao, valores = janela.read()

    # Se foi clicado para criar o contato, entao...
    if botao == 'Criar contato':
        # Abra o arquivo dados.dat em modo de escrita em bytes
        with open('dados.dat', 'wb') as arquivo:
            # Crie um objeto de contato baseado nos valores
            contato = Contato(valores['nome'], valores['telefone'])
            # Adicione o contato na lista agenda
            agenda.append(contato)
            # Serialize (transforme) a lista de contatos para o arquivo
            pickle.dump(agenda, arquivo)
            # Limpe os campos do formulario
            janela['nome'].update('')
            janela['telefone'].update('')
            # Atualize a lista de contatos
            janela['lista'].update(agenda)

    # Se foi clicado para remover o contato, entao...
    elif botao == 'Remover contato selecionado':
        # Abra o arquivo dados.dat em modo de escrita em bytes
        with open('dados.dat', 'wb') as arquivo:
            # Itere sobre os indices selecionados da lista de contatos
            # de forma reversa, pois remover de tras para frente nao gera
            # mudancas nos indices consecutivos
            for indice in reversed(sorted(janela['lista'].get_indexes())):
                # Remove o elemento da agenda no indice especificado
                del agenda[indice]

            # Serialize (transforme) a lista de contatos para o arquivo
            pickle.dump(agenda, arquivo)

            # Atualize a lista de contatos
            janela['lista'].update(agenda)

    # Caso nenhum dos botoes anteriores tenha sido clicado
    # entao encerra o loop e finaliza o programa
    else:
        break