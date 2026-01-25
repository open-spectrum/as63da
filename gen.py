from datetime import date, timedelta

NAMES_FILE = "names.txt"
OUTPUT_FILE = "output.txt"

NUM_START = 0
NUM_END = 9999

# novo padrão extra (0..999)
NUM_SMALL_START = 0
NUM_SMALL_END = 999

DATE_START = date(1990, 1, 1)
DATE_END = date(2026, 1, 1)


def load_names():
    with open(NAMES_FILE, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def generate_dates():
    d = DATE_START
    while d <= DATE_END:
        yield d.strftime("%d%m%Y")
        d += timedelta(days=1)


def name_variants(name: str):
    """
    Gera variações:
      - minúsculo: ana
      - primeira letra maiúscula: Ana
      - maiúsculo: ANA
    Remove duplicatas preservando ordem.
    """
    base = name.strip()
    lower = base.lower()
    cap = lower.capitalize()
    upper = lower.upper()
    return list(dict.fromkeys([lower, cap, upper]))


def main():
    names_raw = load_names()
    dates = list(generate_dates())

    # dedup de nomes (ignorando caixa) pra não inflar a wordlist à toa
    seen = set()
    names = []
    for n in names_raw:
        key = n.strip().lower()
        if key and key not in seen:
            seen.add(key)
            names.append(n.strip())

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for raw_name in names:
            for name in name_variants(raw_name):

                # 1) nome + nome
                out.write(name + name + "\n")

                # 2) nome + número(0000..9999) / número + nome
                for n in range(NUM_START, NUM_END + 1):
                    num = f"{n:04d}"
                    out.write(name + num + "\n")
                    out.write(num + name + "\n")

                # 3) nome + data(ddmmaaaa) / data + nome
                for d in dates:
                    out.write(name + d + "\n")
                    out.write(d + name + "\n")

                # 4) NOVO: nome + número(0..999) / número + nome
                # (mantém sem padding fixo, pra ter exemplos tipo ana2, ana02, ana002? não.)
                # Você pediu exemplos tipo ana02, então vou gerar com 2 e 3 dígitos,
                # cobrindo 00..99 e 000..999 sem perder "02".
                for n in range(NUM_SMALL_START, NUM_SMALL_END + 1):
                    num2 = f"{n:02d}"   # 00..99 e também 100..999 vira "100" (sem truncar)
                    num3 = f"{n:03d}"   # 000..999

                    out.write(name + num2 + "\n")
                    out.write(num2 + name + "\n")

                    out.write(name + num3 + "\n")
                    out.write(num3 + name + "\n")

    print("Wordlist gerada com sucesso em:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
