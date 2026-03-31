-- Sales & Collections, Credit Rating, Accounting, Communications tables

-- Sales contracts
CREATE TABLE IF NOT EXISTS ahmf.sales_contracts (
    contract_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES ahmf.deals(deal_id) ON DELETE CASCADE,
    territory VARCHAR(255),
    distributor_id UUID REFERENCES ahmf.contacts(contact_id),
    mg_amount NUMERIC(15,2),
    currency VARCHAR(10) DEFAULT 'USD',
    payment_schedule JSONB DEFAULT '[]',
    status VARCHAR(50) DEFAULT 'draft',
    created_by UUID REFERENCES ahmf.users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Collections
CREATE TABLE IF NOT EXISTS ahmf.collections (
    collection_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID REFERENCES ahmf.sales_contracts(contract_id) ON DELETE CASCADE,
    amount_due NUMERIC(15,2),
    amount_received NUMERIC(15,2) DEFAULT 0,
    due_date DATE,
    received_date DATE,
    status VARCHAR(50) DEFAULT 'pending'
);

-- Credit ratings
CREATE TABLE IF NOT EXISTS ahmf.credit_ratings (
    rating_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES ahmf.contacts(contact_id) ON DELETE CASCADE,
    score NUMERIC(5,2),
    payment_reliability NUMERIC(5,2),
    risk_tier VARCHAR(20),
    factors JSONB DEFAULT '{}',
    rated_by UUID REFERENCES ahmf.users(user_id),
    rated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Transactions (accounting)
CREATE TABLE IF NOT EXISTS ahmf.transactions (
    txn_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES ahmf.deals(deal_id) ON DELETE CASCADE,
    txn_type VARCHAR(50),
    amount NUMERIC(15,2),
    currency VARCHAR(10) DEFAULT 'USD',
    counterparty_id UUID REFERENCES ahmf.contacts(contact_id),
    reference VARCHAR(500),
    posted_date DATE DEFAULT CURRENT_DATE,
    created_by UUID REFERENCES ahmf.users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Messages / communications
CREATE TABLE IF NOT EXISTS ahmf.messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deal_id UUID REFERENCES ahmf.deals(deal_id) ON DELETE SET NULL,
    from_user UUID REFERENCES ahmf.users(user_id),
    to_user UUID REFERENCES ahmf.users(user_id),
    subject VARCHAR(500),
    body TEXT,
    message_type VARCHAR(50) DEFAULT 'note',
    due_date DATE,
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
