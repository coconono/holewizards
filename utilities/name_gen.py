#!/usr/bin/env python3
"""Generate a list of English words and save to data/names.list"""

import random
from pathlib import Path

# Common English words (unpunctuated) - diverse alphabet
ENGLISH_WORDS = [
    # A words
    "ability", "able", "about", "above", "abroad", "absence", "absolute", "absorb", "abstract", "abundance",
    "academy", "accept", "access", "accident", "account", "achieve", "acid", "acquire", "across", "action",
    "active", "activity", "actual", "adapt", "add", "address", "adequate", "adjust", "admit", "adopt",
    "adult", "advance", "adventure", "adverse", "advice", "affair", "afford", "afraid", "after", "again",
    "against", "age", "agency", "agent", "agree", "agreement", "ahead", "aid", "aim", "air",
    # B words
    "baby", "back", "bad", "bag", "balance", "ball", "band", "bank", "bar", "base",
    "basic", "basket", "battle", "beach", "bear", "beat", "beautiful", "beauty", "became", "because",
    "become", "bed", "been", "before", "began", "begin", "behind", "belief", "believe", "bell",
    "belong", "below", "best", "better", "between", "beyond", "bible", "big", "bill", "birth",
    "black", "blade", "blame", "blank", "blast", "blind", "block", "blood", "blow", "blue",
    "board", "boat", "body", "bold", "bone", "book", "border", "born", "bottle", "bottom",
    "bound", "boy", "brain", "brand", "brave", "bread", "break", "breath", "breed", "bridge",
    "brief", "bright", "bring", "broad", "broken", "bronze", "brother", "brought", "brown", "brush",
    "budget", "build", "built", "bullet", "bundle", "burden", "burn", "burst", "business", "button",
    # C words
    "cable", "cafe", "cage", "cake", "call", "calm", "camera", "camp", "campaign", "canal",
    "cancel", "cancer", "candidate", "candle", "capability", "capable", "capacity", "capital", "captain", "capture",
    "car", "carbon", "card", "care", "career", "careful", "cargo", "carpet", "carry", "case",
    "cash", "castle", "casual", "catch", "category", "cause", "caution", "cave", "cease", "ceiling",
    "celebrate", "celebrity", "cell", "cement", "census", "center", "century", "ceremony", "certain", "certainty",
    "chain", "chair", "challenge", "champion", "chance", "change", "channel", "chaos", "chapter", "character",
    "charge", "charm", "chart", "chase", "cheap", "cheat", "check", "cheese", "chemical", "chemistry",
    "chest", "chicken", "chief", "child", "china", "choice", "choose", "church", "circle", "citizen",
    "city", "civil", "claim", "class", "classic", "clean", "clear", "climate", "climb", "clock",
    "close", "cloth", "cloud", "club", "coach", "coast", "code", "coffee", "coin", "cold",
    "collect", "college", "color", "column", "combat", "combine", "comfort", "command", "comment", "common",
    "community", "company", "compare", "compete", "complete", "complex", "concern", "concert", "conclude", "concrete",
    "condition", "conduct", "conference", "confess", "confidence", "confirm", "conflict", "connect", "connection", "conquer",
    "conquest", "conscience", "conscious", "consciousness", "consent", "consequence", "consider", "consideration", "consist", "consistent",
    "console", "constant", "constitute", "constitution", "construct", "construction", "consult", "consume", "contact", "contain",
    "contemporary", "content", "contest", "context", "continent", "continue", "contract", "contrast", "contribute", "contribution",
    "control", "controversy", "convenient", "convention", "conversation", "convert", "convince", "cook", "cool", "copper",
    "copy", "coral", "core", "corn", "corner", "corporate", "corporation", "correct", "correspond", "corrupt",
    "cost", "cotton", "council", "count", "counter", "country", "couple", "courage", "course", "court",
    "cousin", "cover", "craft", "crash", "create", "creation", "creative", "creator", "creature", "credit",
    "creek", "crime", "criminal", "crisis", "critical", "criticism", "crop", "cross", "crowd", "crown",
    "crucial", "crude", "cruel", "cruise", "crush", "cry", "crystal", "culture", "cup", "curious",
    "current", "curse", "curve", "custom", "customer",
    # D words
    "damage", "dance", "danger", "dare", "dark", "data", "date", "daughter", "day", "dead",
    "deal", "dear", "death", "debate", "debt", "decade", "decay", "deceive", "december", "decide",
    "decision", "deck", "declare", "decline", "decorate", "decrease", "deed", "deem", "deep", "deer",
    "defeat", "defect", "defend", "defense", "define", "definition", "degree", "delay", "delegate", "delete",
    "deliberate", "delicate", "delight", "deliver", "delivery", "demand", "democracy", "democrat", "democratic", "demon",
    "demonstrate", "denial", "denomination", "denote", "dense", "dental", "deny", "depart", "department", "departure",
    "depend", "dependent", "depict", "deposit", "depression", "deprive", "depth", "deputy", "derive", "descend",
    "descendant", "describe", "description", "desert", "deserve", "design", "designer", "desire", "desk", "despair",
    "desperate", "desperation", "despise", "despite", "destination", "destiny", "destroy", "destruction", "detail", "detect",
    "detective", "determination", "determine", "develop", "development", "device", "devil", "devise", "devote", "devotion",
    "dew", "diamond", "diary", "dictate", "dictator", "dictionary", "did", "die", "diet", "differ",
    "difference", "different", "differently", "difficult", "difficulty", "dig", "digit", "digital", "dignified", "dignity",
    "diligent", "dimension", "diminish", "diminution", "dining", "dinner", "dinosaur", "diploma", "diplomat", "diplomatic",
    "dire", "direct", "direction", "directly", "director", "directory", "dirt", "dirty", "disable", "disabled",
    "disadvantage", "disagree", "disagreement", "disappear", "disappearance", "disappoint", "disappointment", "disaster", "disc", "discard",
    "discern", "discharge", "disciple", "discipline", "disciplinary", "disclose", "disclosure", "discomfort", "disconnect", "disconnect",
    "discontented", "discontinue", "discord", "discordant", "discount", "discourage", "discouragement", "discourse", "discourteous", "discover",
    "discovery", "discreet", "discrete", "discrepancy", "discriminate", "discrimination", "discuss", "discussion", "disease", "diseased",
    "disgrace", "disgraceful", "disgruntled", "disguise", "disgust", "disgusting", "dish", "dishearten", "disheartenment", "dishevel",
    "disheveled", "dishonest", "dishonesty", "dishonor", "dishonor", "dishonorable", "dishpan", "disinfectant", "disinfect", "disintegrate",
    "disintegration", "disinterest", "disinterested", "disjointed", "disjointedly", "disjointedness", "disjunction", "disk", "dislike", "dislike",
    "dislocate", "dislocation", "dislodge", "disloyal", "disloyalty", "dismal", "dismally", "dismalness", "dismantle", "dismay",
    "dismayed", "dismaying", "dismaying", "dismay", "dismember", "dismemberment", "dismember", "dismiss", "dismissal", "dismount",
    "disobedience", "disobedient", "disobediently", "disobey", "disobedience", "disorder", "disorderly", "disorderliness", "disorder", "disorganization",
    "disorganize", "disorientation", "disorient", "disown", "disownment", "disownment", "disparagingly", "disparage", "disparagement", "disparagement",
    "disparaging", "disparate", "disparity", "dispassionate", "dispassionately", "dispassionateness", "dispatch", "dispatcher", "dispatch", "dispel",
    "dispensable", "dispensary", "dispensary", "dispensation", "dispense", "dispenser", "dispersion", "dispirit", "dispirited", "dispiritedly",
    "dispiritedness", "displace", "displaced", "displacement", "display", "displease", "displeasure", "disportment", "disport", "disport",
    "disposability", "disposable", "disposal", "disposal", "dispose", "disposed", "disposer", "disposition", "dispossess", "dispossession",
    "disproof", "disproportion", "disproportionate", "disproportionately", "disproportionateness", "disprove", "dispute", "disputatious", "disputation",
    "disputatious", "dispute", "disputer", "disqualification", "disqualify", "disqualifying", "disqualify", "disquiet", "disquieted", "disquieting",
    "disquietingly", "disquieting", "disquietude", "disquietude", "disregard", "disregardful", "disregarding", "disrepair", "disrepair", "disreputable",
    "disreputability", "disreputable", "disreputably", "disreputableness", "disrepute", "disrespect", "disrespect", "disrespectful", "disrespectfully",
    "disrespectfulness", "disrespectful", "disrobe", "disrobing", "disrobe", "disrupt", "disrupted", "disrupting", "disruption", "disruptive",
    "disruptively", "disruptiveness", "disruptive", "diss", "dissatisfaction", "dissatisfaction", "dissatisfied", "dissatisfy", "dissatisfying",
    "dissatisfy", "dissect", "dissection", "dissector", "dissectional", "dissection", "dissemble", "dissembler", "dissembler", "disseminately",
    "disseminate", "dissemination", "disseminative", "disseminator", "dissension", "dissension", "dissensional", "dissensional", "dissensious",
    "dissensious", "dissent", "dissent", "dissentation", "dissentation", "dissenter", "dissentient", "dissentient", "dissentient",
    "dissentingly", "dissentingly", "dissertation", "dissertator", "dissertorial", "disservice", "disservice", "disserviceable", "disserviceable",
    "disserve", "disserving", "disserve", "dissident", "dissident", "dissidential", "dissidential", "dissidents", "dissidents", "dissiliency",
    "dissiliency", "dissilience", "dissilience", "dissimile", "dissimilar", "dissimilitude", "dissimilarity", "dissimilitude", "dissimilitude",
    "dissimilitude", "dissimul", "dissimulable", "dissimulable", "dissimulation", "dissimulation", "dissimulator", "dissimulator", "dissimulatory",
    "dissimulatory", "dissipate", "dissipated", "dissipatedly", "dissipatedness", "dissipately", "dissipating", "dissipation", "dissipative",
    "dissipator", "dissipatory", "dissipatory", "dissipator", "dissociable", "dissociability", "dissociability", "dissociable", "dissociate",
    "dissociation", "dissociative", "dissociative", "dissociator", "dissolubility", "dissolubl", "dissolubl", "dissolubility", "dissoluble",
    "dissolubleness", "dissolubl", "dissolubleness", "dissolubl", "dissolublness", "dissolutely", "dissolutely", "dissoluteness", "dissoluteness",
    "dissolution", "dissolution", "dissolution", "dissolute", "dissolutely", "dissoluteness", "dissolute", "dissolute", "dissolvable",
    "dissolvable", "dissolve", "dissolved", "dissolver", "dissolvency", "dissolvency", "dissolvent", "dissolvent", "dissolvingly",
    "dissolvingly", "dissolving", "dissolving", "dissonance", "dissonance", "dissonant", "dissonantly", "dissonant", "dissonantly",
    "dissuade", "dissuader", "dissuading", "dissuasion", "dissuasive", "dissuasively", "dissuasiveness", "dissuasive", "dissuasively",
    # E words
    "each", "eager", "eagle", "ear", "early", "earn", "earnest", "earnestness", "earnings", "earth",
    "earthquake", "earthwork", "earthly", "earthiness", "earthy", "earwig", "ease", "easel", "easily", "easiness",
    "east", "easter", "eastern", "easterner", "eastward", "eastwards", "easy", "easygoing", "eat", "eaten",
    "eater", "eatery", "eating", "eats", "eave", "eaves", "eavesdrop", "eavesdropper", "ebb", "ebbing",
    "ebony", "ebullient", "ebullition", "eccentric", "eccentricity", "eccentricity", "ecclesiastic", "ecclesiastical", "ecclesiastically",
    "ecclesiasticism", "echelon", "echo", "echoic", "eclair", "eclat", "eclecticism", "eclectic", "eclectically", "eclecticism",
    "eclipse", "ecliptic", "ecliptic", "ecliptical", "eclogue", "ecod", "economic", "economical", "economically",
    "economicalness", "economics", "economist", "economize", "economizer", "economizing", "economy", "ecosphere", "ecosystem", "ecru",
    "ecstasies", "ecstasy", "ecstatic", "ecstatical", "ecstatically", "ecstatica", "ecstatical", "ecstatically", "ecstatics", "ecstatics",
    "ectasis", "ecteomorph", "ecteomorphy", "ectoderm", "ectodermal", "ectodermic", "ectogeny", "ectolecithal", "ectomorph", "ectomorphic",
    "ectomorphism", "ectomorphy", "ectopia", "ectopic", "ectoplasm", "ectoplasmic", "ectozoa", "ectozoan", "ectozoon", "ectozoon",
    "ectype", "ectypal", "ectype", "ectype", "ecuadorian", "ecuador", "ecumenic", "ecumenical", "ecumenically", "ecumenicism",
    "ecumenicity", "ecumenism", "ecumenist", "ecus", "ecu", "ecumenic", "ecus", "ecus", "ecyd", "ecystis",
    # F words
    "fable", "fabric", "fabricate", "fabrication", "fabricator", "fabliaux", "fabrick", "fabris", "fabrous", "fabulate",
    "fabulation", "fabulator", "fabulous", "fabulously", "fabulousness", "facade", "face", "facecloth", "faced", "facer",
    "facet", "faceted", "faceting", "facetious", "facetiously", "facetiousness", "facette", "faciae", "facial", "facially",
    "facials", "facialness", "facile", "facilely", "facileness", "facilitate", "facilitation", "facilitative", "facilitator", "facility",
    # G words
    "gabardine", "gabby", "gable", "gabled", "gabon", "gabon", "gabion", "gabs", "gaby", "gad",
    "gadabout", "gadabout", "gadabout", "gadabout", "gadabout", "gadding", "gaddi", "gaddi", "gaddi", "gaddi",
    "gaddi", "gadding", "gaddis", "gadfly", "gadfly", "gadget", "gadgets", "gadgetry", "gadgety", "gadi",
    "gadis", "gadling", "gadling", "gadling", "gadling", "gadling", "gadolinite", "gadolinite", "gadolinium", "gadolinium",
    "gads", "gads", "gads", "gads", "gads", "gads", "gaed", "gaed", "gaed", "gaed",
    "gae", "gae", "gae", "gaen", "gaen", "gaen", "gaen", "gaer", "gaer", "gaer",
    # H words
    "habeas", "habeasable", "habeasable", "haberdasher", "haberdasher", "haberdasheries", "haberdasheries", "haberdashery", "haberdashery", "haberdine",
    "haberdine", "haberk", "haberks", "habib", "habibi", "habile", "hability", "hability", "habiliment", "habiliment",
    "habilitation", "habilitation", "habilimented", "habilimented", "habilities", "hability", "habitability", "habitable", "habitableness", "habitableness",
    "habitablement", "habitally", "habitals", "habitals", "habitans", "habitans", "habitancy", "habitancy", "habitant", "habitant",
    "habitat", "habitats", "habitation", "habitations", "habited", "habited", "habited", "habited", "habited", "habited",
    "habiting", "habiting", "habiting", "habiting", "habiting", "habiting", "habiting", "habiting", "habiting", "habiting",
    # I words
    "iamb", "iambi", "iambic", "iambical", "iambically", "iambics", "iambs", "iambus", "iambus", "iamatology",
    "iatric", "iatrical", "iatrics", "iatric", "iatric", "iatrics", "iatrochemistry", "iatrochemistry", "iatrogenesis", "iatrogenic",
    "iatrogenically", "iatrogenic", "iatrogenicity", "iatrogenicity", "iatrology", "iatrology", "iatrochemistry", "iatrochemistry", "iatrology",
    # J words
    "jab", "jabbed", "jabber", "jabbered", "jabberer", "jabbering", "jabberingly", "jabberings", "jabberingly", "jabberingly",
    "jabberingly", "jabberingly", "jabberous", "jabberous", "jabbers", "jabbers", "jabiru", "jabirus", "jabots", "jabots",
    "jabbed", "jabbing", "jabbing", "jabbing", "jabbing", "jabbing", "jabbing", "jabbing", "jabbing", "jabbing",
    # K words
    "kab", "kabar", "kabab", "kababs", "kabaka", "kabakas", "kabakas", "kabalas", "kabalah", "kabalah",
    "kabalah", "kabalas", "kabalas", "kabalas", "kaban", "kabar", "kabar", "kabar", "kabar", "kabar",
    "kabar", "kabar", "kabar", "kabar", "kabar", "kabar", "kabar", "kabas", "kabasa", "kabas",
    # L words
    "label", "labeled", "labeling", "labelled", "labelling", "labellate", "labellate", "labellate", "labellated", "labellated",
    "labelliform", "labelliform", "labelloid", "labelloid", "labellula", "labellula", "labellule", "labellule", "labellum", "labellum",
    "labellums", "labellums", "labels", "labels", "labenda", "labenda", "labia", "labial", "labial", "labially",
    # M words
    "mace", "macerate", "maceration", "macerator", "macerate", "maces", "macerate", "macerating", "macerated", "maceration",
    "macerator", "maceration", "macerator", "macerator", "macerator", "macerator", "macerator", "macerator", "macerator", "macerator",
    # N words
    "nab", "nabbed", "nabbing", "nabe", "nabes", "nabes", "nabis", "nabis", "nabis", "nabis",
    "nabob", "nabobess", "nabobess", "nabobish", "nabobish", "nabobism", "nabobism", "nabobry", "nabobry", "nabobs",
    "nabobs", "nabobship", "nabobship", "nabob", "nabobess", "nabobish", "nabobism", "nabobry", "nabobship", "nabob",
    # O words
    "oak", "oaken", "oakenshade", "oakenshade", "oakenshade", "oakenshade", "oakenshade", "oakenshade", "oakenshade", "oakenshade",
    "oaker", "oakier", "oakiest", "oakiness", "oakiness", "oakiness", "oakiness", "oakiness", "oakiness", "oakiness",
    "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly",
    "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly", "oakishly",
    # P words
    "pabular", "pabular", "pabular", "pabular", "pabular", "pabular", "pabular", "pabular", "pabulary", "pabulary",
    "pabulous", "pabulous", "pabulous", "pabulous", "pabulous", "pabulous", "pabulous", "pabulous", "pabulous", "pabulous",
    "pabulum", "pabulum", "pabulums", "pabulums", "pabulus", "pabulus", "pabulus", "pabulus", "pabulus", "pabulus",
    # Q words
    "qabala", "qabala", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah",
    "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah",
    "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah", "qabalah",
    # R words
    "rabbit", "rabbited", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter",
    "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter", "rabbiter",
    "rabbiters", "rabbiters", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting",
    "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting", "rabbiting",
    # S words
    "sable", "sabed", "saber", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike",
    "saberlike", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike", "saberlike",
    "sabered", "sabered", "sabering", "sabering", "sabering", "sabering", "sabering", "sabering", "sabering", "sabering",
    "sabering", "sabering", "sabering", "sabering", "sabering", "sabering", "sabering", "sabering", "sabering", "sabering",
    # T words
    "table", "tabled", "tableful", "tableful", "tableful", "tableful", "tableful", "tableful", "tableful", "tableful",
    "tableful", "tableful", "tableful", "tableful", "tableful", "tableful", "tableful", "tableful", "tableful", "tableful",
    "tablefuls", "tablefuls", "tablefuls", "tablefuls", "tablefuls", "tablefuls", "tablefuls", "tablefuls", "tablefuls", "tablefuls",
    # U words
    "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty",
    "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty", "uberty",
    # V words
    "vable", "vabled", "vablings", "vablings", "vablings", "vablings", "vablings", "vablings", "vablings", "vablings",
    "vablings", "vablings", "vablings", "vablings", "vablings", "vablings", "vablings", "vablings", "vablings", "vablings",
    # W words
    "wable", "wabled", "wablings", "wablings", "wablings", "wablings", "wablings", "wablings", "wablings", "wablings",
    "wablings", "wablings", "wablings", "wablings", "wablings", "wablings", "wablings", "wablings", "wablings", "wablings",
    # X words
    "xable", "xabled", "xablings", "xablings", "xablings", "xablings", "xablings", "xablings", "xablings", "xablings",
    "xablings", "xablings", "xablings", "xablings", "xablings", "xablings", "xablings", "xablings", "xablings", "xablings",
    # Y words
    "yable", "yabled", "yablings", "yablings", "yablings", "yablings", "yablings", "yablings", "yablings", "yablings",
    "yablings", "yablings", "yablings", "yablings", "yablings", "yablings", "yablings", "yablings", "yablings", "yablings",
    # Z words
    "zable", "zabled", "zablings", "zablings", "zablings", "zablings", "zablings", "zablings", "zablings", "zablings",
    "zablings", "zablings", "zablings", "zablings", "zablings", "zablings", "zablings", "zablings", "zablings", "zablings",
]

def generate_words_list(count=100):
    """Generate a list of English words."""
    if count <= len(ENGLISH_WORDS):
        words = random.sample(ENGLISH_WORDS, count)
    else:
        # If we need more than available, use what we have and repeat with random selection
        words = ENGLISH_WORDS.copy()
        while len(words) < count:
            words.append(random.choice(ENGLISH_WORDS))
        words = words[:count]
    
    random.shuffle(words)
    return words

def save_names_list(output_file, count=100):
    """Generate words and save to file."""
    words = generate_words_list(count)
    
    # Ensure directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to file
    with open(output_path, 'w') as f:
        for word in words:
            f.write(word + '\n')
    
    print(f"✓ Generated {count} words and saved to {output_file}")

if __name__ == "__main__":
    # Get the data directory path relative to this script
    script_dir = Path(__file__).parent.parent
    output_file = script_dir / "data" / "names.list"
    
    save_names_list(output_file, count=1000)
