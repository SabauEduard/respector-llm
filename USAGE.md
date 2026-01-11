# Ghid de Utilizare Respector-LLM Enhancer

## Comenzi Esențiale

### 🚀 Generare Documentație

```bash
# Procesează un spec Respector
python enhancer.py respector-generated/order-api.json

# Cu progress verbose
python enhancer.py respector-generated/order-api.json -v

# Output custom
python enhancer.py respector-generated/order-api.json -o custom/path/output.json
```

### 👀 Vizualizare în Swagger UI

#### Pornire Servere

```bash
# Metoda 1: Script automat
./view-docs.sh

# Metoda 2: Docker Compose manual
docker-compose up -d
```

**URL-uri disponibile:**
- 📄 **BEFORE** (Raw Respector): http://localhost:9081
- ✨ **AFTER** (Enhanced): http://localhost:9082

#### Oprire Servere

```bash
# Oprire completă
docker-compose down

# Oprire și ștergere volume-uri
docker-compose down -v

# Verificare status
docker-compose ps
```

### 🔍 Verificare Rezultate

```bash
# Verifică că JSON-ul este valid
python -m json.tool respector-enhanced-generated/order-api.json > /dev/null && echo "✓ Valid JSON"

# Caută câmpurile generate
grep -A 2 '"summary"' respector-enhanced-generated/order-api.json

# Compară before/after
diff respector-generated/order-api.json respector-enhanced-generated/order-api.json
```

## Workflow Tipic

```bash
# 1. SETUP INIȚIAL (doar prima dată)
cp config.example.env .env
# Editează .env cu credențiale Azure OpenAI

# 2. PROCESARE SPEC
python enhancer.py respector-generated/my-api.json -v

# 3. VIZUALIZARE
docker-compose up -d
# Deschide http://localhost:9081 și http://localhost:9082

# 4. CLEANUP
docker-compose down
```

## Parametri CLI

```bash
python enhancer.py --help
```

**Argumente disponibile:**
- `input` - Calea către spec-ul Respector (obligatoriu)
- `-o, --output` - Calea pentru output (opțional)
- `-v, --verbose` - Afișează progress detaliat (opțional)

**Exemple:**
```bash
# Minimal
python enhancer.py input.json

# Cu toate opțiunile
python enhancer.py input.json -o output.json -v
```

## Gestionare Erori

### Eroare: "Port already in use"

```bash
# Găsește procesul care folosește portul
lsof -ti:9081

# Oprește containerele existente
docker-compose down

# Sau schimbă porturile în docker-compose.yml
```

### Eroare: "Azure OpenAI authentication failed"

```bash
# Verifică fișierul .env
cat .env

# Asigură-te că conține:
# AZURE_OPENAI_API_KEY=your-key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

### Eroare: "Docker daemon not running"

```bash
# Start Docker Desktop
open -a Docker

# Verifică status
docker info
```

### Eroare: "JSON parsing error"

```bash
# Validează input-ul
python -m json.tool respector-generated/my-api.json

# Verifică encoding
file respector-generated/my-api.json
```

## Tips & Tricks

### Procesare Batch

```bash
# Procesează toate spec-urile dintr-un folder
for file in respector-generated/*.json; do
    python enhancer.py "$file" -v
done
```

### Comparare Rapidă

```bash
# Deschide ambele spec-uri în editor
code -d respector-generated/order-api.json \
        respector-enhanced-generated/order-api.json
```

### Export pentru Prezentare

```bash
# Salvează screenshot-uri
# 1. Deschide http://localhost:9081
# 2. Cmd+Shift+4 (macOS) sau Print Screen (Windows)
# 3. Repeat pentru http://localhost:9082
```

### Verificare Rapidă

```bash
# Contorizează endpoint-urile procesate
grep -c '"x-enhanced-by"' respector-enhanced-generated/order-api.json

# Extrage toate summary-urile
jq -r '.paths[][] | select(.summary) | .summary' respector-enhanced-generated/order-api.json
```

## Integrare în Workflow

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
if [ -f respector-generated/api.json ]; then
    python enhancer.py respector-generated/api.json
    git add respector-enhanced-generated/api.json
fi
```

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/docs.yml
name: Generate API Docs
on: [push]
jobs:
  enhance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Enhance docs
        env:
          AZURE_OPENAI_API_KEY: ${{ secrets.AZURE_OPENAI_KEY }}
        run: python enhancer.py respector-generated/*.json
```

## Resurse Suplimentare

- 📖 [README.md](README.md) - Documentație completă
- 🚀 [QUICK-START.md](QUICK-START.md) - Ghid rapid de început
- 📋 [spec.md](spec.md) - Specificație tehnică detaliată
- 🔗 [editor.swagger.io](https://editor.swagger.io) - Vizualizare online

