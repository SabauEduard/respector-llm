# Quick Start Guide

## 1️⃣ Instalare Dependențe

```bash
# Creează virtual environment (recomandat)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalează pachete
pip install -r requirements.txt
```

## 2️⃣ Configurare Azure OpenAI

```bash
# Copiază fișierul de configurare
cp config.example.env .env

# Editează .env cu credențialele tale:
# - AZURE_OPENAI_API_KEY
# - AZURE_OPENAI_ENDPOINT
# - AZURE_OPENAI_DEPLOYMENT_NAME
```

## 3️⃣ Rulare Enhancer

```bash
# Procesează un spec Respector
python enhancer.py respector-generated/order-api.json -v

# Output va fi în: respector-enhanced-generated/order-api.json
```

Progresul va arăta astfel:
```
📂 Loading spec from: respector-generated/order-api.json
🔌 Connecting to Azure OpenAI...
✓ Using deployment: gpt-4o
📋 Found 6 endpoints to enhance

🚀 Enhancing endpoints: |████████████████████| 6/6 [00:12<00:00]

💾 Writing enhanced spec to: respector-enhanced-generated/order-api.json

==================================================
✅ Enhancement complete!
==================================================
   Total endpoints:  6
   Successful:       6
   Output file:      respector-enhanced-generated/order-api.json
==================================================
```

## 4️⃣ Vizualizare Rezultate

### Pornire Swagger UI

```bash
# Start Docker containers
./view-docs.sh

# Sau manual:
docker-compose up -d
```

### Accesare în Browser

- **BEFORE** (Raw Respector): http://localhost:9081
- **AFTER** (Enhanced): http://localhost:9082

### Comparare Side-by-Side

1. Deschide ambele URL-uri
2. Arrange ferestrele unul lângă altul
3. Navigate la același endpoint în ambele
4. Observă diferențele:
   - Stânga: doar structură tehnică
   - Dreapta: documentație completă

### Oprire

```bash
# Stop și șterge containerele
docker-compose down
```

## 5️⃣ Workflow Complet

```bash
# 1. Obține spec de la Respector
# (presupunem că ai deja respector-generated/my-api.json)

# 2. Îmbunătățește documentația
python enhancer.py respector-generated/my-api.json -v

# 3. Vizualizează rezultatele
./view-docs.sh

# 4. Deschide browser la:
# - http://localhost:9081 (before)
# - http://localhost:9082 (after)

# 5. Când termini, oprește serverele
docker-compose down
```

## 🆘 Troubleshooting

### "Port already in use"
```bash
# Verifică ce folosește portul
lsof -ti:9081

# Sau schimbă porturile în docker-compose.yml
```

### "Azure OpenAI authentication error"
- Verifică că `.env` conține credențialele corecte
- Asigură-te că endpoint-ul este complet (cu `https://`)
- Verifică că deployment name-ul există în Azure

### "Docker not found"
```bash
# Instalează Docker Desktop:
# https://www.docker.com/products/docker-desktop/

# Sau folosește metoda online:
# https://editor.swagger.io
```

### "JSON parse error"
```bash
# Validează JSON-ul
python -m json.tool respector-generated/my-api.json

# Asigură-te că fișierul este valid OpenAPI 3.0
```

## 📚 Documentație Suplimentară

- [README.md](README.md) - Documentație completă
- [PRESENTATION-CHEATSHEET.md](PRESENTATION-CHEATSHEET.md) - Pentru prezentări
- [spec.md](spec.md) - Specificație tehnică detaliată

## 🚀 Next Steps

După ce ai testat basic workflow-ul:

1. **Încearcă pe propriul tău API**
   ```bash
   python enhancer.py path/to/your/respector-output.json -v
   ```

2. **Customizează prompt-urile** în `enhancer.py`
   - Modifică `SYSTEM_PROMPT` pentru ton diferit
   - Ajustează `USER_PROMPT_TEMPLATE` pentru alte detalii

3. **Integrează în CI/CD**
   - Rulează automat la fiecare build
   - Generează documentație actualizată

4. **Contribuie la proiect**
   - Raportează bug-uri
   - Sugerează îmbunătățiri
   - Trimite pull requests

