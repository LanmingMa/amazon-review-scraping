# from selenium import webdriver
# from selenium.webdriver.support.select import Select
#
# import time
# import random
# import pandas as pd
# import json
# import csv
# import glob
#
# normal_delay = random.normalvariate(3, 0.5)
# normal_delay_2 = random.normalvariate(5, 0.5)
# normal_delay_3 = random.normalvariate(7, 0.5)
#
# # driver = webdriver.Chrome(executable_path='chromedriver.exe')
# driver = webdriver.Chrome()
# # driver.get('https://www.amazon.com/gp/profile/amzn1.account.AHE3Z2VKA7WXH3V5R3H2FQSZDNIA/ref=cm_cr_arp_d_gw_btm?ie=UTF8')
# time.sleep(normal_delay_2)
#
#
# def user_info(driver):
#     helpful_votes = []
#     reviews = []
#     hearts= []
#     idea_lists = []
#     user_rankings = []
#     latest_times = []
#     time.sleep(normal_delay_3)
#     helpful_votes.append(driver.find_element_by_css_selector("#profile_v5 > div > div > "
#                                                              "div.a-section.activity-area-container > "
#                                                              "div.deck-container.main > "
#                                                              "div.desktop.padded.card.dashboard-desktop-card > "
#                                                              "div:nth-child(2) > div > div:nth-child(1) > a > "
#                                                              "div > div.dashboard-desktop-stat-value > "
#                                                              "span").text)
#     reviews.append(driver.find_element_by_css_selector("#profile_v5 > div > div > "
#                                                        "div.a-section.activity-area-container > "
#                                                        "div.deck-container.main > "
#                                                        "div.desktop.padded.card.dashboard-desktop-card > "
#                                                        "div:nth-child(2) > div > div:nth-child(2) > "
#                                                        "a > div > div.dashboard-desktop-stat-value > "
#                                                        "span").text)
#     hearts.append(driver.find_element_by_css_selector("#profile_v5 > div > div > "
#                                                        "div.a-section.activity-area-container > "
#                                                        "div.deck-container.main > "
#                                                        "div.desktop.padded.card.dashboard-desktop-card > "
#                                                        "div:nth-child(2) > div > div:nth-child(3) > "
#                                                        "a > div > div.dashboard-desktop-stat-value > "
#                                                        "span").text)
#     idea_lists.append(driver.find_element_by_css_selector("#profile_v5 > div > div > "
#                                                       "div.a-section.activity-area-container > "
#                                                       "div.deck-container.main > "
#                                                       "div.desktop.padded.card.dashboard-desktop-card > "
#                                                       "div:nth-child(2) > div > div:nth-child(4) > "
#                                                       "a > div > div.dashboard-desktop-stat-value > "
#                                                       "span").text)
#     # user_rankings.append(driver.find_element_by_css_selector("#profile_v5 > div > div"
#     #                                                   "div.a-section.activity-area-container > "
#     #                                                   "div.deck-container.sub > "
#     #                                                   "div:nth-child(3) > div.a-row > div.a-section > "
#     #                                                   "div.a-section.a-spacing-top-base > div.a-row.a-spacing-base > "
#     #                                                   "a > div.a-row > span").text)
#     # latest_times.append(driver.find_element_by_css_selector("#profile_v5 > div > div"
#     #                                                          "div.a-section.activity-area-container > "
#     #                                                          "div.deck-container.main > "
#     #                                                          "div.customer-profile-timeline > "
#     #                                                          "div.profile-at-card-container > "
#     #                                                          "div.desktop card profile-at-card profile-at-review-box > "
#     #                                                          "div.a-row > "
#     #                                                          "div.a-row a-spacing-none profile-at-header profile-at-desktop-header"
#     #                                                          "div > div.a-profile > div.a-profile-content > "
#     #                                                          "span:nth-child(2)").text)
#     driver.back()
#     time.sleep(normal_delay_3)
#     return pd.DataFrame({'Author': author_name, 'helpful_votes': helpful_votes, 'reviews': reviews,
#                          'hearts': hearts, 'idea_lists': idea_lists,
#                          # 'user_ranking': user_rankings,
#                          # 'latest_time': latest_times
#                          })
#
#
# def to_csv():
#     path = r'~/Documents/GitHub/Amazon-Review-Scrapy'
#     allFiles = glob.glob(path + "/*.csv")
#     frame = pd.DataFrame()
#     list_ = []
#     for file_ in allFiles:
#         df = pd.read_csv(file_, index_col=None, header=0)
#         list_.append(df)
#     return pd.concat(list_)
#
#
# df = pd.DataFrame(columns=['Author', 'helpful_votes', 'reviews','hearts','idea_lists',
#                            # 'user_rankings', 'latest_time'
#                            ])
# with open("amazon.csv", "r") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     next(csv_reader)
#     count = 0
#     for line in csv_reader:
#         author_name = line[4]
#         user_link = line[3]
#         driver.get('https://www.amazon.com' + str(user_link) + '/ref=cm_cr_arp_d_gw_btm?ie=UTF8')
#         temp = user_info(driver)
#         df = pd.concat([df, temp], axis=0)
#         # count += 1
#         # if count == 14:
#         #     df.to_csv('user_info.csv')
#         #     count = 0
#     df.to_csv('user_info.csv')
#
# time.sleep(normal_delay_2)
# driver.close()
