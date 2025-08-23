from datetime import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy

# This will be initialized in the app factory
db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

# Articles (Spare Parts)
class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    code_article = db.Column(db.Text, nullable=False, unique=True)
    designation = db.Column(db.Text, nullable=False)
    categorie = db.Column(db.Text, nullable=False)
    marque = db.Column(db.Text)
    reference = db.Column(db.Text)
    stock_initial = db.Column(db.Integer, nullable=False, default=0)
    stock_actuel = db.Column(db.Integer, nullable=False, default=0)
    unite = db.Column(db.Text, nullable=False, default='pcs')
    prix_unitaire = db.Column(db.Numeric(10, 2))
    seuil_minimum = db.Column(db.Integer, default=10)
    fournisseur_id = db.Column(db.String(36))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'codeArticle': self.code_article,
            'designation': self.designation,
            'categorie': self.categorie,
            'marque': self.marque,
            'reference': self.reference,
            'stockInitial': self.stock_initial,
            'stockActuel': self.stock_actuel,
            'unite': self.unite,
            'prixUnitaire': float(self.prix_unitaire) if self.prix_unitaire else None,
            'seuilMinimum': self.seuil_minimum,
            'fournisseurId': self.fournisseur_id,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Suppliers
class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    nom = db.Column(db.Text, nullable=False)
    contact = db.Column(db.Text)
    telephone = db.Column(db.Text)
    email = db.Column(db.Text)
    adresse = db.Column(db.Text)
    conditions_paiement = db.Column(db.Text)
    delai_livraison = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'contact': self.contact,
            'telephone': self.telephone,
            'email': self.email,
            'adresse': self.adresse,
            'conditionsPaiement': self.conditions_paiement,
            'delaiLivraison': self.delai_livraison,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Requestors
class Requestor(db.Model):
    __tablename__ = 'requestors'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    nom = db.Column(db.Text, nullable=False)
    prenom = db.Column(db.Text, nullable=False)
    departement = db.Column(db.Text, nullable=False)
    poste = db.Column(db.Text)
    email = db.Column(db.Text)
    telephone = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'departement': self.departement,
            'poste': self.poste,
            'email': self.email,
            'telephone': self.telephone,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Purchase Requests (Header)
class PurchaseRequest(db.Model):
    __tablename__ = 'purchase_requests'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    date_demande = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    requestor_id = db.Column(db.String(36), nullable=False)
    date_initiation = db.Column(db.DateTime, default=datetime.utcnow)
    observations = db.Column(db.Text)
    statut = db.Column(db.Text, nullable=False, default='en_attente')
    total_articles = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'dateDemande': self.date_demande.isoformat() if self.date_demande else None,
            'requestorId': self.requestor_id,
            'dateInitiation': self.date_initiation.isoformat() if self.date_initiation else None,
            'observations': self.observations,
            'statut': self.statut,
            'totalArticles': self.total_articles,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Purchase Request Items
class PurchaseRequestItem(db.Model):
    __tablename__ = 'purchase_request_items'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    purchase_request_id = db.Column(db.String(36), nullable=False)
    article_id = db.Column(db.String(36), nullable=False)
    quantite_demandee = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.String(36))
    prix_unitaire_estime = db.Column(db.Numeric(10, 2))
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'purchaseRequestId': self.purchase_request_id,
            'articleId': self.article_id,
            'quantiteDemandee': self.quantite_demandee,
            'supplierId': self.supplier_id,
            'prixUnitaireEstime': float(self.prix_unitaire_estime) if self.prix_unitaire_estime else None,
            'observations': self.observations,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Goods Reception
class Reception(db.Model):
    __tablename__ = 'receptions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    date_reception = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    supplier_id = db.Column(db.String(36), nullable=False)
    article_id = db.Column(db.String(36), nullable=False)
    quantite_recue = db.Column(db.Integer, nullable=False)
    prix_unitaire = db.Column(db.Numeric(10, 2))
    numero_bon_livraison = db.Column(db.Text)
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'dateReception': self.date_reception.isoformat() if self.date_reception else None,
            'supplierId': self.supplier_id,
            'articleId': self.article_id,
            'quantiteRecue': self.quantite_recue,
            'prixUnitaire': float(self.prix_unitaire) if self.prix_unitaire else None,
            'numeroBonLivraison': self.numero_bon_livraison,
            'observations': self.observations,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Stock Outbound
class Outbound(db.Model):
    __tablename__ = 'outbounds'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    date_sortie = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    requestor_id = db.Column(db.String(36), nullable=False)
    article_id = db.Column(db.String(36), nullable=False)
    quantite_sortie = db.Column(db.Integer, nullable=False)
    motif_sortie = db.Column(db.Text, nullable=False)
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'dateSortie': self.date_sortie.isoformat() if self.date_sortie else None,
            'requestorId': self.requestor_id,
            'articleId': self.article_id,
            'quantiteSortie': self.quantite_sortie,
            'motifSortie': self.motif_sortie,
            'observations': self.observations,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }