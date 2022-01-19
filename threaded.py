from _thread import start_new_thread
import threading
import chefkoch




def scrape_thread(chefkoch):
    print("scraping")
    chefkoch = chefkoch.RecipeScraper()
    chefkoch.scrapeRecipe("inf")


def main():
    for i in range(10):
        objectname = f"x{i}"
        objectname = threading.Thread(target=scrape_thread, args=(chefkoch,))
        objectname.start()
    
    

if __name__ == "__main__":
    main()