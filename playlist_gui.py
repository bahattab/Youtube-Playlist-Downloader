from tkinter import *
import requests
import os
import sys
from urllib.parse import quote
from urllib.parse import urljoin
from bs4 import BeautifulSoup







def download_video(url,quality,extension,domain,count):
	#print("Lets download")
	filename=''
	try:
		vid_page=requests.get(url)
		vid_page_soup=BeautifulSoup(vid_page.text,'html.parser')
		filename=str(count)+'  '+vid_page_soup.find('span',id='eow-title').get('title').split('/')[0].split('.')[0].split('(')[0].split(')')[0].split('[')[0].split(']')[0].split('{')[0].split('}')[0].split('!')[0]
		#print(filename)
	except:
		print("Downloading of VIDEO " +str(count)+" FAILED.Check your internet connection \n" )
		return
	filename=filename+'.'+extension.lower()
	print(filename +'\n')
	get_url=quote(url,safe='')
	keepvid=''
	try:
		keep_vid=requests.get("http://www.keepvid.com/?url="+get_url)
	except:
		print("Downloading of VIDEO " +str(count)+" FAILED.Check your internet connection \n" )
		return
	soup=BeautifulSoup(keep_vid.text,'html.parser')
	if not soup.find('div',class_="d-info"):
		print("AN ERROR OCCURED.Downloading of video "+str(count)+" Failed \n")
		return 
	else:
		pass
	vid_url=None
	for li in soup.find('div',class_="d-info").find('ul').find_all('li'):
		#print("Ext -->" , extension ,'\n')
		#print("Quality -->",quality,'\n')
		#print(li.a.string,'\n')
		#print(li.b.string,'\n')
		if (quality in li.b.string) and (extension in li.a.string):
			#print(li.a.get('href'))
			vid_url=li.a.get('href')
			break
	if not vid_url:
		print("Check the extension and quality provided \n")
		return
	try:
		vid_request=requests.get(vid_url)
		#print("Here")
		f=open(domain+'/'+filename,'wb')
		f.write(vid_request.content)
		f.close()
	except:
		print("Downloading of video "+str(count)+" failed \n")

def playlist(url,quality,extension,domain):
	playlist_page=''
	try:
		playlist_page=requests.get(url)
	except:
		print("Failed \n Check the url you provided \n")
		return
	soup=BeautifulSoup(playlist_page.text,'html.parser')
	folder=soup.find('h1',class_="pl-header-title").string
	if not folder:
		print("Error \n")
		return
	folder=folder.split('/')[0].split('.')[0]
	domain=domain+'/'+folder
	os.makedirs(domain)
	#print("Hey")
	tbody=soup.find('tbody',id="pl-load-more-destination")
	if not tbody:
		print("Error \n")
		return
	count=1
	#print("Hey")
	for tr in tbody.find_all('tr',class_="pl-video yt-uix-tile "):
		try:
			vid_url=tr.find('td',class_="pl-video-title").find('a').get('href')
			vid_url=urljoin("https://www.youtube.com",vid_url)
			download_video(vid_url,quality.lower(),extension.upper(),domain,count)
		except:
			#print("HoHo\n")
			pass

		count=count+1


def get_form():
	url=form_url.get()
	quality=form_quality.get()
	ext=form_ext.get()
	domain=form_domain.get()
	frame.quit()
	tool.destroy()
	playlist(url,quality,ext,domain)

tool=Tk()
frame=Frame(tool)
form_url=Entry(frame)
form_url.insert(0,"URL")
form_url.pack()
form_quality=Entry(frame)
form_quality.insert(0,"Quality")
form_quality.pack()
form_ext=Entry(frame)
form_ext.insert(0,"Extension")
form_ext.pack()
form_domain=Entry(frame)
form_domain.insert(0,"Domain")
form_domain.pack()
button=Button(frame,text="SUBMIT",command=get_form)
button.pack()
frame.pack()
tool.mainloop()


