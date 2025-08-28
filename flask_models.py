from datetime import datetime, timedelta
import uuid
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# This will be initialized in the app factory
db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

# User Model for Authentication
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'fullName': self.full_name,
            'email': self.email,
            'isActive': self.is_active,
            'lastLogin': self.last_login.isoformat() if self.last_login else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Session Model for Token Management
class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='sessions')
    
    @staticmethod
    def create_session(user_id):
        # 24-hour session duration
        expires_at = datetime.utcnow() + timedelta(hours=24)
        session_token = str(uuid.uuid4())
        
        session = UserSession(
            user_id=user_id,
            session_token=session_token,
            expires_at=expires_at
        )
        return session
    
    def is_valid(self):
        return datetime.utcnow() < self.expires_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'sessionToken': self.session_token,
            'expiresAt': self.expires_at.isoformat() if self.expires_at else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

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
    numero_demande = db.Column(db.String(50), unique=True)
    date_demande = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    requestor_id = db.Column(db.String(36), nullable=False)
    observations = db.Column(db.Text)
    statut = db.Column(db.Text, nullable=False, default='en_attente')  # en_attente, approuve, refuse, commande, recu
    total_articles = db.Column(db.Integer, nullable=False, default=0)
    total_estime = db.Column(db.Numeric(10, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'numeroDemande': self.numero_demande,
            'dateDemande': self.date_demande.isoformat() if self.date_demande else None,
            'requestorId': self.requestor_id,
            'observations': self.observations,
            'statut': self.statut,
            'totalArticles': self.total_articles,
            'totalEstime': float(self.total_estime) if self.total_estime else 0,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Purchase Request Items
class PurchaseRequestItem(db.Model):
    __tablename__ = 'purchase_request_items'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    purchase_request_id = db.Column(db.String(36), db.ForeignKey('purchase_requests.id'), nullable=False)
    article_id = db.Column(db.String(36), db.ForeignKey('articles.id'), nullable=False)
    supplier_id = db.Column(db.String(36), db.ForeignKey('suppliers.id'))
    quantite_demandee = db.Column(db.Integer, nullable=False)
    prix_unitaire_estime = db.Column(db.Numeric(10, 2))
    sous_total = db.Column(db.Numeric(10, 2))
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    purchase_request = db.relationship('PurchaseRequest', backref='items')
    article = db.relationship('Article')
    supplier = db.relationship('Supplier')
    
    def to_dict(self):
        return {
            'id': self.id,
            'purchaseRequestId': self.purchase_request_id,
            'articleId': self.article_id,
            'quantiteDemandee': self.quantite_demandee,
            'supplierId': self.supplier_id,
            'prixUnitaireEstime': float(self.prix_unitaire_estime) if self.prix_unitaire_estime else None,
            'sousTotal': float(self.sous_total) if self.sous_total else 0,
            'observations': self.observations,
            'article': self.article.to_dict() if self.article else None,
            'supplier': self.supplier.to_dict() if self.supplier else None,
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
    numero_sortie = db.Column(db.String(50), nullable=False)  # Transaction number for grouping
    date_sortie = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    requestor_id = db.Column(db.String(36), nullable=True)
    article_id = db.Column(db.String(36), nullable=False)
    quantite_sortie = db.Column(db.Integer, nullable=False)
    motif_sortie = db.Column(db.Text, nullable=False)
    observations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'numeroSortie': self.numero_sortie,
            'dateSortie': self.date_sortie.isoformat() if self.date_sortie else None,
            'requestorId': self.requestor_id,
            'articleId': self.article_id,
            'quantiteSortie': self.quantite_sortie,
            'motifSortie': self.motif_sortie,
            'observations': self.observations,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }

# Activity Log Model
class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), nullable=True, default='system')  # For now, using 'system' as default
    action = db.Column(db.String(50), nullable=False)  # CREATE, UPDATE, DELETE, EXPORT, IMPORT, etc.
    entity_type = db.Column(db.String(50), nullable=False)  # suppliers, requestors, articles, etc.
    entity_id = db.Column(db.String(36), nullable=True)  # ID of affected record
    entity_name = db.Column(db.Text, nullable=True)  # Human readable name/identifier
    old_values = db.Column(db.Text, nullable=True)  # JSON string of old values
    new_values = db.Column(db.Text, nullable=True)  # JSON string of new values  
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'action': self.action,
            'entityType': self.entity_type,
            'entityId': self.entity_id,
            'entityName': self.entity_name,
            'oldValues': self.old_values,
            'newValues': self.new_values,
            'ipAddress': self.ip_address,
            'userAgent': self.user_agent,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_description(self):
        """Generate human-readable description of the activity"""
        action_descriptions = {
            'CREATE': 'Ajout',
            'UPDATE': 'Modification', 
            'DELETE': 'Suppression',
            'EXPORT': 'Export',
            'IMPORT': 'Import'
        }
        
        entity_descriptions = {
            'suppliers': 'fournisseur',
            'requestors': 'demandeur',
            'articles': 'article',
            'purchase_requests': 'demande d\'achat',
            'receptions': 'réception',
            'outbounds': 'sortie'
        }
        
        action_desc = action_descriptions.get(self.action, self.action)
        entity_desc = entity_descriptions.get(self.entity_type, self.entity_type)
        
        if self.entity_name:
            return f"{action_desc} {entity_desc}: {self.entity_name}"
        else:
            return f"{action_desc} {entity_desc}"