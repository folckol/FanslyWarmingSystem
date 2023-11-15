import random
import string

# Components for the nickname generator



prefixes = [
    "Dark", "Mystic", "Red", "Lone", "Silent", "Golden", "Shadow", "Elite", "Brave", "Rogue",
    "Crypto", "Neo", "Tech", "Mega", "Ultra", "Super", "Quantum", "Retro", "Virtual", "Binary",
    "Atomic", "Cyber", "Pixel", "Digital", "Cosmic", "Galactic", "Stellar", "Epic", "Prime", "Nano",
    "Quant", "Hyper", "Giga", "Terra", "Mighty", "Stealth", "Infinite", "Zen", "Nova", "Blazing",
    "Icy", "Thunder", "Storm", "Astral", "Sun", "Moon", "Star", "Comet", "Meteor", "Sonic",
    "Speed", "Light", "Twilight", "Dusk", "Dawn", "Noir", "Crimson", "Azure", "Emerald", "Sapphire",
    "Ruby", "Diamond", "Platinum", "Titanium", "Steel", "Iron", "Bronze", "Gold", "Silver", "Jade",
    "Onyx", "Obsidian", "Amber", "Pearl", "Ivory", "Jet", "Crystal", "Glass", "Frozen", "Fiery",
    "Burning", "Molten", "Watery", "Earthy", "Windy", "Sky", "Cloud", "Mist", "Fog", "Haze"
]

bases = [
    "Wolf", "Knight", "Dragon", "Hunter", "Mage", "Warrior", "Archer", "Sorcerer", "Assassin", "Guardian",
    "Coder", "Hacker", "Bot", "Programmer", "Designer", "Engineer", "Pixel", "Bit", "Byte", "Ninja",
    "Runner", "Driver", "Pilot", "Captain", "Chief", "Baron", "Lord", "Prince", "King", "Emperor",
    "Monk", "Samurai", "Sensei", "Master", "Guru", "Sage", "Wizard", "Alchemist", "Bard", "Cleric",
    "Druid", "Paladin", "Ranger", "Rogue", "Shaman", "Thief", "Valkyrie", "Vampire", "Werewolf", "Zombie",
    "Goblin", "Orc", "Elf", "Dwarf", "Giant", "Titan", "Demon", "Angel", "Deity", "Spirit",
    "Phantom", "Ghost", "Reaper", "Wraith", "Specter", "Beast", "Monster", "Creature", "Fiend", "Alien",
    "Cosmonaut", "Astronaut", "Explorer", "Adventurer", "Seeker", "Wanderer", "Traveler", "Voyager", "Nomad", "Pioneer",
"Cyborg", "Net", "Code", "Script", "Sprite", "Frame", "Glitch", "Pixel", "Troop", "Brute",
    "Caster", "Curse", "Flame", "Mystic", "Blast", "Spark", "Frost", "Bolt", "Wave", "Ray",
    "Drake", "Bear", "Lynx", "Hawk", "Eagle", "Raven", "Lion", "Tiger", "Puma", "Fox",
    "Jester", "Squire", "Smith", "Baron", "Duke", "Count", "Noble", "Peon", "Tsar", "Sultan",
    "Charm", "Riddle", "Echo", "Dream", "Shade", "Gloom", "Whisp", "Wisp", "Nymph", "Sprite",
    "Witch", "Sylph", "Fairy", "Gnome", "Sprite", "Fiend", "Djinn", "Bansh", "Sprite", "Ghost",
    "Phreak", "Admin", "Root", "Mouse", "Macro", "Logic", "Array", "Stack", "Queue", "Heap",
    "Cloud", "Data", "Fiber", "Codec", "Proxy", "Virus", "Worm", "Trojan", "Logic", "Gate",
    "Pulse", "Laser", "Reson", "Tonic", "Rhyth", "Noise", "Chord", "Melod", "Lyric", "Tune",
    "Stint", "Shift", "Streak", "Burst", "Blink", "Flash", "Blast", "Blitz", "Sprint", "Dash",
    "Craft", "Forge", "Build", "Mold", "Shape", "Form", "Draft", "Trace", "Draw", "Sketch",
    "Rust", "Steel", "Stone", "Brick", "Wood", "Metal", "Glass", "Water", "Fire", "Earth",
    "Wind", "Storm", "Blaze", "Ocean", "River", "Stream", "Brook", "Wave", "Mist", "Fog",
    "Dust", "Smoke", "Ash", "Ember", "Flint", "Coal", "Metal", "Bronze", "Copper", "Brass",
    "Gold", "Silver", "Gem", "Ruby", "Opal", "Topaz", "Pearl", "Jade", "Garnet", "Amber",
    "Siren", "Muse", "Flair", "Grace", "Charm", "Favor", "Pleas", "Bliss", "Joy", "Rapture",
    "Sorrow", "Rage", "Fury", "Wrath", "Vex", "Anger", "Bliss", "Ecstasy", "Desire", "Passion",
    "Love", "Hope", "Faith", "Pride", "Zeal", "Lust", "Greed", "Envy", "Sloth", "Glutton",
    "Breeze", "Wind", "Gust", "Storm", "Tempest", "Air", "Draft", "Tornado", "Hurricane", "Typhoon",
    "Sing", "Chant", "Shout", "Claim", "Murmur", "Whisper", "Order", "Command", "Dictate", "Narrate",
    "Speak", "Prate", "Chat", "Relate", "Say", "Tell", "Utter", "State", "Express", "Mention",
    "Reveal", "Divulge", "Disclose", "Expose", "Unveil", "Show", "Display", "Exhibit", "Manifest", "Demonstrate",
    "Glow", "Shine", "Flash", "Glitter", "Glisten", "Sparkle", "Radiate", "Dazzle", "Twinkle", "Gleam"
]

