import model_fixt
import model_fixt

penny = model_fixt.Penguin(u'penny', u'fat')
prince = model_fixt.Penguin(u'prince', u'cool')
puck = model_fixt.Penguin(u'puck', u'boring')
penguins = (penny, prince, puck)

grace = model_fixt.Goose(u'grace', penny)
gale = model_fixt.Goose(u'gale', prince)
ginger = model_fixt.Goose(u'ginger', puck)
geese = (grace, gale, ginger)
