import random

ASTANA_LATITUDE = 51.169392
ASTANA_LONGITUDE = 71.449074


def generate_random_place_in_astana() -> tuple[float, float]:
    """Generate random place in Astana. Maximal radius is 5km"""
    latitude_delta = (random.random() - 0.5) * 0.1
    longitude_delta = (random.random() - 0.5) * 0.1

    return ASTANA_LATITUDE + latitude_delta, ASTANA_LONGITUDE + longitude_delta


def random_dict(source: dict, coefficient: int = 2) -> dict:
    """Returns dict with random elements and random size"""
    # result = {}  # Another implementation
    # for _ in range(random.randint(len(source) // 4, len(source))):
    #     key, value = random.choice(list(source.items()))
    #     result[key] = value
    # return result
    return dict(
        random.sample(
            source.items(), random.randint(len(source) // coefficient, len(source))
        )
    )


def random_int_from_string(source: str, limit: int = 100000) -> int:
    """Returns fake-random int using string. String can be anything"""
    return int.from_bytes(source.encode(), "little") % limit


if __name__ == "__main__":
    for _ in range(10):
        print(generate_random_place_in_astana())
