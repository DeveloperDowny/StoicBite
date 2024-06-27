import regex as re
# Successful response from ready_quote_queue: (\{[^}]+\})
pattern = re.compile(r"Successful response from ready_quote_queue: (\{[^}]+\})")

filepath = "stoic_app_v2.log"

with open(filepath
            ) as f:
        log = f.read()
        matches = pattern.findall(log)
        # save all the groups found in a file in json list
        with open("stoic_app_v2_quotes.json", "w") as f:
            f.write("[\n")
            for match in matches:
                f.write(match + ",\n")
            f.write("]\n")