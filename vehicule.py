# vehicule.py - À COMPLÉTER (épreuve flotte)
#
# Hiérarchie Vehicule / VoitureElectrique / Camion, à transposer de la
# hiérarchie Livre / LivreNumerique / LivreAudio (S11-S18).
# Pour cette épreuve, aucune docstring n'est demandée : les indices «#»
# donnent le RÔLE (et parfois le cas analogue à transposer), et les
# tests (test_vehicule.py) fixent les valeurs et exceptions exactes.
# Complétez les corps « ... ».


class Vehicule:
    # ENTITE largement immuable. Identité métier : le numéro de châssis
    # (qui ne change jamais, contrairement à la plaque). Seule la
    # disponibilité évolue. Transposé de Livre (identité par ISBN).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee):
        # Valider chaque caractéristique avant de la stocker :
        #   - marque, modèle : chaînes non vides ;
        #   - châssis : utiliser la méthode de validation dédiée ;
        #   - nb_places, année : entiers, bornes exactes dans les tests.
        # Distinguer TypeError (mauvais type) et ValueError (mauvaise valeur).
        # À la création, le véhicule est disponible.
        if not isinstance(marque, str) or marque.strip() == "":
            raise ValueError("la chaîne de charactère marque doit être non vide")
        if not isinstance(modele, str) or modele.strip() == "":
            raise ValueError("la chaîne de charactère modèle doit être non vide")
        if not self.chassis_valide(numero_chassis):
            raise ValueError("Numéro de châssis invalide")
        if not isinstance(nb_places, int) or isinstance(nb_places, bool):
            raise TypeError("nb_places doit être un entier")
        if nb_places < 1 or nb_places > 80:
            raise ValueError("nb_places doit être entre 1 et 80")
        if not isinstance(annee, int) or isinstance(annee, bool):
            raise TypeError("annee doit être un entier")
        if annee < 1851: 
            raise ValueError("annee doit être >= 1851")

        self._marque = marque
        self._modele = modele
        self._numero_chassis = numero_chassis
        self._nb_places = nb_places
        self._annee = annee
        self._disponible = True
    # --- Propriétés en lecture seule ---

    @property
    def marque(self):
        return self._marque

    @property
    def modele(self):
        return self._modele

    @property
    def numero_chassis(self):
        return self._numero_chassis

    @property
    def nb_places(self):
        return self._nb_places

    @property
    def annee(self):
        return self._annee

    @property
    def disponible(self):
        return self._disponible

    # --- Méthode statique ---

    @staticmethod
    def chassis_valide(chaine):
        # Vrai si la chaîne a exactement la bonne longueur et n'est faite
        # que de caractères alphanumériques. Longueur et nature exactes :
        # déductibles des tests. Une entrée non-str renvoie False.
        if not isinstance(chaine, str):
            return False
        if len(chaine) != 17:
            return False
        return chaine.isalnum()

    # --- Constructeur alternatif ---

    @classmethod
    def depuis_csv(cls, ligne):
        # Découper la ligne, vérifier le nombre de champs, construire via
        # cls(...). Même rôle que Livre.depuis_chaine_csv : utiliser cls
        # (et non Vehicule) est ce qui donnera le TYPE EXACT dans les
        # sous-classes.
        champs = ligne.split(";")
        if len(champs) != 5:
            raise ValueError("il doit avoir 5 champs")
        marque, modele, chassis, nb_places_str, annee_str = champs
        return cls(marque, modele, chassis, int(nb_places_str), int(annee_str),)

    # --- Sérialisation JSON ---

    def to_dict(self):
        # Produire un dict marqué d'un champ « type » (le discriminateur
        # qui guidera la reconstruction). Clés attendues : voir les tests.
        return {
            "type" : "Vehicule",
            "marque" : self._marque,
            "modele" : self._modele,
            "numero_chassis" : self._numero_chassis,
            "nb_places" : self._nb_places,
            "annee" : self.annee,
            "disponible" : self._disponible
        }

    @classmethod
    def from_dict(cls, donnees):
        # Pendant de to_dict : reconstruire via cls(...), puis restaurer la
        # disponibilité par l'API publique (jamais en écrivant l'attribut
        # privé). Même logique que Livre.from_dict.
        vehicule = cls(donnees["marque"], donnees["modele"],donnees["numero_chassis"],
                    donnees["nb_places"], donnees["annee"])
        cls._restaurer_disponibilite(vehicule, donnees)
        return vehicule
    @staticmethod
    def _restaurer_disponibilite(vehicule, donnees):
        # Si l'objet était loué, le replacer dans cet état via la méthode
        # métier. Factorisé : toutes les sous-classes restaurent pareil.
        if not donnees.get("disponible", True):
            vehicule._disponible = False

    # --- Méthodes métier ---

    def louer(self):
        # Bascule vers « loué » ; refuser si déjà loué.
        if not self._disponible:
            raise ValueError("Vehicule déjà loué")
        self._disponible = False

    def restituer(self):
        # Bascule vers « disponible » ; refuser si déjà disponible.
        if self._disponible:
            raise ValueError("Vehicule déjà dusponible")
        self._disponible = True

    def fiche_resume(self):
        # Description de la capacité d'un véhicule générique. Format exact :
        # voir les tests. (Transposé de Livre.taille_estimee.)
        return f"{self._nb_places} places"

    # --- Représentations ---

    def __str__(self):
        if self._disponible:
            etat = "disponible"
        else:
            etat = "loué"
        return f"{self._marque} {self._modele} ({etat})"


    def __repr__(self):
        return f"Vehicule({self._marque!r}, {self._modele!r}, {self._numero_chassis!r},{self._nb_places!r}, {self._annee!r})"

    # --- Identité (entité) ---

    def __eq__(self, autre):
        # Vehicule est une ENTITE : égalité par numéro de châssis (comme
        # Livre par ISBN). NotImplemented si « autre » n'est pas un Vehicule.
        if not isinstance(autre, Vehicule):
            return NotImplemented
        return self._numero_chassis == autre._numero_chassis

    def __hash__(self):
        # Cohérent avec __eq__ : fondé sur le châssis.
        return hash(self._numero_chassis)


