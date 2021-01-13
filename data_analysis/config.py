# subreddit names
subreddits = ["airbnb_hosts", "AirBnB", "couchsurfing", "vrbo", "CaregiverSupport", "Nanny", "AmazonFlexDrivers", 
            "InstacartShoppers", "instacart", "ShiptShoppers", "doordash", "doordash_drivers",
            "UberEATS", "grubhubdrivers", "postmates", "TaskRabbit", "RoverPetSitting",
            "Etsy", "EtsySellers", "uber", "uberdrivers", "lyftdrivers", "Lyft", 
            "mturk", "TurkerNation","HITsWorthTurkingFor", "vipkid", "Upwork", "Fiverr", "MusicEd"]
# subreddit and type of work
types = {
    "Housing/Accommodation": ["airbnb_hosts", "AirBnB", "couchsurfing", "vrbo"],
    "Caregiving": ["CaregiverSupport", "Nanny", "RoverPetSitting"],
    "Delivery": ["AmazonFlexDrivers", "InstacartShoppers", "instacart", "ShiptShoppers", "doordash", "doordash_drivers",
                "UberEATS", "grubhubdrivers", "postmates"],
    "Retail": ["Etsy", "EtsySellers"],
    "Passenger Transportation": ["uber", "uberdrivers", "lyftdrivers", "Lyft"],
    "Crowd Work": ["mturk", "TurkerNation","HITsWorthTurkingFor"],
    "Education": ["vipkid", "MusicEd"],
    "Freelance Labor": ["Upwork", "Fiverr", "TaskRabbit"],
}

# collective action words
lem_verbs = ['strike', 'join', 'organize', 'participate', 'fight', 'sue', 'protest', 'advocate', 'reform', 'defend', 'oppose', 'engage', 'prosecute', 'collective', 'action', 'activist', 'activism']