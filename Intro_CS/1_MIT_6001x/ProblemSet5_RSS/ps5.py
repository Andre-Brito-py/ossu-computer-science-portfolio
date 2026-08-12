# Problem Set 5
# Name: Andre Brito
# Collaborators: None
# Time Spent: 2:00

import string

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word.lower()
        
    def is_word_in(self, text):
        text = text.lower()
        for punc in string.punctuation:
            text = text.replace(punc, ' ')
        words = text.split()
        return self.word in words

class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_title())

class DescriptionTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_description())

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) and self.t2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
        
    def evaluate(self, story):
        return self.t1.evaluate(story) or self.t2.evaluate(story)

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self): return self.guid
    def get_title(self): return self.title
    def get_description(self): return self.description
    def get_link(self): return self.link
    def get_pubdate(self): return self.pubdate

if __name__ == '__main__':
    story = NewsStory("1", "Hello World", "This is a great description.", "http://example.com", "Now")
    t1 = TitleTrigger("hello")
    t2 = DescriptionTrigger("great")
    t3 = AndTrigger(t1, t2)
    print("Does story match 'hello' in title and 'great' in description?", t3.evaluate(story))
