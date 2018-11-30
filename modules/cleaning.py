import re


###### CREATION_DATE
centuries_approximations = { "début XXe siècle":"1900 - 1930",
            "fin XIXe siècle - début XXe siècle": "1880 - 1930",
            "1ère moitié XXe siècle":"1900 - 1950",
            "milieu de XIXe siècle": "1830 - 1860",
            "XIXe siècle": "1800 - 1899",
            "XVIIIe siècle": "1700 - 1799",
            "vers XVIIe siècle": "1600 - 1699"}

years_re = re.compile(r"\d{4}")

# return a clean version of creation date
def creation_date_cleaning(creation_date):

    def clean_creation_date(date):
        if date:
            years = years_re.findall(date)
            if len(years)>=1:
                return min(years)
            return ''

    if creation_date and creation_date in centuries_approximations:
        return(clean_creation_date(centuries_approximations[creation_date]))
    else:
        return(clean_creation_date(creation_date))
 

###### ACQUISITION_MODE

acquisition_mode_aggregation = {"Achat":"Achat",
"Achat en vente publique":"Achat",
"Achat par commande":"commande",
"Achat par préemption":"Achat",
"Achat sur les arrérages d'un legs":"Achat",
"Achat en salon":"Achat", #added by Ruta Binkyte
"Achat sur la liste civile":"Achat", #added by Ruta Binkyte
"Attribution Capc - Centre d'arts plastiques contemporains":"Attribution", #added by Ruta Binkyte
'Attribution Centre national des arts plastiques':"Attribution", #added by Ruta Binkyte
"Attribution Etat":"Attribution", 
"Attribution Ministère de l'économie, des finances et de l'industrie":"Attribution", #added by Ruta Binkyte
'Attribution Ministère des Affaires étrangères et du Développement international':"Attribution", #added by Ruta Binkyte
'Attribution Ministère de la culture et de la communication':"Attribution", #added by Ruta Binkyte
"Attribution Direction de l'Urbanisme":"Attribution", #added by Ruta Binkyte
"Attribution Fonds national d'art contemporain":"Attribution",
"Attribution":"Attribution",
"Attribution par l'office des Biens et Intérêts Privés":"Attribution",
"Attribution Musée du Luxembourg":"Attribution",
"Attribution Musée du Jeu de Paume":"Attribution",
"Attribution Musée national d'art moderne / Centre de création industrielle":"Attribution",
"Attribution Centre Pompidou":"Attribution",
"Attribution Musées nationaux":"Attribution",
"Attribution Réunion des Musées Nationaux":"Attribution",
"Attribution Les Arts Décoratifs":"Attribution",
"Attribution Mobilier national et Manufactures des Gobelins, de Beauvais et de la Savonnerie":"Attribution",
'Attribution Petit Palais - Musée des Beaux-Arts de la Ville de Paris':"Attribution",  #added by Ruta Binkyte
"Commande publique":"Commande publique", #added by Ruta Binkyte
"Commande publique par commande":"Commande publique", #added by Ruta Binkyte
"Mode d'acquisition non renseigné par commande":"Mode d'acquisition non renseigné par commande", #added by Ruta Binkyte
"Dation":"Dation",
"Dépôt Fonds départemental d'art contemporain d'Ille-et-Vilaine":"Dépôt entrant",#added by Ruta Binkyte
"Dépôt Centre Pompidou Foundation":"Dépôt entrant",
"Dépôt Centre national des arts plastiques":"Dépôt entrant",
"Dépôt":"Dépôt entrant",
"Dépôt Bibliothèque littéraire Jacques Doucet":"Dépôt entrant",
"Dépôt Centre international d'art et du paysage de l'île de Vassivière":"Dépôt entrant",
"Dépôt Direction des musées de France":"Dépôt entrant",
"Dépôt Etablissement public des musées d'Orsay et de l'Orangerie":"Dépôt entrant",
"Dépôt Etablissement public pour l'aménagement de la région de la Défense":"Dépôt entrant",
"Dépôt Fonds national d'art contemporain":"Dépôt entrant",
"Dépôt Mobilier national et Manufactures des Gobelins, de Beauvais et de la Savonnerie":"Dépôt entrant",
"Dépôt Musée national Picasso":"Dépôt entrant",
"Dépôt Société des Amis du Musée national d'art moderne":"Dépôt entrant",
"Dépôt Siège national du Parti communiste français":"Dépôt entrant",
"Dépôt Association française d'action artistique": "Dépôt entrant",
"Dépôt Musée des Beaux-Arts de Nantes": "Dépôt entrant", #added by Ruta Binkyte
"Dépôt Musée d'art et d'industrie": "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Musée alsacien': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Nouveau Musée': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Gilles Lewalle': "Dépôt entrant",#added by Ruta Binkyte
"Dépôt Musée régional d'ethnologie": "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Musée des Beaux-Arts de Dunkerque': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt les Abattoirs, Musée - Frac Occitanie Toulouse': "Dépôt entrant",#added by Ruta Binkyte
"Dépôt Mairie de Villeneuve-d'Ascq": "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Musée national de la Céramique': "Dépôt entrant",#added by Ruta Binkyte
"Dépôt Le Consortium Centre d'art contemporain": "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Claire Durand-Ruel': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Cabinet du Maire': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Fédération Wallonie-Bruxelles':'Dépôt Fédération Wallonie-Bruxelles',#added by Ruta Binkyte
'Dépôt Musée du Luxembourg': "Dépôt entrant",#added by Ruta Binkyte
"Dépôt Mobilier national d'Alsace-Lorraine": "Dépôt entrant",#added by Ruta Binkyte
"Dépôt Fondation Camille Bryen sous l'égide de la Fondation de France": "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Petit Palais - Musée des Beaux-Arts de la Ville de Paris': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Jean Mairet': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt DENNEY Anthony et Célia': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Maître Guy Loudmer': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Haim Chanin Fine Arts Gallery': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Mme Marie Houzelle': "Dépôt entrant",#added by Ruta Binkyte
"Dépôt Lab'Bel, Fonds Culturel et artistique du Groupe Bel": "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Centre Pompidou, MNAM-CCI': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Kadist Art Foundation': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Bibliothèque municipale Guy de Maupassant': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt GARCIA Dora': "Dépôt entrant",#added by Ruta Binkyte
'Dépôt Noël Le Gall': "Dépôt entrant",#added by Ruta Binkyte
"Don":"Don",
"Donation":"Donation",
"Echange":"Echange",
"Inscription à l'inventaire":"Inscription à l'inventaire",
"Legs":"Legs",
"Mode d'acquisition mixte, voir détail sur les éléments":"Mode d'acquisition mixte",
"Mode d'acquisition non renseigné":"Mode d'acquisition non renseigné",
'Remplacement après sinistre':'Remplacement après sinistre', #added by Ruta Binkyte
"Saisie de l'Administration des Douanes":"Saisie",
"Saisie":"Saisie"}

