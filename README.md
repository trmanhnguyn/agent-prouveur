# Agent-Prouveur

Projet de Licence 3 MIAGE – Université Paris Nanterre

## Description

Ce projet a pour objectif de développer une infrastructure permettant à un agent basé sur un LLM de générer, invalider et, à terme, démontrer des conjectures en théorie des graphes.

La première étape du projet consiste à réimplémenter un invalidateur de conjectures inspiré de celui décrit dans le mémoire d'HDR de François Delbot. L'invalidateur doit être capable de rechercher automatiquement des contre-exemples à des conjectures exprimées sous forme d'inégalités entre invariants de graphes.

Le projet est conçu selon une architecture modulaire compatible avec le protocole MCP (Model Context Protocol).

---

## Fonctionnalités implémentées

### Lecture de graphes au format graph6

Le module `graph_tools` permet :

* le chargement de graphes encodés au format graph6 ;
* la conversion en objets NetworkX ;
* le calcul de plusieurs invariants.

Invariants actuellement disponibles :

* nombre de sommets (`n`)
* nombre d'arêtes (`m`)
* densité (`density`)
* rayon (`radius`)
* diamètre (`diameter`)
* degré moyen (`avg`)
* degré minimum (`delta`)
* degré maximum (`Delta`)

---

### Vérification de conjectures

Le module `verifier` permet :

* le chargement de conjectures stockées en JSON ;
* l'évaluation des expressions mathématiques ;
* la vérification automatique de contre-exemples connus ;
* la génération de rapports CSV.

Conjectures actuellement testées :

* HDR-001
* HDR-002

---

### Recherche de contre-exemples

Le module `invalidator` contient :

#### Random Search

Génération aléatoire de graphes connexes et recherche de contre-exemples.

#### Local Search

Recherche locale basée sur des mutations du graphe :

* ajout d'arêtes ;
* suppression d'arêtes ;
* conservation des meilleures solutions selon une fonction de score.

---

### Serveur MCP

Le projet contient une première implémentation d'un serveur MCP permettant d'exposer les fonctionnalités d'invalidation sous forme d'outils réutilisables par un agent.

---

## Architecture

```text
src/
├── graph_tools/
│   └── graph_reader.py
│
├── verifier/
│   ├── verify.py
│   └── verify_all.py
│
├── invalidator/
│   ├── random_search.py
│   └── local_search.py
│
├── mcp_invalidator/
│   └── server.py
│
└── controller/
    └── test_invalidator.py
```

---

## Structure des données

```text
data/
└── false_conjectures/
    ├── HDR-001.json
    └── HDR-002.json
```

Chaque conjecture est décrite sous forme JSON :

```json
{
  "id": "HDR-001",
  "left_invariant": "density",
  "relation": "<=",
  "right_expression": "...",
  "known_counterexample": {
    "format": "graph6",
    "value": "..."
  }
}
```

---

## Dépendances

* Python 3.13
* NetworkX
* MCP
* Matplotlib

Installation :

```bash
pip install networkx matplotlib mcp
```

---

## Exécution

### Vérification d'une conjecture

```bash
python src/verifier/verify.py
```

### Vérification de toutes les conjectures

```bash
python src/verifier/verify_all.py
```

### Recherche aléatoire

```bash
python src/invalidator/random_search.py
```

### Recherche locale

```bash
python src/invalidator/local_search.py
```

### Test du contrôleur

```bash
python src/controller/test_invalidator.py
```

### Serveur MCP

```bash
python src/mcp_invalidator/server.py
```

---

## Travaux futurs

Les prochaines étapes du projet incluent :

* amélioration des heuristiques de recherche ;
* implémentation d'algorithmes de recherche locale avancés ;
* intégration complète avec MCP ;
* développement d'un agent capable d'appeler automatiquement les outils ;
* intégration d'un système de preuve formelle basé sur Lean ;
* génération automatique de conjectures.

---

## Auteurs

* NGUYEN Ngoc Tram Anh
* VU Thi Khanh Huyen

Encadrement :

* François Delbot
