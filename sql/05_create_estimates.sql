-- Sales Estimates & Comp Films tables

CREATE TABLE IF NOT EXISTS ahmf.sales_estimates (
    estimate_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    genre VARCHAR(100),
    budget_range VARCHAR(100),
    cast_names TEXT[],
    director VARCHAR(500),
    script_summary TEXT,
    domestic_forecast JSONB DEFAULT '{}',
    international_forecast JSONB DEFAULT '{}',
    territory_mgs JSONB DEFAULT '{}',
    confidence_score NUMERIC(5,2),
    comp_film_ids UUID[],
    model_version VARCHAR(50),
    created_by UUID REFERENCES ahmf.users(user_id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ahmf.comp_films (
    comp_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tmdb_id INTEGER,
    imdb_id VARCHAR(20),
    title VARCHAR(500),
    year INTEGER,
    genre VARCHAR(255),
    budget NUMERIC(15,2),
    worldwide_gross NUMERIC(15,2),
    domestic_gross NUMERIC(15,2),
    cast_names TEXT[],
    director VARCHAR(500),
    popularity NUMERIC(10,2),
    territory_sales JSONB DEFAULT '{}',
    cached_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_comp_films_tmdb ON ahmf.comp_films(tmdb_id);
CREATE INDEX IF NOT EXISTS idx_comp_films_genre ON ahmf.comp_films(genre);