suffixes = [
    "007", "X", "Prime", "95", "Elite", "Pro", "Master", "One", "Zero", "Legend",
    "NFT", "Token", "Chain", "Block", "Net", "Web", "Link", "Node", "Stream", "Flow",
    "Ox", "101", "202", "303", "404", "505", "606", "707", "808", "909",
    "Max", "Ultra", "Mega", "Giga", "Tera", "Peta", "Exa", "Zetta", "Yotta", "Theta",
    "Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa",
    "Lambda", "Mu", "Nu", "Xi", "Omicron", "Pi", "Rho", "Sigma", "Tau", "Upsilon",
    "Phi", "Chi", "Psi", "Omega", "End", "Final", "True", "Real", "Pure", "Absolute",
    "Aero", "Neo", "Zen", "Myth", "Void", "Nova", "Luna", "Star", "Sol", "Frost",
    "Pyro", "Geo", "Tide", "Wave", "Mist", "Wind", "Flux", "Vex", "Rush", "Blitz",
    "Glow", "Haze", "Faze", "Warp", "Bolt", "Pulse", "Rift", "Dusk", "Dawn", "Burst",
    "Blaze", "Shade", "Echo", "Neb", "Orb", "Halo", "Mach", "Ion", "Ark", "Sage",
    "Wisp", "Flare", "Glint", "Shred", "Knot", "Twist", "Bloom", "Gloom", "Flash", "Spike",
    "Spire", "Peak", "Muse", "Vibe", "Prowl", "Roam", "Glide", "Skim", "Zoom", "Zest",
    "Quest", "Rune", "Sigil", "Glyph", "Icon", "Idol", "Nyx", "Omen", "Rave", "Rage",
    "Fury", "Veil", "Mesh", "Dot", "Link", "Node", "Core", "Crest", "Crown", "Forge",
    "Mold", "Weld", "Braid", "Twine", "Fuse", "Meld", "Blend", "Mingle", "Stir", "Swirl",
    "Whirl", "Spin", "Twirl", "Dash", "Flick", "Flip", "Snap", "Click", "Tap", "Jolt"
]

