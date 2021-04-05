from functools import reduce
from typing import List, Tuple, Set, Dict
from collections import defaultdict
import sys
from queue import Queue

number_of_states = 0
EPS = ""
SINK = -1
delta = dict()
final_states = set()
# mapare intre seturile de stari si indice
mapping = dict()
# alfabetul automatului
alphabet = set()
#
nfa = dict()
# coada pt stari
q = []
def foo(d):
	for k, v in d.items():
		print(k[0], k[1], v)
def compute(delta, source, mapping, q, finalStates, numberOfStates):
	# calculeaza epsilon closure si atribuie pt starea initiala, starea 0
	source_set = set()
	eps_vector = compute_eps_closure(delta, numberOfStates)
	source_set.update(eps_vector[0])
	idx = 0
	sink_flag = False
	# adauga pt a face mapare intre setul de stari si un indice
	# aka starea noua
	mapping[idx] = source_set
	# adauga in coada setul de stari
	q.append(source_set)
	idx += 1
	new_idx = 0
	while q:
		# scoate din coada si prelucreaza seturile de stari pt
		# fiecare caracter din alfabet si insereaza in dict nfa
		this_set = q.pop(0)
		for i in alphabet:
			if i != '':
				# creaza lista de stari pentru a le parcurge
				this_list = list(this_set)
				# setul pt esilon stari
				eps_set = set()
				for j in this_list:
					# pt fiecare stare din lista, extrage valoarea din dfa-ul delta
					# daca s-a consumat un cuvant adauga la set si epsilon tranzitiile
					if (j, i) in delta:
						sink_flag = True
						eps_set.update(delta[(j,i)])
						eps_list = list(eps_set)
						new_new_set = set()
						for e in eps_list:
							new_new_set.update(eps_vector[e])
				# daca nu s-a gasit nici o stare pt caracterul curent,
				# atunci avem un sink state
				if sink_flag == False:
					new_new_set = set()
					new_new_set.add(SINK)
				nfa[(new_idx, i, 'N')] = new_new_set
				# verificam sa nu avem deja setul de stari in mapping,
				# prevenim dublicatele
				if new_new_set in mapping.values():
					pass
				else:
				# daca nu s-a gasit setul de stari, atunci in adaugam
				# in coada de asteptare si facem maparea catre acest set
					mapping[idx] = new_new_set
					q.append(new_new_set)
					idx += 1
				sink_flag = False
		new_idx += 1
	# returnam nfaul corespunzator
	return nfa
def compute_eps_closure(delta, numberOfStates):
	# facem un dfs pe starile epsilon
	eps_vector = [0] * numberOfStates
	for i in range (0, numberOfStates):
		if (i, '') in delta:
			visited = [0] * 100
			eps_set = set()
			make_eps_rec(visited, i, eps_set)
			eps_vector[i] = eps_set
		else:
			eps_set = set()
			eps_set.add(i)
			eps_vector[i] = eps_set
	return eps_vector
def make_eps_rec(visited, source, eps_set):
	if (source, '') in delta:
		eps_set.add(source)
		set_of_stares = delta[(source, '')]
		list_of_states = list(set_of_stares)
		visited[source] = 1
		for i in range(0, len(list_of_states)):
			if visited[list_of_states[i]] == 0:
				eps_set.add(list_of_states[i])
				make_eps_rec(visited, list_of_states[i], eps_set)
def convert(nfa, mapping, final_states):
	# convertire de la dictionarul de nfa intr-un mod mai human readable
	# calculez si starile finale si numarul de stari
	new_nfa = dict()
	for k, v in nfa.items():
		value = list(mapping.keys())[list(mapping.values()).index(v)]
		new_nfa[k] = value
		# verifica tripletul (stare, carater, caracter)
		# 'F' ==> stare finala, si adauga in lista de stari finale
		if k[2] == 'F':
			final_states.add(new_nfa[k])
		number_of_states = k[0] + 1
	# returneaza numarul de stari si noul nfa cu starile finale
	return number_of_states, new_nfa
def check_if(nfa, finalStates):
	new_nfa = dict()
	final_states = list(finalStates)
	for i in final_states:
		for k, v in nfa.items():
			if i in v:
				new_nfa[(k[0], k[1], 'F')] = v
			else:
				new_nfa[(k[0], k[1], 'N')] = v
		break
	return new_nfa
if __name__ == '__main__':
	with open("tests/ref/nfa/random_file" + sys.argv[2][25:], "r") as file:
		numberOfStates = int(file.readline().rstrip())
		finalStates = set(map(int, file.readline().rstrip().split(" ")))
		while True:
			transition = file.readline().rstrip().split(" ")
			if transition == ['']:
				break
			if transition[1] == "eps":
				transition[1] = EPS
			delta[(int(transition[0]), transition[1])] = set(map(int, transition[2:]))
			alphabet.add(transition[1])
	original_stdout = sys.stdout
	with open(sys.argv[3], "w") as f:
		n = compute(delta, {0}, mapping, q, finalStates, numberOfStates)
		new_n = check_if(n, finalStates)
		new_nfa = convert(new_n, mapping, final_states)
		sys.stdout = f
		print(new_nfa[0])
		l = list(final_states)
		print(*l)
		foo(new_nfa[1])
		sys.stdout = original_stdout