def acquisition_mode_cleaning(acquisition_mode):
    am = acquisition_mode.strip(' ')
    return acquisition_mode_aggregation[am] if am in acquisition_mode_aggregation else am

#### BIRTH DEATH PLACE AND YEAR
birthdeath_re = re.compile(r"(?: - )?([\w\- ]*) \((?:([\w\- ]*)?, )?([\w\- ]*)\), (\d{4})", flags = re.U)

# parsing artist_birthdeath retur a dictionnary
def artist_birthdeath_parsing(artist_birthdeath):
    birthdeath = birthdeath_re.findall(artist_birthdeath)
    result={}
    birthCity = ''
    birthState = ''
    birthCountry = ''
    birthYear = ''
    deathCity = ''
    deathState = ''
    deathCountry = ''
    deathYear = ''
    if len(birthdeath)>0:
        (birthCity, birthState, birthCountry, birthYear) = birthdeath[0]
    if len(birthdeath)>1:
        (deathCity, deathState, deathCountry, deathYear) = birthdeath[1]
    else:
        birthdeathyears = years_re.findall(artist_birthdeath)
        if len(birthdeathyears)>0:
            birthYear = min(birthdeathyears)
        if len(birthdeathyears)>1:
            deathYear = max(birthdeathyears)
    result["birthCity"]=birthCity
    result["birthState"]=birthState
    result["birthCountry"]=birthCountry
    result["birthYear"]=birthYear
    result["deathCity"]=deathCity
    result["deathState"]=deathState
    result["deathCountry"]=deathCountry
    result["deathYear"]=deathYear
    return(result)


# nationalities
split_nationality_re = re.compile(r"(^[\w'\- ]+?)(?: \(([\w'\- \(\)]+?)(?:, ([\w'\- \(\)]*?))?\))?$", flags = re.U)
nationality_re = re.compile(r"^([\w'\-]+)(?:\w*(?: \(avant (\d{4})\))?( à la naissance)?)?(?: depuis (\d{4}))?$", flags = re.U)
# nationality
# still not done... Should try a less ambitious parsing.
# if "artist_nationalities" in artist and artist["artist_nationalities"]!='':
#     print(artist['artist_nationalities'])
#     if ' et ' in artist['artist_nationalities'] :
#         artist['artist_nationalities'] = artist['artist_nationalities'].split(' et ')
#         artist['artist_nationalities'].reverse()
#         print(artist['artist_nationalities']) 
#         artist['artist_nationalities']="%s (%s)"%tuple(artist['artist_nationalities'])

    
#     nationalities_groups = split_nationality_re.match(artist['artist_nationalities'])
#     if nationalities_groups:
#         nationalities_groups= nationalities_groups.groups()
#         print(nationalities_groups)
#         print([nationality_re.findall(g) for g in nationalities_groups if g])
#     else:
#         print("bug")
#         exit(1)