names = [
    "John", "Alice", "Mike", "Anna", "Alex", "Emily", "Chris", "Kate", "Tom", "Sarah",
    "Robert", "Jennifer", "Michael", "Jessica", "William", "Ashley", "David", "Amanda", "Joseph", "Linda",
    "Richard", "Michelle", "Charles", "Kimberly", "Thomas", "Amy", "Daniel", "Crystal", "Matthew", "Nicole",
    "Mark", "Megan", "Brian", "Heather", "Steven", "Rebecca", "Kevin", "Tiffany", "Jeffrey", "Chelsea",
    "Jason", "Melissa", "Ryan", "Danielle", "Jacob", "Amber", "Joshua", "Brittany", "Eric", "Christina",
    "Stephen", "Katherine", "Andrew", "Natalie", "Timothy", "Laura", "Brandon", "Stephanie", "Jonathan", "Samantha",
    "Adam", "Rachel", "Aaron", "Vanessa", "Justin", "Cassandra", "Samuel", "Courtney", "Scott", "Alicia",
    "Benjamin", "Allison", "Gregory", "Michele", "Derek", "Andrea", "Edward", "Shannon", "Patrick", "Alyssa"
]

crypto_suffixes = [
    "Crypto", "Token", "Chain", "Block", "Hash", "HODL", "DeFi", "Altcoin", "Satoshi", "Fiat",
    "Wallet", "Bull", "Bear", "Moon", "Dip", "Pump", "Swap", "Stake", "Mine", "Ledger",
    "FOMO", "ATH", "ICO", "NFT", "DAO", "DEX", "Whale", "Gas", "Fork", "Airdrop",
    "Halving", "SegWit", "Lambo", "Hodler", "Rekt", "BUIDL", "Cap", "FA", "TA", "ToTheMoon"
]

suffixes.extend(crypto_suffixes)

def GenerateNickname():
    additional_prefixes = [generate_sounding_word() for _ in range(1000)]
    prefixes.extend(additional_prefixes)

    # Ensure the nickname length is within the specified range, not only from prefix, and always consists of a combination
    while True:
        prefix_choice = random.choice(names + prefixes) if random.randint(0, 2) != 0 else ""
        base_choice = random.choice(bases)
        suffix_choice = random.choice(suffixes) if random.randint(0, 1) else ""

        # Decide if we should use an underscore for 2-word nicknames
        underscore = "_" if random.randint(0, 4) == 0 and prefix_choice and base_choice and not suffix_choice else ""

        nickname = f"{prefix_choice}{underscore}{base_choice}{suffix_choice}"

        # Decide if the nickname should start with a lowercase letter
        if random.randint(0, 1):
            nickname = nickname[0].lower() + nickname[1:]

        # Decide if the entire nickname should be in lowercase with a 10% chance
        if random.randint(0, 4) == 0:
            nickname = nickname.lower()

        # Ensure nickname is a combination and not just a single word
        if 6 <= len(nickname) <= 13 and (
                prefix_choice and (base_choice or suffix_choice) or (base_choice and suffix_choice)):
            return nickname


def generate_sounding_word():
    # Define possible syllables and letter combinations
    vowels = "aeiouy"
    consonants = "".join(set(string.ascii_lowercase) - set(vowels))

    # Generate a sounding word using random combinations of consonants and vowels
    word = ""
    word_length = random.randint(2, 5)
    for i in range(word_length):
        if i % 2 == 0:
            word += random.choice(consonants)
        else:
            word += random.choice(vowels)

    return word.capitalize()



# Generate 20 sample nicknames with the final filtered generator

if __name__ == '__main__':

    final_filtered_sample_nicknames = [GenerateNickname() for _ in range(100)]

    o = ''
    for i in final_filtered_sample_nicknames:
        o+=i+'   '

    print(o)
