"""Reddit bot konfigürasyon dosyası."""


class Config:
    """Reddit bot konfigürasyon sınıfı."""
    
    USER_AGENT = "PetBot/1.0"
    
    # Yorum metinleri (rastgele seçilecek)
    COMMENT_TEXTS = [
        "I've been working on a small side project called PawNear. It helps people share nearby lost or found animals on a map. If you want to try it out and tell me what you think, feel free.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I recently released PawNear, a simple app that gathers local lost and found animal posts in one place. If this kind of tool is useful to you, you can give it a look.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I built a lightweight app named PawNear to make it easier to track lost, found, and injured animals around your neighborhood. Anyone who wants to check it out is welcome.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "If you're someone who likes helping animals in your area, PawNear might be useful. It's a small map-based app for nearby lost and found animal reports. Try it if you want.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I've launched a simple community tool called PawNear. It organizes lost animal reports from your surroundings and shows them clearly on a map. You can test it and share feedback.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "For anyone interested in local animal welfare, I put together a basic app called PawNear. You can post or browse nearby lost/found animals. Check it out if you're curious.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I just made PawNear, a small tool to help organize lost and found animal posts in crowded cities. If you'd like to explore it or leave thoughts, here it is.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "Here's something I've been working on lately: PawNear, an app that shows lost and found animals around you. It's minimal and straightforward. Feel free to try it.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I created PawNear to centralize nearby lost and found animal info in one place. It might help people who follow such posts often. You can take a look if you'd like.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "If you often see lost animal posts and wish they were easier to track, I built a small app called PawNear. It's designed for quick browsing. Try it whenever you want.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I've been experimenting with a small project called PawNear. It lets people view and share nearby lost or found animals on a map. You can check it out if you want.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I made an app named PawNear to keep local lost and found animal posts in one place. If you're curious about tools like this, you can try it.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "If you've ever tried to follow lost animal posts in your area, you know how scattered they are. PawNear is my attempt to gather them on a single map. Check it out if you'd like.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I built PawNear as a small, map-focused app for people who want to keep track of lost or found animals around them. Anyone who wants to try it is welcome.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "Recently finished a simple tool called PawNear. It shows nearby lost and found animal reports so you don't have to search across multiple platforms. Have a look if you want.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I've been working on PawNear, an app that makes it easier to see lost or found animal posts close to your location. If it sounds useful, give it a try.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "Here's something simple I put together: PawNear. It helps people share lost/found animal info with exact locations. Feel free to check it out.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I created PawNear because local animal posts were too scattered to follow. Now they show up on a single map. Try it out if you're curious.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "If you care about neighborhood animals, you might find PawNear helpful. It's a small app to browse nearby lost or found animal reports. Check it out whenever.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear",
        "I made PawNear to make lost animal updates easier to follow in crowded areas. It's straightforward and map-based. You can take a look if you'd like.\n\nAndroid: https://play.google.com/store/apps/details?id=com.petrichor.pawnear"
    ]
    
    # Evcil hayvan subredditleri
    PET_SUBREDDITS = [
        "aww",
        "cats",
        "dogs",
        "puppies",
        "kittens",
        "rarepuppers"
    ]

