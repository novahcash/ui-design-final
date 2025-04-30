CLASS_INFO = {
    "Fighter": {
        "name": "Fighter",
        "image": "magnolia.png",
        "level": 1,
        "hp": 11,
        "primary_stat": "Strength",
        "weapon_proficiencies": "All",
        "armor_proficiencies": "All",
        "available_skills": [
            {"name": "Acrobatics", "description": "(Dexterity) Perform acrobatic stunts."},
            {"name": "Animal Handling", "description": "(Wisdom) Calm or control animals."},
            {"name": "Athletics", "description": "(Strength) Perform feats of strength."},
            {"name": "History", "description": "(Intelligence) Recall historical knowledge."},
            {"name": "Insight", "description": "(Wisdom) Read people and situations."},
            {"name": "Intimidation", "description": "(Charisma) Threaten or coerce others."},
            {"name": "Perception", "description": "(Wisdom) Spot or hear hidden things."},
            {"name": "Persuasion", "description": "(Charisma) Influence or negotiate."},
            {"name": "Survival", "description": "(Wisdom) Track, hunt, or endure wilderness."}
        ],
        "stats": [...],
        "abilities": [
            {
                "name": "Second Wind",
                "description": "As a <span class='tooltip-highlight' title='Fill in during the next prototype'>Bonus Action</span>, regain <span class='clickable-roll'>🎲 1d10+1</span> HP. 2 uses."
            }
        ],
        "equipment": ["Chain Mail", "Greatsword", "Flail", "8 Javelins", "Dungeoneer's Pack", "4 GP"],
        "recommended_backgrounds": ["Soldier", "Guard", "Farmer"]
    },

    "Rogue": {
        "name": "Rogue",
        "image": "magnolia.png",
        "level": 1,
        "hp": 9,
        "primary_stat": "Dexterity",
        "weapon_proficiencies": "Simple weapons; Finesse or Light Martial weapons",
        "armor_proficiencies": "Light armor",
        "available_skills": [
            {"name": "Acrobatics", "description": "(Dexterity) Perform acrobatic stunts."},
            {"name": "Athletics", "description": "(Strength) Perform feats of strength."},
            {"name": "Deception", "description": "(Charisma) Lie or mislead."},
            {"name": "Insight", "description": "(Wisdom) Read people and situations."},
            {"name": "Intimidation", "description": "(Charisma) Threaten or coerce others."},
            {"name": "Investigation", "description": "(Intelligence) Search or analyze clues."},
            {"name": "Perception", "description": "(Wisdom) Spot or hear hidden things."},
            {"name": "Sleight of Hand", "description": "(Dexterity) Pick pockets or manipulate objects."},
            {"name": "Stealth", "description": "(Dexterity) Move quietly and unseen."}
        ],
        "stats": [...],
        "abilities": [],
        "equipment": ["Leather Armor", "2 Daggers", "Shortsword", "Shortbow", "20 Arrows", "Quiver", "Thieves' Tools", "Burglar's Pack", "8 GP"],
        "recommended_backgrounds": ["Criminal", "Urchin", "Sailor"]
    },

    "Wizard": {
        "name": "Wizard",
        "image": "magnolia.png",
        "level": 1,
        "hp": 7,
        "primary_stat": "Intelligence",
        "weapon_proficiencies": "Simple weapons",
        "armor_proficiencies": "None",
        "available_skills": [
            {"name": "Arcana", "description": "(Intelligence) Recall magical lore."},
            {"name": "History", "description": "(Intelligence) Recall historical knowledge."},
            {"name": "Insight", "description": "(Wisdom) Read people and situations."},
            {"name": "Investigation", "description": "(Intelligence) Search or analyze clues."},
            {"name": "Medicine", "description": "(Wisdom) Stabilize or diagnose conditions."},
            {"name": "Religion", "description": "(Intelligence) Understand divine lore."}
        ],
        "stats": [...],
        "abilities": [
            {
                "name": "Ritual Adept",
                "description": "You can cast any spell as a <span class='tooltip-highlight' title='Fill in during the next prototype'>Ritual</span> if that spell has the Ritual tag and is in your spellbook."
            },
            {
                "name": "Arcane Recovery",
                "description": "(1 use) Upon finishing a <span class='tooltip-highlight' title='Fill in during the next prototype'>Short Rest</span>, recover a level 1 spell slot."
            }
        ],
        "spells": {
            "cantrips": ["Fire Bolt", "Mage Hand", "Prestidigitation"],
            "level1": ["Mage Armor", "Magic Missile", "Shield", "Detect Magic"],
            "prepared_text": "Upon finishing a <span class='tooltip-highlight' title='Fill in during the next prototype'>Long Rest</span>, you can change your list of prepared spells, replacing any of the spells there with spells from your spellbook.",
            "spellbook_text": "Your spellbook contains the following spells: Detect Magic, Feather Fall, Mage Armor, Magic Missile, Sleep, and Thunderwave."
        },
        "equipment": ["2 Daggers", "Arcane Focus (Quarterstaff)", "Robe", "Spellbook", "Scholar's Pack", "5 GP"],
        "recommended_backgrounds": ["Sage", "Acolyte", "Hermit"]
    },

    "Cleric": {
        "name": "Cleric",
        "image": "magnolia.png",
        "level": 1,
        "hp": 9,
        "primary_stat": "Wisdom",
        "weapon_proficiencies": "Simple weapons",
        "armor_proficiencies": "Light, Medium armor; Shields",
        "available_skills": [
            {"name": "Arcana", "description": "(Intelligence) Recall magical lore."},
            {"name": "History", "description": "(Intelligence) Recall historical knowledge."},
            {"name": "Insight", "description": "(Wisdom) Read people and situations."},
            {"name": "Investigation", "description": "(Intelligence) Search or analyze clues."},
            {"name": "Medicine", "description": "(Wisdom) Stabilize or diagnose conditions."},
            {"name": "Religion", "description": "(Intelligence) Understand divine lore."}
        ],
        "stats": [...],
        "abilities": [],  # Deliberately hidden at level 1
        "spells": {
            "cantrips": ["Guidance", "Sacred Flame", "Thaumaturgy"],
            "level1": ["Cure Wounds", "Shield of Faith", "Bless", "Detect Evil and Good"],
            "prepared_text": "Whenever you finish a <span class='tooltip-highlight' title='Fill in during the next prototype'>Long Rest</span>, you can change your list of prepared spells, replacing any of the spells there with other Cleric spells for which you have spell slots."
        },
        "equipment": ["Chain Shirt", "Shield", "Mace", "Holy Symbol", "Priest's Pack", "7 GP"],
        "recommended_backgrounds": ["Acolyte", "Sage", "Hermit"]
    }
}
