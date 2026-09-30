import json
import re

from typing import Optional

from app.core.config import settings

from app.services.catalog import link


# ---------------------------------------------------------
# Gemini SDK
# ---------------------------------------------------------

try:

    from google import genai
    from google.genai import types

except ImportError:

    genai = None
    types = None


# ---------------------------------------------------------
# JSON cleaner
# ---------------------------------------------------------

def clean_json(text: str):

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return json.loads(text)


# =========================================================
# HOME MOCK RECOMMENDATIONS
# =========================================================

def mock_home(data):

    budget = data["budget"]

    products = [

        (
            "Furniture",
            "Compact 3-Seater Sofa",
            "Space-efficient sofa suitable for a comfortable living room.",
            0.38,
            "IKEA",
            "3 seater sofa",
        ),

        (
            "Lighting",
            "LED Ceiling Light",
            "Warm-white ceiling light for a modern interior.",
            0.15,
            "Amazon",
            "LED ceiling light",
        ),

        (
            "Decor",
            "Minimal Wall Art Set",
            "Neutral wall-art set for a clean modern appearance.",
            0.17,
            "Flipkart",
            "minimal wall art set",
        ),

        (
            "Storage",
            "Modular Storage Cabinet",
            "Flexible storage for bedroom or living room.",
            0.15,
            "IKEA",
            "modular storage cabinet",
        ),

        (
            "Dining",
            "4-Seater Dining Table",
            "Compact dining table for everyday use.",
            0.15,
            "Amazon",
            "4 seater dining table",
        ),
    ]

    recommendations = []

    for (
        category,
        name,
        description,
        percentage,
        platform,
        query,
    ) in products:

        price = round(
            budget * percentage,
            2,
        )

        recommendations.append(
            {
                "category": category,
                "name": name,
                "description": description,
                "price": price,
                "platform": platform,
                "url": link(
                    platform,
                    query,
                ),
            }
        )

    rooms = (
        ", ".join(data["rooms"])
        if data["rooms"]
        else "your selected rooms"
    )

    return {

        "planner": "home",

        "budget": budget,

        "allocated_total": round(
            budget,
            2,
        ),

        "summary": (
            f"A {data['style']} home setup "
            f"distributed across {rooms}."
        ),

        "tips": [

            "Keep around 10% unallocated for delivery charges or price changes.",

            "Measure available space before ordering large furniture.",

            "Compare final cart totals including delivery charges.",

        ],

        "recommendations":
            recommendations,

        "source": "mock",
    }


# =========================================================
# PARTY MOCK RECOMMENDATIONS
# =========================================================

def mock_party(data):

    budget = data["budget"]

    guests = data["guests"]

    specifications = [

        (
            "Catering",
            0.50,
            "Swiggy",
            "party catering",
        ),

        (
            "Venue",
            0.20,
            "OYO",
            data["city"],
        ),

        (
            "Decoration",
            0.15,
            "Amazon",
            "party decorations",
        ),

        (
            "Entertainment",
            0.15,
            "Zomato",
            "party entertainment",
        ),

    ]

    recommendations = []

    for (
        category,
        percentage,
        platform,
        query,
    ) in specifications:

        price = round(
            budget * percentage,
            2,
        )

        recommendations.append(
            {
                "category": category,

                "name":
                    f"{data['event_type']} "
                    f"{category} package",

                "description":
                    f"Budget placeholder for "
                    f"{guests} guests.",

                "price": price,

                "platform": platform,

                "url": link(
                    platform,
                    query,
                ),
            }
        )

    return {

        "planner": "party",

        "budget": budget,

        "allocated_total": round(
            budget,
            2,
        ),

        "summary":
            f"Planning a {data['event_type']} "
            f"for {guests} guests with a "
            f"{data['venue']} venue preference.",

        "tips": [

            "Confirm per-person catering costs before booking.",

            "Keep a contingency amount for last-minute guests.",

            "Check venue cancellation and timing policies.",

        ],

        "recommendations":
            recommendations,

        "source": "mock",
    }


