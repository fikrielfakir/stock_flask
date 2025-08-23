from flask import jsonify, request
from datetime import datetime
import uuid
from sqlalchemy import or_, func, desc

def register_routes(app, db):
    from flask_models import Article, Supplier, Requestor, PurchaseRequest, PurchaseRequestItem, Reception, Outbound
    
    # Articles routes
    @app.route("/api/articles", methods=['GET'])
    def get_articles():
        try:
            articles = Article.query.all()
            return jsonify([article.to_dict() for article in articles])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des articles'}), 500

    @app.route("/api/articles/search", methods=['GET'])
    def search_articles():
        try:
            query = request.args.get('query', '')
            if not query or len(query) < 3:
                return jsonify([])
            
            search_term = f'%{query.lower()}%'
            articles = Article.query.filter(
                or_(
                    func.lower(Article.designation).like(search_term),
                    func.lower(Article.code_article).like(search_term),
                    func.lower(Article.reference).like(search_term),
                    func.lower(Article.categorie).like(search_term)
                )
            ).limit(10).all()
            
            return jsonify([article.to_dict() for article in articles])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la recherche d\'articles'}), 500

    @app.route("/api/search/global", methods=['GET'])
    def global_search():
        try:
            query = request.args.get('query', '')
            if not query or len(query) < 2:
                return jsonify({'results': [], 'totalCount': 0})
            
            search_term = f'%{query.lower()}%'
            results = []
            
            # Search Articles
            articles = Article.query.filter(
                or_(
                    func.lower(Article.designation).like(search_term),
                    func.lower(Article.code_article).like(search_term),
                    func.lower(Article.reference).like(search_term),
                    func.lower(Article.categorie).like(search_term)
                )
            ).limit(5).all()
            
            for article in articles:
                results.append({
                    'type': 'article',
                    'id': article.id,
                    'title': article.designation,
                    'subtitle': f'{article.code_article} - {article.categorie}',
                    'extra': f'Stock: {article.stock_actuel}',
                    'path': '/articles',
                    'data': article.to_dict()
                })
            
            # Search Suppliers
            suppliers = Supplier.query.filter(
                or_(
                    func.lower(Supplier.nom).like(search_term),
                    func.lower(Supplier.contact).like(search_term)
                )
            ).limit(5).all()
            
            for supplier in suppliers:
                results.append({
                    'type': 'supplier',
                    'id': supplier.id,
                    'title': supplier.nom,
                    'subtitle': supplier.contact or 'Pas de contact',
                    'extra': supplier.adresse or '',
                    'path': '/suppliers',
                    'data': supplier.to_dict()
                })
            
            # Search Requestors
            requestors = Requestor.query.filter(
                or_(
                    func.lower(func.concat(Requestor.prenom, ' ', Requestor.nom)).like(search_term),
                    func.lower(Requestor.departement).like(search_term),
                    func.lower(Requestor.poste).like(search_term)
                )
            ).limit(5).all()
            
            for requestor in requestors:
                results.append({
                    'type': 'requestor',
                    'id': requestor.id,
                    'title': f'{requestor.prenom} {requestor.nom}',
                    'subtitle': requestor.departement,
                    'extra': requestor.poste or '',
                    'path': '/requestors',
                    'data': requestor.to_dict()
                })
            
            return jsonify({
                'results': results[:15],
                'totalCount': len(results),
                'categories': {
                    'articles': len([r for r in results if r['type'] == 'article']),
                    'suppliers': len([r for r in results if r['type'] == 'supplier']),
                    'requestors': len([r for r in results if r['type'] == 'requestor'])
                }
            })
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la recherche globale'}), 500

    @app.route("/api/articles/<article_id>", methods=['GET'])
    def get_article(article_id):
        try:
            article = Article.query.get(article_id)
            if not article:
                return jsonify({'message': 'Article non trouvé'}), 404
            return jsonify(article.to_dict())
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération de l\'article'}), 500

    @app.route("/api/articles", methods=['POST'])
    def create_article():
        try:
            data = request.get_json()
            article = Article(
                code_article=data['codeArticle'],
                designation=data['designation'],
                categorie=data['categorie'],
                marque=data.get('marque'),
                reference=data.get('reference'),
                stock_initial=data.get('stockInitial', 0),
                stock_actuel=data.get('stockInitial', 0),
                unite=data.get('unite', 'pcs'),
                prix_unitaire=data.get('prixUnitaire'),
                seuil_minimum=data.get('seuilMinimum', 10),
                fournisseur_id=data.get('fournisseurId')
            )
            db.session.add(article)
            db.session.commit()
            return jsonify(article.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    @app.route("/api/articles/<article_id>", methods=['PUT'])
    def update_article(article_id):
        try:
            article = Article.query.get(article_id)
            if not article:
                return jsonify({'message': 'Article non trouvé'}), 404
            
            data = request.get_json()
            for key, value in data.items():
                if hasattr(article, key.replace('C', '_c').replace('A', '_a').replace('I', '_i').replace('M', '_m').replace('S', '_s').replace('P', '_p').replace('F', '_f').lower()):
                    setattr(article, key.replace('C', '_c').replace('A', '_a').replace('I', '_i').replace('M', '_m').replace('S', '_s').replace('P', '_p').replace('F', '_f').lower(), value)
            
            db.session.commit()
            return jsonify(article.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la mise à jour', 'error': str(e)}), 400

    @app.route("/api/articles/<article_id>", methods=['DELETE'])
    def delete_article(article_id):
        try:
            article = Article.query.get(article_id)
            if not article:
                return jsonify({'message': 'Article non trouvé'}), 404
            
            db.session.delete(article)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la suppression'}), 500

    @app.route("/api/articles/low-stock", methods=['GET'])
    def get_low_stock_articles():
        try:
            articles = Article.query.filter(Article.stock_actuel <= Article.seuil_minimum).all()
            return jsonify([article.to_dict() for article in articles])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des articles en stock bas'}), 500

    # Suppliers routes
    @app.route("/api/suppliers", methods=['GET'])
    def get_suppliers():
        try:
            suppliers = Supplier.query.all()
            return jsonify([supplier.to_dict() for supplier in suppliers])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des fournisseurs'}), 500

    @app.route("/api/suppliers", methods=['POST'])
    def create_supplier():
        try:
            data = request.get_json()
            supplier = Supplier(
                nom=data['nom'],
                contact=data.get('contact'),
                telephone=data.get('telephone'),
                email=data.get('email'),
                adresse=data.get('adresse'),
                conditions_paiement=data.get('conditionsPaiement'),
                delai_livraison=data.get('delaiLivraison')
            )
            db.session.add(supplier)
            db.session.commit()
            return jsonify(supplier.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    @app.route("/api/suppliers/<supplier_id>", methods=['PUT'])
    def update_supplier(supplier_id):
        try:
            supplier = Supplier.query.get(supplier_id)
            if not supplier:
                return jsonify({'message': 'Fournisseur non trouvé'}), 404
            
            data = request.get_json()
            for key, value in data.items():
                snake_key = key.replace('conditionsPaiement', 'conditions_paiement').replace('delaiLivraison', 'delai_livraison')
                if hasattr(supplier, snake_key):
                    setattr(supplier, snake_key, value)
            
            db.session.commit()
            return jsonify(supplier.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la mise à jour', 'error': str(e)}), 400

    @app.route("/api/suppliers/<supplier_id>", methods=['DELETE'])
    def delete_supplier(supplier_id):
        try:
            supplier = Supplier.query.get(supplier_id)
            if not supplier:
                return jsonify({'message': 'Fournisseur non trouvé'}), 404
            
            db.session.delete(supplier)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la suppression'}), 500

    # Requestors routes
    @app.route("/api/requestors", methods=['GET'])
    def get_requestors():
        try:
            requestors = Requestor.query.all()
            return jsonify([requestor.to_dict() for requestor in requestors])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des demandeurs'}), 500

    @app.route("/api/requestors", methods=['POST'])
    def create_requestor():
        try:
            data = request.get_json()
            requestor = Requestor(
                nom=data['nom'],
                prenom=data['prenom'],
                departement=data['departement'],
                poste=data.get('poste'),
                email=data.get('email'),
                telephone=data.get('telephone')
            )
            db.session.add(requestor)
            db.session.commit()
            return jsonify(requestor.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    @app.route("/api/requestors/<requestor_id>", methods=['PUT'])
    def update_requestor(requestor_id):
        try:
            requestor = Requestor.query.get(requestor_id)
            if not requestor:
                return jsonify({'message': 'Demandeur non trouvé'}), 404
            
            data = request.get_json()
            for key, value in data.items():
                if hasattr(requestor, key):
                    setattr(requestor, key, value)
            
            db.session.commit()
            return jsonify(requestor.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la mise à jour', 'error': str(e)}), 400

    @app.route("/api/requestors/<requestor_id>", methods=['DELETE'])
    def delete_requestor(requestor_id):
        try:
            requestor = Requestor.query.get(requestor_id)
            if not requestor:
                return jsonify({'message': 'Demandeur non trouvé'}), 404
            
            db.session.delete(requestor)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la suppression'}), 500

    # Purchase Requests routes
    @app.route("/api/purchase-requests", methods=['GET'])
    def get_purchase_requests():
        try:
            requests = PurchaseRequest.query.all()
            return jsonify([request.to_dict() for request in requests])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des demandes d\'achat'}), 500

    @app.route("/api/purchase-requests", methods=['POST'])
    def create_purchase_request():
        try:
            data = request.get_json()
            purchase_request = PurchaseRequest(
                date_demande=datetime.fromisoformat(data['dateDemande'].replace('Z', '+00:00')) if 'dateDemande' in data else datetime.utcnow(),
                requestor_id=data['requestorId'],
                observations=data.get('observations'),
                statut=data.get('statut', 'en_attente'),
                total_articles=0
            )
            db.session.add(purchase_request)
            db.session.commit()
            return jsonify(purchase_request.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    @app.route("/api/purchase-requests/<request_id>", methods=['PUT'])
    def update_purchase_request(request_id):
        try:
            purchase_request = PurchaseRequest.query.get(request_id)
            if not purchase_request:
                return jsonify({'message': 'Demande non trouvée'}), 404
            
            data = request.get_json()
            
            # Handle status updates
            if 'statut' in data:
                purchase_request.statut = data['statut']
            
            if 'observations' in data:
                purchase_request.observations = data['observations']
            
            db.session.commit()
            return jsonify(purchase_request.to_dict())
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la mise à jour', 'error': str(e)}), 400

    @app.route("/api/purchase-requests/<request_id>", methods=['DELETE'])
    def delete_purchase_request(request_id):
        try:
            purchase_request = PurchaseRequest.query.get(request_id)
            if not purchase_request:
                return jsonify({'message': 'Demande non trouvée'}), 404
            
            # Also delete related items
            PurchaseRequestItem.query.filter_by(purchase_request_id=request_id).delete()
            db.session.delete(purchase_request)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Erreur lors de la suppression'}), 500

    # Purchase Request Items routes
    @app.route("/api/purchase-request-items", methods=['POST'])
    def create_purchase_request_item():
        try:
            data = request.get_json()
            item = PurchaseRequestItem(
                purchase_request_id=data['purchaseRequestId'],
                article_id=data['articleId'],
                quantite_demandee=data['quantiteDemandee'],
                supplier_id=data.get('supplierId'),
                prix_unitaire_estime=data.get('prixUnitaireEstime'),
                observations=data.get('observations')
            )
            db.session.add(item)
            
            # Update total articles count
            item_count = PurchaseRequestItem.query.filter_by(purchase_request_id=data['purchaseRequestId']).count() + 1
            purchase_request = PurchaseRequest.query.get(data['purchaseRequestId'])
            if purchase_request:
                purchase_request.total_articles = item_count
            
            db.session.commit()
            return jsonify(item.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    @app.route("/api/purchase-request-items/<purchase_request_id>", methods=['GET'])
    def get_purchase_request_items(purchase_request_id):
        try:
            items = PurchaseRequestItem.query.filter_by(purchase_request_id=purchase_request_id).all()
            return jsonify([item.to_dict() for item in items])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des éléments'}), 500

    # Complete purchase request creation
    @app.route("/api/purchase-requests/complete", methods=['POST'])
    def create_complete_purchase_request():
        try:
            data = request.get_json()
            
            # Create purchase request header
            purchase_request = PurchaseRequest(
                date_demande=datetime.fromisoformat(data['dateDemande'].replace('Z', '+00:00')) if 'dateDemande' in data else datetime.utcnow(),
                requestor_id=data['requestorId'],
                observations=data.get('observations'),
                total_articles=len(data['items']),
                statut='en_attente'
            )
            db.session.add(purchase_request)
            db.session.flush()  # Get the ID
            
            # Create items
            items = []
            for item_data in data['items']:
                item = PurchaseRequestItem(
                    purchase_request_id=purchase_request.id,
                    article_id=item_data['articleId'],
                    quantite_demandee=item_data['quantiteDemandee'],
                    supplier_id=item_data.get('supplierId'),
                    prix_unitaire_estime=item_data.get('prixUnitaireEstime'),
                    observations=item_data.get('observations')
                )
                db.session.add(item)
                items.append(item)
            
            db.session.commit()
            
            return jsonify({
                **purchase_request.to_dict(),
                'items': [item.to_dict() for item in items]
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    # Reception routes
    @app.route("/api/receptions", methods=['GET'])
    def get_receptions():
        try:
            receptions = Reception.query.all()
            return jsonify([reception.to_dict() for reception in receptions])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des réceptions'}), 500

    @app.route("/api/receptions", methods=['POST'])
    def create_reception():
        try:
            data = request.get_json()
            reception = Reception(
                date_reception=datetime.fromisoformat(data['dateReception'].replace('Z', '+00:00')) if 'dateReception' in data else datetime.utcnow(),
                supplier_id=data['supplierId'],
                article_id=data['articleId'],
                quantite_recue=data['quantiteRecue'],
                prix_unitaire=data.get('prixUnitaire'),
                numero_bon_livraison=data.get('numeroBonLivraison'),
                observations=data.get('observations')
            )
            db.session.add(reception)
            
            # Update article stock
            article = Article.query.get(data['articleId'])
            if article:
                article.stock_actuel += data['quantiteRecue']
            
            db.session.commit()
            return jsonify(reception.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    # Outbound routes
    @app.route("/api/outbounds", methods=['GET'])
    def get_outbounds():
        try:
            outbounds = Outbound.query.all()
            return jsonify([outbound.to_dict() for outbound in outbounds])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des sorties'}), 500

    @app.route("/api/outbounds", methods=['POST'])
    def create_outbound():
        try:
            data = request.get_json()
            outbound = Outbound(
                date_sortie=datetime.fromisoformat(data['dateSortie'].replace('Z', '+00:00')) if 'dateSortie' in data else datetime.utcnow(),
                requestor_id=data['requestorId'],
                article_id=data['articleId'],
                quantite_sortie=data['quantiteSortie'],
                motif_sortie=data['motifSortie'],
                observations=data.get('observations')
            )
            db.session.add(outbound)
            
            # Update article stock
            article = Article.query.get(data['articleId'])
            if article:
                article.stock_actuel -= data['quantiteSortie']
                if article.stock_actuel < 0:
                    article.stock_actuel = 0
            
            db.session.commit()
            return jsonify(outbound.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Données invalides', 'error': str(e)}), 400

    # Analytics routes
    @app.route("/api/analytics/overview", methods=['GET'])
    def get_analytics_overview():
        try:
            total_articles = Article.query.count()
            total_suppliers = Supplier.query.count()
            total_requests = PurchaseRequest.query.count()
            low_stock_count = Article.query.filter(Article.stock_actuel <= Article.seuil_minimum).count()
            
            return jsonify({
                'totalArticles': total_articles,
                'totalSuppliers': total_suppliers,
                'totalRequests': total_requests,
                'lowStockCount': low_stock_count
            })
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des analytics'}), 500