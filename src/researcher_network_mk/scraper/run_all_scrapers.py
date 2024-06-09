from researcher_network_mk.scraper.ukim_scrapers import run_all_ukim_scrapers
from researcher_network_mk.scraper.uklo_scrapers import run_all_uklo_scrapers
from researcher_network_mk.scraper.ugd_scrapers import ugd_name_scraper
from researcher_network_mk.scraper.unite_scrapers import unite_name_scraper

def main():
    ugd_name_scraper.main()
    unite_name_scraper.main()
    run_all_uklo_scrapers.main()
    run_all_ukim_scrapers.main()

if __name__ == "__main__":
    main()