# =========================================================
# JEWELRY MOCK RECOMMENDATIONS
# =========================================================

def mock_jewelry(data):

    budget = data["budget"]

    style = data["style"]

    occasion = data["occasion"]

    specifications = [

        (
            "Earrings",
            "Statement Earrings",
            0.25,
            "Amazon",
            "statement earrings",
        ),

        (
            "Necklace",
            "Elegant Necklace Set",
            0.45,
            "Flipkart",
            "elegant necklace set",
        ),

        (
            "Bangles",
            "Minimal Bangle Set",
            0.20,
            "Amazon",
            "minimal bangle set",
        ),

        (
            "Ring",
            "Classic Ring",
            0.10,
            "Flipkart",
            "classic ring",
        ),

    ]

    recommendations = []

    for (
        category,
        name,
        percentage,
        platform,
        query,
    ) in specifications:

        recommendations.append(
            {

                "category": category,

                "name": name,

                "description":
                    f"{style} choice suitable "
                    f"for a {occasion.lower()} "
                    f"occasion.",

                "price":
                    round(
                        budget * percentage,
                        2,
                    ),

                "platform": platform,

                "url":
                    link(
                        platform,
                        query,
                    ),
            }
        )

    outfit_context = (
        data.get("outfit_color")
        or data.get("outfit_description")
        or "not specified"
    )

    return {

        "planner": "jewelry",

        "budget": budget,

        "allocated_total":
            round(budget, 2),

        "summary":
            f"{style} jewelry ideas for "
            f"{occasion}, with outfit context: "
            f"{outfit_context}.",

        "tips": [

            "Match the metal tone with outfit undertones.",

            "For statement pieces, keep the remaining jewelry simpler.",

            "Verify material, size and return policy before purchasing.",

        ],

        "recommendations":
            recommendations,

        "source": "mock",
    }


# =========================================================
# GEMINI PROMPT
# =========================================================

def build_prompt(
    planner,
    data,
):

    return f"""
You are PocketSmart AI,
a budget-aware recommendation assistant.

Planner:
{planner}

User data:
{json.dumps(data, indent=2)}

Return ONLY valid JSON.

Required top-level keys:

planner
budget
allocated_total
summary
tips
recommendations

Each recommendation must contain:

category
name
description
price
platform
url

Requirements:

1. Respect the user's total budget.

2. Make allocations realistic.

3. Do not claim live inventory.

4. Do not invent exact live product pages.

5. Use platform search URLs when possible.

6. Suggested platforms may include:
Amazon
Flipkart
IKEA
Swiggy
Zomato
OYO

7. Give practical budget planning tips.

8. Keep recommendations concise.
"""


# =========================================================
# MAIN GENERATOR
# =========================================================

def generate_recommendations(
    planner,
    data,
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None,
):

    # -----------------------------------------------------
    # Mock mode
    # -----------------------------------------------------

    if (
        not settings.gemini_enabled
        or genai is None
    ):

        mock_functions = {

            "home":
                mock_home,

            "party":
                mock_party,

            "jewelry":
                mock_jewelry,

        }

        return mock_functions[
            planner
        ](data)

    # -----------------------------------------------------
    # Gemini mode
    # -----------------------------------------------------

    client = genai.Client(
        api_key=settings.GEMINI_API_KEY
    )

    contents = [
        build_prompt(
            planner,
            data,
        )
    ]

    # -----------------------------------------------------
    # Optional image
    # -----------------------------------------------------

    if image_bytes:

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=(
                    mime_type
                    or "image/jpeg"
                ),
            )
        )

        contents.append(
            """
Use the outfit image only for
broad color and style coordination.

Do not identify the person
or infer sensitive personal attributes.
"""
        )

    # -----------------------------------------------------
    # Gemini request
    # -----------------------------------------------------

    response = (
        client.models.generate_content(

            model=settings.GEMINI_MODEL,

            contents=contents,

            config=types.GenerateContentConfig(

                response_mime_type="application/json",

                temperature=0.4,

            ),
        )
    )

    result = clean_json(
        response.text
    )

    result["source"] = "gemini"

    return result