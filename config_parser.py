def read_config(filename: str) -> dict:
    config = {}

    with open(filename) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=")
            config[key] = value

    return config


if __name__ == "__main__":
    di = read_config("default_config.txt")
    print(di)
