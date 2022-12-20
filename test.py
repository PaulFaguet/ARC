from readability import Readability
import textstat as ts
import math 

text_bad_fr = """
Le mécanisme de régulation de la température interne du corps humain est complexe et dépend de nombreux facteurs, tels que l'exposition au froid ou à la chaleur, l'activité physique, l'alimentation et l'état de santé général. 
La thermorégulation est assurée par le système nerveux et endocrinien, qui agissent en synergie pour maintenir la température du corps à un niveau optimal. 
Lorsque la température du corps augmente, par exemple en cas de fièvre ou d'exercice physique intense, le système de thermorégulation active des mécanismes de refroidissement tels que la transpiration ou la vasodilatation des vaisseaux sanguins de la peau. 
À l'inverse, lorsque la température du corps diminue, par exemple en cas de froid ou de stress, le système de thermorégulation active des mécanismes de réchauffement tels que la contraction des vaisseaux sanguins de la peau ou la production de chaleur par le métabolisme cellulaire.
"""
sent_bad_fr = "mécanisme de régulation de la température interne du corps humain"

text_bad_en = """
The mechanism of regulation of the human body's internal temperature is complex and depends on many factors, such as exposure to cold or heat, physical activity, nutrition, and general health. 
Thermoregulation is carried out by the nervous and endocrine systems, which work together to maintain the body's temperature at an optimal level. 
When the body temperature increases, for example in the case of fever or intense physical exercise, the thermoregulation system activates cooling mechanisms such as sweating or vasodilation of the skin's blood vessels. 
On the other hand, when the body temperature decreases, for example in the case of cold or stress, the thermoregulation system activates warming mechanisms such as contraction of the skin's blood vessels or production of heat by cellular metabolism.
"""
sent_bad_en = "mechanism of regulation of the human body's internal temperature"

text_good_fr = """
Le soleil est une étoile de type G2, c'est-à-dire une étoile de la séquence principale de type spectral G, de la deuxième sous-classe. 
Elle est située au centre de notre système solaire et constitue la principale source de lumière et de chaleur pour la Terre et les autres planètes du système solaire. 
Le soleil est composé principalement de gaz hydrogène et hélium, et sa température à la surface est d'environ 5 500 degrés Celsius. 
Sa luminosité est due à la réaction de fusion nucléaire qui a lieu au cœur de l'étoile, où l'hydrogène est converti en hélium grâce à la libération d'énergie sous forme de lumière et de chaleur. 
Le soleil a une durée de vie estimée à environ 10 milliards d'années et est considéré comme étant dans sa phase principale depuis environ 4,6 milliards d'années.
"""
sent_good_fr = "étoile de type G2 située au centre de notre système solaire"

text_good_en = """
The sun is a G2-type star, that is, a main sequence star of spectral type G, of the second subclass. 
It is located at the center of our solar system and is the main source of light and heat for the Earth and other planets in the solar system. 
The sun is mainly composed of hydrogen and helium gas, and its surface temperature is about 5,500 degrees Celsius. 
Its luminosity is due to the nuclear fusion reaction that takes place at the core of the star, where hydrogen is converted into helium through the release of energy in the form of light and heat. 
The sun has an estimated lifetime of about 10 billion years and has been in its main phase for about 4.6 billion years.
"""
sent_good_en = "G2-type star located at the center of our solar system"

texts = [text_bad_fr, text_good_fr, text_bad_en, text_good_en]
sents = [sent_bad_fr, sent_bad_en, sent_good_fr, sent_good_en]

for text in texts:
    ts.set_lang("fr")
    flesch = ts.flesch_reading_ease(text)
    
    dc = ts.dale_chall_readability_score(text)
    fk = ts.flesch_kincaid_grade(text)
    ari = ts.automated_readability_index(text)
    grade_moyen = (dc + fk + ari) / 3
    
    rt = ts.reading_time(text)
    rt = math.ceil(rt / 60) if rt > 60 else math.ceil(rt)
    
    print(f"""
            ----
            flesch: {flesch}
            
            ----
            dale chall: {dc}
            fk: {fk}
            ari: {ari}
            ----
            grade moyen: {grade_moyen}
            
            ----
            reading time: {rt} {'secondes' if rt < 60 else 'minutes'}
          """)


for text, sent in zip(texts, sents):
        
    r = Readability(text)
    # precision, recall, f1 = score([sent_good_en], [text_good_en], lang="en", verbose=False, model_type="bert-base-multilingual-cased")
    fk = r.flesch_kincaid()
    f = r.flesch()
    gf = r.gunning_fog()
    cl = r.coleman_liau()
    dc = r.dale_chall()
    a = r.ari()
    lw = r.linsear_write()
    # try:
    s = r.smog(all_sentences=True)
    # except:
    #     s = 'trop peu de phrases'
    sp = r.spache()

    print(f"""
        fl_kincaid: {fk.score} | {fk.grade_level} | difficulty of technical manuals
        -- flesch: {f.score} | {f.grade_levels} | {f.ease} | standard test of readability
        dale_chall: {dc.score} | {dc.grade_levels} | nombre de mots connus ou inconnus présents

        ari: {a.score} | longueur moyenne des phrases et des mots
        -- gunning_fog: {gf.score} | {gf.grade_level} | measures the readability of English writing.
        -- smog: {s.score if s != 'trop peu de phrases' else s} 
        
        linsear_write: {lw.score} | la structure syntaxique du texte
        spache: {sp.score} |  calculate the difficulty of text that falls at the 3rd grade level or below
        """)

# flesch -> la longueur moyenne des phrases et la longueur moyenne des mots d'un texte. Plus le score FLESCH d'un texte est élevé, plus le texte est considéré comme facile à lire.
