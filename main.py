#André Sapucaia de Araujo - 10418734
# -*- coding: utf-8 -*-
from grafoLista import Grafo 
import os

class AppRecomendacao:
    def __init__(self):
        self.g = None
        self.nomes_vertices = {}
        self.tipo_grafo = 0

    def menu(self):
        while True:
            print("\n" + "="*40)
            print("  SISTEMA DE LOOKS  ")
            print("="*40)
            print("a) Ler dados do arquivo grafo.txt")
            print("b) Gravar dados no arquivo grafo.txt")
            print("c) Inserir peca (Vertice)")
            print("d) Inserir combinacao (Aresta)")
            print("e) Remover peca (Vertice)")
            print("f) Remover combinacao (Aresta)")
            print("g) Mostrar conteudo do arquivo")
            print("h) Mostrar lista de adjacencia")
            print("i) Analisar Conexidade")
            print("r) RECOMENDAR LOOK")
            print("j) Encerrar")
            
            op = input("\nEscolha uma opcao: ").lower().strip()

            if op == 'a': self.ler_arquivo()
            elif op == 'g': self.mostrar_arquivo()
            elif op == 'j': break

            elif self.g is None:
                print("\n[AVISO] Voce precisa carregar o arquivo primeiro!")

            else:
                if op == 'b': self.gravar_arquivo()
                elif op == 'c': self.inserir_v()
                elif op == 'd': self.inserir_a()
                elif op == 'e': self.remover_v()
                elif op == 'f': self.remover_a()
                elif op == 'h': self.g.show()
                elif op == 'i': self.verificar_conexidade()
                elif op == 'r': self.recomendar()
                else: print("Opcao invalida.")

    def ler_arquivo(self):
        try:
            with open("grafo.txt", "r", encoding='utf-8') as f:
                linhas = [l.strip() for l in f.readlines() if l.strip()]
            
            self.tipo_grafo = int(linhas[0])
            n_vertices = int(linhas[1])
            self.g = Grafo(n_vertices)

            ptr = 2

            # VERTICES
            for _ in range(n_vertices):
                partes = linhas[ptr].split('"')
                idx = int(partes[0].strip())
                self.nomes_vertices[idx] = partes[1]
                ptr += 1

            # ARESTAS
            m_arestas = int(linhas[ptr])
            ptr += 1

            for _ in range(m_arestas):
                dados = linhas[ptr].split()
                self.g.insereA(int(dados[0]), int(dados[1]))
                ptr += 1

            print(f"\n[SUCESSO] {n_vertices} pecas carregadas!")

        except Exception as e:
            print(f"\n[ERRO NA LEITURA] {e}")

    # ================= MOSTRAR ARQUIVO =================
    def mostrar_arquivo(self):
        if os.path.exists("grafo.txt"):
            with open("grafo.txt", "r", encoding='utf-8') as f:
                print("\n--- CONTEUDO DO ARQUIVO ---")
                print(f.read())
        else:
            print("Arquivo nao encontrado.")

    # ================= INSERIR =================
    def inserir_v(self):
        nome = input("Nome da nova peca: ")
        novo_id = self.g.n
        self.nomes_vertices[novo_id] = nome
        self.g.listaAdj.append([])
        self.g.n += 1
        print(f"Peca {nome} adicionada com ID {novo_id}")

    def inserir_a(self):
        try:
            v = int(input("ID Peca 1: "))
            w = int(input("ID Peca 2: "))
            self.g.insereA(v, w)
            print("Combinacao criada!")
        except:
            print("Erro nos IDs.")

    # ================= REMOVER =================
    def remover_v(self):
        try:
            v = int(input("ID da peca a remover: "))

            if v >= self.g.n:
                print("ID invalido.")
                return

            for i in range(self.g.n):
                if v in self.g.listaAdj[i]:
                    self.g.listaAdj[i].remove(v)
                    self.g.m -= 1

            self.g.listaAdj[v] = []

            if v in self.nomes_vertices:
                del self.nomes_vertices[v]

            print(f"Peca {v} removida (conexoes apagadas).")

        except:
            print("Erro ao remover.")

    def remover_a(self):
        try:
            v = int(input("ID Peca 1: "))
            w = int(input("ID Peca 2: "))

            if w in self.g.listaAdj[v]:
                self.g.listaAdj[v].remove(w)
                self.g.m -= 1
                print("Combinacao removida!")
            else:
                print("Essa combinacao nao existe.")

        except:
            print("Erro nos IDs.")

    def verificar_conexidade(self):
        visitados = [False] * self.g.n

        def dfs(v):
            visitados[v] = True
            for vizinho in self.g.listaAdj[v]:
                if not visitados[vizinho]:
                    dfs(vizinho)

        dfs(0)

        if all(visitados):
            print("\nGrafo CONEXO")
        else:
            print("\nGrafo DESCONEXO")

    # ================= RECOMENDACAO =================
    def recomendar(self):
        try:
            id_b = int(input(f"ID da peca (0 a {self.g.n-1}): "))

            if id_b in self.nomes_vertices:
                print(f"\nPeça: {self.nomes_vertices[id_b]}")
                for v in self.g.listaAdj[id_b]:
                    print(f" -> Combina com: {self.nomes_vertices[v]}")
            else:
                print("ID invalido.")

        except:
            print("Erro.")

    def gravar_arquivo(self):
        try:
            with open("grafo.txt", "w", encoding='utf-8') as f:
                f.write(f"{self.tipo_grafo}\n{self.g.n}\n")

                for i, nome in self.nomes_vertices.items():
                    f.write(f"{i} \"{nome}\" 1\n")

                f.write(f"{self.g.m}\n")

                for v in range(self.g.n):
                    for w in self.g.listaAdj[v]:
                        f.write(f"{v} {w} 1\n")

            print("Arquivo salvo com sucesso!")

        except Exception as e:
            print(f"Erro ao salvar: {e}")


if __name__ == "__main__":
    AppRecomendacao().menu()
