from bs4 import BeautifulSoup
from eplist_urls import rating_list_urls
import matplotlib.pyplot as plt
import numpy as np
import argparse
import requests
import copy

DEFAULT_URL = rating_list_urls['walkingdead']
MAX_RATING = 10

class ImdbRatedEpisode(object):

    def __init__(self, season_id, episode_id, title,
                 user_rating, user_votes):
        self.season_id = season_id
        self.episode_id = episode_id
        self.title = title
        self.user_rating = user_rating
        self.user_votes = user_votes

    def __repr__(self):
         return "Season {0}: Episode #{1} - {2}, rated {3}/{4} by {5}".format(            self.season_id,
            self.episode_id,
            str(self.title),
            self.user_rating,
            MAX_RATING,
            self.user_votes)

    def is_before(self, other_ep):
        if self.season_id == other_ep.season_id:
            return self.episode_id < other_ep.episode_id
        return self.season_id < other_ep.season_id

    def is_after(self, other_ep):
        if self.season_id == other_ep.season_id:
            return self.episode_id < other_ep.episode_id
        return self.season_id < other_ep.season_id
    
    def is_same_ep_num(self, other_ep):
        return not (self.is_before(other_ep) or self.is_after(other_ep))

    def is_rated_higher(self, other_ep):
        return self.user_rating > other_ep.user_rating

    def is_rated_lower(self, other_ep):
        return self.user_rating > other_ep.user_rating

    def is_rated_same(self, other_ep):
        return self.user_rating == other_ep.user_rating

class ImdbRatedEpisodeSet(object):

    def __init__(self, url=DEFAULT_URL):
        self.url = url
        self.episode_list = self.parse_imdb_link(self.url)

    def get_rate_sorted_list(self):
        copy_list = copy.deepcopy(self.episode_list)
        for i in range(0,len(copy_list)):
            for j in range(0, len(copy_list)):
                if copy_list[i].is_rated_lower(copy_list[j]):
                    temp = copy_list[i]
                    copy_list[i] = copy_list[j]
                    copy_list[j] = temp
        return copy_list
 
    def get_cron_sorted_list(self):
        copy_list = copy.deepcopy(self.episode_list)
        #Small list, just bubble sort by season then episode
        for i in range(0,len(copy_list)):
            for j in range(0, len(copy_list)):
                if copy_list[i].is_after(copy_list[j]):
                    temp = copy_list[i]
                    copy_list[i] = copy_list[j]
                    copy_list[j] = temp
        return copy_list
                

    def parse_epnum(self, epnum_str):
        season, episode = epnum_str.strip().split(".")
        return int(season), int(episode)

    def parse_imdb_link(self, url):
        episode_list = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            table_div = soup.find('div', {'id': 'tn15content'})
            table = table_div.find('table')
            rows = table.find_all_next("tr")
            header_row = True 
            for row in rows:
                contents = row.find_all_next('td')
                if not header_row:
                    season_num, ep_num = self.parse_epnum(contents[0].string)
                    title = u''.join(contents[1].string).encode('utf-8').strip()
                    user_rating = float(contents[2].string)
                    user_votes = int(contents[3].string.replace(',',''))
                    ep = ImdbRatedEpisode(season_num, ep_num, title,
                                          user_rating, user_votes)
                    episode_list.append(ep)
                else:
                    header_row = False
        except:
            pass
        return episode_list


