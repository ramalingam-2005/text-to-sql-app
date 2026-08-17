

def format_results(rows):
    """
    Convert database rows into a JSON-friendly format.
    """

    formatted_rows = []

    for row in rows:
        formatted_rows.append(dict(row))

    return formatted_rows


if __name__ == "__main__":

    rows = [
        {
            "name": "John",
            "city": "Chennai"
        },
        {
            "name": "David",
            "city": "Coimbatore"
        }
    ]

    results = format_results(rows)

    print(results)