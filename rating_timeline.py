from bs4 import BeautifulSoup
from eplist_urls import rating_list_urls
import matplotlib.pyplot as plt
import numpy as np
import argparse
import requests
import copy
from imdb_episodes import ImdbRatedEpisodeSet

DEFAULT_URL = rating_list_urls['walkingdead']

class ImdbRatedEpisodePlotter(object):

    def __init__(self, eps):
        self.rated_list = eps.get_rate_sorted_list()
        self.cron_list = eps.get_cron_sorted_list()

    def plot_by_episode_num(self):
        num_eps = len(self.cron_list)
        ep_ratings = [x.user_rating for x in self.cron_list]
        diff_list = [0] + [ep_ratings[x-1] - ep_ratings[x] for x in range(0, num_eps) if x > 0]
        

        episodes = np.array(range(0,num_eps))
        y_stack = np.row_stack((ep_ratings))

        fig = plt.figure(figsize=(10,5))
        ax1 = fig.add_subplot(111)

        ax1.plot(episodes, ep_ratings, label='Episodes', color='r', marker='o')
        #ax1.plot(episodes, diff_list, label='Episodes', color='g', marker='o')
        plt.xticks(episodes)
        plt.xlabel('Episodes')


        #fit1 = np.polyfit(num_eps, ep_ratings, 1)
        #fit1_fn = np.poly1d(fit1)
        #fit2 = np.polyfit(num_eps, diff_list, 1)
        #fit2_fn = np.poly1d(fit2)

        handles, labels = ax1.get_legend_handles_labels()
        lgd = ax1.legend(handles, labels, loc='upper center', bbox_to_anchor=(1.15,1))

        plt.savefig('smooth_plot.png')
        plt.show()
 
def get_full_link(series_id):
    return "http://www.imdb.com/title/{0}/eprate".format(series_id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--link", default=DEFAULT_URL)
    parser.add_argument("--series")
    args = parser.parse_args()
    link = get_full_link(args.series) if args.series else args.link
    eps = ImdbRatedEpisodeSet(link)
    plotter = ImdbRatedEpisodePlotter(eps)
    plotter.plot_by_episode_num()

if __name__ == '__main__':
    main()
