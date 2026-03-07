# Ejercicio 1: Laberinto - Inteligencia Artificial

Este proyecto es una aplicación web desarrollada en React y Vite que forma parte de la Práctica 1 para la materia de Inteligencia Artificial. El objetivo principal es la visualización y resolución de laberintos mediante los algoritmos de IA DFS y BFS.

## 🛠️ Tecnologías Utilizadas

* **Frontend:** React + TypeScript (Vite)
* **Entorno:** Node.js (v22.22.0)
* **Contenedores:** Docker & Docker Compose

## 📋 Requisitos Previos

Para ejecutar este proyecto en tu máquina local sin preocuparte por instalar dependencias de Node, necesitas tener instalados los siguientes programas:

1. [Git](https://git-scm.com/) (Para clonar el repositorio)
2. [Docker Desktop](https://www.docker.com/products/docker-desktop) (Debe estar abierto y ejecutándose en segundo plano)

---

## 🚀 Guía de Instalación y Uso Rápido

Sigue estos 3 sencillos pasos para levantar el proyecto en tu computadora:

**1. Clonar el repositorio**
Abre tu terminal y descarga el código:
`
git clone git@github.com:MXYSL/Inteligencia-Artificial.git
`

**2. Navegar al directorio del proyecto**
Asegúrate de entrar a la carpeta específica donde se encuentra la configuración de Docker:
`
cd "Ejercicio 1_Laberinto/"
`

**3. Construir y levantar el contenedor**
Ejecuta el siguiente comando. Docker se encargará de descargar la imagen correcta de Node, instalar todas las dependencias (`npm install`) y levantar el servidor de desarrollo:
`
docker compose up -d --build
`
*(Nota: La bandera `-d` ejecuta el contenedor en segundo plano para que puedas seguir usando tu terminal).*

---

## 🌐 Acceder a la Aplicación

Una vez que el comando anterior termine de ejecutarse, abre tu navegador web favorito y dirígete a:

👉 **[http://localhost:5173](http://localhost:5173)**

Cualquier cambio que realices en el código fuente (dentro de la carpeta `src/`) se reflejará automáticamente en el navegador gracias al *Hot Module Replacement* (HMR) configurado en Docker.

## 🛑 Detener el Proyecto

Cuando termines de trabajar, puedes apagar el contenedor ejecutando el siguiente comando dentro de la misma carpeta `Ejercicio 1_Laberinto`:
`
docker compose down
`

---
**Autor:** Alan Ivan Sanchez Gomez  
**Institución:** Escuela Superior de Cómputo (ESCOM) - Ingeniería en Sistemas Computacionales