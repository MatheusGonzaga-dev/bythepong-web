# 🚀 Deploy do ByThePong na Vercel

## ✅ Status: PRONTO PARA DEPLOY

O projeto já está configurado para Vercel, mas com algumas limitações importantes.

---

## ⚠️ LIMITAÇÕES IMPORTANTES

### 🔴 **Banco de Dados SQLite não funciona na Vercel**
- **Problema**: Vercel usa funções serverless (stateless) - não há sistema de arquivos persistente
- **Solução atual**: SQLite em memória (`:memory:`)
- **Consequência**: **Rankings e partidas NÃO serão salvos permanentemente**

### 🎮 **O que FUNCIONA:**
✅ Jogo completo (física, colisões, IA)  
✅ Menu de configuração  
✅ Interface responsiva  
✅ Todos os temas visuais  
✅ Dificuldades (fácil, normal, difícil, expert)  

### ❌ **O que NÃO funciona:**
❌ Salvamento de ranking entre sessões  
❌ Histórico de partidas  
❌ Estatísticas persistentes  

---

## 🛠️ OPÇÕES DE DEPLOY

### **Opção 1: Deploy Simples (SEM banco persistente)** ⭐ Recomendado para teste

**Vantagens:**
- Deploy rápido e gratuito
- Perfeito para demonstrações
- Jogo funciona 100%

**Desvantagens:**
- Ranking não persiste

**Passos:** Ver seção "Deploy Rápido" abaixo

---

### **Opção 2: Deploy COMPLETO (COM banco persistente)** ⭐⭐ Ideal para produção

**Usar um dos seguintes bancos:**

#### A) **Vercel Postgres** (Recomendado)
- Gratuito até 60 horas/mês
- Integração nativa com Vercel
- Setup simples

#### B) **Neon PostgreSQL** (Gratuito)
- 100% gratuito
- 500MB de armazenamento
- Fácil integração

#### C) **PlanetScale MySQL** (Gratuito)
- 5GB gratuito
- Boa performance

**Passos:** Ver seção "Deploy com Banco" abaixo

---

## 🚀 DEPLOY RÁPIDO (Opção 1 - SEM persistência)

### **Passo 1: Instalar Vercel CLI**

```bash
npm install -g vercel
```

### **Passo 2: Login na Vercel**

```bash
vercel login
```

### **Passo 3: Deploy**

```bash
cd C:\Users\Matheus\Desktop\bythepong
vercel --prod
```

### **Passo 4: Responder perguntas**

```
? Set up and deploy "bythepong"? [Y/n] Y
? Which scope do you want to deploy to? (seu usuário)
? Link to existing project? [y/N] N
? What's your project's name? bythepong
? In which directory is your code located? ./
? Want to override the settings? [y/N] N
```

### **Passo 5: Acessar**

Após o deploy, você receberá uma URL:
```
https://bythepong.vercel.app
```

✅ **Pronto! Jogo funcionando online!**

---

## 🗄️ DEPLOY COM BANCO (Opção 2 - COM persistência)

### **Usando Vercel Postgres (Recomendado)**

#### **Passo 1: Criar banco no Vercel**

1. Acesse: https://vercel.com/dashboard
2. Selecione seu projeto `bythepong`
3. Vá em **Storage** → **Create Database**
4. Escolha **Postgres**
5. Nomeie: `bythepong-db`
6. Clique em **Create**

#### **Passo 2: Copiar credenciais**

A Vercel fornecerá automaticamente:
```
DATABASE_URL=postgres://user:pass@host:5432/dbname
```

#### **Passo 3: Atualizar dependências**

Adicionar ao `requirements_web.txt`:

```bash
psycopg2-binary==2.9.9
dj-database-url==2.1.0
```

#### **Passo 4: Criar settings para produção**

Vou criar o arquivo agora...

---

## 📝 CHECKLIST PRÉ-DEPLOY

Antes de fazer o deploy, verificar:

- [ ] `vercel.json` existe ✅
- [ ] `wsgi.py` configurado ✅
- [ ] `requirements_web.txt` atualizado ✅
- [ ] `settings_vercel.py` configurado ✅
- [ ] `.gitignore` configurado (não enviar .venv, db.sqlite3) ✅
- [ ] `DEBUG = False` em produção ✅

---

## 🔧 TROUBLESHOOTING

### **Erro: "Application failed to respond"**
- Aumentar timeout no `vercel.json` (já configurado)
- Verificar logs: `vercel logs`

### **Erro: "Static files not found"**
- Executar localmente: `python manage.py collectstatic`
- Verificar WhiteNoise instalado

### **Erro: "Database locked"**
- Normal com SQLite em Vercel
- Usar Postgres (Opção 2)

### **Ver logs em tempo real:**
```bash
vercel logs --follow
```

---

## 💡 DICAS EXTRAS

### **Domínio Customizado (Opcional)**
```bash
vercel domains add seujogo.com.br
```

### **Variáveis de Ambiente**
```bash
vercel env add SECRET_KEY
vercel env add DATABASE_URL
```

### **Múltiplos Ambientes**
```bash
vercel --prod    # Produção
vercel           # Preview
```

---

## 📊 COMPARAÇÃO DE OPÇÕES

| Recurso | Opção 1 (Simples) | Opção 2 (Completo) |
|---------|-------------------|---------------------|
| **Setup** | 5 minutos | 15 minutos |
| **Custo** | Gratuito | Gratuito* |
| **Ranking** | ❌ Não persiste | ✅ Persiste |
| **Performance** | ⚡ Rápido | ⚡ Rápido |
| **Ideal para** | Demo/Teste | Produção |

*Até os limites gratuitos

---

## 🎯 RECOMENDAÇÃO

### **Para Apresentação/Demo:**
➡️ Use **Opção 1** (Deploy Simples)
- Rápido (5 min)
- Mostra toda funcionalidade do jogo
- Não precisa de banco

### **Para Projeto Real:**
➡️ Use **Opção 2** (Deploy com Postgres)
- Ranking funcional
- Estatísticas reais
- Escalável

---

## 🚀 QUER AJUDA?

Se quiser que eu configure o deploy completo com Postgres, me avise!

Posso:
1. ✅ Criar `settings_production.py` otimizado
2. ✅ Configurar migrations para Postgres
3. ✅ Atualizar `requirements_web.txt`
4. ✅ Testar localmente antes do deploy
5. ✅ Fazer o deploy passo a passo com você

---

## 📚 RECURSOS

- [Vercel Django Docs](https://vercel.com/guides/deploying-django-with-vercel)
- [Vercel Postgres](https://vercel.com/docs/storage/vercel-postgres)
- [WhiteNoise Docs](http://whitenoise.evans.io/)

---

**Criado por:** ByThePong Team 🏓  
**Última atualização:** 2024

