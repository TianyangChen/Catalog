from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user
User1 = User(name="John Doe", email="johndoe@gmail.com")
session.add(User1)
session.commit()

# Add 9 categories
category1 = Category(name="Soccer")
session.add(category1)
session.commit()

category2 = Category(name="Basketball")
session.add(category2)
session.commit()

category3 = Category(name="Baseball")
session.add(category3)
session.commit()

category4 = Category(name="Frisbee")
session.add(category4)
session.commit()

category5 = Category(name="Snowboarding")
session.add(category5)
session.commit()

category6 = Category(name="Rock Climbing")
session.add(category6)
session.commit()

category7 = Category(name="Foosball")
session.add(category7)
session.commit()

category8 = Category(name="Skating")
session.add(category8)
session.commit()

category9 = Category(name="Hockey")
session.add(category9)
session.commit()

print "Add 9 categories successfully!"

categoryItem = CategoryItem(
    name="Soccer Cleats",
    description="This is the description of soccer clearts.",
    category=category1,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Jersey",
    description="This is the description of jersey.",
    category=category1,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Bat",
    description="This is the description of bat.",
    category=category3,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Frisbee",
    description="This is the description of Frisbee.",
    category=category4,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Shinguards",
    description="This is the description of Shinguards.",
    category=category1,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Two shinguards",
    description="This is the description of Two shinguards.",
    category=category1,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Snowboard",
    description="This is the description of Snowboard.",
    category=category5,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Goggles",
    description="This is the description of Goggles.",
    category=category5,
    user=User1)
session.add(categoryItem)
session.commit()

categoryItem = CategoryItem(
    name="Stick",
    description="This is the description of Stick.",
    category=category9,
    user=User1)
session.add(categoryItem)
session.commit()

print "Add 9 menu items successfully! -- John Doe"
