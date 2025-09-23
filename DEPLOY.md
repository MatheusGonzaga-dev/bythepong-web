# Deploy na Vercel - ByThePong

## Arquivos Essenciais para Deploy:

### 1. Configuração Principal
- `wsgi.py` - Entrada da aplicação
- `bythepong_web/settings_minimal.py` - Configurações mínimas
- `bythepong_web/urls_minimal.py` - URLs e views inline
- `vercel.json` - Configuração da Vercel
- `requirements_web.txt` - Dependências mínimas

### 2. Templates
- `templates/game/home.html`
- `templates/game/index.html` 
- `templates/game/game.html`
- `templates/game/ranking.html`

### 3. Pasta Static (vazia mas necessária)
- `static/` - Para arquivos estáticos

## Comandos para Deploy:

```bash
# 1. Fazer commit
git add .
git commit -m "Deploy: Versão minimal para Vercel"
git push

# 2. Deploy na Vercel
vercel --prod
```

## Características da Versão Minimal:

- ✅ Django mínimo (só staticfiles)
- ✅ Sem banco de dados
- ✅ Sem models/migrations
- ✅ Views inline nas URLs
- ✅ Jogo funcional em memória
- ✅ Todas as páginas funcionando
- ✅ API do jogo funcionando
- ✅ Estilização completa mantida

## Testado e Funcionando:

- ✅ Django setup sem erros
- ✅ URLs carregando
- ✅ Templates renderizando
- ✅ Static files configurados
- ✅ Jogo completamente funcional
