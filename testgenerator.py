import random
import pandas as pd

random.seed(1234)

people = [
    "Thomas", "Sarah", "Jonathan", "Emily", "Michael", "Anna",
    "David", "Laura", "Robert", "Sophia", "James", "Olivia"
]

noise_sentences = [
    "By the way, the price of oranges went up quite a bit this year.",
    "Nobody really liked the movie they watched on Saturday.",
    "The temperature reached 34 degrees during the afternoon.",
    "The team lost three consecutive matches.",
    "No one remembered where the keys were.",
    "They also bought a new printer for the office.",
    "The train arrived twenty minutes late.",
    "The conference lasted for more than four hours.",
    "Sometimes they write messages with spelling mistakes.",
    "The internet connection failed several times."
]

templates = [
    # 1. Matrimonio estándar con hijo y hermano
    lambda a,b,c,d:
    (
        f"{a} was born on 05/12/1980. They are married to {b}. "
        f"Their child {c} was born on 02/08/2010. "
        f"{random.choice(noise_sentences)} "
        f"{d} is the sibling of {a}.",
        [
            f"{a} ---> [SPOUSE] ---> {b}",
            f"{b} ---> [SPOUSE] ---> {a}",
            f"{a} ---> [CHILD] ---> {c}",
            f"{b} ---> [CHILD] ---> {c}",
            f"{c} ---> [PARENT] ---> {a}",
            f"{c} ---> [PARENT] ---> {b}",
            f"{a} ---> [SIBLING] ---> {d}",
            f"{d} ---> [SIBLING] ---> {a}",
            f"{a} ---> [BIRTHDATE] ---> 05/12/1980",
            f"{c} ---> [BIRTHDATE] ---> 02/08/2010"
        ]
    ),

    # 2. Pareja celebrando cumpleaños con hermana
    lambda a,b,c,d:
    (
        f"{a} and {b} celebrated the birthday of their daughter {c}. "
        f"She received many gifts. "
        f"{random.choice(noise_sentences)} "
        f"{d}, {b}'s sister, also attended.",
        [
            f"{a} ---> [CHILD] ---> {c}",
            f"{b} ---> [CHILD] ---> {c}",
            f"{c} ---> [PARENT] ---> {a}",
            f"{c} ---> [PARENT] ---> {b}",
            f"{b} ---> [SIBLING] ---> {d}",
            f"{d} ---> [SIBLING] ---> {b}"
        ]
    ),

    # 3. Adopción
    lambda a,b,c,d:
    (
        f"{a} and {b} adopted {c} years ago. "
        f"Many mistakenly believe they are their nephew. "
        f"{random.choice(noise_sentences)}",
        [
            f"{a} ---> [CHILD] ---> {c}",
            f"{b} ---> [CHILD] ---> {c}",
            f"{c} ---> [PARENT] ---> {a}",
            f"{c} ---> [PARENT] ---> {b}"
        ]
    ),

    # 4. Relación pasada
    lambda a,b,c,d:
    (
        f"{a} was previously married to {b}, but currently lives with {c}. "
        f"{d} is the child of {a} and {b}. "
        f"{random.choice(noise_sentences)}",
        [
            f"{a} ---> [SPOUSE] ---> {b}",
            f"{b} ---> [SPOUSE] ---> {a}",
            f"{a} ---> [CHILD] ---> {d}",
            f"{b} ---> [CHILD] ---> {d}",
            f"{d} ---> [PARENT] ---> {a}",
            f"{d} ---> [PARENT] ---> {b}"
        ]
    ),

    # 5. Silencio absoluto (sin parentesco)
    lambda a,b,c,d:
    (
        f"{a}, {b}, {c}, and {d} participated in a chess tournament. "
        f"{random.choice(noise_sentences)} "
        f"No family relationship was indicated.",
        []
    ),

    # 6. Interacción sin parentesco claro
    lambda a,b,c,d:
    (
        f"{a} visited {b} along with {c}. "
        f"Later, {d} arrived. "
        f"It was unclear if there was any kinship.",
        []
    ),

    # 7. Texto coloquial / Jerga ("ta casao" -> "is hitched to")
    lambda a,b,c,d:
    (
        f"{a} is hitched to {b}. "
        f"Their kid {c} had a bday yesterday. "
        f"{random.choice(noise_sentences)}",
        [
            f"{a} ---> [SPOUSE] ---> {b}",
            f"{b} ---> [SPOUSE] ---> {a}",
            f"{a} ---> [CHILD] ---> {c}",
            f"{b} ---> [CHILD] ---> {c}",
            f"{c} ---> [PARENT] ---> {a}",
            f"{c} ---> [PARENT] ---> {b}"
        ]
    )
]

rows = []

for i in range(1000):
    a,b,c,d = random.sample(people, 4)
    text, output = random.choice(templates)(a,b,c,d)
    
    rows.append({
        "id": i+1,
        "input": text,
        "expected_output": "\n".join(output)
    })

df = pd.DataFrame(rows)

df.to_csv(
    "family_relations_noisy_1000_EN.csv",
    index=False,
    encoding="utf-8"
)

print(df.head())