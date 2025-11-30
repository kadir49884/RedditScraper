"""Reddit bot konfigürasyon dosyası."""


class Config:
    """Reddit bot konfigürasyon sınıfı."""
    
    USER_AGENT = "PetBot/1.0"
    
    # Yorum metinleri (rastgele seçilecek)
    COMMENT_TEXTS = [
        "I've been trying to solve the problem of scattered lost animal posts, so I built a small app called PawNear.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nIf you check it out, I'd like to know whether the map approach makes sense.",
        "I kept seeing lost animal updates across different platforms and wanted a cleaner way to track them, so I made PawNear.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nLet me know if the layout feels useful in real situations.",
        "I put together a simple tool named PawNear for nearby lost/found animal reports.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nI'm curious how people from different cities experience it.",
        "I built PawNear to make following local lost animal posts less chaotic.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nAny honest first impressions would help me shape the next steps.",
        "Lost animal posts were too scattered where I live, so I created PawNear to centralize them.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nI wonder if the idea feels practical to others who deal with similar issues.",
        "I recently finished a small app called PawNear that shows nearby lost and found animals on a map.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nWould love to know if the interface makes things easier to follow.",
        "I've been working on PawNear as a simple space for posting and viewing local lost animals.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nI'm open to any thoughts on whether this kind of tool is actually needed.",
        "I made PawNear because searching for lost animals across multiple pages felt overwhelming.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nIf you try it, I'd like to hear how the map-based view feels.",
        "PawNear is a small project I released to help people share lost and found animals with location details.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nLet me know if the idea connects with real-world use.",
        "I created PawNear as a minimal tool for nearby lost animal alerts.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nI'm trying to understand how intuitive it feels to someone new.",
        "I built PawNear after noticing how difficult it is to track lost animal posts consistently.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nFeedback from fresh eyes would help me improve it.",
        "I designed PawNear to gather lost and found animal reports into one simple feed.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nCurious if the clean design works well for others too.",
        "I've been testing PawNear, a map tool for viewing animals reported lost or found near you.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nIf you give it a try, I'd appreciate any reaction to the overall flow.",
        "I built PawNear for people who want an easier way to follow local lost animal updates.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nInterested to know how it feels on a first use without context.",
        "Here's a small project I made called PawNear — it keeps nearby lost/found animal cases organized.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nLet me know if anything stands out as unclear or helpful.",
        "I put together PawNear as a central place for lost animal posts with map locations.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nAny feedback about usability would be valuable.",
        "I've been trying to simplify how people follow lost animal notices, so I created PawNear.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nI'd like to see how others respond to the idea.",
        "I made PawNear to help track lost and found animals more efficiently.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nIf you check it out, I'm curious whether the concept feels solid.",
        "I launched PawNear to gather lost animal reports that are usually scattered everywhere.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nWould love to hear what kind of improvements users expect.",
        "I developed PawNear for anyone trying to keep up with local lost/found animal updates.\n\nhttps://play.google.com/store/apps/details?id=com.petrichor.pawnear\n\nI'm interested in how it feels compared to following posts on social media."
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

