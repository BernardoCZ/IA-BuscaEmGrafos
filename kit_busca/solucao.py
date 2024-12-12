# Permite usar a classe Nodo dentro da classe Nodo
from __future__ import annotations

from asyncio.windows_events import NULL
import time
from typing import Iterable, Set, Tuple
from queue import PriorityQueue
import numpy as np

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """

    estado = "12345678_"
    pai = NULL
    acao = NULL
    custo = -1
    filhos = set()

    def __init__(self, estado:str, pai:Nodo, acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
    def __lt__(self, other):
        return self.estado < other.estado


objectivo = "12345678_"


def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # Salva a posição do espaço vazio no estado atual
    empty = estado.find('_')

    # Transforma string do estado em uma lista
    stateList = list(estado)

    # Inicializa conjunto de retorno
    actions = set()
    
    # Adiciona a ação "acima" caso o espaço vazio não esteja na primeira linha
    if empty > 2:
        newStateList = stateList.copy()
        newStateList[empty] = newStateList[empty - 3]
        newStateList[empty - 3] = '_'
        actions.add(("acima", ''.join(newStateList)))

    # Adiciona a ação "baixo" caso o espaço vazio não esteja na última linha
    if empty <= 5:
        newStateList = stateList.copy()
        newStateList[empty] = newStateList[empty + 3]
        newStateList[empty + 3] = '_'
        actions.add(("abaixo", ''.join(newStateList)))

    # Adiciona a ação "esquerda" caso o espaço vazio não esteja na primeira coluna
    if empty % 3 != 0:
        newStateList = stateList.copy()
        newStateList[empty] = newStateList[empty - 1]
        newStateList[empty - 1] = '_'
        actions.add(("esquerda", ''.join(newStateList)))

    # Adiciona a ação "direita" caso o espaço vazio não esteja na última coluna
    if (empty + 1) % 3 != 0:
        newStateList = stateList.copy()
        newStateList[empty] = newStateList[empty + 1]
        newStateList[empty + 1] = '_'
        actions.add(("direita", ''.join(newStateList)))

    # Retorna o conjunto de tuplas (ação, estado atingido)
    return actions



def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # Inicializa conjunto de retorno
    filhos = set()

    # Pega o estado recebido
    estado = nodo.estado

    # Conjunto de sucessores de um dado estado
    sucessores = sucessor(estado)

    # Loop por sucessores do estado
    for s in sucessores:
        move = s[0]
        next_state = s[1]
        filho = Nodo(next_state, nodo, move, nodo.custo + 1)
        nodo.filhos.add(filho)
        filhos.add(filho)
    return filhos


def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # Inicia nodo com estado enviado
    inicio = Nodo(estado, NULL, NULL, 0)

    # Conjunto de estados explorados pelo algoritmo
    explorados = set()

    # fronteira é uma lista de elementos prioritários
    fronteira = PriorityQueue()

    # O início é adicionado aos estados fronteira
    fronteira.put((0,inicio))

    iteracoes = 0
    inicio_timer = time.time()

    while(True): # Executa até achar estado ótimo ou erro
        iteracoes = iteracoes + 1
        if(fronteira.empty()): # Tudo foi explorado sem sucesso
            break
        v = fronteira.get()[1] # Retorna o estado com menor valor na fila, por exemplo em {(1, xx), (2,yy), (3, zz)} retorna xx
        if(v.estado == objectivo): # Se a fronteira selecionada = objetivo, retorna resultado
            fim_timer = time.time()
            print("\nHamming: iteracoes - " + str(iteracoes) + " /// expandidos - " + str(len(explorados)) + f" /// Tempo de execução - {(fim_timer - inicio_timer):.4f} segundos", end='\n')
            return caminho(v)
        if(not v.estado in explorados): # Se a fronteira selecionada não foi explorada
            explorados.add(v.estado)
            vizinhos = expande(v)
            for vizinho in vizinhos: # Para cada estado vizinho do atual
                if(not vizinho.estado in explorados): # Se o estado vizinho não foi explorado, torna-se fronteira
                    fronteira.put((vizinho.custo + hamming(vizinho), vizinho))

def hamming(nodo:Nodo)->int:
    estado = nodo.estado
    distancia_hamming = 0
    for i in range(len(estado)):
        # Comparação de igualdade de caracteres para soma de custo
        if((estado[i] != '_') and (estado[i] != objectivo[i])):
            distancia_hamming += 1

    return distancia_hamming

def caminho(nodo:Nodo)->str:
    acoes = []
    nodo_Rec = nodo
    while(nodo_Rec.pai != NULL):
        acoes.insert(0, nodo_Rec.acao)
        nodo_Rec = nodo_Rec.pai
    return acoes

def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    
    # Inicia nodo com estado enviado
    inicio = Nodo(estado, NULL, NULL, 0)

    # Conjunto de estados explorados pelo algoritmo
    explorados = set()

    # fronteira é uma lista de elementos prioritários
    fronteira = PriorityQueue()

    # O início é adicionado aos estados fronteira
    fronteira.put((0,inicio))

    iteracoes = 0
    inicio_timer = time.time()

    while(True): # Executa até achar estado ótimo ou erro
        iteracoes = iteracoes + 1
        if(fronteira.empty()): # Tudo foi explorado sem sucesso
            break
        v = fronteira.get()[1] # Retorna o estado com menor valor na fila, por exemplo em {(1, xx), (2,yy), (3, zz)} retorna xx
        if(v.estado == objectivo): # Se a fronteira selecionada = objetivo, retorna resultado
            fim_timer = time.time()
            print("\nManhattan: iteracoes - " + str(iteracoes) + " /// expandidos - " + str(len(explorados)) + f" /// Tempo de execução - {(fim_timer - inicio_timer):.4f} segundos", end='\n')
            return caminho(v)
        if(not v.estado in explorados): # Se a fronteira selecionada não foi explorada
            explorados.add(v.estado)
            vizinhos = expande(v)
            for vizinho in vizinhos: # Para cada estado vizinho do atual
                if(not vizinho.estado in explorados): # Se o estado vizinho não foi explorado, torna-se fronteira
                    fronteira.put((vizinho.custo + manhattan(vizinho), vizinho))                
   

def manhattan(nodo:Nodo)->int:
    distancia_manhattan = 0
    #transforma o valor do array do estado atual em um grid 3x3 do 8 puzzle
    state = np.array(list(nodo.estado))
    grid = state.reshape(3,3)
    obj = np.array(list(objectivo))
    target = obj.reshape(3,3)
    
    #grid do estado é percorrido e comparado com o objetivo
    for i in range(3):
     for j in range(3):
            if grid[i,j] != '_':
                v = grid[i,j]
                posicao_target = np.where(target == v)
                #quantidade de movimentos necessárias para uma peça estar na sua posição target é acumulada em distancia_manhattan
                distancia_manhattan += (abs(i - posicao_target[0]) + abs(j - posicao_target[1]))                
    
    return distancia_manhattan
        






#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
    