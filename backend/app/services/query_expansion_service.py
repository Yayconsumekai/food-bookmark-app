"""
Query Expansion using a curated food synonym dictionary.
Improves search recall by automatically adding related terms.
This is a standard IR technique — mention it by name in your demo.
"""

FOOD_SYNONYMS: dict[str, list[str]] = {
    # Proteins
    "chicken":    ["poultry", "hen"],
    "beef":       ["meat", "steak", "ground beef"],
    "pork":       ["ham", "bacon", "swine"],
    "fish":       ["seafood", "salmon", "tuna", "cod"],
    "shrimp":     ["prawn", "seafood"],
    "lamb":       ["mutton", "meat"],
    "turkey":     ["poultry"],

    # Vegetables
    "potato":     ["spud", "tater"],
    "tomato":     ["tomatoes"],
    "onion":      ["onions", "shallot"],
    "pepper":     ["capsicum", "chilli", "chili"],
    "mushroom":   ["fungi", "mushrooms"],
    "spinach":    ["greens", "leafy"],
    "carrot":     ["carrots"],
    "corn":       ["maize", "sweetcorn"],

    # Cooking methods
    "fried":      ["pan fried", "deep fried", "crispy"],
    "baked":      ["roasted", "oven"],
    "grilled":    ["bbq", "barbecue", "chargrilled"],
    "steamed":    ["poached"],
    "slow cooked":["crockpot", "braised"],

    # Dish types
    "pasta":      ["noodles", "spaghetti", "fettuccine"],
    "soup":       ["broth", "stew", "chowder"],
    "salad":      ["slaw", "greens"],
    "cake":       ["dessert", "baked goods"],
    "bread":      ["loaf", "dough", "bun"],
    "sandwich":   ["wrap", "sub", "roll"],
    "curry":      ["masala", "spiced"],
    "rice":       ["pilaf", "risotto", "fried rice"],
    "sauce":      ["gravy", "dressing", "marinade"],

    # Flavors
    "spicy":      ["hot", "chili", "pepper"],
    "sweet":      ["sugary", "honey", "caramel"],
    "savory":     ["umami", "salty"],
    "creamy":     ["rich", "buttery", "smooth"],
}

def expand_query(query: str, max_expansions: int = 3) -> dict:
    """
    Given a search query, find synonym expansions.
    Returns:
      - expanded_terms: extra terms to OR into the tsquery
      - expansions_used: human-readable map of what was expanded (for UI display)
    """
    words            = query.lower().split()
    expansions_used  = {}
    expanded_terms   = []

    for word in words:
        if word in FOOD_SYNONYMS:
            synonyms = FOOD_SYNONYMS[word][:max_expansions]
            expansions_used[word] = synonyms
            expanded_terms.extend(synonyms)

    return {
        "original_query":  query,
        "expanded_terms":  expanded_terms,
        "expansions_used": expansions_used,
        "has_expansions":  len(expanded_terms) > 0,
    }


def build_expanded_tsquery(query: str) -> tuple[str, dict]:
    """
    Build a PostgreSQL tsquery that includes synonym expansions.
    Original terms use AND (must match), expansions use OR (nice to have).

    Example:
      "chicken soup" → 'chicken & soup | poultry | broth | stew'
    """
    import re
    words     = re.findall(r'[a-zA-Z0-9]+', query.lower())
    if not words:
        return None, {}

    expansion = expand_query(query)

    # Base query — all original words must match (AND)
    base_tsquery = " & ".join(words)

    # Add synonyms as OR alternatives
    if expansion["expanded_terms"]:
        synonym_parts = []
        for term in expansion["expanded_terms"]:
            clean = re.findall(r'[a-zA-Z0-9]+', term.lower())
            if clean:
                synonym_parts.append(" & ".join(clean))

        if synonym_parts:
            expanded = base_tsquery + " | " + " | ".join(synonym_parts)
            return expanded, expansion

    return base_tsquery, expansion