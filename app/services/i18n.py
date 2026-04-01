TRANSLATIONS = {
    "es": {"welcome": "Bienvenido", "new_lead": "Contacto nuevo", "campaign": "Campaña"},
    "en": {"welcome": "Welcome", "new_lead": "New lead", "campaign": "Campaign"},
    "pt": {"welcome": "Bem-vindo", "new_lead": "Novo lead", "campaign": "Campanha"},
}


def t(lang: str, key: str) -> str:
    return TRANSLATIONS.get(lang, TRANSLATIONS["es"]).get(key, key)
