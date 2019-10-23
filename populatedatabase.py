from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Categories, Base, Items, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = create_engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


User1 = User

# Category: Soccer

category1 = Categories(name="Soccer")
session.add(category1)
session.commit()

# Soccer Items

categoryItem1 = Items(
    name="Soccer Ball",
    description="Ball used for the sport of Soccer",
    category=category1
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Soccer Cleats",
    description="Footwear used when playing Soccer. \
    Used for added traction on grassy fields",
    category=category1
)
session.add(categoryItem2)
session.commit()

# Category: Basketball

category2 = Categories(name="Basketball")
session.add(category2)
session.commit()

# Basetkball Items

categoryItem1 = Items(
    name="Basketball",
    description="Ball used for the sport of Basketball",
    category=category2
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Basketball Shoes",
    description="Shoes when playing Soccer. \
    Added traction while on the Basketball court",
    category=category2
)
session.add(categoryItem2)
session.commit()

# Category: Baseball

category3 = Categories(name="Baseball")
session.add(category3)
session.commit()

# Baseball Items

categoryItem1 = Items(
    name="Baseball",
    description="Ball used for the sport of Baseball",
    category=category3
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Baseball Bat",
    description="Bat used for hitting the baseball",
    category=category3
)
session.add(categoryItem1)
session.commit()

# Category: Frisbee

category4 = Categories(name="Frisbee")
session.add(category4)
session.commit()

# Frisbee Items

categoryItem1 = Items(
    name="Frisbee",
    description="Disc used for the sport of Frisbee",
    category=category4
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Frisbee Gloves",
    description="Gloves used to grip the Frisbee",
    category=category4
)
session.add(categoryItem2)
session.commit()

# Category: Snowboarding

category5 = Categories(name="Snowboarding")
session.add(category5)
session.commit()

# Snowboarding Items

categoryItem1 = Items(
    name="Snowboard",
    description="Board used for going down snowy mountains",
    category=category5
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Goggles",
    description="Protective eyewear for snowboarding",
    category=category5
)
session.add(categoryItem2)
session.commit()

# Category: Rock Climbing

category6 = Categories(name="Rock Climbing")
session.add(category6)
session.commit()

# Rock Climbing Items

categoryItem1 = Items(
    name="Harness",
    description="Harness used for safety when repelling",
    category=category6
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Climbing Shoes",
    description="Shoes used specifically for Rock Climbing",
    category=category6
)
session.add(categoryItem2)
session.commit()

# Category: Foosball

category7 = Categories(name="Foosball")
session.add(category7)
session.commit()

# Foosball Items

categoryItem1 = Items(
    name="Foosball Table",
    description="Table required to play the sport of Foosball",
    category=category7
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Foosball",
    description="Ball used for playing Foosball",
    category=category7
)
session.add(categoryItem2)
session.commit()

# Category: Skating

category8 = Categories(name="Skating")
session.add(category8)
session.commit

# Skating Items

categoryItem1 = Items(
    name="Skateboard",
    description="Board used to skate around",
    category=category8
)
session.add(categoryItem1)
session.commit

categoryItem2 = Items(
    name="Skateboarding Shoes",
    description="Shoes used while skateboarding to provide more grip",
    category=category8
)
session.add(category8)
session.commit()

# Category: Hockey
category9 = Categories(name="Hockey")
session.add(category9)
session.commit()

# Hockey Items

categoryItem1 = Items(
    name="Hockey Puck",
    description="Rubber puck used in Hockey games",
    category=category9
)
session.add(categoryItem1)
session.commit()

categoryItem2 = Items(
    name="Hockey Stick",
    description="Used to move and shoot the Hockey puck",
    category=category9
)
session.add(categoryItem1)
session.commit()
