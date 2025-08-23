var __defProp = Object.defineProperty;
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};

// server/index-desktop.ts
import express from "express";
import path2 from "path";
import { fileURLToPath } from "url";

// server/db-local.ts
import Database from "better-sqlite3";
import { drizzle } from "drizzle-orm/better-sqlite3";

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

// server/db-local.ts
import path from "path";
import fs from "fs";
var getUserDataPath = () => {
  if (process.env.NODE_ENV === "development") {
    return path.join(process.cwd(), "data");
  }
  return path.join(process.cwd(), "data");
};
var dataDir = getUserDataPath();
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}
var dbPath = path.join(dataDir, "stockceramique.db");
var sqlite = new Database(dbPath);
sqlite.pragma("foreign_keys = ON");
var db = drizzle(sqlite, { schema: schema_exports });
var initializeDatabase = () => {
  try {
    console.log("Initializing local SQLite database...");
    console.log("Database path:", dbPath);
    const schemaSQL = `
      -- Articles table
      CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reference TEXT NOT NULL UNIQUE,
        designation TEXT NOT NULL,
        stock_quantity INTEGER NOT NULL DEFAULT 0,
        min_stock INTEGER NOT NULL DEFAULT 0,
        unit_price REAL NOT NULL DEFAULT 0,
        supplier_id INTEGER,
        category TEXT,
        location TEXT,
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch()),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
      );

      -- Suppliers table
      CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        contact_person TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch())
      );

      -- Requestors table
      CREATE TABLE IF NOT EXISTS requestors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        email TEXT,
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch())
      );

      -- Purchase Requests table
      CREATE TABLE IF NOT EXISTS purchase_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        requestor_id INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        total_amount REAL NOT NULL DEFAULT 0,
        notes TEXT,
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch()),
        FOREIGN KEY (requestor_id) REFERENCES requestors(id)
      );

      -- Purchase Request Items table
      CREATE TABLE IF NOT EXISTS purchase_request_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase_request_id INTEGER NOT NULL,
        article_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        supplier_id INTEGER,
        FOREIGN KEY (purchase_request_id) REFERENCES purchase_requests(id) ON DELETE CASCADE,
        FOREIGN KEY (article_id) REFERENCES articles(id),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
      );

      -- Receptions table
      CREATE TABLE IF NOT EXISTS receptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        purchase_request_id INTEGER,
        supplier_id INTEGER NOT NULL,
        delivery_note TEXT,
        total_amount REAL NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'pending',
        received_at INTEGER DEFAULT (unixepoch()),
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch()),
        FOREIGN KEY (purchase_request_id) REFERENCES purchase_requests(id),
        FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
      );

      -- Reception Items table
      CREATE TABLE IF NOT EXISTS reception_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        reception_id INTEGER NOT NULL,
        article_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (reception_id) REFERENCES receptions(id) ON DELETE CASCADE,
        FOREIGN KEY (article_id) REFERENCES articles(id)
      );

      -- Outbounds table
      CREATE TABLE IF NOT EXISTS outbounds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        requestor_id INTEGER NOT NULL,
        total_quantity INTEGER NOT NULL DEFAULT 0,
        notes TEXT,
        created_at INTEGER DEFAULT (unixepoch()),
        updated_at INTEGER DEFAULT (unixepoch()),
        FOREIGN KEY (requestor_id) REFERENCES requestors(id)
      );

      -- Outbound Items table
      CREATE TABLE IF NOT EXISTS outbound_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        outbound_id INTEGER NOT NULL,
        article_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (outbound_id) REFERENCES outbounds(id) ON DELETE CASCADE,
        FOREIGN KEY (article_id) REFERENCES articles(id)
      );

      -- Stock Movements table
      CREATE TABLE IF NOT EXISTS stock_movements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        article_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        reference_id INTEGER,
        reference_type TEXT,
        notes TEXT,
        created_at INTEGER DEFAULT (unixepoch()),
        FOREIGN KEY (article_id) REFERENCES articles(id)
      );

      -- Create indexes for better performance
      CREATE INDEX IF NOT EXISTS idx_articles_reference ON articles(reference);
      CREATE INDEX IF NOT EXISTS idx_articles_supplier ON articles(supplier_id);
      CREATE INDEX IF NOT EXISTS idx_stock_movements_article ON stock_movements(article_id);
      CREATE INDEX IF NOT EXISTS idx_stock_movements_type ON stock_movements(type);
      CREATE INDEX IF NOT EXISTS idx_purchase_requests_status ON purchase_requests(status);
      CREATE INDEX IF NOT EXISTS idx_receptions_status ON receptions(status);
    `;
    sqlite.exec(schemaSQL);
    console.log("\u2705 Database initialized successfully");
    return true;
  } catch (error) {
    console.error("\u274C Error initializing database:", error);
    return false;
  }
};
var sqlite3 = sqlite;
process.on("exit", () => {
  sqlite.close();
});
process.on("SIGINT", () => {
  sqlite.close();
  process.exit(0);
});

