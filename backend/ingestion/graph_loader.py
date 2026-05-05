from db.neo4j_client import run_query

# ---------------------------------------------------------------------------
# Seed data: 50 conditions, each with symptoms and treatments
# ---------------------------------------------------------------------------
MEDICAL_GRAPH_DATA = [
    # ── Endocrine ────────────────────────────────────────────────────────────
    {
        "condition": "Type 1 Diabetes",
        "description": "Autoimmune destruction of pancreatic beta cells causing insulin deficiency",
        "symptoms": ["excessive thirst", "frequent urination", "unintended weight loss", "fatigue", "blurred vision", "fruity-smelling breath"],
        "treatments": [
            {"name": "Insulin therapy", "type": "medication"},
            {"name": "Blood glucose monitoring", "type": "procedure"},
            {"name": "Carbohydrate counting diet", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Type 2 Diabetes",
        "description": "Metabolic disorder with insulin resistance and relative insulin deficiency",
        "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow-healing wounds", "frequent infections"],
        "treatments": [
            {"name": "Metformin", "type": "medication"},
            {"name": "GLP-1 receptor agonists", "type": "medication"},
            {"name": "Low-carbohydrate diet", "type": "lifestyle"},
            {"name": "Regular physical activity", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Hypothyroidism",
        "description": "Underactive thyroid gland producing insufficient thyroid hormone",
        "symptoms": ["fatigue", "weight gain", "cold intolerance", "constipation", "dry skin", "hair loss", "depression", "slow heart rate"],
        "treatments": [
            {"name": "Levothyroxine", "type": "medication"},
            {"name": "Regular TSH monitoring", "type": "procedure"},
        ],
    },
    {
        "condition": "Hyperthyroidism",
        "description": "Overactive thyroid gland producing excess thyroid hormone",
        "symptoms": ["unintended weight loss", "rapid heartbeat", "anxiety", "tremors", "heat intolerance", "excessive sweating", "irritability"],
        "treatments": [
            {"name": "Methimazole", "type": "medication"},
            {"name": "Radioactive iodine therapy", "type": "procedure"},
            {"name": "Beta-blockers", "type": "medication"},
            {"name": "Thyroidectomy", "type": "surgery"},
        ],
    },
    # ── Cardiovascular ───────────────────────────────────────────────────────
    {
        "condition": "Hypertension",
        "description": "Persistently elevated arterial blood pressure",
        "symptoms": ["headache", "dizziness", "chest pain", "shortness of breath", "nosebleeds", "visual changes"],
        "treatments": [
            {"name": "ACE inhibitors", "type": "medication"},
            {"name": "Beta-blockers", "type": "medication"},
            {"name": "Calcium channel blockers", "type": "medication"},
            {"name": "DASH diet", "type": "lifestyle"},
            {"name": "Sodium restriction", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Coronary Artery Disease",
        "description": "Narrowing of coronary arteries due to atherosclerotic plaque buildup",
        "symptoms": ["chest pain", "chest tightness", "shortness of breath", "fatigue", "heart palpitations"],
        "treatments": [
            {"name": "Aspirin", "type": "medication"},
            {"name": "Statins", "type": "medication"},
            {"name": "Nitroglycerin", "type": "medication"},
            {"name": "Percutaneous coronary intervention", "type": "procedure"},
            {"name": "Coronary artery bypass graft", "type": "surgery"},
        ],
    },
    {
        "condition": "Heart Failure",
        "description": "Chronic condition in which the heart cannot pump enough blood to meet body needs",
        "symptoms": ["shortness of breath", "fatigue", "leg swelling", "rapid heartbeat", "persistent cough", "reduced exercise tolerance"],
        "treatments": [
            {"name": "ACE inhibitors", "type": "medication"},
            {"name": "Beta-blockers", "type": "medication"},
            {"name": "Diuretics", "type": "medication"},
            {"name": "Sodium restriction", "type": "lifestyle"},
            {"name": "Cardiac resynchronization therapy", "type": "procedure"},
        ],
    },
    {
        "condition": "Atrial Fibrillation",
        "description": "Irregular and often rapid heart rate that increases risk of stroke and heart failure",
        "symptoms": ["irregular heartbeat", "heart palpitations", "shortness of breath", "fatigue", "chest pain", "dizziness"],
        "treatments": [
            {"name": "Anticoagulants", "type": "medication"},
            {"name": "Rate control medications", "type": "medication"},
            {"name": "Cardioversion", "type": "procedure"},
            {"name": "Catheter ablation", "type": "procedure"},
        ],
    },
    {
        "condition": "Stroke",
        "description": "Brain damage from interrupted blood supply, either ischemic or hemorrhagic",
        "symptoms": ["sudden numbness", "confusion", "trouble speaking", "vision problems", "severe headache", "loss of balance", "facial drooping"],
        "treatments": [
            {"name": "tPA thrombolysis", "type": "procedure"},
            {"name": "Mechanical thrombectomy", "type": "procedure"},
            {"name": "Antiplatelet therapy", "type": "medication"},
            {"name": "Rehabilitation therapy", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Deep Vein Thrombosis",
        "description": "Blood clot forming in a deep vein, typically in the leg",
        "symptoms": ["leg pain", "leg swelling", "redness", "warmth in leg", "skin discoloration"],
        "treatments": [
            {"name": "Anticoagulants", "type": "medication"},
            {"name": "Compression stockings", "type": "procedure"},
            {"name": "Thrombolytic therapy", "type": "medication"},
            {"name": "Leg elevation", "type": "lifestyle"},
        ],
    },
    # ── Respiratory ──────────────────────────────────────────────────────────
    {
        "condition": "Asthma",
        "description": "Chronic inflammatory airway disease causing reversible airflow obstruction",
        "symptoms": ["wheezing", "shortness of breath", "chest tightness", "chronic cough", "nighttime cough"],
        "treatments": [
            {"name": "Short-acting beta-agonists", "type": "medication"},
            {"name": "Inhaled corticosteroids", "type": "medication"},
            {"name": "Leukotriene modifiers", "type": "medication"},
            {"name": "Avoiding allergens", "type": "lifestyle"},
        ],
    },
    {
        "condition": "COPD",
        "description": "Chronic obstructive pulmonary disease causing progressive airflow limitation",
        "symptoms": ["chronic cough", "excessive mucus production", "shortness of breath", "wheezing", "fatigue", "cyanosis"],
        "treatments": [
            {"name": "Bronchodilators", "type": "medication"},
            {"name": "Inhaled corticosteroids", "type": "medication"},
            {"name": "Smoking cessation", "type": "lifestyle"},
            {"name": "Pulmonary rehabilitation", "type": "lifestyle"},
            {"name": "Supplemental oxygen", "type": "procedure"},
        ],
    },
    {
        "condition": "Pneumonia",
        "description": "Infection causing inflammation of air sacs in one or both lungs",
        "symptoms": ["cough with phlegm", "fever", "chills", "shortness of breath", "chest pain", "fatigue", "nausea"],
        "treatments": [
            {"name": "Antibiotics", "type": "medication"},
            {"name": "Antiviral medications", "type": "medication"},
            {"name": "Rest and hydration", "type": "lifestyle"},
            {"name": "Oxygen therapy", "type": "procedure"},
        ],
    },
    {
        "condition": "Pulmonary Embolism",
        "description": "Blockage of pulmonary arteries by blood clots, usually from deep veins",
        "symptoms": ["sudden shortness of breath", "chest pain", "coughing up blood", "rapid heart rate", "dizziness", "leg pain"],
        "treatments": [
            {"name": "Anticoagulants", "type": "medication"},
            {"name": "Thrombolytics", "type": "medication"},
            {"name": "Surgical embolectomy", "type": "surgery"},
            {"name": "Vena cava filter", "type": "procedure"},
        ],
    },
    {
        "condition": "Tuberculosis",
        "description": "Bacterial infection primarily affecting the lungs caused by Mycobacterium tuberculosis",
        "symptoms": ["persistent cough", "coughing blood", "night sweats", "fever", "unintended weight loss", "fatigue", "chest pain"],
        "treatments": [
            {"name": "Isoniazid", "type": "medication"},
            {"name": "Rifampin", "type": "medication"},
            {"name": "Pyrazinamide", "type": "medication"},
            {"name": "Ethambutol", "type": "medication"},
        ],
    },
    # ── Gastrointestinal ─────────────────────────────────────────────────────
    {
        "condition": "GERD",
        "description": "Gastroesophageal reflux disease with chronic acid reflux into the esophagus",
        "symptoms": ["heartburn", "acid regurgitation", "difficulty swallowing", "chest pain", "chronic cough", "sore throat"],
        "treatments": [
            {"name": "Proton pump inhibitors", "type": "medication"},
            {"name": "H2 blockers", "type": "medication"},
            {"name": "Antacids", "type": "medication"},
            {"name": "Dietary modifications", "type": "lifestyle"},
            {"name": "Weight loss", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Peptic Ulcer Disease",
        "description": "Open sores on the stomach lining or upper small intestine",
        "symptoms": ["burning stomach pain", "nausea", "bloating", "heartburn", "dark stools", "vomiting blood"],
        "treatments": [
            {"name": "Proton pump inhibitors", "type": "medication"},
            {"name": "H. pylori eradication antibiotics", "type": "medication"},
            {"name": "Avoiding NSAIDs", "type": "lifestyle"},
            {"name": "Avoiding alcohol", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Crohn's Disease",
        "description": "Inflammatory bowel disease causing inflammation throughout the digestive tract",
        "symptoms": ["abdominal pain", "diarrhea", "blood in stool", "fatigue", "unintended weight loss", "mouth sores", "fever"],
        "treatments": [
            {"name": "Corticosteroids", "type": "medication"},
            {"name": "Immunomodulators", "type": "medication"},
            {"name": "Biologics anti-TNF therapy", "type": "medication"},
            {"name": "Low-fiber diet", "type": "lifestyle"},
            {"name": "Bowel resection surgery", "type": "surgery"},
        ],
    },
    {
        "condition": "Ulcerative Colitis",
        "description": "Inflammatory bowel disease causing ulcers in the colon and rectum lining",
        "symptoms": ["bloody diarrhea", "abdominal cramping", "urgency to defecate", "fatigue", "unintended weight loss", "fever"],
        "treatments": [
            {"name": "Aminosalicylates", "type": "medication"},
            {"name": "Corticosteroids", "type": "medication"},
            {"name": "Immunomodulators", "type": "medication"},
            {"name": "Colectomy", "type": "surgery"},
        ],
    },
    {
        "condition": "Irritable Bowel Syndrome",
        "description": "Chronic disorder of the large intestine causing bowel habit changes without structural damage",
        "symptoms": ["abdominal pain", "bloating", "gas", "diarrhea", "constipation", "mucus in stool"],
        "treatments": [
            {"name": "Antispasmodics", "type": "medication"},
            {"name": "Laxatives", "type": "medication"},
            {"name": "Antidiarrheal agents", "type": "medication"},
            {"name": "High-fiber diet", "type": "lifestyle"},
            {"name": "Stress management", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Gallstones",
        "description": "Hardened digestive fluid deposits forming in the gallbladder",
        "symptoms": ["sudden severe abdominal pain", "back pain between shoulder blades", "nausea", "vomiting", "jaundice"],
        "treatments": [
            {"name": "Cholecystectomy", "type": "surgery"},
            {"name": "Ursodiol", "type": "medication"},
            {"name": "Pain management", "type": "medication"},
        ],
    },
    {
        "condition": "Pancreatitis",
        "description": "Acute or chronic inflammation of the pancreas",
        "symptoms": ["severe upper abdominal pain", "pain radiating to back", "nausea", "vomiting", "fever", "rapid pulse"],
        "treatments": [
            {"name": "IV fluids", "type": "procedure"},
            {"name": "Pain medications", "type": "medication"},
            {"name": "Fasting and bowel rest", "type": "lifestyle"},
            {"name": "Alcohol cessation", "type": "lifestyle"},
            {"name": "Enzyme supplements", "type": "medication"},
        ],
    },
    {
        "condition": "Liver Cirrhosis",
        "description": "Late-stage liver scarring caused by long-term liver disease",
        "symptoms": ["fatigue", "easy bruising", "jaundice", "abdominal swelling", "leg swelling", "confusion", "spider angiomas"],
        "treatments": [
            {"name": "Alcohol cessation", "type": "lifestyle"},
            {"name": "Diuretics", "type": "medication"},
            {"name": "Beta-blockers", "type": "medication"},
            {"name": "Liver transplantation", "type": "surgery"},
        ],
    },
    {
        "condition": "Hepatitis B",
        "description": "Viral liver infection caused by hepatitis B virus, can become chronic",
        "symptoms": ["jaundice", "abdominal pain", "dark urine", "fatigue", "nausea", "vomiting", "joint pain"],
        "treatments": [
            {"name": "Tenofovir", "type": "medication"},
            {"name": "Entecavir", "type": "medication"},
            {"name": "Hepatitis B vaccination", "type": "procedure"},
        ],
    },
    {
        "condition": "Hepatitis C",
        "description": "Viral liver infection caused by hepatitis C virus, often chronic and curable",
        "symptoms": ["fatigue", "jaundice", "dark urine", "nausea", "abdominal pain", "joint pain", "clay-colored stools"],
        "treatments": [
            {"name": "Direct-acting antivirals", "type": "medication"},
            {"name": "Sofosbuvir", "type": "medication"},
            {"name": "Alcohol cessation", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Appendicitis",
        "description": "Acute inflammation of the appendix requiring emergency treatment",
        "symptoms": ["pain migrating to lower right abdomen", "nausea", "vomiting", "fever", "loss of appetite", "abdominal rigidity"],
        "treatments": [
            {"name": "Appendectomy", "type": "surgery"},
            {"name": "Antibiotics", "type": "medication"},
        ],
    },
    # ── Renal ────────────────────────────────────────────────────────────────
    {
        "condition": "Chronic Kidney Disease",
        "description": "Gradual and irreversible loss of kidney function over months or years",
        "symptoms": ["fatigue", "leg swelling", "shortness of breath", "nausea", "decreased urine output", "blood in urine", "high blood pressure"],
        "treatments": [
            {"name": "ACE inhibitors", "type": "medication"},
            {"name": "Blood pressure control", "type": "medication"},
            {"name": "Low-protein diet", "type": "lifestyle"},
            {"name": "Dialysis", "type": "procedure"},
            {"name": "Kidney transplantation", "type": "surgery"},
        ],
    },
    {
        "condition": "Urinary Tract Infection",
        "description": "Bacterial infection anywhere in the urinary tract, most commonly the bladder",
        "symptoms": ["burning urination", "frequent urination", "cloudy urine", "strong urine odor", "pelvic pain", "fever"],
        "treatments": [
            {"name": "Antibiotics", "type": "medication"},
            {"name": "Increased fluid intake", "type": "lifestyle"},
            {"name": "Urinary analgesics", "type": "medication"},
        ],
    },
    # ── Musculoskeletal ──────────────────────────────────────────────────────
    {
        "condition": "Osteoarthritis",
        "description": "Degenerative joint disease causing progressive cartilage breakdown",
        "symptoms": ["joint pain", "morning stiffness", "decreased range of motion", "joint swelling", "grinding sensation", "bone spurs"],
        "treatments": [
            {"name": "NSAIDs", "type": "medication"},
            {"name": "Acetaminophen", "type": "medication"},
            {"name": "Corticosteroid injections", "type": "procedure"},
            {"name": "Physical therapy", "type": "lifestyle"},
            {"name": "Joint replacement surgery", "type": "surgery"},
        ],
    },
    {
        "condition": "Rheumatoid Arthritis",
        "description": "Autoimmune disease causing chronic symmetric joint inflammation",
        "symptoms": ["joint pain", "joint swelling", "morning stiffness", "fatigue", "fever", "loss of appetite", "symmetric joint involvement"],
        "treatments": [
            {"name": "DMARDs methotrexate", "type": "medication"},
            {"name": "Biologics anti-TNF", "type": "medication"},
            {"name": "NSAIDs", "type": "medication"},
            {"name": "Corticosteroids", "type": "medication"},
            {"name": "Physical therapy", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Osteoporosis",
        "description": "Systemic skeletal disease characterized by low bone mass and microarchitectural deterioration",
        "symptoms": ["back pain", "loss of height over time", "stooped posture", "fragility fractures"],
        "treatments": [
            {"name": "Bisphosphonates", "type": "medication"},
            {"name": "Calcium supplementation", "type": "medication"},
            {"name": "Vitamin D supplementation", "type": "medication"},
            {"name": "Weight-bearing exercise", "type": "lifestyle"},
            {"name": "Fall prevention strategies", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Gout",
        "description": "Crystal arthropathy caused by uric acid deposition in joints",
        "symptoms": ["sudden severe joint pain", "joint redness", "joint warmth", "joint swelling", "limited range of motion"],
        "treatments": [
            {"name": "NSAIDs", "type": "medication"},
            {"name": "Colchicine", "type": "medication"},
            {"name": "Allopurinol", "type": "medication"},
            {"name": "Low-purine diet", "type": "lifestyle"},
            {"name": "Avoiding alcohol", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Fibromyalgia",
        "description": "Chronic disorder causing widespread musculoskeletal pain with fatigue and mood disturbances",
        "symptoms": ["widespread pain", "fatigue", "sleep problems", "cognitive difficulties", "headaches", "depression", "irritable bowel symptoms"],
        "treatments": [
            {"name": "Duloxetine", "type": "medication"},
            {"name": "Pregabalin", "type": "medication"},
            {"name": "Amitriptyline", "type": "medication"},
            {"name": "Aerobic exercise", "type": "lifestyle"},
            {"name": "Cognitive behavioral therapy", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Lupus",
        "description": "Systemic autoimmune disease causing widespread inflammation and multi-organ tissue damage",
        "symptoms": ["butterfly rash on face", "fatigue", "joint pain", "joint swelling", "fever", "photosensitivity", "hair loss", "chest pain"],
        "treatments": [
            {"name": "Hydroxychloroquine", "type": "medication"},
            {"name": "Corticosteroids", "type": "medication"},
            {"name": "Immunosuppressants", "type": "medication"},
            {"name": "Sun protection", "type": "lifestyle"},
        ],
    },
    # ── Neurological ─────────────────────────────────────────────────────────
    {
        "condition": "Multiple Sclerosis",
        "description": "Autoimmune disease where the immune system attacks myelin sheaths of CNS nerve fibers",
        "symptoms": ["numbness or tingling", "muscle weakness", "vision problems", "balance problems", "fatigue", "cognitive changes", "bladder problems"],
        "treatments": [
            {"name": "Interferon beta", "type": "medication"},
            {"name": "Glatiramer acetate", "type": "medication"},
            {"name": "Natalizumab", "type": "medication"},
            {"name": "Physical therapy", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Parkinson's Disease",
        "description": "Progressive neurological disorder causing dopamine deficiency and motor dysfunction",
        "symptoms": ["resting tremor", "bradykinesia", "muscle rigidity", "postural instability", "stooped posture", "soft speech", "micrographia"],
        "treatments": [
            {"name": "Levodopa", "type": "medication"},
            {"name": "Dopamine agonists", "type": "medication"},
            {"name": "Deep brain stimulation", "type": "procedure"},
            {"name": "Physical therapy", "type": "lifestyle"},
            {"name": "Speech therapy", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Alzheimer's Disease",
        "description": "Progressive neurodegenerative disorder causing memory loss and cognitive decline",
        "symptoms": ["memory loss", "confusion", "disorientation", "mood changes", "difficulty with daily tasks", "communication problems", "wandering"],
        "treatments": [
            {"name": "Cholinesterase inhibitors", "type": "medication"},
            {"name": "Memantine", "type": "medication"},
            {"name": "Cognitive exercises", "type": "lifestyle"},
            {"name": "Caregiver support", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Epilepsy",
        "description": "Neurological disorder characterized by recurrent unprovoked seizures",
        "symptoms": ["seizures", "temporary confusion", "staring spells", "uncontrollable jerking movements", "loss of consciousness", "anxiety before seizures"],
        "treatments": [
            {"name": "Valproate", "type": "medication"},
            {"name": "Lamotrigine", "type": "medication"},
            {"name": "Levetiracetam", "type": "medication"},
            {"name": "Ketogenic diet", "type": "lifestyle"},
            {"name": "Vagus nerve stimulation", "type": "procedure"},
            {"name": "Epilepsy surgery", "type": "surgery"},
        ],
    },
    {
        "condition": "Migraine",
        "description": "Neurological disease causing recurrent severe headaches often with sensory disturbances",
        "symptoms": ["severe headache", "nausea", "vomiting", "photosensitivity", "phonosensitivity", "visual aura", "throbbing pain"],
        "treatments": [
            {"name": "Triptans", "type": "medication"},
            {"name": "NSAIDs", "type": "medication"},
            {"name": "Preventive beta-blockers", "type": "medication"},
            {"name": "Topiramate", "type": "medication"},
            {"name": "CGRP inhibitors", "type": "medication"},
            {"name": "Avoiding migraine triggers", "type": "lifestyle"},
        ],
    },
    # ── Mental Health ────────────────────────────────────────────────────────
    {
        "condition": "Major Depressive Disorder",
        "description": "Mental health condition characterized by persistent low mood and loss of interest",
        "symptoms": ["persistent sadness", "loss of interest", "fatigue", "sleep disturbances", "appetite changes", "difficulty concentrating", "suicidal thoughts"],
        "treatments": [
            {"name": "SSRIs", "type": "medication"},
            {"name": "SNRIs", "type": "medication"},
            {"name": "Cognitive behavioral therapy", "type": "lifestyle"},
            {"name": "Psychotherapy", "type": "lifestyle"},
            {"name": "Electroconvulsive therapy", "type": "procedure"},
        ],
    },
    {
        "condition": "Generalized Anxiety Disorder",
        "description": "Persistent and excessive worry about various aspects of daily life",
        "symptoms": ["excessive worry", "restlessness", "fatigue", "difficulty concentrating", "irritability", "muscle tension", "sleep problems"],
        "treatments": [
            {"name": "SSRIs", "type": "medication"},
            {"name": "SNRIs", "type": "medication"},
            {"name": "Buspirone", "type": "medication"},
            {"name": "Cognitive behavioral therapy", "type": "lifestyle"},
            {"name": "Relaxation techniques", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Bipolar Disorder",
        "description": "Mental health condition causing extreme mood swings between mania and depression",
        "symptoms": ["manic episodes", "depressive episodes", "impulsive behavior", "grandiosity", "decreased need for sleep", "racing thoughts"],
        "treatments": [
            {"name": "Lithium", "type": "medication"},
            {"name": "Valproate", "type": "medication"},
            {"name": "Atypical antipsychotics", "type": "medication"},
            {"name": "Psychotherapy", "type": "lifestyle"},
            {"name": "Regular sleep schedule", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Schizophrenia",
        "description": "Serious chronic mental disorder affecting thinking, feeling, and behavior",
        "symptoms": ["hallucinations", "delusions", "disorganized thinking", "flat affect", "social withdrawal", "cognitive impairment"],
        "treatments": [
            {"name": "Antipsychotics", "type": "medication"},
            {"name": "Clozapine", "type": "medication"},
            {"name": "Psychosocial therapy", "type": "lifestyle"},
            {"name": "Social skills training", "type": "lifestyle"},
        ],
    },
    {
        "condition": "ADHD",
        "description": "Neurodevelopmental disorder characterized by inattention, hyperactivity, and impulsivity",
        "symptoms": ["inattention", "hyperactivity", "impulsivity", "difficulty organizing", "forgetfulness", "fidgeting", "difficulty completing tasks"],
        "treatments": [
            {"name": "Methylphenidate", "type": "medication"},
            {"name": "Amphetamine salts", "type": "medication"},
            {"name": "Atomoxetine", "type": "medication"},
            {"name": "Behavioral therapy", "type": "lifestyle"},
            {"name": "Organizational skills training", "type": "lifestyle"},
        ],
    },
    # ── Infectious Disease ───────────────────────────────────────────────────
    {
        "condition": "COVID-19",
        "description": "Respiratory illness caused by SARS-CoV-2 coronavirus with broad systemic effects",
        "symptoms": ["fever", "cough", "shortness of breath", "fatigue", "loss of taste", "loss of smell", "body aches", "sore throat"],
        "treatments": [
            {"name": "Nirmatrelvir-ritonavir Paxlovid", "type": "medication"},
            {"name": "Remdesivir", "type": "medication"},
            {"name": "Rest and hydration", "type": "lifestyle"},
            {"name": "Oxygen therapy", "type": "procedure"},
            {"name": "Corticosteroids dexamethasone", "type": "medication"},
        ],
    },
    {
        "condition": "Influenza",
        "description": "Contagious respiratory illness caused by influenza A or B viruses",
        "symptoms": ["fever", "chills", "muscle aches", "cough", "sore throat", "runny nose", "headache", "fatigue"],
        "treatments": [
            {"name": "Oseltamivir", "type": "medication"},
            {"name": "Rest", "type": "lifestyle"},
            {"name": "Hydration", "type": "lifestyle"},
            {"name": "Annual influenza vaccine", "type": "procedure"},
            {"name": "Antipyretics", "type": "medication"},
        ],
    },
    {
        "condition": "HIV/AIDS",
        "description": "Viral infection attacking CD4 T cells and the immune system caused by HIV",
        "symptoms": ["fever", "night sweats", "fatigue", "swollen lymph nodes", "unintended weight loss", "chronic diarrhea", "oral thrush"],
        "treatments": [
            {"name": "Antiretroviral therapy", "type": "medication"},
            {"name": "Pre-exposure prophylaxis PrEP", "type": "medication"},
            {"name": "Opportunistic infection prophylaxis", "type": "medication"},
            {"name": "Regular CD4 monitoring", "type": "procedure"},
        ],
    },
    # ── Cancer ───────────────────────────────────────────────────────────────
    {
        "condition": "Breast Cancer",
        "description": "Malignant tumor originating in breast tissue, most common cancer in women",
        "symptoms": ["breast lump", "breast pain", "nipple discharge", "breast skin changes", "swollen axillary lymph nodes"],
        "treatments": [
            {"name": "Lumpectomy", "type": "surgery"},
            {"name": "Mastectomy", "type": "surgery"},
            {"name": "Chemotherapy", "type": "medication"},
            {"name": "Radiation therapy", "type": "procedure"},
            {"name": "Hormone therapy tamoxifen", "type": "medication"},
            {"name": "Targeted therapy trastuzumab", "type": "medication"},
        ],
    },
    {
        "condition": "Lung Cancer",
        "description": "Malignant tumor originating in lung tissue, strongly associated with tobacco smoking",
        "symptoms": ["persistent cough", "coughing up blood", "chest pain", "shortness of breath", "hoarseness", "unintended weight loss", "bone pain"],
        "treatments": [
            {"name": "Surgical resection", "type": "surgery"},
            {"name": "Chemotherapy", "type": "medication"},
            {"name": "Radiation therapy", "type": "procedure"},
            {"name": "Immunotherapy checkpoint inhibitors", "type": "medication"},
            {"name": "Targeted therapy EGFR inhibitors", "type": "medication"},
            {"name": "Smoking cessation", "type": "lifestyle"},
        ],
    },
    {
        "condition": "Colorectal Cancer",
        "description": "Malignant tumor of the colon or rectum, often arising from adenomatous polyps",
        "symptoms": ["blood in stool", "change in bowel habits", "abdominal pain", "unintended weight loss", "fatigue", "feeling of incomplete evacuation"],
        "treatments": [
            {"name": "Colectomy", "type": "surgery"},
            {"name": "Chemotherapy", "type": "medication"},
            {"name": "Radiation therapy", "type": "procedure"},
            {"name": "Targeted therapy bevacizumab", "type": "medication"},
            {"name": "Regular colonoscopy screening", "type": "procedure"},
        ],
    },
    {
        "condition": "Prostate Cancer",
        "description": "Malignant tumor arising in the prostate gland, common in older men",
        "symptoms": ["difficulty urinating", "frequent urination at night", "blood in urine", "blood in semen", "bone pain", "erectile dysfunction"],
        "treatments": [
            {"name": "Active surveillance", "type": "procedure"},
            {"name": "Radical prostatectomy", "type": "surgery"},
            {"name": "Radiation therapy", "type": "procedure"},
            {"name": "Androgen deprivation therapy", "type": "medication"},
            {"name": "Chemotherapy", "type": "medication"},
        ],
    },
    {
        "condition": "Leukemia",
        "description": "Cancer of blood-forming tissues affecting the blood and bone marrow",
        "symptoms": ["fatigue", "frequent infections", "easy bruising", "bleeding gums", "swollen lymph nodes", "bone pain", "fever", "night sweats"],
        "treatments": [
            {"name": "Chemotherapy", "type": "medication"},
            {"name": "Targeted therapy imatinib", "type": "medication"},
            {"name": "Bone marrow transplantation", "type": "procedure"},
            {"name": "Immunotherapy", "type": "medication"},
        ],
    },
    {
        "condition": "Lymphoma",
        "description": "Cancer of the lymphatic system, including Hodgkin and non-Hodgkin types",
        "symptoms": ["swollen lymph nodes", "fatigue", "fever", "night sweats", "unintended weight loss", "itching", "shortness of breath"],
        "treatments": [
            {"name": "Chemotherapy CHOP regimen", "type": "medication"},
            {"name": "Radiation therapy", "type": "procedure"},
            {"name": "Rituximab immunotherapy", "type": "medication"},
            {"name": "Stem cell transplantation", "type": "procedure"},
        ],
    },
    # ── Hematologic ──────────────────────────────────────────────────────────
    {
        "condition": "Iron Deficiency Anemia",
        "description": "Most common anemia type caused by insufficient iron for hemoglobin production",
        "symptoms": ["fatigue", "pale skin", "shortness of breath", "dizziness", "chest pain", "cold hands and feet", "brittle nails", "headache"],
        "treatments": [
            {"name": "Oral iron supplementation", "type": "medication"},
            {"name": "Iron-rich diet", "type": "lifestyle"},
            {"name": "IV iron infusion", "type": "procedure"},
            {"name": "Treating underlying bleeding source", "type": "procedure"},
        ],
    },
]


# ---------------------------------------------------------------------------
# Graph construction helpers
# ---------------------------------------------------------------------------

def _create_constraints():
    constraints = [
        "CREATE CONSTRAINT condition_unique IF NOT EXISTS FOR (c:Condition) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT symptom_unique IF NOT EXISTS FOR (s:Symptom) REQUIRE s.name IS UNIQUE",
        "CREATE CONSTRAINT treatment_unique IF NOT EXISTS FOR (t:Treatment) REQUIRE t.name IS UNIQUE",
    ]
    for cypher in constraints:
        try:
            run_query(cypher)
        except Exception:
            pass  # constraints may already exist or syntax differs by Neo4j version


def _load_condition(entry: dict):
    run_query(
        "MERGE (c:Condition {name: $name}) SET c.description = $description",
        {"name": entry["condition"], "description": entry["description"]},
    )
    for symptom in entry["symptoms"]:
        run_query(
            """
            MERGE (s:Symptom {name: $symptom})
            WITH s
            MATCH (c:Condition {name: $condition})
            MERGE (s)-[:INDICATES]->(c)
            """,
            {"symptom": symptom, "condition": entry["condition"]},
        )
    for treatment in entry["treatments"]:
        run_query(
            """
            MERGE (t:Treatment {name: $name}) SET t.type = $type
            WITH t
            MATCH (c:Condition {name: $condition})
            MERGE (c)-[:TREATED_BY]->(t)
            """,
            {"name": treatment["name"], "type": treatment["type"], "condition": entry["condition"]},
        )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def load_graph():
    print("  Creating Neo4j constraints...")
    _create_constraints()

    print(f"  Loading {len(MEDICAL_GRAPH_DATA)} conditions into Neo4j...")
    for i, entry in enumerate(MEDICAL_GRAPH_DATA, 1):
        _load_condition(entry)
        if i % 10 == 0 or i == len(MEDICAL_GRAPH_DATA):
            print(f"    {i}/{len(MEDICAL_GRAPH_DATA)} conditions loaded")

    # Summary query
    counts = run_query(
        """
        MATCH (c:Condition) WITH count(c) AS conditions
        MATCH (s:Symptom)   WITH conditions, count(s) AS symptoms
        MATCH (t:Treatment) RETURN conditions, symptoms, count(t) AS treatments
        """
    )
    if counts:
        r = counts[0]
        print(f"  Graph ready — {r['conditions']} conditions, {r['symptoms']} symptoms, {r['treatments']} treatments")
