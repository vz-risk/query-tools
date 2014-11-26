import fixture_model

penny = fixture_model.Penguin(u'penny', u'fat')
prince = fixture_model.Penguin(u'prince', u'cool')
puck = fixture_model.Penguin(u'puck', u'boring')
penguins = (penny, prince, puck)

grace = fixture_model.Goose(u'grace', penny)
gale = fixture_model.Goose(u'gale', prince)
ginger = fixture_model.Goose(u'ginger', puck)
geese = (grace, gale, ginger)
