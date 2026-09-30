from urllib.parse import quote_plus


PLATFORMS = {

    "Amazon":
        "https://www.amazon.in/s?k={}",

    "Flipkart":
        "https://www.flipkart.com/search?q={}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={}",

    "Swiggy":
        "https://www.swiggy.com/search?query={}",

    "Zomato":
        "https://www.zomato.com/search?query={}",

    "OYO":
        "https://www.oyorooms.com/search/?location={}",
}


def link(
    platform: str,
    query: str,
) -> str:

    if platform not in PLATFORMS:

        platform = "Amazon"

    return PLATFORMS[
        platform
    ].format(
        quote_plus(query)
    )