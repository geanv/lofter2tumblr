# lofter2tumblr

lofter2tumblr is a python project that helps one to migrate blogs from LOFTER.com to Tumblr.com. lofter2tumblr requires a source XML file exported from LOFTER, and uses open APIs to post blogs on Tumblr.


## Preparation

To migrate the blogs from LOFTER to Tumblr, you need to prepare the following things:

- Python 2.7 runtime environment: [download Python](https://www.python.org/downloads/)
- The XML file consisting of all the posts exported from LOFTER: [export the posts](http://www.lofter.com/export)
- An OAuth key of Tumblr for using the open API: [register one](https://www.tumblr.com/oauth/apps)

## Migrating to Tumblr

- Backup LOFTER XML file

After logging into [LOFTER](http://www.lofter.com/export) with your account, go to the "export" page by clicking "更多->导入导出" on the top bar. Choose the blog that you want to export, and export the XML file by clicking "导出XML文件".

- Register an OAuth key of Tumblr

Go to the [register page](https://www.tumblr.com/oauth/apps), and register a new application. You will get a pair of keys such as:

>consumer_key: **********icCHd47HFuTrL5AjqB6V75XgYm1tTmItovcgCh
>
>consumer_secret: **********INjcFwIv1lmekj8qhbExXkHJ8A23k5X8jK3DVCl

Mark them down. You will need to use them in the importer program.

- Run importer

Download the project and go to the folder where `importer.py` locates. Make sure you have Python 2.7 runtime environment. Run the program named `importer.py`, or open the command window and type:

	python importer.py

The program will ask you to type your `consumer_key` and `consumer_secret` at the first time. It will store the keys and oauth token on your home directory once the authentication is finished. If the authentication finishes correctly, you can input the name of the XML file. It's better to put the XML file is in the same folder with `importer.py`.

	Input the XML file exported from LOFTER: blog.xml

Then, you will need to input your blog url or name, such as `blog-name.tumblr.com` or just using the blog name `blog-name`.

	Input site address (e.g., abc.tumblr.com): blog-name

The importer will ask you if you need to delete all the existing posts on that blog. If you type `Y`, the importer will delete all the posts. So, be carefull to use this function. To skip deleting, just type `Enter`.

	Delete all posts first? ("Y" to delete):

After all the setups, the importer begins to parse the XML file, download the necessary images and post the items to Tumblr. The posts will be sorted by the publish time. The earlier published ones will be posted first.

	----------- Delete all posts at blog-name ------------
	[1 Deleted] {u'id': 144230413380L}
	[2 Deleted] {u'id': 144230410185L}
	[3 Deleted] {u'id': 144230406025L}
	----------- Format post from LOFTER XML ------------
	[1 Find post] type: Photo, id: 10nf79_9234r941
	 - [Downloading] http://imglf2.nos.netease.com/img/RkJreGZSEx.jpg
	 - [Downloading] http://imglf2.nos.netease.com/img/kJreGxRPT0.jpg
	[2 Find post] type: Text, id: 10nf79_9234r942
	[3 Find post] type: Text, id: 10nf79_9234r921
	----------- Send post to blog-name -------------
	[1 Posting item] type: Text, id: 10nf79_9234r942
	 - [Succeed] Post id: 144230475595
	[2 Posting item] type: Text, id: 10nf79_9234r921
	 - [Succeed] Post id: 144230475230
	[3 Posting item] type: Photo, id: 10nf79_9234r941
	 - [Removing] temp file: RkJreGZSEx.jpg
	 - [Removing] temp file: kJreGxRPT0.jpg
	 - [Succeed] Post id: 144233385685
	[Result] All posts are uploaded: 3 posts

If the posting operation fails after retrying 5 times, the importer will treat this post as a failed post. It will report the IDs of all failed posts in the end.

# Copyright and license

Project copyright 2016 by GJ.

API copyright 2013 by Tumblr, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this work except in compliance with the License. You may obtain a copy of
the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations.
