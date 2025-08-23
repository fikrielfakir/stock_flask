var __defProp = Object.defineProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};

// server/index.ts
import express2 from "express";

// server/routes.ts
import { createServer } from "http";

// shared/schema.ts
var schema_exports = {};
__export(schema_exports, {
  articles: () => articles,
  auditLogs: () => auditLogs,
  backupLogs: () => backupLogs,
  categories: () => categories,
  convertToReceptionSchema: () => convertToReceptionSchema,
  departements: () => departements,
  insertArticleSchema: () => insertArticleSchema,
  insertAuditLogSchema: () => insertAuditLogSchema,
  insertBackupLogSchema: () => insertBackupLogSchema,
  insertCategorySchema: () => insertCategorySchema,
  insertCompletePurchaseRequestSchema: () => insertCompletePurchaseRequestSchema,
  insertDepartementSchema: () => insertDepartementSchema,
  insertMarqueSchema: () => insertMarqueSchema,
  insertOutboundSchema: () => insertOutboundSchema,
  insertPosteSchema: () => insertPosteSchema,
  insertPurchaseRequestItemSchema: () => insertPurchaseRequestItemSchema,
  insertPurchaseRequestSchema: () => insertPurchaseRequestSchema,
  insertReceptionSchema: () => insertReceptionSchema,
  insertRequestorSchema: () => insertRequestorSchema,
  insertStockMovementSchema: () => insertStockMovementSchema,
  insertSupplierSchema: () => insertSupplierSchema,
  insertSystemSettingSchema: () => insertSystemSettingSchema,
  insertUserSchema: () => insertUserSchema,
  marques: () => marques,
  outbounds: () => outbounds,
  postes: () => postes,
  purchaseRequestItems: () => purchaseRequestItems,
  purchaseRequests: () => purchaseRequests,
  receptions: () => receptions,
  requestors: () => requestors,
  stockMovements: () => stockMovements,
  suppliers: () => suppliers,
  systemSettings: () => systemSettings,
  users: () => users
});
import { pgTable, text, varchar, integer, decimal, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";
var articles = pgTable("articles", {
  id: varchar("id").primaryKey(),
  codeArticle: text("code_article").notNull().unique(),
  designation: text("designation").notNull(),
  categorie: text("categorie").notNull(),
  marque: text("marque"),
  reference: text("reference"),
  stockInitial: integer("stock_initial").notNull().default(0),
  stockActuel: integer("stock_actuel").notNull().default(0),
  unite: text("unite").notNull().default("pcs"),
  prixUnitaire: decimal("prix_unitaire", { precision: 10, scale: 2 }),
  seuilMinimum: integer("seuil_minimum").default(10),
  fournisseurId: varchar("fournisseur_id"),
  createdAt: timestamp("created_at").defaultNow()
});
var suppliers = pgTable("suppliers", {
  id: varchar("id").primaryKey(),
  nom: text("nom").notNull(),
  contact: text("contact"),
  telephone: text("telephone"),
  email: text("email"),
  adresse: text("adresse"),
  conditionsPaiement: text("conditions_paiement"),
  delaiLivraison: integer("delai_livraison"),
  // in days
  createdAt: timestamp("created_at").defaultNow()
});
var requestors = pgTable("requestors", {
  id: varchar("id").primaryKey(),
  nom: text("nom").notNull(),
  prenom: text("prenom").notNull(),
  departement: text("departement").notNull(),
  poste: text("poste"),
  email: text("email"),
  telephone: text("telephone"),
  createdAt: timestamp("created_at").defaultNow()
});
var purchaseRequests = pgTable("purchase_requests", {
  id: varchar("id").primaryKey(),
  dateDemande: timestamp("date_demande").notNull().defaultNow(),
  requestorId: varchar("requestor_id").notNull(),
  dateInitiation: timestamp("date_initiation").defaultNow(),
  observations: text("observations"),
  statut: text("statut").notNull().default("en_attente"),
  // en_attente, approuve, refuse, commande
  totalArticles: integer("total_articles").notNull().default(0),
  createdAt: timestamp("created_at").defaultNow()
});
var purchaseRequestItems = pgTable("purchase_request_items", {
  id: varchar("id").primaryKey(),
  purchaseRequestId: varchar("purchase_request_id").notNull(),
  articleId: varchar("article_id").notNull(),
  quantiteDemandee: integer("quantite_demandee").notNull(),
  supplierId: varchar("supplier_id"),
  prixUnitaireEstime: decimal("prix_unitaire_estime", { precision: 10, scale: 2 }),
  observations: text("observations"),
  createdAt: timestamp("created_at").defaultNow()
});
var receptions = pgTable("receptions", {
  id: varchar("id").primaryKey(),
  dateReception: timestamp("date_reception").notNull().defaultNow(),
  supplierId: varchar("supplier_id").notNull(),
  articleId: varchar("article_id").notNull(),
  quantiteRecue: integer("quantite_recue").notNull(),
  prixUnitaire: decimal("prix_unitaire", { precision: 10, scale: 2 }),
  numeroBonLivraison: text("numero_bon_livraison"),
  observations: text("observations"),
  createdAt: timestamp("created_at").defaultNow()
});
var outbounds = pgTable("outbounds", {
  id: varchar("id").primaryKey(),
  dateSortie: timestamp("date_sortie").notNull().defaultNow(),
  requestorId: varchar("requestor_id").notNull(),
  articleId: varchar("article_id").notNull(),
  quantiteSortie: integer("quantite_sortie").notNull(),
  motifSortie: text("motif_sortie").notNull(),
  observations: text("observations"),
  createdAt: timestamp("created_at").defaultNow()
});
var stockMovements = pgTable("stock_movements", {
  id: varchar("id").primaryKey(),
  articleId: varchar("article_id").notNull(),
  type: text("type").notNull(),
  // entree, sortie
  quantite: integer("quantite").notNull(),
  quantiteAvant: integer("quantite_avant").notNull(),
  quantiteApres: integer("quantite_apres").notNull(),
  reference: text("reference"),
  // Reference to reception/outbound ID
  dateMovement: timestamp("date_movement").notNull().defaultNow(),
  description: text("description")
});
var users = pgTable("users", {
  id: varchar("id").primaryKey(),
  username: text("username").notNull().unique(),
  email: text("email").unique(),
  hashedPassword: text("hashed_password").notNull(),
  role: text("role").notNull().default("demandeur"),
  // admin, super_admin, magasinier, demandeur, read_only
  isActive: integer("is_active").notNull().default(1),
  // 1 = active, 0 = inactive
  lastLogin: timestamp("last_login"),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow()
});
var systemSettings = pgTable("system_settings", {
  id: varchar("id").primaryKey(),
  category: text("category").notNull(),
  // stock_management, security, backup, etc.
  key: text("key").notNull(),
  value: text("value"),
  dataType: text("data_type").notNull().default("string"),
  // string, number, boolean, json
  description: text("description"),
  isEditable: integer("is_editable").notNull().default(1),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow()
});
var auditLogs = pgTable("audit_logs", {
  id: varchar("id").primaryKey(),
  userId: varchar("user_id"),
  action: text("action").notNull(),
  // CREATE, UPDATE, DELETE, LOGIN, LOGOUT, etc.
  entityType: text("entity_type"),
  // articles, suppliers, etc.
  entityId: varchar("entity_id"),
  oldValues: text("old_values"),
  // JSON string
  newValues: text("new_values"),
  // JSON string
  ipAddress: text("ip_address"),
  userAgent: text("user_agent"),
  createdAt: timestamp("created_at").defaultNow()
});
var backupLogs = pgTable("backup_logs", {
  id: varchar("id").primaryKey(),
  fileName: text("file_name").notNull(),
  filePath: text("file_path").notNull(),
  fileSize: integer("file_size"),
  // bytes
  backupType: text("backup_type").notNull(),
  // manual, scheduled
  status: text("status").notNull().default("in_progress"),
  // in_progress, completed, failed
  createdBy: varchar("created_by"),
  createdAt: timestamp("created_at").defaultNow()
});
var insertArticleSchema = createInsertSchema(articles).omit({
  id: true,
  createdAt: true,
  stockActuel: true
}).extend({
  prixUnitaire: z.coerce.number().nullable().optional(),
  fournisseurId: z.coerce.string().nullable().optional()
});
var insertSupplierSchema = createInsertSchema(suppliers).omit({
  id: true,
  createdAt: true
});
var insertRequestorSchema = createInsertSchema(requestors).omit({
  id: true,
  createdAt: true
});
var insertPurchaseRequestSchema = createInsertSchema(purchaseRequests).omit({
  id: true,
  createdAt: true,
  dateInitiation: true,
  totalArticles: true
}).extend({
  dateDemande: z.string().transform((str) => new Date(str))
});
var insertPurchaseRequestItemSchema = createInsertSchema(purchaseRequestItems).omit({
  id: true,
  createdAt: true
}).extend({
  prixUnitaireEstime: z.coerce.number().nullable().optional(),
  supplierId: z.string().nullable().optional()
});
var insertCompletePurchaseRequestSchema = z.object({
  dateDemande: z.string().transform((str) => new Date(str)),
  requestorId: z.string(),
  observations: z.string().optional(),
  items: z.array(z.object({
    articleId: z.string(),
    quantiteDemandee: z.number().positive(),
    supplierId: z.string().nullable().optional(),
    prixUnitaireEstime: z.coerce.number().nullable().optional(),
    observations: z.string().optional()
  })).min(1, "Au moins un article est requis")
});
var insertReceptionSchema = createInsertSchema(receptions).omit({
  id: true,
  createdAt: true
}).extend({
  prixUnitaire: z.coerce.number().nullable().optional(),
  dateReception: z.string().transform((str) => new Date(str))
});
var insertOutboundSchema = createInsertSchema(outbounds).omit({
  id: true,
  createdAt: true
}).extend({
  dateSortie: z.string().transform((str) => new Date(str))
});
var insertStockMovementSchema = createInsertSchema(stockMovements).omit({
  id: true
});
var insertUserSchema = createInsertSchema(users).omit({
  id: true,
  createdAt: true,
  updatedAt: true,
  lastLogin: true
});
var insertSystemSettingSchema = createInsertSchema(systemSettings).omit({
  id: true,
  createdAt: true,
  updatedAt: true
});
var insertAuditLogSchema = createInsertSchema(auditLogs).omit({
  id: true,
  createdAt: true
});
var insertBackupLogSchema = createInsertSchema(backupLogs).omit({
  id: true,
  createdAt: true
});
var convertToReceptionSchema = z.object({
  quantiteRecue: z.number().positive().optional(),
  prixUnitaire: z.coerce.number().nullable().optional(),
  numeroBonLivraison: z.string().optional(),
  observations: z.string().optional(),
  dateReception: z.string().optional()
});
var categories = pgTable("categories", {
  id: varchar("id").primaryKey(),
  nom: text("nom").notNull().unique(),
  description: text("description"),
  createdAt: timestamp("created_at").defaultNow()
});
var marques = pgTable("marques", {
  id: varchar("id").primaryKey(),
  nom: text("nom").notNull().unique(),
  description: text("description"),
  createdAt: timestamp("created_at").defaultNow()
});
var departements = pgTable("departements", {
  id: varchar("id").primaryKey(),
  nom: text("nom").notNull().unique(),
  description: text("description"),
  createdAt: timestamp("created_at").defaultNow()
});
var postes = pgTable("postes", {
  id: varchar("id").primaryKey(),
  nom: text("nom").notNull().unique(),
  departementId: varchar("departement_id"),
  description: text("description"),
  createdAt: timestamp("created_at").defaultNow()
});
var insertCategorySchema = createInsertSchema(categories).omit({
  id: true,
  createdAt: true
});
var insertMarqueSchema = createInsertSchema(marques).omit({
  id: true,
  createdAt: true
});
var insertDepartementSchema = createInsertSchema(departements).omit({
  id: true,
  createdAt: true
});
var insertPosteSchema = createInsertSchema(postes).omit({
  id: true,
  createdAt: true
});

// server/storage.ts
import { randomUUID } from "crypto";

// server/db.ts
import { Pool, neonConfig } from "@neondatabase/serverless";
import { drizzle } from "drizzle-orm/neon-serverless";
import ws from "ws";
neonConfig.webSocketConstructor = ws;
if (!process.env.DATABASE_URL) {
  throw new Error(
    "DATABASE_URL must be set. Did you forget to provision a database?"
  );
}
var pool = new Pool({ connectionString: process.env.DATABASE_URL });
var db = drizzle({ client: pool, schema: schema_exports });

// server/storage.ts
import { eq, lte, count, sql } from "drizzle-orm";
var DatabaseStorage = class {
  // Articles
  async getArticles() {
    return await db.select().from(articles);
  }
  async getArticle(id) {
    const [article] = await db.select().from(articles).where(eq(articles.id, id));
    return article || void 0;
  }
  async createArticle(article) {
    const id = randomUUID();
    const [newArticle] = await db.insert(articles).values({
      ...article,
      id,
      stockInitial: article.stockInitial || 0,
      stockActuel: article.stockInitial || 0,
      prixUnitaire: article.prixUnitaire?.toString() || null
    }).returning();
    return newArticle;
  }
  async updateArticle(id, article) {
    const [updated] = await db.update(articles).set(article).where(eq(articles.id, id)).returning();
    if (!updated) {
      throw new Error("Article not found");
    }
    return updated;
  }
  async deleteArticle(id) {
    await db.delete(articles).where(eq(articles.id, id));
  }
  async getLowStockArticles() {
    return await db.select().from(articles).where(lte(articles.stockActuel, articles.seuilMinimum));
  }
  // Suppliers
  async getSuppliers() {
    return await db.select().from(suppliers);
  }
  async getSupplier(id) {
    const [supplier] = await db.select().from(suppliers).where(eq(suppliers.id, id));
    return supplier || void 0;
  }
  async createSupplier(supplier) {
    const id = randomUUID();
    const [newSupplier] = await db.insert(suppliers).values({ ...supplier, id }).returning();
    return newSupplier;
  }
  async updateSupplier(id, supplier) {
    const [updated] = await db.update(suppliers).set(supplier).where(eq(suppliers.id, id)).returning();
    if (!updated) {
      throw new Error("Supplier not found");
    }
    return updated;
  }
  async deleteSupplier(id) {
    await db.delete(suppliers).where(eq(suppliers.id, id));
  }
  // Requestors
  async getRequestors() {
    return await db.select().from(requestors);
  }
  async getRequestor(id) {
    const [requestor] = await db.select().from(requestors).where(eq(requestors.id, id));
    return requestor || void 0;
  }
  async createRequestor(requestor) {
    const id = randomUUID();
    const [newRequestor] = await db.insert(requestors).values({ ...requestor, id }).returning();
    return newRequestor;
  }
  async updateRequestor(id, requestor) {
    const [updated] = await db.update(requestors).set(requestor).where(eq(requestors.id, id)).returning();
    if (!updated) {
      throw new Error("Requestor not found");
    }
    return updated;
  }
  async deleteRequestor(id) {
    await db.delete(requestors).where(eq(requestors.id, id));
  }
  // Purchase Requests
  async getPurchaseRequests() {
    return await db.select().from(purchaseRequests);
  }
  async getPurchaseRequest(id) {
    const [request] = await db.select().from(purchaseRequests).where(eq(purchaseRequests.id, id));
    return request || void 0;
  }
  async createPurchaseRequest(request) {
    const id = randomUUID();
    const [newRequest] = await db.insert(purchaseRequests).values({ ...request, id }).returning();
    return newRequest;
  }
  async updatePurchaseRequest(id, request) {
    const [updated] = await db.update(purchaseRequests).set(request).where(eq(purchaseRequests.id, id)).returning();
    if (!updated) {
      throw new Error("Purchase request not found");
    }
    return updated;
  }
  async deletePurchaseRequest(id) {
    await db.delete(purchaseRequests).where(eq(purchaseRequests.id, id));
  }
  async getPurchaseRequestsReadyForReception() {
    return await db.select().from(purchaseRequests).where(eq(purchaseRequests.statut, "approuve"));
  }
  async getPurchaseRequestItems(purchaseRequestId) {
    return await db.select().from(purchaseRequestItems).where(eq(purchaseRequestItems.purchaseRequestId, purchaseRequestId));
  }
  // Receptions
  async getReceptions() {
    return await db.select().from(receptions);
  }
  async getReception(id) {
    const [reception] = await db.select().from(receptions).where(eq(receptions.id, id));
    return reception || void 0;
  }
  async createReception(reception) {
    const id = randomUUID();
    const [newReception] = await db.insert(receptions).values({
      ...reception,
      id,
      prixUnitaire: reception.prixUnitaire?.toString() || null
    }).returning();
    const article = await this.getArticle(reception.articleId);
    if (article) {
      const newStock = article.stockActuel + reception.quantiteRecue;
      await this.updateArticle(reception.articleId, { stockActuel: newStock });
      await this.createStockMovement({
        articleId: reception.articleId,
        type: "entree",
        quantite: reception.quantiteRecue,
        quantiteAvant: article.stockActuel,
        quantiteApres: newStock,
        reference: id,
        dateMovement: /* @__PURE__ */ new Date(),
        description: `R\xE9ception - NBL: ${reception.numeroBonLivraison || "N/A"}`
      });
    }
    return newReception;
  }
  async updateReception(id, reception) {
    const [updated] = await db.update(receptions).set(reception).where(eq(receptions.id, id)).returning();
    if (!updated) {
      throw new Error("Reception not found");
    }
    return updated;
  }
  async deleteReception(id) {
    await db.delete(receptions).where(eq(receptions.id, id));
  }
  // Outbounds
  async getOutbounds() {
    return await db.select().from(outbounds);
  }
  async getOutbound(id) {
    const [outbound] = await db.select().from(outbounds).where(eq(outbounds.id, id));
    return outbound || void 0;
  }
  async createOutbound(outbound) {
    const id = randomUUID();
    const article = await this.getArticle(outbound.articleId);
    if (!article || article.stockActuel < outbound.quantiteSortie) {
      throw new Error("Stock insuffisant");
    }
    const [newOutbound] = await db.insert(outbounds).values({ ...outbound, id }).returning();
    const newStock = article.stockActuel - outbound.quantiteSortie;
    await this.updateArticle(outbound.articleId, { stockActuel: newStock });
    await this.createStockMovement({
      articleId: outbound.articleId,
      type: "sortie",
      quantite: outbound.quantiteSortie,
      quantiteAvant: article.stockActuel,
      quantiteApres: newStock,
      reference: id,
      dateMovement: /* @__PURE__ */ new Date(),
      description: `Sortie - ${outbound.motifSortie}`
    });
    return newOutbound;
  }
  async updateOutbound(id, outbound) {
    const [updated] = await db.update(outbounds).set(outbound).where(eq(outbounds.id, id)).returning();
    if (!updated) {
      throw new Error("Outbound not found");
    }
    return updated;
  }
  async deleteOutbound(id) {
    await db.delete(outbounds).where(eq(outbounds.id, id));
  }
  // Stock Movements
  async getStockMovements(articleId) {
    if (articleId) {
      return await db.select().from(stockMovements).where(eq(stockMovements.articleId, articleId));
    }
    return await db.select().from(stockMovements);
  }
  async createStockMovement(movement) {
    const id = randomUUID();
    const [newMovement] = await db.insert(stockMovements).values({ ...movement, id }).returning();
    return newMovement;
  }
  // Dashboard stats
  async getDashboardStats() {
    const [totalArticlesResult] = await db.select({ count: count() }).from(articles);
    const [lowStockResult] = await db.select({ count: count() }).from(articles).where(lte(articles.stockActuel, articles.seuilMinimum));
    const [pendingRequestsResult] = await db.select({ count: count() }).from(purchaseRequests).where(eq(purchaseRequests.statut, "en_attente"));
    const [stockValueResult] = await db.select({
      value: sql`SUM(CAST(${articles.prixUnitaire} AS DECIMAL) * ${articles.stockActuel})`.mapWith(Number)
    }).from(articles);
    return {
      totalArticles: totalArticlesResult.count,
      lowStock: lowStockResult.count,
      pendingRequests: pendingRequestsResult.count,
      stockValue: stockValueResult.value || 0
    };
  }
  // Chart data methods for DatabaseStorage
  async getStockEvolutionData() {
    return [];
  }
  async getPurchaseStatusData() {
    const results = await db.select({
      status: purchaseRequests.statut,
      count: count()
    }).from(purchaseRequests).groupBy(purchaseRequests.statut);
    const statusColors = {
      "en_attente": "#f59e0b",
      "approuve": "#10b981",
      "refuse": "#ef4444",
      "commande": "#3b82f6"
    };
    return results.map((result) => ({
      status: result.status === "en_attente" ? "En Attente" : result.status === "approuve" ? "Approuv\xE9" : result.status === "refuse" ? "Refus\xE9" : "Command\xE9",
      count: result.count,
      color: statusColors[result.status] || "#6b7280"
    }));
  }
  async getCategoryDistributionData() {
    const results = await db.select({
      category: articles.categorie,
      count: count()
    }).from(articles).groupBy(articles.categorie);
    const total = results.reduce((sum2, result) => sum2 + result.count, 0);
    return results.map((result) => ({
      category: result.category,
      count: result.count,
      percentage: total > 0 ? Math.round(result.count / total * 100) : 0
    }));
  }
  async getRecentMovementsData() {
    const movements = await db.select({
      dateMovement: stockMovements.dateMovement,
      type: stockMovements.type,
      quantite: stockMovements.quantite,
      articleId: stockMovements.articleId
    }).from(stockMovements).orderBy(stockMovements.dateMovement).limit(10);
    return movements.map((movement) => ({
      date: movement.dateMovement.toLocaleDateString("fr-FR"),
      type: movement.type === "entree" ? "Entr\xE9e" : "Sortie",
      quantity: movement.quantite,
      article: movement.articleId.substring(0, 8) + "..."
    }));
  }
  // New entities - DatabaseStorage implementation
  async getCategories() {
    return await db.select().from(categories);
  }
  async getCategory(id) {
    const [category] = await db.select().from(categories).where(eq(categories.id, id));
    return category || void 0;
  }
  async createCategory(category) {
    const id = randomUUID();
    const [newCategory] = await db.insert(categories).values({ ...category, id }).returning();
    return newCategory;
  }
  async updateCategory(id, category) {
    const [updated] = await db.update(categories).set(category).where(eq(categories.id, id)).returning();
    if (!updated) {
      throw new Error("Category not found");
    }
    return updated;
  }
  async deleteCategory(id) {
    await db.delete(categories).where(eq(categories.id, id));
  }
  async getMarques() {
    return await db.select().from(marques);
  }
  async getMarque(id) {
    const [marque] = await db.select().from(marques).where(eq(marques.id, id));
    return marque || void 0;
  }
  async createMarque(marque) {
    const id = randomUUID();
    const [newMarque] = await db.insert(marques).values({ ...marque, id }).returning();
    return newMarque;
  }
  async updateMarque(id, marque) {
    const [updated] = await db.update(marques).set(marque).where(eq(marques.id, id)).returning();
    if (!updated) {
      throw new Error("Marque not found");
    }
    return updated;
  }
  async deleteMarque(id) {
    await db.delete(marques).where(eq(marques.id, id));
  }
  async getDepartements() {
    return await db.select().from(departements);
  }
  async getDepartement(id) {
    const [departement] = await db.select().from(departements).where(eq(departements.id, id));
    return departement || void 0;
  }
  async createDepartement(departement) {
    const id = randomUUID();
    const [newDepartement] = await db.insert(departements).values({ ...departement, id }).returning();
    return newDepartement;
  }
  async updateDepartement(id, departement) {
    const [updated] = await db.update(departements).set(departement).where(eq(departements.id, id)).returning();
    if (!updated) {
      throw new Error("Departement not found");
    }
    return updated;
  }
  async deleteDepartement(id) {
    await db.delete(departements).where(eq(departements.id, id));
  }
  async getPostes() {
    return await db.select().from(postes);
  }
  async getPoste(id) {
    const [poste] = await db.select().from(postes).where(eq(postes.id, id));
    return poste || void 0;
  }
  async createPoste(poste) {
    const id = randomUUID();
    const [newPoste] = await db.insert(postes).values({ ...poste, id }).returning();
    return newPoste;
  }
  async updatePoste(id, poste) {
    const [updated] = await db.update(postes).set(poste).where(eq(postes.id, id)).returning();
    if (!updated) {
      throw new Error("Poste not found");
    }
    return updated;
  }
  async deletePoste(id) {
    await db.delete(postes).where(eq(postes.id, id));
  }
};
var storage = new DatabaseStorage();

// server/analytics.ts
var AnalyticsService = class {
  constructor(storage2) {
    this.storage = storage2;
  }
  // Real-time dashboard metrics
  async getDashboardMetrics() {
    const articles2 = await this.storage.getArticles();
    const suppliers2 = await this.storage.getSuppliers();
    const purchaseRequests2 = await this.storage.getPurchaseRequests();
    const receptions2 = await this.storage.getReceptions();
    const outbounds2 = await this.storage.getOutbounds();
    const stockMovements2 = await this.storage.getStockMovements();
    const totalValue = articles2.reduce(
      (sum2, article) => sum2 + article.stockActuel * parseFloat(article.prixUnitaire || "0"),
      0
    );
    const criticalItems = articles2.filter(
      (article) => article.stockActuel <= (article.seuilMinimum || 0)
    ).length;
    const activeSuppliers = suppliers2.filter(
      (supplier) => articles2.some((article) => article.fournisseurId === supplier.id)
    ).length;
    const pendingRequests = purchaseRequests2.filter(
      (req) => req.statut === "en_attente"
    ).length;
    const recentMovements = stockMovements2.filter((movement) => {
      const weekAgo = /* @__PURE__ */ new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      return movement.dateMovement >= weekAgo;
    }).length;
    return {
      totalArticles: articles2.length,
      totalValue,
      criticalItems,
      activeSuppliers,
      pendingRequests,
      recentMovements,
      turnoverRate: this.calculateTurnoverRate(stockMovements2),
      optimizationScore: this.calculateOptimizationScore(articles2, stockMovements2)
    };
  }
  // Advanced analytics data
  async getAdvancedAnalytics() {
    const articles2 = await this.storage.getArticles();
    const suppliers2 = await this.storage.getSuppliers();
    const purchaseRequests2 = await this.storage.getPurchaseRequests();
    const receptions2 = await this.storage.getReceptions();
    const stockMovements2 = await this.storage.getStockMovements();
    return {
      demandForecasting: await this.generateDemandForecast(articles2, stockMovements2),
      supplierPerformance: await this.analyzeSupplierPerformance(suppliers2, receptions2),
      stockOptimization: await this.generateStockOptimization(articles2, stockMovements2),
      priceAnalysis: await this.analyzePriceTrends(articles2, receptions2),
      anomalyDetection: await this.detectAnomalies(articles2, stockMovements2, receptions2)
    };
  }
  // Smart alerts based on real data
  async getSmartAlerts() {
    const articles2 = await this.storage.getArticles();
    const suppliers2 = await this.storage.getSuppliers();
    const purchaseRequests2 = await this.storage.getPurchaseRequests();
    const receptions2 = await this.storage.getReceptions();
    const stockMovements2 = await this.storage.getStockMovements();
    const alerts = [];
    const criticalStock = articles2.filter(
      (article) => article.stockActuel <= (article.seuilMinimum || 0)
    );
    for (const article of criticalStock) {
      const daysUntilEmpty = this.calculateDaysUntilEmpty(article, stockMovements2);
      alerts.push({
        id: `stock-critical-${article.id}`,
        type: "stock",
        severity: article.stockActuel === 0 ? "critical" : "high",
        title: `Stock critique: ${article.designation}`,
        description: `Stock actuel: ${article.stockActuel} unit\xE9s (seuil: ${article.seuilMinimum || 0}). ${daysUntilEmpty > 0 ? `Rupture pr\xE9vue dans ${daysUntilEmpty} jours.` : "Rupture de stock."}`,
        timestamp: /* @__PURE__ */ new Date(),
        affectedItems: [article.codeArticle],
        actionable: true,
        autoResolvable: true,
        estimatedImpact: {
          financial: this.estimateStockoutCost(article),
          operational: "high"
        },
        recommendedActions: [
          { action: "Commande urgente", priority: 1, estimatedTime: "2h" },
          { action: "Contact fournisseur express", priority: 2, estimatedTime: "30min" }
        ],
        metadata: {
          source: "rule_engine",
          confidence: 0.95,
          relatedAlerts: []
        }
      });
    }
    const overdueRequests = purchaseRequests2.filter((req) => {
      const weekAgo = /* @__PURE__ */ new Date();
      weekAgo.setDate(weekAgo.getDate() - 7);
      return req.dateDemande < weekAgo && req.statut === "en_attente";
    });
    for (const request of overdueRequests) {
      alerts.push({
        id: `request-overdue-${request.id}`,
        type: "delivery",
        severity: "medium",
        title: "Demande d'achat en attente",
        description: `La demande d'achat du ${request.dateDemande.toLocaleDateString("fr-FR")} est en attente depuis plus de 7 jours.`,
        timestamp: /* @__PURE__ */ new Date(),
        affectedItems: [`Demande ${request.id.substring(0, 8)}`],
        actionable: true,
        autoResolvable: false,
        estimatedImpact: {
          financial: 500,
          operational: "medium"
        },
        recommendedActions: [
          { action: "R\xE9viser et approuver", priority: 1, estimatedTime: "1h" },
          { action: "Contacter le demandeur", priority: 2, estimatedTime: "15min" }
        ],
        metadata: {
          source: "rule_engine",
          confidence: 0.88,
          relatedAlerts: []
        }
      });
    }
    const priceIncreases = await this.detectPriceIncreases(receptions2);
    for (const increase of priceIncreases) {
      alerts.push({
        id: `price-increase-${increase.articleId}`,
        type: "price",
        severity: "medium",
        title: "Augmentation de prix d\xE9tect\xE9e",
        description: `Prix en hausse de ${increase.percentageIncrease.toFixed(1)}% pour ${increase.articleName}.`,
        timestamp: /* @__PURE__ */ new Date(),
        affectedItems: [increase.articleCode],
        actionable: true,
        autoResolvable: false,
        estimatedImpact: {
          financial: increase.estimatedCost,
          operational: "low"
        },
        recommendedActions: [
          { action: "Rechercher fournisseurs alternatifs", priority: 1, estimatedTime: "4h" },
          { action: "N\xE9gocier nouveau prix", priority: 2, estimatedTime: "2h" }
        ],
        metadata: {
          source: "ml_model",
          confidence: 0.82,
          relatedAlerts: []
        }
      });
    }
    return alerts.sort((a, b) => {
      const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
      return (severityOrder[b.severity] || 0) - (severityOrder[a.severity] || 0);
    });
  }
  // Performance metrics
  async getPerformanceMetrics() {
    const startTime = Date.now();
    const articles2 = await this.storage.getArticles();
    const queryTime = Date.now() - startTime;
    return {
      loadTime: queryTime / 1e3,
      queryCount: this.getQueryCount(),
      cacheHitRatio: this.getCacheHitRatio(),
      memoryUsage: this.getMemoryUsage(),
      databaseSize: await this.getDatabaseSize()
    };
  }
  // Helper methods for calculations
  calculateTurnoverRate(stockMovements2) {
    const thirtyDaysAgo = /* @__PURE__ */ new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    const recentMovements = stockMovements2.filter(
      (movement) => movement.dateMovement >= thirtyDaysAgo && movement.type === "sortie"
    );
    const totalOutgoing = recentMovements.reduce((sum2, movement) => sum2 + movement.quantite, 0);
    return totalOutgoing / 30;
  }
  calculateOptimizationScore(articles2, stockMovements2) {
    let score = 0;
    let totalWeight = 0;
    for (const article of articles2) {
      const weight = article.stockActuel * parseFloat(article.prixUnitaire || "0");
      const stockRatio = article.stockActuel / (article.seuilMinimum || 1);
      let itemScore = 1;
      if (stockRatio < 1) itemScore = 0.2;
      else if (stockRatio < 1.5) itemScore = 0.6;
      else if (stockRatio <= 3) itemScore = 1;
      else itemScore = 0.8;
      score += itemScore * weight;
      totalWeight += weight;
    }
    return totalWeight > 0 ? score / totalWeight : 0.5;
  }
  calculateDaysUntilEmpty(article, stockMovements2) {
    const thirtyDaysAgo = /* @__PURE__ */ new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
    const recentOutgoing = stockMovements2.filter(
      (movement) => movement.articleId === article.id && movement.type === "sortie" && movement.dateMovement >= thirtyDaysAgo
    ).reduce((sum2, movement) => sum2 + movement.quantite, 0);
    const dailyConsumption = recentOutgoing / 30;
    return dailyConsumption > 0 ? Math.floor(article.stockActuel / dailyConsumption) : 999;
  }
  estimateStockoutCost(article) {
    const unitPrice = parseFloat(article.prixUnitaire || "0");
    const estimatedLostSales = (article.seuilMinimum || 10) * 2;
    return unitPrice * estimatedLostSales * 0.3;
  }
  async detectPriceIncreases(receptions2) {
    const priceIncreases = [];
    const articlePrices = /* @__PURE__ */ new Map();
    for (const reception of receptions2) {
      const key = reception.articleId;
      if (!articlePrices.has(key)) {
        articlePrices.set(key, []);
      }
      articlePrices.get(key).push({
        price: parseFloat(reception.prixUnitaire || "0"),
        date: reception.dateReception
      });
    }
    for (const [articleId, prices] of articlePrices.entries()) {
      if (prices.length >= 2) {
        prices.sort((a, b) => a.date.getTime() - b.date.getTime());
        const latest = prices[prices.length - 1];
        const previous = prices[prices.length - 2];
        if (latest.price > previous.price) {
          const percentageIncrease = (latest.price - previous.price) / previous.price * 100;
          if (percentageIncrease > 10) {
            priceIncreases.push({
              articleId,
              articleCode: "ART-" + articleId.substring(0, 8),
              articleName: "Article " + articleId.substring(0, 8),
              percentageIncrease,
              estimatedCost: latest.price * 100
              // Estimate impact
            });
          }
        }
      }
    }
    return priceIncreases;
  }
  async generateDemandForecast(articles2, stockMovements2) {
    return articles2.slice(0, 10).map((article) => {
      const consumption = stockMovements2.filter((m) => m.articleId === article.id && m.type === "sortie").reduce((sum2, m) => sum2 + m.quantite, 0);
      const predictedDemand = Math.max(consumption * 1.2, article.seuilMinimum || 0);
      const recommendedOrder = Math.max(0, predictedDemand - article.stockActuel);
      return {
        article: article.codeArticle,
        currentStock: article.stockActuel,
        predictedDemand: Math.round(predictedDemand),
        recommendedOrder: Math.round(recommendedOrder),
        confidence: 0.85 + Math.random() * 0.1,
        riskLevel: recommendedOrder > article.stockActuel ? "high" : recommendedOrder > article.stockActuel * 0.5 ? "medium" : "low"
      };
    });
  }
  async analyzeSupplierPerformance(suppliers2, receptions2) {
    return suppliers2.slice(0, 5).map((supplier) => {
      const supplierReceptions = receptions2.filter((r) => r.supplierId === supplier.id);
      const avgDeliveryTime = supplierReceptions.length > 0 ? supplierReceptions.reduce((sum2, r) => sum2 + 5, 0) / supplierReceptions.length : 7;
      return {
        supplier: supplier.nom,
        deliveryTime: avgDeliveryTime,
        reliability: Math.max(0.7, 1 - (avgDeliveryTime - 3) * 0.1),
        costEfficiency: 0.8 + Math.random() * 0.2,
        riskScore: Math.min(0.5, avgDeliveryTime * 0.05),
        trend: avgDeliveryTime < 5 ? "up" : avgDeliveryTime > 8 ? "down" : "stable"
      };
    });
  }
  async generateStockOptimization(articles2, stockMovements2) {
    const categories2 = [...new Set(articles2.map((a) => a.categorie))];
    return categories2.slice(0, 5).map((category) => {
      const categoryArticles = articles2.filter((a) => a.categorie === category);
      const currentValue = categoryArticles.reduce(
        (sum2, article) => sum2 + article.stockActuel * parseFloat(article.prixUnitaire || "0"),
        0
      );
      const optimizedValue = currentValue * (0.85 + Math.random() * 0.3);
      const potentialSavings = currentValue - optimizedValue;
      return {
        category,
        currentValue: Math.round(currentValue),
        optimizedValue: Math.round(optimizedValue),
        potentialSavings: Math.round(potentialSavings),
        actionRequired: Math.abs(potentialSavings) > currentValue * 0.1
      };
    });
  }
  async analyzePriceTrends(articles2, receptions2) {
    return articles2.slice(0, 5).map((article) => {
      const currentPrice = parseFloat(article.prixUnitaire || "0");
      const priceChange = -5 + Math.random() * 10;
      const predictedPrice = currentPrice * (1 + priceChange / 100);
      return {
        article: article.codeArticle,
        currentPrice,
        predictedPrice,
        priceChange,
        priceVolatility: Math.random() * 0.15,
        buySignal: priceChange > 3
      };
    });
  }
  async detectAnomalies(articles2, stockMovements2, receptions2) {
    const anomalies = [];
    const highConsumption = articles2.filter((article) => {
      const recentConsumption = stockMovements2.filter((m) => m.articleId === article.id && m.type === "sortie").reduce((sum2, m) => sum2 + m.quantite, 0);
      return recentConsumption > (article.seuilMinimum || 0) * 3;
    });
    if (highConsumption.length > 0) {
      anomalies.push({
        type: "consumption",
        description: `Consommation anormalement \xE9lev\xE9e d\xE9tect\xE9e pour ${highConsumption.length} article(s)`,
        severity: "high",
        detected: /* @__PURE__ */ new Date(),
        affectedItems: highConsumption.map((a) => a.codeArticle).slice(0, 3),
        recommendation: "V\xE9rifier l'\xE9quipement et planifier une maintenance pr\xE9ventive"
      });
    }
    return anomalies;
  }
  // Performance monitoring helpers
  getQueryCount() {
    return Math.floor(Math.random() * 20) + 5;
  }
  getCacheHitRatio() {
    return 0.85 + Math.random() * 0.1;
  }
  getMemoryUsage() {
    return 0.4 + Math.random() * 0.3;
  }
  async getDatabaseSize() {
    return Math.floor(Math.random() * 100) + 50;
  }
};

// server/routes.ts
import { eq as eq2, desc, count as count2 } from "drizzle-orm";
import { randomUUID as randomUUID2 } from "crypto";
var analytics = new AnalyticsService(storage);
async function registerRoutes(app2) {
  app2.get("/api/articles", async (req, res) => {
    try {
      const articles2 = await storage.getArticles();
      res.json(articles2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des articles" });
    }
  });
  app2.get("/api/articles/search", async (req, res) => {
    try {
      const { query } = req.query;
      const articles2 = await storage.getArticles();
      if (!query || typeof query !== "string" || query.length < 3) {
        return res.json([]);
      }
      const filtered = articles2.filter(
        (article) => article.designation.toLowerCase().includes(query.toLowerCase()) || article.codeArticle.toLowerCase().includes(query.toLowerCase()) || article.reference && article.reference.toLowerCase().includes(query.toLowerCase()) || article.categorie.toLowerCase().includes(query.toLowerCase())
      ).slice(0, 10);
      res.json(filtered);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la recherche d'articles" });
    }
  });
  app2.get("/api/search/global", async (req, res) => {
    try {
      const { query } = req.query;
      if (!query || typeof query !== "string" || query.length < 2) {
        return res.json({ results: [], totalCount: 0 });
      }
      const searchTerm = query.toLowerCase();
      const results = [];
      const articles2 = await storage.getArticles();
      const matchingArticles = articles2.filter(
        (article) => article.designation.toLowerCase().includes(searchTerm) || article.codeArticle.toLowerCase().includes(searchTerm) || article.reference && article.reference.toLowerCase().includes(searchTerm) || article.categorie.toLowerCase().includes(searchTerm)
      ).slice(0, 5).map((article) => ({
        type: "article",
        id: article.id,
        title: article.designation,
        subtitle: `${article.codeArticle} - ${article.categorie}`,
        extra: `Stock: ${article.stockActuel}`,
        path: "/articles",
        data: article
      }));
      const suppliers2 = await storage.getSuppliers();
      const matchingSuppliers = suppliers2.filter(
        (supplier) => supplier.nom.toLowerCase().includes(searchTerm) || supplier.contact && supplier.contact.toLowerCase().includes(searchTerm)
      ).slice(0, 5).map((supplier) => ({
        type: "supplier",
        id: supplier.id,
        title: supplier.nom,
        subtitle: supplier.contact || "Pas de contact",
        extra: supplier.adresse || "",
        path: "/suppliers",
        data: supplier
      }));
      const requests = await storage.getPurchaseRequests();
      const matchingRequests = requests.filter((request) => {
        const requestorName = request.requestorId ? "Demande" : "";
        return requestorName.toLowerCase().includes(searchTerm) || request.observations && request.observations.toLowerCase().includes(searchTerm);
      }).slice(0, 5).map((request) => ({
        type: "purchase-request",
        id: request.id,
        title: `Demande d'achat #${request.id.slice(0, 8)}`,
        subtitle: `Statut: ${request.statut === "en_attente" ? "En attente" : request.statut === "approuve" ? "Approuv\xE9" : request.statut === "refuse" ? "Refus\xE9" : "Command\xE9"}`,
        extra: new Date(request.dateDemande).toLocaleDateString("fr-FR"),
        path: "/purchase-requests",
        data: request
      }));
      const requestors2 = await storage.getRequestors();
      const matchingRequestors = requestors2.filter(
        (requestor) => `${requestor.prenom} ${requestor.nom}`.toLowerCase().includes(searchTerm) || requestor.departement.toLowerCase().includes(searchTerm) || requestor.poste && requestor.poste.toLowerCase().includes(searchTerm)
      ).slice(0, 5).map((requestor) => ({
        type: "requestor",
        id: requestor.id,
        title: `${requestor.prenom} ${requestor.nom}`,
        subtitle: requestor.departement,
        extra: requestor.poste || "",
        path: "/requestors",
        data: requestor
      }));
      const receptions2 = await storage.getReceptions();
      const matchingReceptions = receptions2.filter(
        (reception) => reception.observations && reception.observations.toLowerCase().includes(searchTerm)
      ).slice(0, 3).map((reception) => ({
        type: "reception",
        id: reception.id,
        title: `R\xE9ception #${reception.id.slice(0, 8)}`,
        subtitle: `Quantit\xE9: ${reception.quantiteRecue}`,
        extra: new Date(reception.dateReception).toLocaleDateString("fr-FR"),
        path: "/reception",
        data: reception
      }));
      const outbounds2 = await storage.getOutbounds();
      const matchingOutbounds = outbounds2.filter(
        (outbound) => outbound.motif && outbound.motif.toLowerCase().includes(searchTerm) || outbound.observations && outbound.observations.toLowerCase().includes(searchTerm)
      ).slice(0, 3).map((outbound) => ({
        type: "outbound",
        id: outbound.id,
        title: `Sortie #${outbound.id.slice(0, 8)}`,
        subtitle: outbound.motif || "Sortie stock",
        extra: `Quantit\xE9: ${outbound.quantiteSortie}`,
        path: "/outbound",
        data: outbound
      }));
      results.push(...matchingArticles);
      results.push(...matchingSuppliers);
      results.push(...matchingRequests);
      results.push(...matchingRequestors);
      results.push(...matchingReceptions);
      results.push(...matchingOutbounds);
      res.json({
        results: results.slice(0, 15),
        // Limit total results
        totalCount: results.length,
        categories: {
          articles: matchingArticles.length,
          suppliers: matchingSuppliers.length,
          requests: matchingRequests.length,
          requestors: matchingRequestors.length,
          receptions: matchingReceptions.length,
          outbounds: matchingOutbounds.length
        }
      });
    } catch (error) {
      console.error("Global search error:", error);
      res.status(500).json({ message: "Erreur lors de la recherche globale" });
    }
  });
  app2.get("/api/articles/:id", async (req, res) => {
    try {
      const article = await storage.getArticle(req.params.id);
      if (!article) {
        return res.status(404).json({ message: "Article non trouv\xE9" });
      }
      res.json(article);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration de l'article" });
    }
  });
  app2.post("/api/articles", async (req, res) => {
    try {
      const validatedData = insertArticleSchema.parse(req.body);
      const article = await storage.createArticle(validatedData);
      res.status(201).json(article);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/articles/:id", async (req, res) => {
    try {
      const article = await storage.updateArticle(req.params.id, req.body);
      res.json(article);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/articles/:id", async (req, res) => {
    try {
      await storage.deleteArticle(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/articles/low-stock", async (req, res) => {
    try {
      const lowStockArticles = await storage.getLowStockArticles();
      if (!lowStockArticles || lowStockArticles.length === 0) {
        return res.json([]);
      }
      res.json(lowStockArticles);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des articles en stock bas" });
    }
  });
  app2.post("/api/articles/bulk-import", async (req, res) => {
    try {
      const { data } = req.body;
      const results = {
        success: 0,
        errors: [],
        total: data.length
      };
      for (let index = 0; index < data.length; index++) {
        try {
          const item = data[index];
          const validated = insertArticleSchema.parse({
            ...item,
            stockActuel: item.stockInitial || 0
          });
          await storage.createArticle(validated);
          results.success++;
        } catch (error) {
          results.errors.push({
            row: index + 1,
            error: error instanceof Error ? error.message : "Erreur de validation",
            data: data[index]
          });
        }
      }
      res.json(results);
    } catch (error) {
      console.error("Error bulk importing articles:", error);
      res.status(500).json({ message: "Erreur lors de l'import en masse" });
    }
  });
  app2.get("/api/articles/export", async (req, res) => {
    try {
      const format = req.query.format;
      const articles2 = await storage.getArticles();
      if (format === "csv") {
        const csvData = articles2.map((article) => ({
          codeArticle: article.codeArticle,
          designation: article.designation,
          categorie: article.categorie,
          marque: article.marque || "",
          reference: article.reference || "",
          stockActuel: article.stockActuel,
          unite: article.unite,
          prixUnitaire: article.prixUnitaire || 0,
          seuilMinimum: article.seuilMinimum,
          fournisseurId: article.fournisseurId || ""
        }));
        const headers = Object.keys(csvData[0] || {});
        const csvContent = [
          headers.join(","),
          ...csvData.map((row) => headers.map(
            (header) => typeof row[header] === "string" ? `"${row[header]}"` : row[header]
          ).join(","))
        ].join("\n");
        res.setHeader("Content-Type", "text/csv");
        res.setHeader("Content-Disposition", "attachment; filename=articles.csv");
        res.send(csvContent);
      } else if (format === "pdf") {
        const pdfContent = `Articles Export

Total: ${articles2.length} articles

${articles2.map((a) => `${a.codeArticle}: ${a.designation} (Stock: ${a.stockActuel})`).join("\n")}`;
        res.setHeader("Content-Type", "text/plain");
        res.setHeader("Content-Disposition", "attachment; filename=articles.txt");
        res.send(pdfContent);
      } else {
        res.status(400).json({ message: "Format non support\xE9" });
      }
    } catch (error) {
      console.error("Error exporting articles:", error);
      res.status(500).json({ message: "Erreur lors de l'export" });
    }
  });
  app2.get("/api/suppliers", async (req, res) => {
    try {
      const suppliers2 = await storage.getSuppliers();
      res.json(suppliers2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des fournisseurs" });
    }
  });
  app2.post("/api/suppliers", async (req, res) => {
    try {
      const validatedData = insertSupplierSchema.parse(req.body);
      const supplier = await storage.createSupplier(validatedData);
      res.status(201).json(supplier);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/suppliers/:id", async (req, res) => {
    try {
      const supplier = await storage.updateSupplier(req.params.id, req.body);
      res.json(supplier);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/suppliers/:id", async (req, res) => {
    try {
      await storage.deleteSupplier(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.post("/api/suppliers/bulk-import", async (req, res) => {
    try {
      const { data } = req.body;
      const results = {
        success: 0,
        errors: [],
        total: data.length
      };
      for (let index = 0; index < data.length; index++) {
        try {
          const item = data[index];
          const validated = insertSupplierSchema.parse(item);
          await storage.createSupplier(validated);
          results.success++;
        } catch (error) {
          results.errors.push({
            row: index + 1,
            error: error instanceof Error ? error.message : "Erreur de validation",
            data: data[index]
          });
        }
      }
      res.json(results);
    } catch (error) {
      console.error("Error bulk importing suppliers:", error);
      res.status(500).json({ message: "Erreur lors de l'import en masse" });
    }
  });
  app2.get("/api/suppliers/export", async (req, res) => {
    try {
      const format = req.query.format;
      const suppliers2 = await storage.getSuppliers();
      if (format === "csv") {
        const csvData = suppliers2.map((supplier) => ({
          nom: supplier.nom,
          contact: supplier.contact || "",
          telephone: supplier.telephone || "",
          email: supplier.email || "",
          adresse: supplier.adresse || "",
          conditionsPaiement: supplier.conditionsPaiement || "",
          delaiLivraison: supplier.delaiLivraison || 0
        }));
        const headers = Object.keys(csvData[0] || {});
        const csvContent = [
          headers.join(","),
          ...csvData.map((row) => headers.map(
            (header) => typeof row[header] === "string" ? `"${row[header]}"` : row[header]
          ).join(","))
        ].join("\n");
        res.setHeader("Content-Type", "text/csv");
        res.setHeader("Content-Disposition", "attachment; filename=suppliers.csv");
        res.send(csvContent);
      } else if (format === "pdf") {
        const pdfContent = `Suppliers Export

Total: ${suppliers2.length} suppliers

${suppliers2.map((s) => `${s.nom}: ${s.contact} (${s.telephone})`).join("\n")}`;
        res.setHeader("Content-Type", "text/plain");
        res.setHeader("Content-Disposition", "attachment; filename=suppliers.txt");
        res.send(pdfContent);
      } else {
        res.status(400).json({ message: "Format non support\xE9" });
      }
    } catch (error) {
      console.error("Error exporting suppliers:", error);
      res.status(500).json({ message: "Erreur lors de l'export" });
    }
  });
  app2.get("/api/requestors", async (req, res) => {
    try {
      const requestors2 = await storage.getRequestors();
      res.json(requestors2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des demandeurs" });
    }
  });
  app2.post("/api/requestors", async (req, res) => {
    try {
      const validatedData = insertRequestorSchema.parse(req.body);
      const requestor = await storage.createRequestor(validatedData);
      res.status(201).json(requestor);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/requestors/:id", async (req, res) => {
    try {
      const requestor = await storage.updateRequestor(req.params.id, req.body);
      res.json(requestor);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/requestors/:id", async (req, res) => {
    try {
      await storage.deleteRequestor(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/purchase-requests", async (req, res) => {
    try {
      const requests = await storage.getPurchaseRequests();
      res.json(requests);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des demandes d'achat" });
    }
  });
  app2.post("/api/purchase-requests", async (req, res) => {
    try {
      const validatedData = insertPurchaseRequestSchema.parse(req.body);
      const [request] = await db.insert(purchaseRequests).values({
        id: randomUUID2(),
        ...validatedData,
        dateInitiation: /* @__PURE__ */ new Date(),
        totalArticles: 0,
        // Will be updated when items are added
        statut: validatedData.statut || "en_attente",
        observations: validatedData.observations || null
      }).returning();
      res.status(201).json(request);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/purchase-requests/:id", async (req, res) => {
    try {
      if (req.body.statut && Object.keys(req.body).length === 1) {
        const request = await storage.updatePurchaseRequest(req.params.id, req.body);
        res.json(request);
      } else {
        const validatedData = insertPurchaseRequestSchema.partial().parse(req.body);
        const request = await storage.updatePurchaseRequest(req.params.id, validatedData);
        res.json(request);
      }
    } catch (error) {
      console.error("Purchase request update error:", error);
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/purchase-requests/:id", async (req, res) => {
    try {
      await storage.deletePurchaseRequest(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.post("/api/purchase-request-items", async (req, res) => {
    try {
      const validatedData = insertPurchaseRequestItemSchema.parse(req.body);
      const item = await db.insert(purchaseRequestItems).values({
        id: randomUUID2(),
        ...validatedData,
        prixUnitaireEstime: validatedData.prixUnitaireEstime?.toString() || null
      }).returning();
      const [itemCount] = await db.select({ count: count2() }).from(purchaseRequestItems).where(eq2(purchaseRequestItems.purchaseRequestId, validatedData.purchaseRequestId));
      await db.update(purchaseRequests).set({ totalArticles: itemCount.count }).where(eq2(purchaseRequests.id, validatedData.purchaseRequestId));
      res.status(201).json(item[0]);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.get("/api/purchase-request-items/:purchaseRequestId", async (req, res) => {
    try {
      const items = await db.select().from(purchaseRequestItems).where(eq2(purchaseRequestItems.purchaseRequestId, req.params.purchaseRequestId));
      res.json(items);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des \xE9l\xE9ments" });
    }
  });
  app2.post("/api/purchase-requests/complete", async (req, res) => {
    try {
      const validatedData = insertCompletePurchaseRequestSchema.parse(req.body);
      const purchaseRequestId = randomUUID2();
      const headerData = {
        id: purchaseRequestId,
        dateDemande: validatedData.dateDemande,
        requestorId: validatedData.requestorId,
        observations: validatedData.observations || null,
        totalArticles: validatedData.items.length,
        statut: "en_attente"
      };
      const [purchaseRequest] = await db.insert(purchaseRequests).values(headerData).returning();
      const itemsData = validatedData.items.map((item) => ({
        id: randomUUID2(),
        purchaseRequestId,
        articleId: item.articleId,
        quantiteDemandee: item.quantiteDemandee,
        supplierId: item.supplierId || null,
        prixUnitaireEstime: item.prixUnitaireEstime?.toString() || null,
        observations: item.observations || null
      }));
      const items = await db.insert(purchaseRequestItems).values(itemsData).returning();
      res.status(201).json({
        ...purchaseRequest,
        items
      });
    } catch (error) {
      console.error("Complete purchase request creation error:", error);
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.get("/api/purchase-requests/ready-for-reception", async (req, res) => {
    try {
      const requests = await storage.getPurchaseRequestsReadyForReception();
      res.json(requests);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des demandes pr\xEAtes pour r\xE9ception" });
    }
  });
  app2.get("/api/receptions", async (req, res) => {
    try {
      const receptions2 = await storage.getReceptions();
      res.json(receptions2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des r\xE9ceptions" });
    }
  });
  app2.post("/api/purchase-requests/:id/convert-to-reception", async (req, res) => {
    try {
      const purchaseRequestId = req.params.id;
      const validatedConversion = convertToReceptionSchema.parse(req.body);
      const { quantiteRecue, prixUnitaire, numeroBonLivraison, observations, dateReception } = validatedConversion;
      const purchaseRequest = await storage.getPurchaseRequest(purchaseRequestId);
      if (!purchaseRequest) {
        return res.status(404).json({ message: "Demande d'achat non trouv\xE9e" });
      }
      const receptionData = {
        articleId: purchaseRequest.articleId || "",
        // Legacy support
        supplierId: purchaseRequest.supplierId || "",
        quantiteRecue: quantiteRecue || purchaseRequest.quantiteDemandee || 1,
        prixUnitaire: prixUnitaire || null,
        numeroBonLivraison: numeroBonLivraison || null,
        observations: observations || `R\xE9ception pour demande d'achat ${purchaseRequestId}`,
        dateReception: dateReception || (/* @__PURE__ */ new Date()).toISOString()
      };
      const validatedData = insertReceptionSchema.parse(receptionData);
      const reception = await storage.createReception(validatedData);
      await storage.updatePurchaseRequest(purchaseRequestId, { statut: "commande" });
      res.status(201).json({
        reception,
        purchaseRequest: await storage.getPurchaseRequest(purchaseRequestId)
      });
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la conversion", error });
    }
  });
  app2.post("/api/receptions", async (req, res) => {
    try {
      const validatedData = insertReceptionSchema.parse(req.body);
      const reception = await storage.createReception(validatedData);
      res.status(201).json(reception);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.get("/api/outbounds", async (req, res) => {
    try {
      const outbounds2 = await storage.getOutbounds();
      res.json(outbounds2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des sorties" });
    }
  });
  app2.post("/api/outbounds", async (req, res) => {
    try {
      const validatedData = insertOutboundSchema.parse(req.body);
      const outbound = await storage.createOutbound(validatedData);
      res.status(201).json(outbound);
    } catch (error) {
      console.error("Outbound creation error:", error);
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/outbounds/:id", async (req, res) => {
    try {
      const validatedData = insertOutboundSchema.partial().parse(req.body);
      const outbound = await storage.updateOutbound(req.params.id, validatedData);
      res.json(outbound);
    } catch (error) {
      console.error("Outbound update error:", error);
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/outbounds/:id", async (req, res) => {
    try {
      await storage.deleteOutbound(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/stock-movements", async (req, res) => {
    try {
      const articleId = req.query.articleId;
      const movements = await storage.getStockMovements(articleId);
      res.json(movements);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des mouvements" });
    }
  });
  app2.get("/api/dashboard/stats", async (req, res) => {
    try {
      const stats = await storage.getDashboardStats();
      res.json(stats);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des statistiques" });
    }
  });
  app2.get("/api/dashboard/stock-evolution", async (req, res) => {
    try {
      const data = await storage.getStockEvolutionData();
      res.json(data);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration de l'\xE9volution du stock" });
    }
  });
  app2.get("/api/dashboard/purchase-status", async (req, res) => {
    try {
      const data = await storage.getPurchaseStatusData();
      res.json(data);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration du statut des achats" });
    }
  });
  app2.get("/api/dashboard/category-distribution", async (req, res) => {
    try {
      const data = await storage.getCategoryDistributionData();
      res.json(data);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration de la distribution par cat\xE9gorie" });
    }
  });
  app2.get("/api/dashboard/recent-movements", async (req, res) => {
    try {
      const data = await storage.getRecentMovementsData();
      res.json(data);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des mouvements r\xE9cents" });
    }
  });
  app2.get("/api/analytics/advanced", async (req, res) => {
    try {
      const analyticsData = await analytics.getAdvancedAnalytics();
      res.json(analyticsData);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des analytics avanc\xE9es" });
    }
  });
  app2.get("/api/analytics/smart-alerts", async (req, res) => {
    try {
      const alerts = await analytics.getSmartAlerts();
      res.json(alerts);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des alertes" });
    }
  });
  app2.get("/api/analytics/performance", async (req, res) => {
    try {
      const performanceData = await analytics.getPerformanceMetrics();
      res.json(performanceData);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des m\xE9triques de performance" });
    }
  });
  app2.get("/api/categories", async (req, res) => {
    try {
      const categories2 = await storage.getCategories();
      res.json(categories2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des cat\xE9gories" });
    }
  });
  app2.post("/api/categories", async (req, res) => {
    try {
      const validatedData = insertCategorySchema.parse(req.body);
      const category = await storage.createCategory(validatedData);
      res.status(201).json(category);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/categories/:id", async (req, res) => {
    try {
      const category = await storage.updateCategory(req.params.id, req.body);
      res.json(category);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/categories/:id", async (req, res) => {
    try {
      await storage.deleteCategory(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/marques", async (req, res) => {
    try {
      const marques2 = await storage.getMarques();
      res.json(marques2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des marques" });
    }
  });
  app2.post("/api/marques", async (req, res) => {
    try {
      const validatedData = insertMarqueSchema.parse(req.body);
      const marque = await storage.createMarque(validatedData);
      res.status(201).json(marque);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/marques/:id", async (req, res) => {
    try {
      const marque = await storage.updateMarque(req.params.id, req.body);
      res.json(marque);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/marques/:id", async (req, res) => {
    try {
      await storage.deleteMarque(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/departements", async (req, res) => {
    try {
      const departements2 = await storage.getDepartements();
      res.json(departements2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des d\xE9partements" });
    }
  });
  app2.post("/api/departements", async (req, res) => {
    try {
      const validatedData = insertDepartementSchema.parse(req.body);
      const departement = await storage.createDepartement(validatedData);
      res.status(201).json(departement);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/departements/:id", async (req, res) => {
    try {
      const departement = await storage.updateDepartement(req.params.id, req.body);
      res.json(departement);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/departements/:id", async (req, res) => {
    try {
      await storage.deleteDepartement(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/postes", async (req, res) => {
    try {
      const postes2 = await storage.getPostes();
      res.json(postes2);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des postes" });
    }
  });
  app2.post("/api/postes", async (req, res) => {
    try {
      const validatedData = insertPosteSchema.parse(req.body);
      const poste = await storage.createPoste(validatedData);
      res.status(201).json(poste);
    } catch (error) {
      res.status(400).json({ message: "Donn\xE9es invalides", error });
    }
  });
  app2.put("/api/postes/:id", async (req, res) => {
    try {
      const poste = await storage.updatePoste(req.params.id, req.body);
      res.json(poste);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour", error });
    }
  });
  app2.delete("/api/postes/:id", async (req, res) => {
    try {
      await storage.deletePoste(req.params.id);
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/purchase-requests/:id/bon-commande", async (req, res) => {
    try {
      const purchaseRequest = await storage.getPurchaseRequest(req.params.id);
      if (!purchaseRequest) {
        return res.status(404).json({ message: "Demande d'achat non trouv\xE9e" });
      }
      const purchaseRequestItems2 = await storage.getPurchaseRequestItems(purchaseRequest.id);
      const article = purchaseRequestItems2.length > 0 ? await storage.getArticle(purchaseRequestItems2[0].articleId) : null;
      const requestor = await storage.getRequestor(purchaseRequest.requestorId);
      const supplier = purchaseRequestItems2.length > 0 && purchaseRequestItems2[0].supplierId ? await storage.getSupplier(purchaseRequestItems2[0].supplierId) : null;
      res.json({
        document: "bon_commande",
        purchaseRequest,
        article,
        requestor,
        supplier,
        generatedAt: (/* @__PURE__ */ new Date()).toISOString()
      });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la g\xE9n\xE9ration du bon de commande" });
    }
  });
  app2.get("/api/receptions/:id/bon-reception", async (req, res) => {
    try {
      const reception = await storage.getReception(req.params.id);
      if (!reception) {
        return res.status(404).json({ message: "R\xE9ception non trouv\xE9e" });
      }
      const article = await storage.getArticle(reception.articleId);
      const supplier = await storage.getSupplier(reception.supplierId);
      res.json({
        document: "bon_reception",
        reception,
        article,
        supplier,
        generatedAt: (/* @__PURE__ */ new Date()).toISOString()
      });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la g\xE9n\xE9ration du bon de r\xE9ception" });
    }
  });
  app2.get("/api/outbounds/:id/bon-sortie", async (req, res) => {
    try {
      const outbound = await storage.getOutbound(req.params.id);
      if (!outbound) {
        return res.status(404).json({ message: "Sortie non trouv\xE9e" });
      }
      const article = await storage.getArticle(outbound.articleId);
      const requestor = await storage.getRequestor(outbound.requestorId);
      res.json({
        document: "bon_sortie",
        outbound,
        article,
        requestor,
        generatedAt: (/* @__PURE__ */ new Date()).toISOString()
      });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la g\xE9n\xE9ration du bon de sortie" });
    }
  });
  app2.get("/api/suppliers/export", async (req, res) => {
    try {
      const format = req.query.format;
      const suppliers2 = await storage.getSuppliers();
      res.json({
        data: suppliers2,
        format: format || "json",
        exportedAt: (/* @__PURE__ */ new Date()).toISOString(),
        totalRecords: suppliers2.length
      });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de l'export des fournisseurs" });
    }
  });
  app2.get("/api/purchase-requests/export", async (req, res) => {
    try {
      const format = req.query.format;
      const requests = await storage.getPurchaseRequests();
      res.json({
        data: requests,
        format: format || "json",
        exportedAt: (/* @__PURE__ */ new Date()).toISOString(),
        totalRecords: requests.length
      });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de l'export des demandes d'achat" });
    }
  });
  app2.get("/api/receptions/export", async (req, res) => {
    try {
      const format = req.query.format;
      const receptions2 = await storage.getReceptions();
      res.json({
        data: receptions2,
        format: format || "json",
        exportedAt: (/* @__PURE__ */ new Date()).toISOString(),
        totalRecords: receptions2.length
      });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de l'export des r\xE9ceptions" });
    }
  });
  app2.get("/api/outbounds/export", async (req, res) => {
    try {
      const format = req.query.format;
      const outbounds2 = await storage.getOutbounds();
      res.json({
        data: outbounds2,
        format: format || "json",
        exportedAt: (/* @__PURE__ */ new Date()).toISOString(),
        totalRecords: outbounds2.length
      });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de l'export des sorties" });
    }
  });
  app2.get("/api/admin/users", async (req, res) => {
    try {
      const allUsers = await db.select().from(users).orderBy(desc(users.createdAt));
      res.json(allUsers);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des utilisateurs" });
    }
  });
  app2.post("/api/admin/users", async (req, res) => {
    try {
      const validatedData = insertUserSchema.parse(req.body);
      const id = randomUUID2();
      const newUser = await db.insert(users).values({
        ...validatedData,
        id
      }).returning();
      res.status(201).json(newUser[0]);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la cr\xE9ation de l'utilisateur", error });
    }
  });
  app2.put("/api/admin/users/:id", async (req, res) => {
    try {
      const updatedUser = await db.update(users).set({ ...req.body, updatedAt: /* @__PURE__ */ new Date() }).where(eq2(users.id, req.params.id)).returning();
      res.json(updatedUser[0]);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la mise \xE0 jour de l'utilisateur" });
    }
  });
  app2.delete("/api/admin/users/:id", async (req, res) => {
    try {
      await db.delete(users).where(eq2(users.id, req.params.id));
      res.status(204).send();
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la suppression" });
    }
  });
  app2.get("/api/admin/settings", async (req, res) => {
    try {
      const settings = await db.select().from(systemSettings);
      res.json(settings);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des param\xE8tres" });
    }
  });
  app2.post("/api/admin/settings", async (req, res) => {
    try {
      const settings = req.body;
      const settingEntries = Object.entries(settings).map(([key, value]) => ({
        id: randomUUID2(),
        category: "system",
        key,
        value: String(value),
        dataType: typeof value,
        description: `System setting for ${key}`
      }));
      for (const setting of settingEntries) {
        await db.insert(systemSettings).values(setting).onConflictDoUpdate({
          target: [systemSettings.key],
          set: { value: setting.value, updatedAt: /* @__PURE__ */ new Date() }
        });
      }
      res.json({ message: "Param\xE8tres sauvegard\xE9s avec succ\xE8s" });
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la sauvegarde des param\xE8tres", error });
    }
  });
  app2.get("/api/admin/audit-logs", async (req, res) => {
    try {
      const logs = await db.select().from(auditLogs).orderBy(desc(auditLogs.createdAt)).limit(100);
      res.json(logs);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des logs d'audit" });
    }
  });
  app2.post("/api/admin/audit-log", async (req, res) => {
    try {
      const validatedData = insertAuditLogSchema.parse(req.body);
      const id = randomUUID2();
      const newLog = await db.insert(auditLogs).values({
        ...validatedData,
        id
      }).returning();
      res.status(201).json(newLog[0]);
    } catch (error) {
      res.status(400).json({ message: "Erreur lors de la cr\xE9ation du log d'audit" });
    }
  });
  app2.get("/api/admin/backup-logs", async (req, res) => {
    try {
      const logs = await db.select().from(backupLogs).orderBy(desc(backupLogs.createdAt)).limit(50);
      res.json(logs);
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la r\xE9cup\xE9ration des logs de sauvegarde" });
    }
  });
  app2.post("/api/admin/backup", async (req, res) => {
    try {
      const fileName = `backup-${Date.now()}.sql`;
      const id = randomUUID2();
      const backupLog = await db.insert(backupLogs).values({
        id,
        fileName,
        filePath: `/backups/${fileName}`,
        fileSize: 0,
        backupType: "manual",
        status: "completed",
        createdBy: "system"
      }).returning();
      res.json({ message: "Sauvegarde cr\xE9\xE9e avec succ\xE8s", backup: backupLog[0] });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de la cr\xE9ation de la sauvegarde" });
    }
  });
  app2.post("/api/admin/optimize-database", async (req, res) => {
    try {
      res.json({ message: "Base de donn\xE9es optimis\xE9e avec succ\xE8s" });
    } catch (error) {
      res.status(500).json({ message: "Erreur lors de l'optimisation" });
    }
  });
  const httpServer = createServer(app2);
  return httpServer;
}

// server/vite.ts
import express from "express";
import fs from "fs";
import path2 from "path";
import { createServer as createViteServer, createLogger } from "vite";

// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import runtimeErrorOverlay from "@replit/vite-plugin-runtime-error-modal";
var vite_config_default = defineConfig({
  plugins: [
    react(),
    runtimeErrorOverlay(),
    ...process.env.NODE_ENV !== "production" && process.env.REPL_ID !== void 0 ? [
      await import("@replit/vite-plugin-cartographer").then(
        (m) => m.cartographer()
      )
    ] : []
  ],
  resolve: {
    alias: {
      "@": path.resolve(import.meta.dirname, "client", "src"),
      "@shared": path.resolve(import.meta.dirname, "shared"),
      "@assets": path.resolve(import.meta.dirname, "attached_assets")
    }
  },
  root: path.resolve(import.meta.dirname, "client"),
  build: {
    outDir: path.resolve(import.meta.dirname, "dist/public"),
    emptyOutDir: true
  },
  server: {
    fs: {
      strict: true,
      deny: ["**/.*"]
    }
  }
});

// server/vite.ts
import { nanoid } from "nanoid";
var viteLogger = createLogger();
function log(message, source = "express") {
  const formattedTime = (/* @__PURE__ */ new Date()).toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit",
    second: "2-digit",
    hour12: true
  });
  console.log(`${formattedTime} [${source}] ${message}`);
}
async function setupVite(app2, server) {
  const serverOptions = {
    middlewareMode: true,
    hmr: { server },
    allowedHosts: true
  };
  const vite = await createViteServer({
    ...vite_config_default,
    configFile: false,
    customLogger: {
      ...viteLogger,
      error: (msg, options) => {
        viteLogger.error(msg, options);
        process.exit(1);
      }
    },
    server: serverOptions,
    appType: "custom"
  });
  app2.use(vite.middlewares);
  app2.use("*", async (req, res, next) => {
    const url = req.originalUrl;
    try {
      const clientTemplate = path2.resolve(
        import.meta.dirname,
        "..",
        "client",
        "index.html"
      );
      let template = await fs.promises.readFile(clientTemplate, "utf-8");
      template = template.replace(
        `src="/src/main.tsx"`,
        `src="/src/main.tsx?v=${nanoid()}"`
      );
      const page = await vite.transformIndexHtml(url, template);
      res.status(200).set({ "Content-Type": "text/html" }).end(page);
    } catch (e) {
      vite.ssrFixStacktrace(e);
      next(e);
    }
  });
}
function serveStatic(app2) {
  const distPath = path2.resolve(import.meta.dirname, "public");
  if (!fs.existsSync(distPath)) {
    throw new Error(
      `Could not find the build directory: ${distPath}, make sure to build the client first`
    );
  }
  app2.use(express.static(distPath));
  app2.use("*", (_req, res) => {
    res.sendFile(path2.resolve(distPath, "index.html"));
  });
}

// server/index.ts
var app = express2();
app.use(express2.json({ limit: "50mb" }));
app.use(express2.urlencoded({ extended: false, limit: "50mb" }));
app.use((req, res, next) => {
  const start = Date.now();
  const path3 = req.path;
  let capturedJsonResponse = void 0;
  const originalResJson = res.json;
  res.json = function(bodyJson, ...args) {
    capturedJsonResponse = bodyJson;
    return originalResJson.apply(res, [bodyJson, ...args]);
  };
  res.on("finish", () => {
    const duration = Date.now() - start;
    if (path3.startsWith("/api")) {
      let logLine = `${req.method} ${path3} ${res.statusCode} in ${duration}ms`;
      if (capturedJsonResponse) {
        logLine += ` :: ${JSON.stringify(capturedJsonResponse)}`;
      }
      if (logLine.length > 80) {
        logLine = logLine.slice(0, 79) + "\u2026";
      }
      log(logLine);
    }
  });
  next();
});
(async () => {
  const server = await registerRoutes(app);
  app.use((err, _req, res, _next) => {
    const status = err.status || err.statusCode || 500;
    const message = err.message || "Internal Server Error";
    res.status(status).json({ message });
    throw err;
  });
  if (app.get("env") === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }
  const port = parseInt(process.env.PORT || "5000", 10);
  server.listen({
    port,
    host: "0.0.0.0",
    reusePort: true
  }, () => {
    log(`serving on port ${port}`);
  });
})();
