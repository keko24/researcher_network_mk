from researcher_network_mk.scraper.uklo_scrapers import (
    bezb_name_scraper,
    ekon_name_scraper,
    med_name_scraper,
    praven_name_scraper,
    ttfv_name_scraper,
    tutun_name_scraper,
    bioteh_name_scraper,
    fikt_name_scraper,
    ped_name_scraper,
    teh_name_scraper,
    turizam_name_scraper,
    vet_name_scraper
)

def main():
    bezb_name_scraper.main()
    ekon_name_scraper.main()
    med_name_scraper.main()
    praven_name_scraper.main()
    ttfv_name_scraper.main()
    tutun_name_scraper.main()
    bioteh_name_scraper.main()
    fikt_name_scraper.main()
    ped_name_scraper.main()
    teh_name_scraper.main()
    turizam_name_scraper.main()
    vet_name_scraper.main()

if __name__ == "__main__":
    main()
