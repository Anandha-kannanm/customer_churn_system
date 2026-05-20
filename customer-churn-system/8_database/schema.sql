CREATE TABLE IF NOT EXISTS customers (
    customerID TEXT PRIMARY KEY,
    gender TEXT,
    SeniorCitizen INTEGER,
    Partner INTEGER,
    Dependents INTEGER,
    tenure INTEGER,
    PhoneService INTEGER,
    InternetService TEXT,
    Contract TEXT,
    PaymentMethod TEXT,
    MonthlyCharges REAL,
    TotalCharges REAL,
    Churn INTEGER
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customerID TEXT,
    churn_probability REAL,
    will_churn INTEGER,
    risk_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customerID) REFERENCES customers(customerID)
);

CREATE INDEX IF NOT EXISTS idx_predictions_customer ON predictions(customerID);
CREATE INDEX IF NOT EXISTS idx_predictions_risk ON predictions(risk_level);
