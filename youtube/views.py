
from django.shortcuts import render
from pytube import YouTube
import os
import datetime
import glob
import sys

from django.http import FileResponse

def index(request):

	try:
		
		# check request.method is post or not
		if request.method == 'POST':
			try:
				# get link from the html form
				link = request.POST['link']
				video = YouTube(link)

				# set video resolution
				stream = video.streams.get_lowest_resolution()
				title = video.title

				
				

				# download the video 
				# filename=title+'.mp4'
				path = stream.download()
				# videopath = os.path.basename(path).split('/')[-1]
				response = FileResponse(open(path, 'rb'), as_attachment=True)
				return response

				# render HTML page
				# return render(request, 'index.html', {'msg':'<a href="'+videopath+'">'+videopath+'</a>'})
			except:
				return render(request, 'index.html', {'msg':'Video not downloaded...check the link'})
		return render(request, 'index.html', {'msg':''})
	except:
		return render(request, "index.html", {"msg":"Sorry something went wrong!"})
	
def delete(request):
	retention = 10
	current_time = datetime.datetime.now()
	retention_tiom =  current_time - datetime.timedelta(minutes=retention)
	print('current time : {0}'.format(current_time))
	print('retention time : {0}'.format(retention_tiom))

	directory = os.getcwd()
	print(directory)
	search_log = os.path.join(directory, '*.mp4')

	allfiles = glob.glob(search_log)
	# print(allfiles)

	for t_files in allfiles:
		t_mod = os.path.getmtime(t_files)
		t_mod = datetime.datetime.fromtimestamp(t_mod)

		print('{0} : {1}'.format(t_files, t_mod))

		if retention_tiom > t_mod:
			try:
				os.remove(t_files)
			except Exception:
				pass



	return render(request, "index.html", {"msg":"Sorry something went wrong!"})

