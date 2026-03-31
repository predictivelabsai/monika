"""App configuration constants."""

APP_NAME = "Ashland Hill Media Finance"
APP_SHORT = "AHMF"
APP_PORT = 5010
APP_VERSION = "0.1.0"

# Deal statuses
DEAL_STATUSES = ["pipeline", "active", "closed", "declined"]

# Contact types
CONTACT_TYPES = ["distributor", "producer", "sales_agent", "investor", "legal", "talent", "crew", "other"]

# Project types
PROJECT_TYPES = ["feature_film", "documentary", "series", "short", "animation"]

# Genres
GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "Horror", "Mystery", "Romance",
    "Sci-Fi", "Thriller", "War", "Western",
]

# Territories for sales mapping
TERRITORIES = [
    "Domestic (US/Canada)", "UK", "Germany", "France", "Italy", "Spain",
    "Scandinavia", "Benelux", "Australia/NZ", "Japan", "South Korea",
    "China", "Latin America", "Middle East", "Africa", "Eastern Europe",
    "India", "Southeast Asia", "Rest of World",
]

# Currencies
CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY"]
