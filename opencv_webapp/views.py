from django.shortcuts import render
from .forms import SimpleUploadForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .cv_functions import cv_detect_face

# Create your views here.
def first_view(request):
    return render(request, 'opencv_webapp/first_view.html',{})

def simple_upload(request):
    if request.method == 'POST': #POST
        form = SimpleUploadForm(request.POST, request.FILES)

        if form.is_valid():
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            context = {'form':form,'uploaded_file_url':uploaded_file_url}
            return render(request, 'opencv_webapp/simple_upload.html',context)

    else:    #GET
        form = SimpleUploadForm()
        context = {'form':form}
        return render(request, 'opencv_webapp/simple_upload.html',context)

def detect_face(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES) # filled form
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            imageURL = settings.MEDIA_URL + form.instance.document.name
                     # = '/media/' + 'ses.jpg'
                     # = '/media/ses.jpg'

            cv_detect_face(settings.MEDIA_ROOT_URL + imageURL)
	        # document : ImageUploadModel Class에 선언되어 있는 “document”에 해당
            # print(
            # form.instance,                ImageUploadModel object (1)
            # form.instance.document.name,  images/2021/02/08/ses.jpg
            # form.instance.document.url    /media/images/2021/02/08/ses.jpg
            # )
            # cv_detect_face('./media/ses.jpg') # 추후 구현 예정
            context = {'form':form, 'post':post}
            return render(request, 'opencv_webapp/detect_face.html', context)
    else:
        form = ImageUploadForm() # empty forms
        return render(request, 'opencv_webapp/detect_face.html', {'form':form})
