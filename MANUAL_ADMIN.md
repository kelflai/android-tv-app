# 🔧 Manual do Administrador - Android TV App

## 🎯 Visão Geral

Este manual é destinado aos administradores do sistema Android TV App. Aqui você encontrará todas as informações necessárias para gerenciar usuários, conteúdo, e manter o sistema funcionando adequadamente.

## 🔐 Acesso Administrativo

### Login como Administrador

1. **Acesse a aplicação**: `http://[IP_DO_SERVIDOR]:5000`
2. **Use as credenciais administrativas**:
   - **Usuário**: `admin`
   - **Senha**: `admin123`
3. **Faça login** normalmente

### Acessando o Painel Administrativo

1. **Após fazer login**, navegue para: `http://[IP_DO_SERVIDOR]:5000/admin.html`
2. **Ou clique** no link "Painel Admin" se disponível
3. **Você verá** a interface administrativa completa

## 📊 Dashboard Administrativo

### Estatísticas do Sistema

O painel exibe em tempo real:

- **Categorias**: Número total de categorias criadas
- **Canais**: Quantidade de canais disponíveis
- **Filmes**: Total de filmes no sistema
- **Séries**: Número de séries cadastradas
- **Episódios**: Total de episódios disponíveis

### Atualizando Estatísticas

- **Clique em "🔄 Atualizar Estatísticas"** para refresh manual
- **As estatísticas são atualizadas** automaticamente após operações
- **Use para verificar** o impacto de mudanças no sistema

## 📺 Gerenciamento de Conteúdo M3U

### Upload via URL

1. **Seção "Upload de Lista M3U/M3U8"**
2. **Cole a URL** da lista M3U no campo apropriado
3. **Clique em "📥 Carregar da URL"**
4. **Aguarde o processamento** (pode levar alguns minutos)
5. **Verifique as estatísticas** para confirmar a importação

#### Exemplo de URLs Suportadas
```
http://exemplo.com/lista.m3u
https://servidor.tv/canais.m3u8
ftp://servidor.com/playlist.m3u
```

### Upload via Arquivo

1. **Seção de upload de arquivo**
2. **Arraste um arquivo M3U** para a área designada
3. **Ou clique para selecionar** um arquivo do dispositivo
4. **O upload iniciará** automaticamente
5. **Acompanhe o progresso** na interface

#### Formatos Aceitos
- `.m3u` - Lista M3U padrão
- `.m3u8` - Lista M3U UTF-8
- Tamanho máximo recomendado: 50MB

### Processamento Automático

O sistema automaticamente:
- **Analisa o conteúdo** da lista M3U
- **Extrai informações** como nome, logo, categoria
- **Classifica automaticamente** em canais, filmes ou séries
- **Cria categorias** conforme necessário
- **Atualiza o banco de dados** com novo conteúdo

## 🎬 Gerenciamento de Conteúdo

### Criando Conteúdo de Exemplo

1. **Clique em "✨ Criar Conteúdo de Exemplo"**
2. **O sistema criará**:
   - Categorias padrão para cada tipo
   - Canais de exemplo (Globo News, SporTV, Multishow)
   - Filmes de exemplo (Vingadores, Se Beber Não Case, Cidade de Deus)
   - Séries de exemplo (Breaking Bad, The Office, Stranger Things)
   - Episódios para cada série

### Limpando Todo Conteúdo

⚠️ **ATENÇÃO**: Esta ação é irreversível!

1. **Clique em "🗑️ Limpar Todo Conteúdo"**
2. **Confirme a ação** no popup
3. **Todo o conteúdo será removido**:
   - Todas as categorias
   - Todos os canais
   - Todos os filmes
   - Todas as séries
   - Todos os episódios

### Verificando Resultados

Após qualquer operação:
- **Verifique as estatísticas** atualizadas
- **Teste a interface principal** para confirmar mudanças
- **Faça logout e login** se necessário para refresh

## 👥 Gerenciamento de Usuários

### Criando Usuários Padrão

1. **Clique em "👤 Criar Usuários Padrão"**
2. **O sistema criará** (se não existirem):
   - 1 usuário admin (admin/admin123)
   - 10 usuários padrão (user1-user10/user123)

### Usuários Existentes

O sistema suporta:
- **Máximo de 10 usuários** simultâneos
- **1 administrador** com acesso total
- **9 usuários padrão** com acesso limitado

### Modificando Usuários

Para alterações avançadas, edite diretamente:
```python
# Arquivo: src/utils/user_manager.py
default_users = [
    {'username': 'novo_admin', 'password': 'nova_senha'},
    {'username': 'usuario1', 'password': 'senha123'},
    # Adicione mais usuários conforme necessário
]
```

## 🔧 Configurações Avançadas

### Configuração do Servidor

#### Porta e Host
```python
# Arquivo: src/main.py
app.run(host='0.0.0.0', port=5000, debug=True)
```

