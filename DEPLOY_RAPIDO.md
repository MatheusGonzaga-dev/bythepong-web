# 🚀 DEPLOY RÁPIDO NA VERCEL - 5 MINUTOS

## ⚡ Comandos para executar

### 1️⃣ Instalar Vercel CLI (se não tiver)
```bash
npm install -g vercel
```

### 2️⃣ Fazer login
```bash
vercel login
```

### 3️⃣ Deploy (executar na pasta do projeto)
```bash
cd C:\Users\Matheus\Desktop\bythepong
vercel --prod
```

---

## 💬 Respostas para as perguntas

Quando perguntar, responder:

```
? Set up and deploy "bythepong"? 
  → Y

? Which scope do you want to deploy to? 
  → (selecione seu usuário)

? Link to existing project? 
  → N

? What's your project's name? 
  → bythepong

? In which directory is your code located? 
  → ./

? Want to override the settings? 
  → N
```

---

## ✅ PRONTO!

Após alguns minutos você receberá:

```
✅ Production: https://bythepong-xxxxx.vercel.app [ready]
```

Acesse essa URL e o jogo estará funcionando! 🎮

---

## ⚠️ IMPORTANTE

**O que funciona:**
- ✅ Jogo completo
- ✅ Todos os temas
- ✅ Todas as dificuldades
- ✅ Interface responsiva

**O que NÃO persiste:**
- ❌ Ranking (reseta a cada deploy)
- ❌ Histórico de partidas

Para ter ranking persistente, veja o arquivo `DEPLOY_VERCEL.md` completo.

---

## 🔄 Para atualizar depois

```bash
cd C:\Users\Matheus\Desktop\bythepong
vercel --prod
```

Simples assim! 🚀

