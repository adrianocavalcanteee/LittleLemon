# 🍋 LittleLemon API

Este projeto é uma **API RESTful** desenvolvida como parte do **Curso de APIs do Meta**.  
A aplicação simula o backend do restaurante **Little Lemon**, fornecendo endpoints para gerenciamento de dados e integração com aplicações front-end.

O objetivo do projeto é aplicar conceitos fundamentais de desenvolvimento de APIs, como rotas, requisições HTTP, estruturação de backend e boas práticas.

---

## 🚀 Funcionalidades

- Criação de endpoints REST
- Operações CRUD (Create, Read, Update, Delete)
- Estrutura organizada para APIs
- Preparado para integração com aplicações web ou mobile
- Projeto educacional seguindo padrões do Meta

---

## 🛠 Tecnologias Utilizadas

- **Python**
- **Django**
- **Django REST Framework**
- **SQLite** (ambiente de desenvolvimento)
- **Postman / Insomnia** para testes de API

---

## Como rodar o projeto

### Clonar o repositório
git clone https://github.com/adrianocavalcanteee/LittleLemon.git  
cd LittleLemon

### Criar ambiente virtual
python -m venv venv

### Ativar o ambiente virtual

Windows:
venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

### Instalar dependências
pip install -r requirements.txt

### Executar migrações
python manage.py migrate

### Rodar o servidor
python manage.py runserver

A aplicação estará disponível em:
http://127.0.0.1:8000/


**Nota:** O projeto contém um arquivo `.txt` com instruções detalhadas sobre como realizar os testes da API.
