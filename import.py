#!/usr/bin/python

import pytumblr
import yaml
import os
import urlparse
import code
import oauth2 as oauth    
    
import urllib

import xml.etree.ElementTree as ET
import json
import time
import string

import sys

def download_img(url, file_name):
    print " - [Downloading] " + url
    urllib.urlretrieve(url, file_name)

def format_time(publish_time):
    x = time.localtime(string.atof(publish_time)/1000)
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    publish_time_GMT = time.strftime(GMT_FORMAT, x)
    return publish_time_GMT

def send_post(post_item, site):
    #posting
    if (post_item['type'] == 'Photo'):
        ret = client.create_photo(site, state="published", date=post_item['date'], format="html", data=post_item['data'], caption=post_item['caption'])
        
        for file_name in post_item['data']:
            if os.path.isfile(file_name):
                print " - [Removing] temp file: " + file_name
                os.remove(file_name)
    if (post_item['type'] == 'Text'):
        ret = client.create_text(site, state="published", date=post_item['date'], title=post_item['title'], body=post_item['body'], native_inline_images=True)    
    
    if ('id' in ret):
        print " - [Succeed] Post id: " + str(ret['id'])
        return True
    else:
        print " - [Failed] Tumblr.com response: " + str(ret['response'])
        return False

def add_post(tree, site):
    print "----------- Format post from LOFTER XML ------------"
    post_list = []
    count = 1
    for post in tree.iterfind('PostItem'):
        #type
        type = post.find('type')
        id = post.find('permalink')
        #time
        publish_time = post.find('publishTime')
        GMT_time = format_time(publish_time.text)
        
        post_item = {
            "type": type.text,
            "time": publish_time.text,
            "date": GMT_time,
            "id": id.text,
        }
        print "[" + str(count) + " Find post] type: " + post_item['type'] + ", id: " + post_item['id']
        count = count + 1
        
        #A photo
        if (type.text == 'Photo'):
            #caption
            caption = post.find('caption')
            post_item['caption'] = caption.text
            #imgs
            photo_links = post.find('photoLinks')
            urls = json.loads(photo_links.text)
            file_names = []
            for url in urls:
                if "raw" in url:
                    img = url['raw']
                elif "orign" in url:
                    img = url['orign']
            file_name = img[img.rfind('/') + 1: len(img)]
            download_img(img, file_name)
            file_names.append(file_name)            
            post_item['data'] = file_names
            
            #posting
            #print "Posting photo: " + GMT_time
            #ret = client.create_photo(site, state="published", date=GMT_time, format="html", data=file_names, caption=caption.text)
            #print ret            
            
        if (type.text == 'Text'):
            #title
            title = post.find('title')
            post_item['title'] = title.text
            #body
            content = post.find('content')            
            post_item['body'] = content.text
            
            #posting
            #print "Posting text: " + GMT_time
            #ret = client.create_text(site, state="published", date=GMT_time, title=title.text, body=content.text)
            #print ret
            
        post_list.append(post_item)
        
    #sort by time
    print "----------- Send post to " + site + " ------------"
    post_list.sort(key=lambda post:post['time'])
    count = 1
    failed_post = []
    for post_item in post_list:
        print "[" + str(count) + " Posting item] type: " + post_item['type'] +  ", id: " + post_item['id']
        count = count + 1
        
        retry_times = 0
        while not send_post(post_item, site) and retry_times < 5:
            print " - [Re-posting] Post id: " + post_item['id']
            retry_times = retry_times + 1
        
        if retry_times == 5:
            failed_post.append(post_item['id'])
    
    if not failed_post:
        print "[Result] All posts are uploaded: " + str(count) + " posts"
    else:
        print "[Result] Failed posts: " + str(failed_post)
        
def del_all_posts(site):
    print "----------- Delete all posts at " + site + " ------------"
    posts_info = client.posts(site)
    while posts_info['total_posts'] > 0:
        for post in posts_info['posts']:
            ret = client.delete_post(site, post['id'])
            print "[Deleted] " + str(ret)
        posts_info = client.posts(site)

def new_oauth(yaml_path):
    '''
    Return the consumer and oauth tokens with three-legged OAuth process and
    save in a yaml file in the user's home directory.
    '''

    print 'Retrieve consumer key and consumer secret from http://www.tumblr.com/oauth/apps'
    consumer_key = raw_input('Paste the consumer key here: ')
    consumer_secret = raw_input('Paste the consumer secret here: ')

    request_token_url = 'http://www.tumblr.com/oauth/request_token'
    authorize_url = 'http://www.tumblr.com/oauth/authorize'
    access_token_url = 'http://www.tumblr.com/oauth/access_token'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # Get request token
    resp, content = client.request(request_token_url, "POST")
    request_token =  urlparse.parse_qs(content)

    # Redirect to authentication page
    print '\nPlease go here and authorize:\n%s?oauth_token=%s' % (authorize_url, request_token['oauth_token'][0])
    redirect_response = raw_input('Allow then paste the full redirect URL here:\n')

    # Retrieve oauth verifier
    url = urlparse.urlparse(redirect_response)
    query_dict = urlparse.parse_qs(url.query)
    oauth_verifier = query_dict['oauth_verifier'][0]

    # Request access token
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'][0])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = urlparse.parse_qs(content)

    tokens = {
        'consumer_key': consumer_key,
        'consumer_secret': consumer_secret,
        'oauth_token': access_token['oauth_token'][0],
        'oauth_token_secret': access_token['oauth_token_secret'][0]
    }

    yaml_file = open(yaml_path, 'w+')
    yaml.dump(tokens, yaml_file, indent=2)
    yaml_file.close()

    return tokens

if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    yaml_path = os.path.expanduser('~') + '/.tumblr'

    if not os.path.exists(yaml_path):
        tokens = new_oauth(yaml_path)
    else:
        yaml_file = open(yaml_path, "r")
        tokens = yaml.safe_load(yaml_file)
        yaml_file.close()

    client = pytumblr.TumblrRestClient(
        tokens['consumer_key'],
        tokens['consumer_secret'],
        tokens['oauth_token'],
        tokens['oauth_token_secret']
    )

    print 'pytumblr client created. You may run pytumblr commands prefixed with "client".\n'
    
    #file_name = 'test.xml'
    file_name = raw_input("Input the XML file exported from LOFTER: ")
    tree = ET.ElementTree(file=file_name)
    #site_url = '2016-4-3.tumblr.com'
    site_url = raw_input("Input site address (e.g., abc.tumblr.com): ")
    delete_all = raw_input("Delete all posts first? (\"Y\" to delete): ")
    
    if delete_all == 'Y' or delete_all == 'y':
        del_all_posts(site_url)
        
    add_post(tree, site_url)
    