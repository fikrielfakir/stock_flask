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
            print(f"Purchase requests error: {str(e)}")
            return jsonify({'message': f'Erreur lors de la récupération des demandes d\'achat: {str(e)}'}), 500

    @app.route("/api/purchase-requests", methods=['POST'])
    def create_purchase_request():
        try:
            data = request.get_json()
            
            # Generate request number
            count = PurchaseRequest.query.count() + 1
            numero_demande = f"DA-{datetime.utcnow().strftime('%Y')}-{count:04d}"
            
            # Calculate total
            total_estime = sum(item['quantiteDemandee'] * item['prixUnitaireEstime'] 
                             for item in data.get('articles', []))
            
            purchase_request = PurchaseRequest(
                numero_demande=numero_demande,
                date_demande=datetime.fromisoformat(data['dateDemande'].replace('Z', '+00:00')) if 'dateDemande' in data else datetime.utcnow(),
                requestor_id=data['requestorId'],
                observations=data.get('observations'),
                statut=data.get('statut', 'en_attente'),
                total_articles=len(data.get('articles', [])),
                total_estime=total_estime
            )
            db.session.add(purchase_request)
            db.session.flush()  # Get the ID
            
            # Add articles
            for article_data in data.get('articles', []):
                sous_total = article_data['quantiteDemandee'] * article_data['prixUnitaireEstime']
                
                item = PurchaseRequestItem(
                    purchase_request_id=purchase_request.id,
                    article_id=article_data['articleId'],
                    supplier_id=article_data.get('supplierId'),
                    quantite_demandee=article_data['quantiteDemandee'],
                    prix_unitaire_estime=article_data['prixUnitaireEstime'],
                    sous_total=sous_total
                )
                db.session.add(item)
            
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
            
            # If updating articles, delete existing and recreate
            if 'articles' in data:
                # Delete existing items
                PurchaseRequestItem.query.filter_by(purchase_request_id=request_id).delete()
                
                # Add new articles
                total_estime = 0
                for article_data in data['articles']:
                    sous_total = article_data['quantiteDemandee'] * article_data['prixUnitaireEstime']
                    total_estime += sous_total
                    
                    item = PurchaseRequestItem(
                        purchase_request_id=request_id,
                        article_id=article_data['articleId'],
                        supplier_id=article_data.get('supplierId'),
                        quantite_demandee=article_data['quantiteDemandee'],
                        prix_unitaire_estime=article_data['prixUnitaireEstime'],
                        sous_total=sous_total
                    )
                    db.session.add(item)
                
                purchase_request.total_articles = len(data['articles'])
                purchase_request.total_estime = total_estime
            
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

    @app.route("/api/purchase-requests/<request_id>/items", methods=['GET'])
    def get_purchase_request_items(request_id):
        try:
            items = PurchaseRequestItem.query.filter_by(purchase_request_id=request_id).all()
            return jsonify([item.to_dict() for item in items])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des éléments'}), 500
    
    # Convert Purchase Request to Reception
    @app.route("/api/purchase-requests/<request_id>/convert-reception", methods=['POST'])
    def convert_purchase_request_to_reception(request_id):
        try:
            data = request.get_json()
            
            # Get purchase request and items
            purchase_request = PurchaseRequest.query.get_or_404(request_id)
            items = PurchaseRequestItem.query.filter_by(purchase_request_id=request_id).all()
            
            # Create reception records for each article
            receptions_created = []
            
            for reception_article in data.get('articles', []):
                # Find corresponding item
                item = next((i for i in items if i.id == reception_article['itemId']), None)
                if not item:
                    continue
                
                # Create reception record
                reception = Reception(
                    date_reception=datetime.strptime(data['dateReception'], '%Y-%m-%d').date(),
                    supplier_id=item.supplier_id,
                    article_id=item.article_id,
                    quantite_recue=reception_article['quantiteRecue'],
                    prix_unitaire=reception_article['prixUnitaire'],
                    numero_bon_livraison=data.get('numeroBonLivraison'),
                    observations=data.get('observations')
                )
                db.session.add(reception)
                
                # Update article stock
                article = Article.query.get(item.article_id)
                if article:
                    article.stock_actuel += reception_article['quantiteRecue']
                
                receptions_created.append(reception)
            
            db.session.commit()
            
            return jsonify({
                'message': f'{len(receptions_created)} réceptions créées avec succès',
                'receptions': [r.to_dict() for r in receptions_created]
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Erreur lors de la conversion: {str(e)}'}), 500

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

    # Dashboard stats endpoint  
    @app.route("/api/dashboard/stats", methods=['GET'])
    def get_dashboard_stats():
        try:
            total_articles = Article.query.count()
            total_suppliers = Supplier.query.count()
            total_requestors = Requestor.query.count()
            total_requests = PurchaseRequest.query.count()
            total_receptions = Reception.query.count()
            total_outbounds = Outbound.query.count()
            low_stock_count = Article.query.filter(Article.stock_actuel <= Article.seuil_minimum).count()
            
            # Get recent activity
            recent_receptions = Reception.query.order_by(desc(Reception.date_reception)).limit(5).all()
            recent_outbounds = Outbound.query.order_by(desc(Outbound.date_sortie)).limit(5).all()
            
            return jsonify({
                'totalArticles': total_articles,
                'totalSuppliers': total_suppliers,
                'totalRequestors': total_requestors,
                'totalRequests': total_requests,
                'totalReceptions': total_receptions,
                'totalOutbounds': total_outbounds,
                'lowStockCount': low_stock_count,
                'recentReceptions': [reception.to_dict() for reception in recent_receptions],
                'recentOutbounds': [outbound.to_dict() for outbound in recent_outbounds]
            })
        except Exception as e:
            print(f"Dashboard stats error: {str(e)}")
            return jsonify({'message': f'Erreur lors de la récupération des statistiques: {str(e)}'}), 500

    # Stock status analytics
    @app.route("/api/stock-status/analytics", methods=['GET'])
    def get_stock_status_analytics():
        try:
            articles = Article.query.all()
            
            # Categorize by stock levels
            critical = []  # 0 stock
            low = []       # below minimum
            medium = []    # 1-2x minimum
            good = []      # above 2x minimum
            
            for article in articles:
                seuil = article.seuil_minimum or 10
                if article.stock_actuel == 0:
                    critical.append(article.to_dict())
                elif article.stock_actuel <= seuil:
                    low.append(article.to_dict())
                elif article.stock_actuel <= seuil * 2:
                    medium.append(article.to_dict())
                else:
                    good.append(article.to_dict())
            
            return jsonify({
                'critical': critical,
                'low': low,
                'medium': medium,
                'good': good,
                'summary': {
                    'critical_count': len(critical),
                    'low_count': len(low),
                    'medium_count': len(medium),
                    'good_count': len(good),
                    'total_count': len(articles)
                }
            })
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération du statut stock'}), 500

    # Purchase follow-up analytics
    @app.route("/api/purchase-follow/status", methods=['GET'])
    def get_purchase_follow_status():
        try:
            pending = PurchaseRequest.query.filter_by(statut='en_attente').all()
            approved = PurchaseRequest.query.filter_by(statut='approuve').all()
            ordered = PurchaseRequest.query.filter_by(statut='commande').all()
            refused = PurchaseRequest.query.filter_by(statut='refuse').all()
            
            return jsonify({
                'pending': [req.to_dict() for req in pending],
                'approved': [req.to_dict() for req in approved],
                'ordered': [req.to_dict() for req in ordered],
                'refused': [req.to_dict() for req in refused]
            })
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération du suivi'}), 500

    # Reports endpoints
    @app.route("/api/reports/stock", methods=['GET'])
    def generate_stock_report():
        try:
            articles = Article.query.all()
            report_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'total_articles': len(articles),
                'articles': [article.to_dict() for article in articles],
                'summary': {
                    'total_value': sum(article.prix_unitaire * article.stock_actuel for article in articles if article.prix_unitaire),
                    'low_stock_count': len([a for a in articles if a.stock_actuel <= (a.seuil_minimum or 10)])
                }
            }
            return jsonify(report_data)
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la génération du rapport'}), 500

    # Settings endpoints
    @app.route("/api/settings/categories", methods=['GET'])
    def get_categories():
        try:
            categories = db.session.query(Article.categorie).distinct().all()
            return jsonify([cat[0] for cat in categories if cat[0]])
        except Exception as e:
            return jsonify({'message': 'Erreur lors de la récupération des catégories'}), 500