def main():
    with open("scholar_scraper.log", "r") as f:
        lines = f.readlines()
        for line in lines:
            if (
                "An error occured for"
                in line
                # or "found but with an email domain" in line
            ):
                print(line)


if __name__ == "__main__":
    main()