// server/index-desktop.ts
var __filename = typeof __filename !== "undefined" ? __filename : fileURLToPath(import.meta.url);
var __dirname = typeof __dirname !== "undefined" ? __dirname : path2.dirname(__filename);
var app = express();
var PORT = parseInt(process.env.DESKTOP_PORT || "3001");
app.use(express.json({ limit: "10mb" }));
app.use(express.urlencoded({ extended: true }));
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, PATCH");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
  if (req.method === "OPTIONS") {
    res.sendStatus(200);
  } else {
    next();
  }
});
var dbInitialized = initializeDatabase();
if (!dbInitialized) {
  console.error("Failed to initialize database");
  process.exit(1);
}
app.get("/api/health", (req, res) => {
  res.json({
    status: "Desktop server running",
    database: "SQLite connected",
    dbPath: sqlite3.name
  });
});
app.get("/api/articles", (req, res) => {
  try {
    const articles2 = sqlite3.prepare("SELECT * FROM articles ORDER BY created_at DESC").all();
    res.json(articles2);
  } catch (error) {
    console.error("Error fetching articles:", error);
    res.status(500).json({ error: "Failed to fetch articles" });
  }
});
app.post("/api/articles", (req, res) => {
  try {
    const { reference, designation, stock_quantity, min_stock, unit_price, supplier_id, category, location } = req.body;
    const stmt = sqlite3.prepare(`
      INSERT INTO articles (reference, designation, stock_quantity, min_stock, unit_price, supplier_id, category, location)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);
    const result = stmt.run(reference, designation, stock_quantity || 0, min_stock || 0, unit_price || 0, supplier_id, category, location);
    const newArticle = sqlite3.prepare("SELECT * FROM articles WHERE id = ?").get(result.lastInsertRowid);
    res.status(201).json(newArticle);
  } catch (error) {
    console.error("Error creating article:", error);
    res.status(500).json({ error: "Failed to create article" });
  }
});
app.get("/api/dashboard/stats", (req, res) => {
  try {
    const totalArticles = sqlite3.prepare("SELECT COUNT(*) as count FROM articles").get();
    const lowStock = sqlite3.prepare("SELECT COUNT(*) as count FROM articles WHERE stock_quantity <= min_stock").get();
    const totalValue = sqlite3.prepare("SELECT SUM(stock_quantity * unit_price) as total FROM articles").get();
    res.json({
      totalArticles: totalArticles.count || 0,
      lowStock: lowStock.count || 0,
      totalValue: totalValue.total || 0,
      pendingRequests: 0
      // Placeholder
    });
  } catch (error) {
    console.error("Error fetching dashboard stats:", error);
    res.status(500).json({ error: "Failed to fetch dashboard stats" });
  }
});
if (process.env.NODE_ENV === "production") {
  const publicPath = path2.join(__dirname, "../dist/public");
  app.use(express.static(publicPath));
  app.get("*", (req, res) => {
    if (!req.path.startsWith("/api/")) {
      res.sendFile(path2.join(publicPath, "index.html"));
    }
  });
}
app.use((err, req, res, next) => {
  console.error("Server error:", err);
  res.status(500).json({ error: "Internal server error" });
});
var server = app.listen(PORT, "127.0.0.1", () => {
  console.log(`\u{1F5A5}\uFE0F  Desktop server running on http://127.0.0.1:${PORT}`);
  console.log(`\u{1F4C1} Database path: ${sqlite3.name}`);
  console.log(`\u{1F680} Mode: ${process.env.NODE_ENV || "development"}`);
});
var index_desktop_default = server;
export {
  index_desktop_default as default
};