class VoitureElectrique(Vehicule):
    # Enrichit Vehicule d'une autonomie. Transposé de LivreNumerique.

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                autonomie_km):
        # Déléguer la validation héritée au parent, puis valider l'attribut
        # propre (autonomie : entier strictement positif).
        super().__init__(marque,modele, numero_chassis, nb_places, annee)
        if not isinstance(autonomie_km, int) or isinstance(autonomie_km, bool):
            raise TypeError("autonomie_km doit être un entier")
        if autonomie_km <= 0:
            raise ValueError("autonomie_km doit être strictement positif")
        self._autonomie_km = autonomie_km
    @property
    def autonomie_km(self):
        return self._autonomie_km

    @classmethod
    def depuis_csv(cls, ligne):
        # Comme Vehicule.depuis_csv, mais un champ de plus (l'autonomie).
        champs = ligne.split(";")
        if len(champs) != 6: 
            raise ValueError("il doit avoir 6 champs")
        marque, modele, chassis, nb_places_str, annee_str, autonomie_str = champs
        return cls(marque, modele, chassis, int(nb_places_str), int(annee_str), int(autonomie_str))
    def to_dict(self):
        # ENRICHIR le dictionnaire hérité du parent (ne pas le réécrire) :
        # corriger « type » et ajouter l'attribut propre. (Geste de
        # LivreNumerique.to_dict.)
        dic = super().to_dict()
        dic["type"] = "VoitureElectrique"
        dic["autonomie_km"] = self.autonomie_km
        return dic

    @classmethod
    def from_dict(cls, donnees):
        vehicule = cls(donnees["marque"], donnees["modele"], donnees["numero_chassis"], donnees["nb_places"],
                    donnees["annee"], donnees["autonomie_km"],)
        cls._restaurer_disponibilite(vehicule, donnees)
        return vehicule

    def fiche_resume(self):
        # On REPREND la fiche de base et on la complète : la capacité reste
        # un préfixe (ENRICHISSEMENT). Format exact : voir les tests.
        capacite = super().fiche_resume()
        return f"{capacite} [électrique, {self._autonomie_km} km]"

    def __str__(self):
        if self._disponible:
            etat = "disponible"
        else:
            etat = "loué" 
        return f"{self._marque} {self._modele} (électrique, {etat})"

    def __repr__(self):
        return f"VoitureElectrique({self._marque!r}, {self._modele!r}, {self._numero_chassis!r},{self._nb_places!r}, {self._annee!r}, {self._autonomie_km!r})"


class Camion(Vehicule):
    # La mesure pertinente est la charge utile, pas le nombre de places.
    # Transposé de LivreAudio (durée d'écoute plutôt que pages).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                charge_utile_t):
        # Déléguer au parent, puis valider l'attribut propre (charge :
        # nombre strictement positif, stocké en float).
        super().__init__(marque, modele, numero_chassis, nb_places, annee)
        if not isinstance(charge_utile_t, (int, float)) or isinstance(charge_utile_t, bool):
            raise TypeError("charge_utilie_t doit être un nombre")
        if charge_utile_t <= 0:
            raise ValueError("charge_utile_t doit être strictement positif")
        self._charge_utile_t = float(charge_utile_t)

    @property
    def charge_utile_t(self):
        return self._charge_utile_t

    @classmethod
    def depuis_csv(cls, ligne):
        champs = ligne.split(";")
        if len(champs) != 6:
            raise ValueError(f"il doit avoir 6 champs")
        marque, modele, chassis, nb_places_str, annee_str, charge_str = champs
        return cls( marque, modele, chassis, int(nb_places_str), int(annee_str), float(charge_str))
    def to_dict(self):
        dic = super().to_dict()
        dic["type"] = "Camion"
        dic["charge_utile_t"] = self._charge_utile_t
        return dic

    @classmethod
    def from_dict(cls, donnees):
        vehicule = cls(donnees["marque"], donnees["modele"], donnees["numero_chassis"], donnees["nb_places"],
                    donnees["annee"], donnees["charge_utile_t"],)
        cls._restaurer_disponibilite(vehicule, donnees)
        return vehicule

    def fiche_resume(self):
        # Ici la mesure pertinente n'est PAS le nombre de places : on ne
        # réutilise donc PAS la fiche de base (REMPLACEMENT). Format exact :
        # voir les tests.
        return f"{self._charge_utile_t} t de charge"

    def __str__(self):
        if self._disponible:
            etat = "disponible"
        else:
            etat = "loué"
        return f"{self._marque} {self._modele} (camion, {etat})"

    def __repr__(self):
        return f"Camion({self._marque!r}, {self._modele!r}, {self._numero_chassis!r},{self._nb_places!r}, {self._annee!r}, {self._charge_utile_t!r})"

