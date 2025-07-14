# Android TV App - Sistema IPTV Completo

## 📺 Visão Geral

Este é um aplicativo completo para Android TV que permite gerenciar até 10 usuários com acesso a canais de TV ao vivo, filmes e séries organizados por categorias. O sistema processa listas M3U/M3U8/TS de forma transparente, oferecendo uma experiência de usuário simplificada e intuitiva.

## ✨ Características Principais

### 🔐 Sistema de Autenticação
- Suporte para até 10 usuários simultâneos
- Login seguro com hash de senhas
- Sessões persistentes
- Usuários padrão pré-configurados

### 📺 Gerenciamento de Conteúdo
- **Canais de TV**: Streaming ao vivo com categorização
- **Filmes**: Biblioteca organizada por gêneros
- **Séries**: Episódios organizados por temporadas
- **Categorias**: Sistema dinâmico de classificação

### 🎬 Interface do Usuário
- Design responsivo otimizado para Android TV
- Navegação intuitiva com controle remoto
- Player de vídeo integrado
- Filtros por categoria
- Interface moderna com gradientes e efeitos visuais

### 🔧 Painel Administrativo
- Upload de listas M3U/M3U8 via URL ou arquivo
- Gerenciamento de usuários
- Estatísticas do sistema
- Criação de conteúdo de exemplo
- Limpeza de dados

## 🏗️ Arquitetura do Sistema

### Backend (Flask)
- **Framework**: Flask com SQLAlchemy
- **Banco de Dados**: SQLite
- **Autenticação**: Sessões Flask com hash de senhas
- **API**: RESTful endpoints com CORS habilitado

### Frontend (Web)
- **Tecnologia**: HTML5, CSS3, JavaScript vanilla
- **Design**: Interface responsiva com foco em TV
- **Player**: HTML5 Video com suporte a M3U8/TS
- **Navegação**: Otimizada para controle remoto

### Processamento de Mídia
- **Parser M3U**: Análise automática de listas
- **Categorização**: Classificação inteligente de conteúdo
- **Streaming**: Suporte a múltiplos formatos (M3U8, TS, MP4)

## 📁 Estrutura do Projeto