#### Banco de Dados
```python
# Arquivo: src/main.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///caminho/para/banco.db'
```

### Configuração de Segurança

#### Chave Secreta
```python
# Arquivo: src/main.py
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
```

#### CORS (Cross-Origin Resource Sharing)
```python
# Arquivo: src/main.py
CORS(app)  # Permite acesso de qualquer origem
```

### Logs e Monitoramento

#### Habilitando Logs Detalhados
```python
# Arquivo: src/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Monitorando Atividade
- **Verifique logs** do servidor regularmente
- **Monitore uso de recursos** (CPU, memória)
- **Acompanhe estatísticas** de conteúdo

## 🚨 Solução de Problemas

### Problemas Comuns

#### 1. Lista M3U Não Processa
**Sintomas**: Upload falha ou não adiciona conteúdo
**Soluções**:
- Verifique se a URL está acessível
- Confirme o formato do arquivo M3U
- Teste com uma lista menor primeiro
- Verifique logs do servidor para erros

#### 2. Usuários Não Conseguem Logar
**Sintomas**: Erro de autenticação
**Soluções**:
- Recrie usuários padrão
- Verifique se o banco de dados está funcionando
- Confirme se as senhas estão corretas
- Reinicie o servidor se necessário

#### 3. Conteúdo Não Aparece
**Sintomas**: Interface vazia após upload
**Soluções**:
- Verifique as estatísticas no painel admin
- Confirme se o processamento foi concluído
- Teste fazer logout e login novamente
- Verifique se há erros no console do navegador

#### 4. Performance Lenta
**Sintomas**: Sistema lento ou travando
**Soluções**:
- Limite o tamanho das listas M3U
- Limpe conteúdo desnecessário
- Reinicie o servidor
- Verifique recursos do sistema

### Comandos de Emergência

#### Resetar Banco de Dados
```bash
# Pare o servidor
# Remova o banco existente
rm src/database/app.db
# Reinicie o servidor
python src/main.py
```

#### Backup do Banco
```bash
# Copie o arquivo do banco
cp src/database/app.db backup_$(date +%Y%m%d).db
```

#### Restaurar Backup
```bash
# Pare o servidor
# Restaure o backup
cp backup_YYYYMMDD.db src/database/app.db
# Reinicie o servidor
```

## 📈 Melhores Práticas

### Gerenciamento de Conteúdo

1. **Teste listas M3U** em pequenos lotes primeiro
2. **Faça backup** antes de grandes mudanças
3. **Monitore estatísticas** regularmente
4. **Limpe conteúdo obsoleto** periodicamente
5. **Organize por categorias** para melhor experiência

### Segurança

1. **Altere senhas padrão** em produção
2. **Use HTTPS** em ambiente público
3. **Monitore logs** para atividades suspeitas
4. **Limite acesso** ao painel administrativo
5. **Faça backups** regulares

### Performance

1. **Monitore recursos** do servidor
2. **Limite tamanho** das listas M3U
3. **Use CDN** para conteúdo de mídia se possível
4. **Otimize banco de dados** periodicamente
5. **Configure cache** adequadamente

### Manutenção

1. **Atualize dependências** regularmente
2. **Monitore logs** de erro
3. **Teste funcionalidades** após mudanças
4. **Documente alterações** feitas
5. **Mantenha backups** atualizados

## 🔄 Rotinas de Manutenção

### Diária
- [ ] Verificar logs de erro
- [ ] Monitorar estatísticas de uso
- [ ] Confirmar funcionamento básico

### Semanal
- [ ] Fazer backup do banco de dados
- [ ] Verificar espaço em disco
- [ ] Testar upload de conteúdo
- [ ] Revisar performance do sistema

### Mensal
- [ ] Atualizar dependências
- [ ] Limpar logs antigos
- [ ] Revisar configurações de segurança
- [ ] Testar procedimentos de backup/restore

### Conforme Necessário
- [ ] Adicionar novo conteúdo via M3U
- [ ] Criar/remover usuários
- [ ] Ajustar configurações
- [ ] Resolver problemas reportados

## 📞 Suporte Técnico

### Informações para Coleta

Ao reportar problemas, colete:
- **Versão do sistema** operacional
- **Versão do Python** e dependências
- **Logs de erro** completos
- **Passos para reproduzir** o problema
- **Configurações** relevantes

### Logs Importantes

Localizações dos logs:
- **Logs do Flask**: Console onde o servidor roda
- **Logs do navegador**: Console do desenvolvedor (F12)
- **Logs do sistema**: `/var/log/` (Linux) ou Event Viewer (Windows)

### Contatos de Emergência

Para problemas críticos:
1. **Documente o problema** detalhadamente
2. **Colete logs** e informações do sistema
3. **Tente soluções** deste manual primeiro
4. **Prepare ambiente** de teste se possível

---

**Este manual cobre todas as operações administrativas essenciais. Mantenha-o atualizado conforme o sistema evolui! 🚀**

