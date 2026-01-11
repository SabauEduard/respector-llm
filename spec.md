Specification: Respector-LLM Enhancer
Attribute	Details
Title	Respector-LLM Enhancer: Hybrid Documentation Generation
Author	[Numele Tău]
Based on	

"Generating REST API Specifications through Static Analysis" (ICSE '24)

Status	Proposed / In Development
Version	1.0.0
1. Overview

Această propunere descrie o extensie a uneltei Respector. În timp ce Respector excelează la extragerea structurii tehnice exacte (rute, parametri, constrângeri) prin analiză statică și simbolică, specificațiile generate (OpenAPI 3.0) duc lipsă de informații semantice necesare dezvoltatorilor (câmpurile summary și description).

Respector-LLM Enhancer este un modul de post-procesare care utilizează un Large Language Model (Azure OpenAI GPT-4o) pentru a interpreta metadatele tehnice extrase de Respector și a genera documentație în limbaj natural.
2. Problem Statement

    Documentation Drift: Specificațiile scrise manual devin desincronizate față de implementare.

Limitarea Respector: Deși Respector identifică constrângeri logice complexe (ex: min: 0, required: true), output-ul său JSON este "sec". Nu oferă context de business, ceea ce face dificilă utilizarea API-ului de către terți fără acces la codul sursă.

3. Proposed Solution

Un pipeline automatizat scris în Python care:

    Ingerează fișierul JSON brut generat de Respector.

    Folosește Context Injection: extrage numele metodelor (operationId), parametrii și constrângerile matematice.

    Interoghează Azure OpenAI (GPT-4o) pentru a deduce logica de business.

    Injectează descrierile generate înapoi în specificație pentru a produce un artefact final complet documentat.

4. System Architecture
4.1 Data Flow
Code snippet

graph LR
    Input[("Respector Output
    (raw_spec.json)")] --> Parser(JSON Parser)
    Parser --> Context{Context Extractor}
    
    Context -- "OperationId +
    Constraints" --> PromptEngine(Prompt Builder)
    
    PromptEngine --> LLM(("Azure OpenAI
    GPT-4o"))
    
    LLM -- "Summary &
    Description" --> Injector(Semantic Injector)
    
    Injector --> FinalOutput[("Enhanced Spec
    (enhanced_spec.json)")]

4.2 Technology Stack

    Core Logic: Python 3.9+

    LLM Provider: Azure OpenAI Service (Model: gpt-4o sau gpt-35-turbo)

    Data Format: OpenAPI Specification (OAS) 3.0

    Dependencies: openai, json, os

5. Technical Implementation
5.1 Input Data (Raw Spec)

Un exemplu de input generat de Respector, corect tehnic dar lipsit de descrieri:
JSON

"/students": {
  "post": {
    "operationId": "registerNewStudent",
    "parameters": [],
    "requestBody": { ... },
    "responses": { "201": { "description": "Created" } }
    // Lipsesc summary și description detaliat
  }
}

5.2 Prompt Engineering Strategy

Calitatea documentației depinde de prompt. Vom folosi următorul template pentru a maximiza acuratețea:

System Prompt:

    "You are an expert Technical Writer for REST APIs. Your goal is to generate professional, concise documentation based on technical constraints extracted from static code analysis."

User Prompt Template:
Plaintext

Analyze the following API Endpoint metadata:
1. Operation Name (Java Method): {operation_id}
2. HTTP Method: {method}
3. URL Path: {path}
4. Identified Constraints: {constraints_json}

Task:
- Generate a 'summary' (max 50 chars).
- Generate a 'description' that explains the endpoint's purpose and mentions valid input ranges based on the constraints provided.
- Return strict JSON format.

5.3 Output Data (Enhanced Spec)

Rezultatul așteptat după procesare:
JSON

"/students": {
  "post": {
    "operationId": "registerNewStudent",
    "summary": "Register New Student",
    "description": "Creates a new student record in the system. Requires a JSON body with a valid 'age' (minimum 18) and a non-empty 'name'.",
    "x-enhanced-by": "Respector-LLM"
    ...
  }
}

6. Constraints & Risks

    Cost: Procesarea unui API foarte mare (sute de endpoint-uri) implică costuri de tokeni către Azure.

    Latency: Generarea textului adaugă timp la pipeline-ul de build (aprox. 1-2 secunde per endpoint).

    AI Hallucinations: Dacă numele metodei din cod este ambiguu (ex: doProcess()), AI-ul poate genera o descriere generică sau incorectă.

7. Future Improvements

    Local Inference: Suport pentru modele locale (Llama 3 via Ollama) pentru a elimina costurile și a crește confidențialitatea datelor.

    Diff Checker: Un modul UI care să evidențieze diferențele dintre documentația veche și cea nouă.

    CI/CD Integration: Transformarea scriptului într-un GitHub Action care rulează automat la fiecare Pull Request.