```
android_tv_app/
├── src/
│   ├── models/          # Modelos de dados
│   │   ├── user.py      # Modelo de usuário
│   │   ├── category.py  # Modelo de categoria
│   │   ├── channel.py   # Modelo de canal
│   │   ├── movie.py     # Modelo de filme
│   │   ├── series.py    # Modelo de série
│   │   └── episode.py   # Modelo de episódio
│   ├── routes/          # Rotas da API
│   │   ├── auth.py      # Autenticação
│   │   ├── content.py   # Conteúdo
│   │   ├── admin.py     # Administração
│   │   ├── user_management.py  # Gerenciamento de usuários
│   │   └── m3u_parser.py       # Parser de listas M3U
│   ├── utils/           # Utilitários
│   │   ├── user_manager.py     # Gerenciador de usuários
│   │   └── content_manager.py  # Gerenciador de conteúdo
│   ├── static/          # Arquivos estáticos
│   │   ├── index.html   # Interface principal
│   │   ├── admin.html   # Painel administrativo
│   │   └── app.js       # JavaScript da aplicação
│   ├── database/        # Banco de dados
│   │   └── app.db       # SQLite database
│   └── main.py          # Ponto de entrada
├── venv/                # Ambiente virtual Python
├── requirements.txt     # Dependências Python
└── README.md           # Esta documentação
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou extraia o projeto**
```bash
cd android_tv_app
```

2. **Ative o ambiente virtual**
```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python src/main.py
```

5. **Acesse a aplicação**
- Interface principal: http://localhost:5000
- Painel administrativo: http://localhost:5000/admin.html

## 👥 Usuários Padrão

O sistema cria automaticamente os seguintes usuários:

| Usuário | Senha | Tipo |
|---------|-------|------|
| admin | admin123 | Administrador |
| user1 | user123 | Usuário padrão |
| user2 | user123 | Usuário padrão |
| ... | ... | ... |
| user10 | user123 | Usuário padrão |

## 📋 Funcionalidades Detalhadas

### Interface Principal
- **Login**: Autenticação segura com validação
- **Navegação**: Tabs para Canais, Filmes e Séries
- **Categorias**: Filtros dinâmicos por tipo de conteúdo
- **Player**: Reprodução de vídeo com controles completos
- **Responsividade**: Adaptação automática para diferentes tamanhos de tela

### Painel Administrativo
- **Estatísticas**: Contadores de conteúdo em tempo real
- **Upload M3U**: Processamento de listas via URL ou arquivo
- **Gerenciamento**: Criação e remoção de conteúdo
- **Usuários**: Administração de contas de usuário

### API Endpoints

#### Autenticação
- `POST /api/login` - Realizar login
- `POST /api/logout` - Realizar logout
- `GET /api/check` - Verificar autenticação

#### Conteúdo
- `GET /api/categories` - Listar categorias
- `GET /api/channels` - Listar canais
- `GET /api/movies` - Listar filmes
- `GET /api/series` - Listar séries
- `GET /api/series/{id}/episodes` - Listar episódios

#### Administração
- `POST /api/admin/upload-m3u` - Upload via URL
- `POST /api/admin/upload-m3u-file` - Upload via arquivo
- `POST /api/admin/create-sample-content` - Criar conteúdo de exemplo
- `POST /api/admin/clear-content` - Limpar todo conteúdo
- `GET /api/admin/content-stats` - Estatísticas do sistema

## 🔧 Configuração Avançada

### Personalização de Usuários
Para modificar os usuários padrão, edite o arquivo `src/utils/user_manager.py`:

```python
default_users = [
    {'username': 'seu_usuario', 'password': 'sua_senha'},
    # Adicione mais usuários conforme necessário
]
```

### Configuração de Banco de Dados
O sistema usa SQLite por padrão. Para usar outro banco, modifique a configuração em `src/main.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sua_string_de_conexao'
```

### Personalização da Interface
- **CSS**: Modifique os estilos em `src/static/index.html` e `src/static/admin.html`
- **JavaScript**: Customize a lógica em `src/static/app.js`
- **Cores**: Ajuste as variáveis CSS para alterar o tema

## 📱 Otimização para Android TV

### Navegação por Controle Remoto
- Foco automático em elementos interativos
- Navegação por teclas direcionais
- Suporte a tecla Enter/OK
- Feedback visual para seleção

### Performance
- Carregamento lazy de imagens
- Cache de dados da API
- Otimização de vídeo para streaming
- Compressão de assets

### Compatibilidade
- Suporte a WebView do Android
- Resolução otimizada para TV (1080p/4K)
- Controles de vídeo adaptados
- Interface simplificada

## 🔒 Segurança

### Autenticação
- Senhas com hash usando Werkzeug
- Sessões seguras com Flask
- Validação de entrada em todas as rotas
- Proteção contra CSRF

### Dados
- Sanitização de URLs M3U
- Validação de tipos de arquivo
- Limitação de tamanho de upload
- Logs de atividade administrativa

## 🐛 Solução de Problemas

### Problemas Comuns

**1. Erro de banco de dados**
```bash
# Remova o banco existente e reinicie
rm src/database/app.db
python src/main.py
```

**2. Problemas de dependências**
```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

**3. Erro de CORS**
- Verifique se o Flask-CORS está instalado
- Confirme que CORS está habilitado em `main.py`

**4. Vídeos não reproduzem**
- Verifique se as URLs M3U8/TS são válidas
- Teste as URLs diretamente no navegador
- Confirme que o servidor de mídia está acessível

### Logs e Debug
Para habilitar logs detalhados, modifique `src/main.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 🚀 Deploy em Produção

### Preparação
1. Desabilite o modo debug
2. Configure um servidor WSGI (Gunicorn, uWSGI)
3. Use um banco de dados robusto (PostgreSQL, MySQL)
4. Configure HTTPS
5. Implemente backup automático

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

## 📄 Licença

Este projeto é fornecido como está, para fins educacionais e de demonstração. Use por sua própria conta e risco.

## 🤝 Contribuição

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Teste thoroughly
5. Submeta um pull request

## 📞 Suporte

Para suporte técnico ou dúvidas:
- Verifique a documentação acima
- Consulte os logs de erro
- Teste em ambiente de desenvolvimento primeiro
- Documente problemas com detalhes específicos

---

**Desenvolvido com ❤️ para a comunidade Android TV**

