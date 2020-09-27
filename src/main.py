import yaml
import tweepy

from src.twitter_fragment import TwitterFragment
from src.local_fragment import LocalFragment

username = "zeryx1211"


def parse_adventure(file_path):
    with open(file_path) as f:
        adventure = yaml.safe_load(f)
    return adventure

def parse_credentials(file_path):
    with open(file_path) as f:
        credentials = yaml.safe_load(f)
    consumer = credentials['credentials']['consumerAPI']
    access = credentials['credentials']['access']
    auth = tweepy.OAuthHandler(consumer['key'], consumer['secret'])
    auth.set_access_token(access['token'], access['secret'])
    api = tweepy.API(auth)
    return api


def construct_node(node_id, story):
    story_node = [fragment for fragment in story if fragment['id'] == node_id][0]
    if 'end' in story_node['options']:
        node = LocalFragment(node_id, story_node['body'], terminus=story_node['options']['end'])
    else:
        node = LocalFragment(node_id, story_node['body'], left_path=story_node['options']['left'], right_path=story_node['options']['right'])
    if node.left:
        node.left['fragment'] = construct_node(node.left['id'], story)
    if node.right:
        node.right['fragment'] = construct_node(node.right['id'], story)
    return node


def create_twitter_story(node: LocalFragment, api):
    twitter_node = TwitterFragment(node, api)
    if not twitter_node.terminus:
        left_node = create_twitter_story(node.left['fragment'], api)
        right_node = create_twitter_story(node.right['fragment'], api)
        twitter_node.add_paths(username, left_node, right_node, api)
    return twitter_node



def create_adventure(adventure_path, api):
    adventure_data = parse_adventure(adventure_path)
    story = adventure_data['story']
    local_tree = construct_node(0, story)
    twitter_tree = create_twitter_story(local_tree, api)
    return twitter_tree

