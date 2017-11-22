from bs4 import BeautifulSoup
from eplist_urls import rating_list_urls
import Tkinter
import matplotlib.pyplot as plt
import numpy as np
import argparse
import requests
import copy
from imdb_episodes import ImdbRatedEpisodeSet

DEFAULT_URL = rating_list_urls['walkingdead']
SQUARE_SIZE = 40
MARGIN = int(SQUARE_SIZE / 2)
SPACING = int(SQUARE_SIZE / 10)
RGB_MAX = 255.0

class ImdbBlockInfographic(object):

    def __init__(self, eps):
        self.rated_list = eps.get_rate_sorted_list()
        self.cron_list = eps.get_cron_sorted_list()
        master = Tkinter.Tk()
        self.canvas_width = self.get_width()
        self.canvas_height = self.get_height()
        self.canvas = Tkinter.Canvas(master, 
                                     width=self.canvas_width, 
                                     height=self.canvas_height)
        self.canvas.pack()

    def get_number_of_seasons(self):
        max_season = 0
        for ep in self.cron_list:
            sid = int(ep.season_id)
            max_season = sid if sid > max_season else max_season
        return max_season

    def get_max_episode(self):
        max_episode = 0
        for ep in self.cron_list:
            eid = int(ep.episode_id)
            max_episode = eid if eid > max_episode else max_episode
        return max_episode

    def get_height(self):
        max_episode = self.get_max_episode()
        return (((SQUARE_SIZE + SPACING) * max_episode) + (2 * MARGIN))

    def get_width(self):
        number_seasons = self.get_number_of_seasons()
        return (((SQUARE_SIZE + SPACING) * number_seasons) + (2 * MARGIN))

    def draw_rectangle(self, x, y, color='red', text='10.0'):
        self.canvas.create_rectangle(x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=color)
        self.canvas.create_text((x + SQUARE_SIZE / 2, y + SQUARE_SIZE / 2 ), text=text)

    def get_red(self, rating):
        if rating <= 7.5:
            return RGB_MAX
        if rating >= 10.0:
            return 0.0
        return (RGB_MAX / -2.5) * (rating - 10.0)

    def get_green(self, rating):
        if rating >= 7.5:
            return RGB_MAX
        if rating <= 5.0:
            return 0.0
        return (RGB_MAX / 2.5) * (rating - 5.0)

    def get_blue(self, rating):
        return 0.0

    def map_rating_to_color(self, rating):
        green = self.get_green(rating)
        red = self.get_red(rating)
        blue = self.get_blue(rating)
        return '#%02x%02x%02x' % (red, green, blue)

    def plot_by_episode_num(self):
        y = int(self.canvas_height/2)
         
        for ep in self.cron_list:
            x = int(MARGIN + (SQUARE_SIZE + SPACING) * float(ep.season_id - 1))
            y = int(MARGIN + (SQUARE_SIZE + SPACING) * float(ep.episode_id - 1))
            color = self.map_rating_to_color(float(ep.user_rating))
            text = ep.user_rating
            self.draw_rectangle(x, y, color, text)

        # draw
        Tkinter.mainloop()
        
def get_full_link(series_id):
    return "http://www.imdb.com/title/{0}/eprate".format(series_id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--link", default=DEFAULT_URL)
    parser.add_argument("--series")
    args = parser.parse_args()
    link = get_full_link(args.series) if args.series else args.link
    eps = ImdbRatedEpisodeSet(link)
    plotter = ImdbBlockInfographic(eps)
    plotter.plot_by_episode_num()

if __name__ == '__main__':
    main()
