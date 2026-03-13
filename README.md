# Real-Time Relief Mapping on Arbitrary Polygonal Surfaces

Ce dépôt contient l'implémentation en Python et OpenGL de la technique de **Relief Mapping**, basée sur l'article de recherche de Fábio Policarpo, Manuel M. Oliveira et João L. D. Comba (2005). Ce projet a été réalisé dans le cadre du cours IG3D (Master Image) du Département d'Informatique de Sorbonne Université.

## 🌍 Contexte et Motivation

Les techniques traditionnelles comme le *bump mapping* ou le *parallax mapping* permettent de simuler des détails de surface, mais souffrent souvent d'artefacts visuels : absence d'auto-occultation (self-occlusion), distorsion des textures selon l'angle de vue, ou encore des ombres imprécises. 

Ce projet implémente le **Relief Mapping**, une technique avancée qui permet de rendre des textures très détaillées avec une véritable sensation de profondeur géométrique sur des surfaces polygonales arbitraires. Elle offre un éclairage par pixel (per-pixel lighting) réaliste, gère les auto-occultations et assure un ombrage correct en perspective, tout en fonctionnant de manière optimale dans l'espace tangent (tangent space).

## 🧠 Méthodologie

Le cœur de l'algorithme est implémenté via des *shaders* (notamment le Fragment Shader). La méthode repose sur le lancer de rayons (ray-marching) dans l'espace tangent de la surface :
1. **Recherche linéaire (Linear Search)** : Avancée pas à pas le long du rayon de vue pour trouver la première intersection approximative à l'intérieur de la carte de hauteur (height map).
2. **Recherche dichotomique (Binary Search)** : Affinement précis de la position de l'intersection pour éviter les artefacts visuels et garantir une haute précision de rendu.

## 📂 Structure du Dépôt

Le dépôt contient les fichiers de code source ainsi que la documentation du projet :

* **`1053427.1053453.pdf`** : L'article de recherche original de 2005 définissant la méthode de Relief Mapping.
* **`Report_IG3D_Project.pdf`** : Le rapport technique de ce projet. Il détaille la théorie, les choix d'implémentation, les résultats obtenus ainsi que les limites (performances, ombres portées) et pistes d'amélioration.
* **`main.py`** : Le point d'entrée du programme. Il gère la boucle principale, l'initialisation de la fenêtre graphique avec GLFW et les interactions de la caméra (souris/clavier).
* **`config.py`** : Fichier de configuration gérant la compilation des shaders (Vertex et Fragment shaders) et les paramètres globaux d'OpenGL.
* **`mesh_factory.py`** : Gère la création des objets OpenGL (VBO, VAO) et l'envoi des données (sommets, normales, espace tangent) au GPU.
* **`obj_loader.py`** : Un parseur personnalisé pour charger les modèles 3D au format `.obj` avec leurs coordonnées de texture (UVs) et calculer les vecteurs tangents et bitangents nécessaires au Relief Mapping.

## ⚙️ Installation et Prérequis

Ce projet est développé en Python et utilise **PyOpenGL**. Pour exécuter le code, assurez-vous d'avoir installé les dépendances suivantes :

```bash
pip install PyOpenGL glfw numpy Pillow
```
