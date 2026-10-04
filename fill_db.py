from database import add_entry
import datetime

today = str(datetime.date.today())

add_entry(
    title="Fake: Turmeric cures COVID",
    content="Claim: Drinking turmeric milk cures COVID-19",
    verdict="Fake",
    source="AltNews (example)",
    category="Text",
    date_added=today
)

add_entry(
    title="Fake: Altered protest image",
    content="Claim: This protest image is genuine; actually digitally edited",
    verdict="Fake",
    source="PIB Fact Check (example)",
    category="Image",
    date_added=today
)

print("Inserted sample entries.")