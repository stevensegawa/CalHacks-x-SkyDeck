from openai import OpenAI
import os

def diagnoser(
        csv_file: str,
        prompt: str,
) -> str:
    os.environ["OPENAI_API_KEY"] = "sk-proj-7Fvjyy6R1HzENEQmXRECT3BlbkFJ5IKW1tl8vpcvnsiHYRoe"

    client = OpenAI()
    csv_file = csv_file
    file = client.files.create(
    file=open(csv_file, "rb"),
    purpose='assistants'
    )

    concerns = 'Diabetes, Hypertension, Anxiety, Depression, Flu, Obesity, Asthma, Chronic Obstructive Pulmonary Disease (COPD), Arthritis, Osteoporosis, Cancer, Heart Disease, Stroke, Alzheimers Disease, Parkinsons Disease, Multiple Sclerosis, Epilepsy, Migraine, Allergies, HIV/AIDS, Hepatitis, Tuberculosis, Pneumonia, Influenza, Bronchitis, Sinusitis, Gastroesophageal Reflux Disease (GERD), Irritable Bowel Syndrome (IBS), Crohns Disease, Ulcerative Colitis, Celiac Disease, Gallstones, Kidney Stones, Chronic Kidney Disease, Urinary Tract Infection (UTI), Prostate Cancer, Breast Cancer, Cervical Cancer, Ovarian Cancer, Colorectal Cancer, Lung Cancer, Skin Cancer, Leukemia, Lymphoma, Anemia, Thalassemia, Sickle Cell Disease, Hemophilia, Thrombocytopenia, Hyperthyroidism, Hypothyroidism, Cushings Syndrome, Addisons Disease, Polycystic Ovary Syndrome (PCOS), Endometriosis, Menopause, Erectile Dysfunction, Infertility, Obstructive Sleep Apnea, Insomnia, Narcolepsy, Restless Leg Syndrome, Autism Spectrum Disorder, Attention Deficit Hyperactivity Disorder (ADHD), Dyslexia, Schizophrenia, Bipolar Disorder, Post-Traumatic Stress Disorder (PTSD), Obsessive-Compulsive Disorder (OCD), Eating Disorders, Substance Abuse, Alcoholism, Cirrhosis, Fatty Liver Disease, Pancreatitis, Gallbladder Disease, Hepatic Encephalopathy, Lyme Disease, Malaria, Dengue Fever, Zika Virus, West Nile Virus, Ebola Virus, Measles, Mumps, Rubella, Chickenpox, Shingles, Whooping Cough, Tetanus, Rabies, Anthrax, Cholera, Dysentery, Typhoid Fever, Polio, Hepatitis A, Hepatitis B, Hepatitis C, RSV (Respiratory Syncytial Virus), Hantavirus, SARS (Severe Acute Respiratory Syndrome), MERS (Middle East Respiratory Syndrome), COVID-19, Lupus, Rheumatoid Arthritis, Psoriasis, Eczema, Vitiligo, Scleroderma, Fibromyalgia, Chronic Fatigue Syndrome, Lyme Disease, Amyotrophic Lateral Sclerosis (ALS), Huntingtons Disease, Duchenne Muscular Dystrophy, Spinal Muscular Atrophy, Guillain-Barré Syndrome, Peripheral Neuropathy, Carpal Tunnel Syndrome, Sciatica, Herniated Disc, Scoliosis, Osteoarthritis, Gout, Bursitis, Tendinitis, Plantar Fasciitis, Deep Vein Thrombosis (DVT), Varicose Veins, Lymphedema, Hemorrhoids, Glaucoma, Cataracts, Macular Degeneration, Retinitis Pigmentosa, Diabetic Retinopathy, Conjunctivitis, Keratitis, Uveitis, Retinal Detachment, Strabismus, Amblyopia, Hearing Loss, Tinnitus, Otitis Media, Menieres Disease, Vertigo, Sinusitis, Pharyngitis, Tonsillitis, Laryngitis, Mononucleosis, Influenza, Common Cold, SARS, COVID-19, Bronchiolitis, Emphysema, Cystic Fibrosis, Pulmonary Hypertension, Pneumothorax, Pleural Effusion, Asbestosis, Silicosis, Mesothelioma, Lung Fibrosis, Interstitial Lung Disease, Pulmonary Embolism, Acute Respiratory Distress Syndrome (ARDS), Respiratory Syncytial Virus (RSV), Whooping Cough, Legionnaires Disease, Tuberculosis, Histoplasmosis, Coccidioidomycosis, Blastomycosis, Cryptococcosis, Aspergillosis, Pneumocystis Pneumonia (PCP), Lung Abscess, Bronchiectasis, Pulmonary Edema, Allergic Rhinitis, Anaphylaxis, Food Allergies, Contact Dermatitis, Atopic Dermatitis, Urticaria (Hives), Angioedema, Hypersensitivity Pneumonitis, Eosinophilic Esophagitis, Eosinophilic Granulomatosis with Polyangiitis, Hypereosinophilic Syndrome, Mastocytosis, Mast Cell Activation Syndrome, Cold Urticaria, Exercise-Induced Anaphylaxis, Drug Allergy, Latex Allergy, Insect Sting Allergy, Allergic Conjunctivitis, Allergic Bronchopulmonary Aspergillosis, Seasonal Allergies, Perennial Allergies, Allergic Asthma, Non-Allergic Rhinitis, Vasomotor Rhinitis, Gustatory Rhinitis, Occupational Asthma, Reactive Airways Dysfunction Syndrome (RADS), Vocal Cord Dysfunction, Alpha-1 Antitrypsin Deficiency, Primary Ciliary Dyskinesia, Bronchiolitis Obliterans, Lymphangioleiomyomatosis, Pulmonary Langerhans Cell Histiocytosis, Pulmonary Alveolar Proteinosis, Churg-Strauss Syndrome, Wegeners Granulomatosis, Goodpasture Syndrome, Alveolar Hemorrhage Syndrome, Idiopathic Pulmonary Hemosiderosis, Neurofibromatosis, Tuberous Sclerosis, Von Hippel-Lindau Disease, Hereditary Hemorrhagic Telangiectasia, Marfan Syndrome, Ehlers-Danlos Syndrome, Osteogenesis Imperfecta, Achondroplasia, Cleidocranial Dysplasia, Holt-Oram Syndrome, Noonan Syndrome, Turner Syndrome, Klinefelter Syndrome, Fragile X Syndrome, Prader-Willi Syndrome, Angelman Syndrome, Williams Syndrome, DiGeorge Syndrome, Crouzon Syndrome, Treacher Collins Syndrome, Pierre Robin Sequence, Beckwith-Wiedemann Syndrome, Bardet-Biedl Syndrome, CHARGE Syndrome, VACTERL Association, Cornelia de Lange Syndrome, Smith-Lemli-Opitz Syndrome, Zellweger Syndrome, Alport Syndrome, Fabry Disease, Gaucher Disease, Niemann-Pick Disease, Tay-Sachs Disease, Krabbe Disease, Metachromatic Leukodystrophy, Adrenoleukodystrophy, Mucopolysaccharidoses, Hurler Syndrome, Hunter Syndrome, Sanfilippo Syndrome, Morquio Syndrome, Maroteaux-Lamy Syndrome, Sly Syndrome, Fabry Disease, Pompe Disease, Danon Disease, Glycogen Storage Diseases, McArdle Disease, Hers Disease, Cori Disease, Andersen Disease, Tarui Disease, Fanconi Anemia, Diamond-Blackfan Anemia, Shwachman-Diamond Syndrome, Dyskeratosis Congenita, Severe Combined Immunodeficiency (SCID), Wiskott-Aldrich Syndrome, Chronic Granulomatous Disease, Hyper IgM Syndrome, Common Variable Immunodeficiency (CVID), IgA Deficiency, IgG Subclass Deficiency, Specific Antibody Deficiency, Transient Hypogammaglobulinemia of Infancy, X-Linked Agammaglobulinemia, Hyper IgE Syndrome, DiGeorge Syndrome, Ataxia-Telangiectasia, Nijmegen Breakage Syndrome, Bloom Syndrome, Fanconi Anemia, Werner Syndrome, Cockayne Syndrome, Hutchinson-Gilford Progeria Syndrome, Wiedemann-Steiner Syndrome, Coffin-Lowry Syndrome, Cornelia de Lange Syndrome, Rubinstein-Taybi Syndrome, Smith-Magenis Syndrome, Sotos Syndrome, Weaver Syndrome, Bohring-Opitz Syndrome, Nager Syndrome, Miller Syndrome, Branchio-Oto-Renal Syndrome, CHARGE Syndrome, Waardenburg Syndrome, Alagille Syndrome, Beckwith-Wiedemann Syndrome, Costello Syndrome, Simpson-Golabi-Behmel Syndrome, Kabuki Syndrome, Menkes Disease, Wilson Disease, Hemochromatosis, Porphyria, Cystinuria, Hartnup Disease, Homocystinuria, Maple Syrup Urine Disease, Phenylketonuria, Tyrosinemia, Alkaptonuria, Lesch-Nyhan Syndrome, Fabry Disease, Hunter Syndrome, Sanfilippo Syndrome, Sly Syndrome, Morquio Syndrome, Pompe Disease, Danon Disease, Barth Syndrome, Glycogen Storage Diseases, Mitochondrial Diseases, Leber Hereditary Optic Neuropathy, MELAS Syndrome, MERRF Syndrome, NARP Syndrome, Kearns-Sayre Syndrome, Pearson Syndrome, Leigh Syndrome, Alpers Disease, Mitochondrial Myopathy, Mitochondrial DNA Depletion Syndrome, Coenzyme Q10 Deficiency, Primary Carnitine Deficiency, Secondary Carnitine Deficiency, Fatty Acid Oxidation Disorders, Medium-Chain Acyl-CoA Dehydrogenase Deficiency, Long-Chain 3-Hydroxyacyl-CoA Dehydrogenase Deficiency, Very-Long-Chain Acyl-CoA Dehydrogenase Deficiency, Trifunctional Protein Deficiency, Carnitine Palmitoyltransferase I Deficiency, Carnitine Palmitoyltransferase II Deficiency, Carnitine-Acylcarnitine Translocase Deficiency, Short-Chain Acyl-CoA Dehydrogenase Deficiency, Multiple Acyl-CoA Dehydrogenase Deficiency, Glutaric Acidemia Type I, Glutaric Acidemia Type II, Propionic Acidemia, Methylmalonic Acidemia, Isovaleric Acidemia, 3-Methylcrotonyl-CoA Carboxylase Deficiency, 3-Hydroxy-3-Methylglutaryl-CoA Lyase Def'

    assistant = client.beta.assistants.create(
    name="Data visualizer",
    instructions='Given the CSV file containing a persons health data, analyze the data to identify potential health concerns and determine the level of risk for each concern. The output should be formatted as a list of health concerns, each with an associated percentage indicating the level of risk. Instructions: Input Data: Read the CSV file to extract relevant health data. Health Concerns Identification: Identify potential health concerns based on the data. Please be hesitant when concluding more severe concerns like cancer or heart disease. Risk Level Calculation: Calculate the risk level for each identified health concern. The risk level should be represented as a percentage. Output Formatting: Present the identified health concerns and their respective risk levels in a structured format.',
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
        "file_ids": [file.id]
        }
    }
    )

    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": prompt,
        "attachments": [
            {
            "file_id": file.id,
            "tools": [{"type": "code_interpreter"}]
            }
        ]
        }
    ]
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions=f'Given the CSV file containing a persons health data, analyze the data to identify potential health concerns and determine the level of risk for each concern. The health concerns chosen MUST be apart of the following list otherwise it is not considered a health concern: [{concerns}]. DO NOT USE ANYTHING ELSE, IT MUST COME WORD FOR WORD FROM THAT LIST. Rank the health concerns from top to bottom in the list by their risk level. Please list the top THREE health concerns; even if the percent of risk is very low. The output should be formatted as a list of health concerns, each with an associated percentage indicating the level of risk. Instructions: Input Data: Read the CSV file to extract relevant health data. Health Concerns Identification: Identify potential health concerns based on the data. Please be hesitant when concluding more severe concerns like cancer or heart disease. Risk Level Calculation: Calculate the risk level for each identified health concern. The risk level should be represented as a percentage. Output Formatting: Present the identified health concerns and their respective risk levels in a structured format. Do NOT provide any other text; do NOT provide a summary or any suggestions. Also do NOT use bold, italics, etc.',
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
    else:
        print(run.status)

    response = messages.data[0].content[0].text.value
    return response

def main():
    text_response = diagnoser(
        csv_file = '../scheduler/Health Data/merged_health_data_second.csv',
        prompt = 'Give me suggestions.',
    )
    print(text_response)

if __name__ == "__main__":
    main()